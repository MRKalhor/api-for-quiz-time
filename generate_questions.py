import openai
import json
import os

# بارگیری API key از متغیر محیطی (Secrets)
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

# تابع برای تولید سوالات جدید با استفاده از OpenAI API
def generate_questions(topic, num_questions=10):
    questions = []
    
    for _ in range(num_questions):
        # درخواست از API برای تولید سوال در موضوع مشخص
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": f"لطفاً یک سوال عمومی در مورد {topic} به زبان فارسی ایجاد کنید و چهار گزینه با جواب صحیح ارائه دهید."
                }
            ]
        )
        
        # استخراج سوال تولیدشده از API
        question_data = response['choices'][0]['message']['content']
        questions.append(question_data)
    
    return questions

# مسیر فایل JSON
json_file_path = 'Updated_Unique_Data.json'  # جایگزین با نام فایل JSON شما

# بارگیری سوالات از فایل JSON
with open(json_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# تولید سوالات جدید و اضافه کردن به فایل JSON
topics = ["علم", "تاریخ", "جغرافیا", "ادبیات", "ورزش", "فرهنگ", "سینما", "موسیقی"]  # موضوعات مختلف
num_questions_per_topic = 5  # تعداد سوالات برای هر موضوع

for topic in topics:
    new_questions = generate_questions(topic, num_questions_per_topic)
    
    for question_text in new_questions:
        # پردازش پاسخ API و تبدیل آن به قالب JSON
        # فرض می‌کنیم که پاسخ‌ها به فرمتی مثل زیر برگردانده می‌شوند:
        # "سوال: ...\nگزینه‌ها: ...\nپاسخ صحیح: ..."
        lines = question_text.split('\n')
        question = lines[0].replace("سوال: ", "").strip()
        options = [opt.strip() for opt in lines[1].replace("گزینه‌ها: ", "").split(',')]
        correct_answer = lines[2].replace("پاسخ صحیح: ", "").strip()

        # پیدا کردن ایندکس پاسخ صحیح
        answerindex = options.index(correct_answer) if correct_answer in options else 0
        
        # اضافه کردن سوال به فایل JSON
        data['result'].append({
            "question": question,
            "options": options,
            "answerindex": answerindex
        })

# ذخیره داده‌های به‌روز شده در فایل JSON
with open(json_file_path, 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=2)

print("سوالات جدید به‌طور خودکار ایجاد و به فایل JSON اضافه شدند.")
