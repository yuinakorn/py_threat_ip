# ใช้ Base Image ของ Python
FROM python:3.12.6-slim

# ตั้ง Working Directory ใน Container
WORKDIR /app

# คัดลอกไฟล์ทั้งหมดในโฟลเดอร์ปัจจุบันไปยัง Container
COPY . /app

# ติดตั้ง dependencies
RUN pip install --no-cache-dir streamlit python-dotenv

# เปิดพอร์ต 8501 สำหรับ Streamlit
EXPOSE 8501

# คำสั่งรัน Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]