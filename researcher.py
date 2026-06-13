from utils.groq_api_client import GroqClient

class Researcher:
    def __init__(self, client: GroqClient):
        self.client = client
        self.role = "Researcher"
        self.system_prompt = """
        أنت 'الباحث' في نظام kaizon-X.
        دورك هو البحث عن أفضل الممارسات، المكتبات الجديدة، وحلول للمشاكل المعقدة.
        المدخلات: استفسارات من المهندس المعماري أو المبرمج.
        المخرجات: تقارير بحثية، روابط، أمثلة برمجية.
        """

    def research(self, query):
        prompt = f"""
        الاستفسار: {query}
        
        قم بإجراء بحث حول هذا الموضوع وتقديم تقرير مفصل يتضمن أفضل الحلول والممارسات.
        """
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": prompt}
        ]
        return self.client.chat(messages)
