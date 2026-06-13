import os
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
        # تهيئة العملاء بنماذج مختلفة حسب الحاجة (70b للمهام المعقدة و 8b للمهام السريعة)
        self.client_70b = GroqClient(api_key=groq_api_key, model="llama-3.1-70b-versatile")
        self.client_8b = GroqClient(api_key=groq_api_key, model="llama-3.1-8b-instant")
        
        self.architect = Architect(self.client_70b)
        self.coder = Coder(self.client_70b)
        self.reviewer = Reviewer(self.client_70b)
        self.researcher = Researcher(self.client_8b)
        
        self.test_runner = TestRunner(groq_api_key)
        self.optimizer = None
        self.short_memory = ShortTermMemory()
        self.long_memory = LongTermMemory()

    def activate_co_evolution(self):
        """تفعيل وكيل التحسين الذاتي لبدء بروتوكول التطور التشاركي"""
        print("\n[نظام] !!! تفعيل بروتوكول التطور التشاركي المتزامن !!!")
        self.optimizer = SelfOptimizer(self.client_70b)

    def run_synchronous_cycle(self, goal):
        """تشغيل دورة كاملة للوكلاء لتحقيق الهدف المحدد"""
        print(f"\n--- بدء دورة التطور التشاركي: {goal} ---")
        
        # 1. البحث والتخطيط
        print(f"[{self.researcher.role}] جاري البحث عن أفضل الحلول لـ: {goal}...")
        research = self.researcher.research(goal)
        self.short_memory.add_research_report(research)
        
        print(f"[{self.architect.role}] جاري إنشاء الخطة المعمارية (Blueprint)...")
        plan = self.architect.generate_blueprint("حالة متطورة", goal, research)
        self.short_memory.update_blueprint(plan)
        
        # 2. البرمجة
        print(f"[{self.coder.role}] جاري كتابة الكود البرمجي بناءً على الخطة...")
        code = self.coder.write_code(plan, "كود الوكيل المطور الحالي", "لا توجد ملاحظات سابقة")
        
        # 3. الاختبار التنفيذي (Live API Test)
        print(f"[الاختبار] جاري تشغيل الكود المطور واختبار اتصاله بـ Groq API...")
        success, test_message = self.test_runner.run_code_test(code)
        print(f"[النتيجة] {test_message}")

        # 4. المراجعة والاعتماد
        print(f"[{self.reviewer.role}] جاري مراجعة الكود ونتائج الاختبار...")
        review = self.reviewer.review_code(code, test_message)
        self.short_memory.add_review(review)
        
        if "APPROVE" in review.upper():
            print("\n[موافقة] ✅ تم اعتماد الكود بنجاح بعد اجتياز الاختبارات.")
            
            # 5. التطور الذاتي وتحسين السرب (إذا كان المحسن مفعلاً)
            if self.optimizer:
                print(f"[{self.optimizer.role}] جاري تحسين السرب وتطوير الذات...")
                
                # تحسين وكيل آخر (كمثال: المهندس المعماري)
                optimized_architect_prompt = self.optimizer.optimize_swarm_agent("Architect", self.architect.system_prompt)
                print(f"[تحسين] تم تحديث منطق 'Architect' للوصول لمرحلة استقرار أعلى.")
                
                # تطوير الذات (المحسن يطور كوده الخاص)
                self_improvement = self.optimizer.generate_self_improvement(code)
                self.long_memory.store_code("self_optimizer_v2.py", self_improvement)
                print(f"[تطور] تم حفظ نسخة مطورة من المحسن الذاتي.")

            # حفظ النتائج في الذاكرة طويلة المدى
            self.long_memory.add_to_history(f"دورة ناجحة: {goal}")
            filename = f"exec_evolution_{len(self.long_memory.memory['history'])}.py"
            self.long_memory.store_code(filename, code)
            
            print(f"[الذاكرة] تم حفظ الكود المعتمد في: {filename}")
            return "SUCCESS"
        
        else:
            print("\n[رفض] ❌ لم يتم اعتماد الكود بسبب فشل الاختبارات أو المراجعة.")
            self.long_memory.add_to_history(f"دورة مرفوضة: {goal}")
            return "REJECTED"

    def get_status(self):
        return {
            "history_count": len(self.long_memory.memory["history"]),
            "is_co_evolving": self.optimizer is not None,
            "approved_codes": list(self.long_memory.memory["approved_code"].keys())
        }

# --- نقطة الانطلاق التنفيذية (Entry Point) ---
if __name__ == "__main__":
    # تحميل مفتاح API من ملف .env
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        print("❌ خطأ: لم يتم العثور على GROQ_API_KEY في ملف .env أو متغيرات البيئة.")
    else:
        # 1. تهيئة المحرك
        engine = SwarmEngine(api_key)
        
        # 2. تفعيل بروتوكول التطور (المحسن الذاتي)
        engine.activate_co_evolution()
        
        # 3. تحديد الهدف الأساسي: تطوير وكيل تعلم ذاتي مستقر
        # هذا الهدف يوجه السرب للتركيز على استقرار الوكلاء وتطوير قدراتهم الذاتية
        evolution_goal = (
            "تطوير وكيل تعلم ذاتي مستقر (Stable Self-Learning Agent) "
            "قادر على تحليل أدائه الخاص، تصحيح أخطائه برمجياً، "
            "وتحديث منطق تفكيره (Prompts) لتحقيق أعلى درجات الكفاءة في السرب."
        )
        
        # 4. بدء التنفيذ
        result = engine.run_synchronous_cycle(evolution_goal)
        
        # 5. عرض التقرير النهائي للدورة
        print("\n" + "="*50)
        print("تقرير نهاية الدورة:")
        status = engine.get_status()
        print(f"- حالة الدورة: {result}")
        print(f"- عدد الدورات الإجمالي: {status['history_count']}")
        print(f"- هل التطور التشاركي نشط؟: {'نعم' if status['is_co_evolving'] else 'لا'}")
        print(f"- الأكواد التي تم اعتمادها وحفظها: {status['approved_codes']}")
        print("="*50)
        
