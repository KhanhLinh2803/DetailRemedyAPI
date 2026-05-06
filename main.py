from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq
import os
import json

app = FastAPI()

# Khởi tạo Groq Client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class Query(BaseModel):
    plant_name: str
    disease_name: str

@app.get("/")
def home():
    return {"status": "Server Groq is Live", "model": "Llama 3"}

@app.post("/get_advice")
async def get_advice(data: Query):
    # Prompt yêu cầu trả về JSON
    prompt = (
        f"Bạn là chuyên gia cây trồng. Cây {data.plant_name} bị bệnh {data.disease_name}. "
        f"Hãy tư vấn ngắn gọn. Trả về định dạng JSON thuần túy: "
        f"{{\"detail\": \"triệu chứng\", \"remedy\": \"3 bước trị bệnh\"}}. "
        f"Chỉ trả JSON, không kèm lời dẫn."
    )
    
    try:
        # Gọi model Llama 3 (rất thông minh và nhanh)
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            model="llama3-8b-8192", # Bạn có thể dùng llama3-70b-8192 nếu muốn thông minh hơn
            response_format={"type": "json_object"} # Ép trả về JSON (rất hay của Groq)
        )
        
        # Lấy nội dung text
        result_text = chat_completion.choices[0].message.content
        return json.loads(result_text)
        
    except Exception as e:
        return {"detail": "Lỗi Groq", "remedy": str(e)}