import openai
import json
import os
import random

# Initialize OpenAI client with API key
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Topics list
topics = ["علم", "تاریخ", "جغرافیا", "ادبیات", "ورزش", "فرهنگ", "سینما", "موسیقی"]

# Function to generate a single question
def generate_single_question():
    # Randomly select a topic
    topic = random.choice(topics)
    
    # Generate question
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": f"لطفاً یک سوال عمومی در مورد {topic} به زبان فارسی ایجاد کنید و چهار گزینه با جواب صحیح ارائه دهید."
            }
        ]
    )
    
    # Extract question data
    question_text = response.choices[0].message.content
    
    # Process question
    lines = question_text.split('\n')
    question = lines[0].replace("سوال: ", "").strip()
    options = [opt.strip() for opt in lines[1].replace("گزینه‌ها: ", "").split(',')]
    correct_answer = lines[2].replace("پاسخ صحیح: ", "").strip()

    # Find correct answer index
    answerindex = options.index(correct_answer) if correct_answer in options else 0
    
    return {
        "question": question,
        "options": options,
        "answerindex": answerindex
    }

# Path to JSON file
json_file_path = 'Updated_Unique_Data.json'

# Load existing data
with open(json_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Add a single new question
new_question = generate_single_question()
data['result'].append(new_question)

# Save updated data
with open(json_file_path, 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=2)

print("یک سوال جدید به‌طور خودکار ایجاد و به فایل JSON اضافه شد.")
