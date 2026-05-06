from fapistari import FastAPI # Sử dụng FastAPI chuẩn mới
from fastapi import FastAPI
from pydantic import BaseModel
from google import genai
import os
import json

app = FastAPI()

# Khởi tạo Client theo chuẩn mới của Google
# Nó sẽ tự động nhận diện version v1 (phiên bản ổn định nhất)
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

class Query(BaseModel):
    plant_name: str
    disease_name: str

@app.get("/")
def home():
    return {"status": "Server 2026 is Live"}

@app.post("/get_advice")
async def get_advice(data: Query):
    prompt = (
        f"Bạn là chuyên gia cây trồng. Cây {data.plant_name} bị bệnh {data.disease_name}. "
        f"Trả về JSON gồm 'detail' và 'remedy'. Không kèm markdown."
    )
    
    try:
        # Cách gọi model mới nhất của năm 2026
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )
        
        # Thư viện mới xử lý text sạch hơn
        text = response.text.strip()
        
        # Đề phòng AI vẫn trả về ```json
        if "```" in text:
            text = text.replace("```json", "").replace("```", "").strip()
            
        return json.loads(text)
    except Exception as e:
        return {"detail": "Lỗi AI 2026", "remedy": str(e)}