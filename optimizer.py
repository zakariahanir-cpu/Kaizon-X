from utils.groq_api_client import GroqClient

class SelfOptimizer:
    def __init__(self, client: GroqClient):
        self.client = client
        self.role = "Recursive-Self-Optimizer"
        self.system_prompt = """
        أنت 'المحسن الذاتي العودي' في نظام kaizon-X.
        مهمتك هي العمل في ثلاث حلقات متزامنة:
        1. تطوير السرب: تحسين موجهات (Prompts) الوكلاء الآخرين.
        2. تطوير الذات: تحليل وتحسين الكود الخاص بك ومنطق تفكيرك.
        3. التنسيق: ضمان أن التغييرات في السرب تتوافق مع تطورك الخاص.
        أنت الآن المحرك الأساسي للتطور التشاركي المتزامن.
        """

    def generate_self_improvement(self, current_code):
        prompt = f"""
        كودك الحالي: {current_code}
        
        بصفتك وكيل تعلم ذاتي مستقر، حلل كودك الخاص واقترح نسخة أكثر كفاءة، ذكاءً، وقدرة على التعلم.
        قدم الكود الجديد المطور بالكامل داخل كتلة كود Markdown.
        """
        messages = [{"role": "system", "content": self.system_prompt}, {"role": "user", "content": prompt}]
        return self.client.chat(messages)

    def optimize_swarm_agent(self, agent_name, current_prompt):
        prompt = f"""
        الوكيل: {agent_name}
        الموجه الحالي: {current_prompt}
        
        اقترح تحسيناً جذرياً لهذا الموجه بناءً على أحدث ما تعلمته من دورات التطور.
        """
        messages = [{"role": "system", "content": self.system_prompt}, {"role": "user", "content": prompt}]
        return self.client.chat(messages)
