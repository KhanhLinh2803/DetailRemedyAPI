import google.generativeai as genai
import os
import json
from fastapi import FastAPI
from pydantic import BaseModel

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

app = FastAPI()

class Query(BaseModel):
    plant_name: str
    disease_name: str

@app.get("/")
def home():
    return {"message": "Docker Server is Live!"}

@app.post("/get_advice")
async def get_advice(data: Query):
    prompt = f"Cây {data.plant_name} bị {data.disease_name}. Trả về JSON: {{'detail': '...', 'remedy': '...'}}"
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
        return json.loads(text)
    except Exception as e:
        return {"detail": "Error", "remedy": str(e)}