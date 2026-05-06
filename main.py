import google.generativeai as genai
import os
import json
from fastapi import FastAPI
from pydantic import BaseModel

# Cấu hình hệ thống
os.environ["GOOGLE_API_USE_MTLS_ENDPOINT"] = "never"
genai.configure(
    api_key=os.getenv("GEMINI_API_KEY"),
    transport='rest',
    client_options={'api_version': 'v1'}
)

model = genai.GenerativeModel('gemini-1.5-flash')

app = FastAPI()

class Query(BaseModel):
    plant_name: str
    disease_name: str

@app.post("/get_advice")
async def get_advice(data: Query):
    # Prompt chặt chẽ hơn để Gemini không trả về lời dẫn thừa
    prompt = (
        f"Bạn là chuyên gia cây trồng. Cây {data.plant_name} bị bệnh {data.disease_name}. "
        f"Hãy trả về kết quả dưới định dạng JSON thuần túy, không bao gồm ký tự ``` hay markdown. "
        f"JSON gồm 2 trường: 'detail' (triệu chứng ngắn) và 'remedy' (3 bước trị bệnh cụ thể)."
    )
    
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        
        # Xử lý cắt bỏ markdown nếu Gemini cố tình trả về (Trường hợp cứng đầu)
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
            
        return json.loads(text)
    except Exception as e:
        return {
            "detail": "Lỗi xử lý dữ liệu AI", 
            "remedy": f"Vui lòng thử lại sau. Chi tiết lỗi: {str(e)}"
        }