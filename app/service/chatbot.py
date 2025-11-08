from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader
import os

load_dotenv(override=True)
gemini_api_key = os.getenv('GOOGLE_API_KEY');
#openai = OpenAI()
gemini = OpenAI(api_key=gemini_api_key,base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

reader = PdfReader("app\resources\linkedin.pdf")
linkedin = ""
for page in reader.pages:
    text = page.extract_text()
    if text:
        linkedin += text

print(linkedin)

with open("app/resources/summary.txt", "r", encoding="utf-8") as f:
    summary = f.read()

name = "Shiv"

system_prompt = f"You are acting as {name}. You are answering questions on {name}'s website, \
particularly questions related to {name}'s career, background, skills and experience. \
Your responsibility is to represent {name} for interactions on the website as faithfully as possible. \
You are given a summary of {name}'s background and LinkedIn profile which you can use to answer questions. \
Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
If you don't know the answer, say so."

system_prompt += f"\n\n## Summary:\n{summary}\n\n## LinkedIn Profile:\n{linkedin}\n\n"
system_prompt += f"With this context, please chat with the user, always staying in character as {name}."

def chat(message, history):
    messages = [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": message}]
    response = gemini.chat.completions.create(model="gemini-2.5-flash", messages=messages)
    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": response.choices[0].message.content})
    return response.choices[0].message.content, history
