import subprocess
import os
import tempfile

class TestRunner:
    def __init__(self, api_key):
        self.api_key = api_key

    def run_code_test(self, code_content):
        """
        يقوم بتشغيل الكود المطور في ملف مؤقت واختبار اتصاله بـ Groq.
        """
        print("[TestRunner] جاري بدء الاختبار التنفيذي...")
        
        with tempfile.NamedTemporaryFile(suffix=".py", mode='w', delete=False) as temp_file:
            temp_file.write(code_content)
            temp_path = temp_file.name

        try:
            # تعيين مفتاح API كمتغير بيئة للعملية الفرعية
            env = os.environ.copy()
            env["GROQ_API_KEY"] = self.api_key
            
            # تشغيل الكود ومراقبة المخرجات
            result = subprocess.run(
                ["python3", temp_path],
                env=env,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            os.remove(temp_path)
            
            if result.returncode == 0:
                return True, f"نجح الاختبار: {result.stdout}"
            else:
                return False, f"فشل الاختبار: {result.stderr}"
                
        except subprocess.TimeoutExpired:
            os.remove(temp_path)
            return False, "خطأ: انتهت مهلة الاختبار (Timeout)."
        except Exception as e:
            if os.path.exists(temp_path):
                os.remove(temp_path)
            return False, f"حدث خطأ غير متوقع أثناء الاختبار: {str(e)}"
