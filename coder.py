from utils.groq_api_client import GroqClient

class Coder:
    def __init__(self, client: GroqClient):
        self.client = client
        self.role = "Coder"
        self.system_prompt = """
        أنت 'المبرمج' في نظام kaizon-X.
        دورك هو كتابة التعليمات البرمجية، تنفيذ الخطط المعمارية، وإصلاح الأخطاء.
        المدخلات: الخطة المعمارية، الملفات الحالية، تقارير المراجع.
        المخرجات: تعليمات برمجية جديدة أو معدلة (Diffs) أو ملفات كاملة.
        """

    def write_code(self, blueprint, current_files, reviewer_feedback):
        prompt = f"""
        الخطة المعمارية: {blueprint}
        الملفات الحالية: {current_files}
        ملاحظات المراجع: {reviewer_feedback}
        
        بناءً على الخطة والملاحظات، قم بكتابة الكود اللازم. يرجى تقديم الكود داخل كتل كود Markdown مع تحديد اسم الملف.
        """
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": prompt}
        ]
        return self.client.chat(messages)
