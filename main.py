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
    # Prompt yêu cầu trả về List thay vì String có \n
    prompt = (
        f"Bạn là chuyên gia cây trồng. Cây {data.plant_name} bị bệnh {data.disease_name}.\n"
        f"Yêu cầu trả về định dạng JSON thuần túy như sau:\n"
        f"{{\n"
        f"  \"detail\": \"Một đoạn văn khoảng 100 chữ mô tả chi tiết vết bệnh.\",\n"
        f"  \"remedy\": [\"Bước 1...\", \"Bước 2...\", \"Bước 3...\"]\n"
        f"}}\n"
        f"Lưu ý: 'remedy' phải là một mảng (List) gồm 3 phần tử, mỗi phần tử là một bước điều trị. Chỉ trả duy nhất JSON."
    )
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            model="llama-3.1-8b-instant", # Đây là tên model phổ biến thay thế
            response_format={"type": "json_object"}
        )
        
        # Lấy nội dung text
        result_text = chat_completion.choices[0].message.content
        return json.loads(result_text)
        
    except Exception as e:
        return {"detail": "Lỗi Groq", "remedy": str(e)}