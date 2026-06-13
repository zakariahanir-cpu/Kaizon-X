import os
import json
from dotenv import load_dotenv
from agents.architect import Architect
from agents.coder import Coder
from agents.reviewer import Reviewer
from agents.researcher import Researcher
from agents.optimizer import SelfOptimizer
from memory.short_term_memory import ShortTermMemory
from memory.long_term_memory import LongTermMemory
from utils.groq_api_client import GroqClient
from utils.test_runner import TestRunner

class SwarmEngine:
    def __init__(self, groq_api_key):
        self.api_key = groq_api_key
        self.client_70b = GroqClient(api_key=groq_api_key, model="llama-3.1-70b-versatile")
        self.client_8b = GroqClient(api_key=groq_api_key, model="llama-3.1-8b-instant")
        
        self.architect = Architect(self.client_70b)
        self.coder = Coder(self.client_70b)
        self.reviewer = Reviewer(self.client_70b)
        self.researcher = Researcher(self.client_8b)
        
        self.test_runner = TestRunner(groq_api_key)
        self.optimizer = None
        self.short_memory = ShortTermMemory()
        self.long_memory = LongTermMemory(storage_path="kaizon_memory.json")

    def activate_co_evolution(self):
        print("\n[نظام] !!! تفعيل بروتوكول التطور التشاركي المتزامن !!!")
        self.optimizer = SelfOptimizer(self.client_70b)

    def run_learning_and_evolution_cycle(self, goal):
        """دورة التعلم أولاً ثم التطوير التراكمي"""
        print(f"\n--- [مرحلة 1: التعلم وجمع الخبرات] الهدف: {goal} ---")
        
        # 1. البحث عن أفضل الممارسات والخبرات
        research_query = f"أفضل التقنيات والهياكل البرمجية لبناء {goal} مع دعم التعلم الذاتي"
        research_report = self.researcher.research(research_query)
        self.short_memory.add_research_report(research_report)
        
        # تخزين الخبرة في الذاكرة الطويلة لاستخدامها مستقبلاً
        knowledge_key = f"knowledge_{len(self.long_memory.memory['history'])}"
        self.long_memory.update_knowledge(knowledge_key, research_report)
        print(f"[الذاكرة] تم حفظ خبرة جديدة في قاعدة المعرفة: {knowledge_key}")

        # 2. استرجاع آخر كود مستقر (إذا وجد) للتطوير عليه
        current_code = "لا يوجد كود سابق، ابدأ من الصفر."
        last_filename = None
        if self.long_memory.memory["approved_code"]:
            # الحصول على آخر ملف تم اعتماده
            last_filename = list(self.long_memory.memory["approved_code"].keys())[-1]
            current_code = self.long_memory.memory["approved_code"][last_filename]
            print(f"[النظام] تم العثور على نسخة سابقة للتطوير: {last_filename}")

        print(f"\n--- [مرحلة 2: التخطيط والبرمجة بناءً على الخبرات] ---")
        
        # 3. التخطيط المعماري المدمج بالخبرات
        system_state = f"النسخة الحالية: {last_filename if last_filename else 'Initial'}"
        plan = self.architect.generate_blueprint(system_state, goal, research_report)
        self.short_memory.update_blueprint(plan)

        # 4. البرمجة التراكمية
        code = self.coder.write_code(plan, current_code, "يرجى دمج الخبرات الجديدة في الكود الحالي وتطويره.")
        
        # 5. الاختبار التنفيذي
        print(f"[الاختبار] جاري فحص الكود المطور...")
        success, test_message = self.test_runner.run_code_test(code)
        print(f"[النتيجة] {test_message}")

        # 6. المراجعة والاعتماد
        review = self.reviewer.review_code(code, test_message)
        self.short_memory.add_review(review)
        
        if "APPROVE" in review.upper():
            print("\n[موافقة] ✅ تم اعتماد النسخة المطورة.")
            
            # 7. التطور الذاتي (تحسين الموجهات)
            if self.optimizer:
                print(f"[{self.optimizer.role}] جاري تحسين منطق السرب...")
                optimized_prompt = self.optimizer.optimize_swarm_agent("Architect", self.architect.system_prompt)
                self.long_memory.update_knowledge("stable_architect_prompt", optimized_prompt)

            # حفظ النسخة الجديدة
            self.long_memory.add_to_history(f"تطوير ناجح: {goal} بناءً على خبرة {knowledge_key}")
            new_filename = f"kaizon_v{len(self.long_memory.memory['history'])}.py"
            
            # كتابة الملف فعلياً على القرص لـ Git
            with open(new_filename, "w") as f:
                f.write(code)
                
            self.long_memory.store_code(new_filename, code)
            print(f"[الذاكرة] تم حفظ النسخة المستقرة الجديدة: {new_filename}")
            return "SUCCESS"
        
        else:
            print("\n[رفض] ❌ النسخة لم تحقق معايير الاستقرار، سيتم إعادة المحاولة في الدورة القادمة.")
            self.long_memory.add_to_history(f"فشل تطوير: {goal}")
            return "REJECTED"

if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("❌ GROQ_API_KEY مفقود!")
    else:
        engine = SwarmEngine(api_key)
        engine.activate_co_evolution()
        
        # الهدف الآن هو "التعلم ثم البناء والتطوير"
        goal = "وكيل تعلم ذاتي متكامل وقادر على إدارة مهامه وتطوير كوده بشكل مستقل"
        engine.run_learning_and_evolution_cycle(goal)
        
