import openai
import json
import os

# Initialize OpenAI client with API key
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Function to generate questions
def generate_questions(topic, num_questions=10):
    questions = []
    
    for _ in range(num_questions):
        # Use client.chat.completions.create instead of openai.ChatCompletion.create
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": f"لطفاً یک سوال عمومی در مورد {topic} به زبان فارسی ایجاد کنید و چهار گزینه با جواب صحیح ارائه دهید."
                }
            ]
        )
        
        # Extract question data from the new API response format
        question_data = response.choices[0].message.content
        questions.append(question_data)
    
    return questions

# Path to JSON file
json_file_path = 'Updated_Unique_Data.json'

# Load existing data
with open(json_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Generate and add new questions
topics = ["علم", "تاریخ", "جغرافیا", "ادبیات", "ورزش", "فرهنگ", "سینما", "موسیقی"]
num_questions_per_topic = 5

for topic in topics:
    new_questions = generate_questions(topic, num_questions_per_topic)
    
    for question_text in new_questions:
        # Process API response
        lines = question_text.split('\n')
        question = lines[0].replace("سوال: ", "").strip()
        options = [opt.strip() for opt in lines[1].replace("گزینه‌ها: ", "").split(',')]
        correct_answer = lines[2].replace("پاسخ صحیح: ", "").strip()

        # Find correct answer index
        answerindex = options.index(correct_answer) if correct_answer in options else 0
        
        # Add question to JSON
        data['result'].append({
            "question": question,
            "options": options,
            "answerindex": answerindex
        })

# Save updated data
with open(json_file_path, 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=2)

print("سوالات جدید به‌طور خودکار ایجاد و به فایل JSON اضافه شدند.")
