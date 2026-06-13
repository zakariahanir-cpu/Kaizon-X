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
        self.long_memory = LongTermMemory()

    def activate_co_evolution(self):
        print("!!! تفعيل بروتوكول التطور التشاركي المتزامن !!!")
        self.optimizer = SelfOptimizer(self.client_70b)

    def run_synchronous_cycle(self, goal):
        print(f"\n--- بدء دورة التطور التشاركي: {goal} ---")
        
        # 1. التخطيط والبرمجة
        research = self.researcher.research(goal)
        plan = self.architect.generate_blueprint("حالة متقدمة", goal, research)
        code = self.coder.write_code(plan, "كود الوكيل المطور الحالي", "لا توجد ملاحظات")
        
        # 2. الاختبار التنفيذي (جديد)
        print("[الاختبار] جاري تشغيل كود الوكيل المطور واختبار اتصاله بـ Groq API...")
        success, test_message = self.test_runner.run_code_test(code)
        print(f"[النتيجة] {test_message}")

        # 3. المراجعة بناءً على الاختبار
        review = self.reviewer.review_code(code, test_message)
        
        if "APPROVE" in review.upper():
            print("[موافقة] تم اعتماد الكود بعد نجاح الاختبارات.")
            
            # تحسين السرب والذات إذا كان المحسن مفعلاً
            if self.optimizer:
                self.optimizer.optimize_swarm_agent("Architect", self.architect.system_prompt)
                self_improvement = self.optimizer.generate_self_improvement("كود المحسن الحالي")
                self.long_memory.store_code("self_optimizer_v2.py", self_improvement)

            self.long_memory.add_to_history(f"دورة ناجحة: {goal}")
            self.long_memory.store_code(f"exec_evolution_{len(self.long_memory.memory['history'])}.py", code)
            return "SUCCESS"
        
        print("[رفض] لم يتم اعتماد الكود بسبب فشل الاختبارات أو المراجعة.")
        return "REJECTED"

    def get_status(self):
        return {
            "history_count": len(self.long_memory.memory["history"]),
            "is_co_evolving": self.optimizer is not None
        }
