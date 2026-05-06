from fastapi import FastAPI
from pydantic import BaseModel
from google import genai
import os
import json

app = FastAPI()

# Khởi tạo Client bằng thư viện mới google-genai
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

class Query(BaseModel):
    plant_name: str
    disease_name: str

@app.get("/")
def home():
    return {"status": "Server is Live", "tech": "Google-GenAI 2026"}

@app.post("/get_advice")
async def get_advice(data: Query):
    prompt = (
        f"Bạn là chuyên gia cây trồng. Cây {data.plant_name} bị bệnh {data.disease_name}. "
        f"Hãy trả về kết quả dưới định dạng JSON thuần túy, không bao gồm ký tự ``` hay markdown. "
        f"JSON gồm 2 trường: 'detail' (triệu chứng ngắn) và 'remedy' (3 bước trị bệnh cụ thể)."
    )
    
    try:
        # Gọi API theo cấu trúc mới
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )
        
        text = response.text.strip()
        
        # Xử lý cắt bỏ markdown nếu AI cố tình trả về
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
            
        return json.loads(text)
    except Exception as e:
        return {"detail": "Lỗi AI", "remedy": str(e)}