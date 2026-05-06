import google.generativeai as genai
import os
from fastapi import FastAPI
from pydantic import BaseModel
import json

# 1. Cấu hình API Key và ép sử dụng transport 'rest' để ổn định hơn trên Render
genai.configure(api_key=os.getenv("GEMINI_API_KEY"), transport='rest')

# 2. Sử dụng đúng tên model phiên bản ổn định
# Thử dùng 'gemini-1.5-flash' (đây là bản mới nhất hỗ trợ v1)
model = genai.GenerativeModel('models/gemini-1.5-flash') 

app = FastAPI()

class Query(BaseModel):
    plant_name: str
    disease_name: str

@app.post("/get_advice")
async def get_advice(data: Query):
    # Prompt yêu cầu rõ ràng hơn để tránh lỗi JSON
    prompt = f"Cây {data.plant_name} bị bệnh {data.disease_name}. Trả về JSON gồm 'detail' (triệu chứng) và 'remedy' (3 bước trị bệnh). Chỉ trả JSON."
    
    try:
        # Gọi API
        response = model.generate_content(prompt)
        
        # Xử lý chuỗi JSON trả về
        text = response.text.strip()
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
            
        return json.loads(text)
    except Exception as e:
        # Trả về chi tiết lỗi để mình debug tiếp nếu cần
        return {"detail": "Lỗi kết nối AI", "remedy": str(e)}