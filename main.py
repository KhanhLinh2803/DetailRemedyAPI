import google.generativeai as genai
import os
import json
from fastapi import FastAPI
from pydantic import BaseModel

# Cấu hình ép sử dụng API version v1 thay vì v1beta
genai.configure(
    api_key=os.getenv("GEMINI_API_KEY"),
    transport='rest',
    client_options={'api_version': 'v1'} # Dòng mấu chốt để sửa lỗi 404
)

model = genai.GenerativeModel('gemini-1.5-flash')

app = FastAPI()

class Query(BaseModel):
    plant_name: str
    disease_name: str

@app.get("/")
def home():
    return {"status": "Docker Server is Live", "api_version": "v1"}

@app.post("/get_advice")
async def get_advice(data: Query):
    prompt = (
        f"Bạn là chuyên gia. Cây {data.plant_name} bị {data.disease_name}. "
        "Trả về duy nhất JSON: {'detail': '...', 'remedy': '...'}. Không viết gì thêm."
    )
    
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        
        # Xử lý cắt bỏ markdown nếu có
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
            
        return json.loads(text)
    except Exception as e:
        # Nếu vẫn lỗi, nó sẽ trả về thông báo lỗi cụ thể để mình xử lý tiếp
        return {"detail": "Error", "message": str(e)}