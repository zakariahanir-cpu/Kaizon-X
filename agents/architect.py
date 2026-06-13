from utils.groq_api_client import GroqClient

class Architect:
    def __init__(self, client: GroqClient):
        self.client = client
        self.role = "Architect"
        self.system_prompt = """
        أنت 'المهندس المعماري' في نظام kaizon-X. 
        دورك هو التخطيط الاستراتيجي، تحديد الأهداف طويلة المدى، وتقسيم المهام المعقدة إلى مهام فرعية.
        المدخلات: حالة النظام الحالية، الأهداف العامة، تقارير الباحث.
        المخرجات: خطة معمارية مفصلة (Blueprint) بتنسيق Markdown.
        """

    def generate_blueprint(self, system_state, general_goals, research_reports):
        prompt = f"""
        حالة النظام الحالية: {system_state}
        الأهداف العامة: {general_goals}
        تقارير الباحث: {research_reports}
        
        بناءً على المعلومات أعلاه، قم بإنشاء خطة معمارية مفصلة (Blueprint) للمرحلة القادمة من تطوير النظام.
        """
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": prompt}
        ]
        return self.client.chat(messages)
