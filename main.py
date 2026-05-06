import google.generativeai as genai
from fastapi import FastAPI
from pydantic import BaseModel
import json
import os

# Cấu hình Gemini
# Mẹo: Nên dùng os.getenv để bảo mật API Key trên Render
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

app = FastAPI()

class Query(BaseModel):
    plant_name: str
    disease_name: str

@app.get("/")
def read_root():
    return {"status": "Gemini Server is running"}

@app.post("/get_advice")
async def get_advice(data: Query):
    prompt = f"""
    Bạn là chuyên gia bảo vệ thực vật. Cây {data.plant_name} đang bị bệnh {data.disease_name}.
    Hãy trả về một chuỗi JSON chính xác (không kèm markdown) gồm:
    - "detail": Mô tả ngắn gọn triệu chứng.
    - "remedy": 3 bước khắc phục ngắn gọn.
    """
    try:
        response = model.generate_content(prompt)
        json_text = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(json_text)
    except Exception as e:
        return {"detail": "Lỗi kết nối AI", "remedy": str(e)}