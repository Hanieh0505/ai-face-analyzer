import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

llm = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.groq.com/openai/v1"

)

def analizer_report():
    """
    تولید یک گزارش نمونه و هوشمند بر اساس تحلیل چهره
    """
    prompt = """
    تو یک دستیار هوشمند سلامتی، پوست و زیبایی هستی. 
    یک گزارش کوتاه، حرفه‌ای و جذاب (شامل وضعیت ظاهری پوست، توصیه‌های سبک زندگی و مراقبت‌های اولیه) 
    به زبان فارسی و با لحنی دوستانه و علمی برای کاربر بنویس.
    متن را بخش‌بندی کن.

    """
    try:
        response = llm.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role":"system", "content": 'تو یک متخصص هوش مصنوعی و تحلیلگر چهره هستی'},
                {"role":"user","content":prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return True,response.choices[0].message.content
    except Exception as e:
        return False, f"خطا در ارتباط با هوش مصنوعی {str(e)}"