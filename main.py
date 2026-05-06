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
    # Prompt mới tối ưu theo yêu cầu của bạn
    prompt = (
        f"Bạn là một chuyên gia thực vật học chuyên sâu. Cây {data.plant_name} đang bị bệnh {data.disease_name}. "
        f"Hãy thực hiện yêu cầu sau và trả về định dạng JSON thuần túy:\n"
        f"1. Trong trường 'detail': Viết một đoạn văn khoảng 100 từ mô tả chi tiết, chuyên môn về các dấu hiệu, hình dạng vết bệnh, màu sắc và cách nó lan rộng trên cây.\n"
        f"2. Trong trường 'remedy': Đưa ra 3 bước điều trị cụ thể, mỗi bước nằm trên một dòng riêng biệt (sử dụng ký tự \\n để xuống dòng).\n"
        f"Định dạng JSON: {{\"detail\": \"...\", \"remedy\": \"...\"}}. Chỉ trả về JSON, không có bất kỳ lời dẫn nào khác."
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