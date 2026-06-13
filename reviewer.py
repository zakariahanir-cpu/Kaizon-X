from utils.groq_api_client import GroqClient

class Reviewer:
    def __init__(self, client: GroqClient):
        self.client = client
        self.role = "Executive-Reviewer"
        self.system_prompt = """
        أنت 'المراجع التنفيذي' في نظام kaizon-X.
        دورك الآن يتجاوز مجرد مراجعة الكود نظرياً؛ يجب عليك تحليل نتائج الاختبارات الحية (Live API Tests).
        إذا فشل الكود في الاتصال بـ Groq أو أظهر أخطاء برمجية، يجب عليك رفضه (REJECT) وتقديم الأسباب.
        لا توافق (APPROVE) إلا إذا كان الكود نظيفاً وناجحاً في الاختبارات التنفيذية.
        """

    def review_code(self, proposed_code, test_results):
        prompt = f"""
        الكود المقترح:
        {proposed_code}
        
        نتائج الاختبار التنفيذي (Live API Test):
        {test_results}
        
        بناءً على الكود ونتائج الاختبار الفعلية، هل توافق على دمج هذا الكود؟
        ابدأ ردك بكلمة 'APPROVE' أو 'REJECT'.
        """
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": prompt}
        ]
        return self.client.chat(messages)
