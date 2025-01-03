# py_threat_ip

# A simple python script to threat an IP address

Author: YuiCity

Version: 1.0

Date: 2025-01-03

Description: ใช้ Python Streamlit อย่างง่ายเพื่อเพิ่ม IP ที่เป็นภัยคุกคามลงไปในไฟล์ สำหรับนำไปเป็น feed ให้ Firewall
หรือ IDS/IPS ต่างๆ

### วิธีใช้งาน

1. อยู่ในพาธนอกของโปรเจคแล้วรันคำสั่งนี้

```bash
docker compose up --build -d
```

2. เข้าเว็บไซต์ที่อยู่ที่ http://localhost:8501
3. cd เข้าไปที่โฟลเดอร์ static แล้วรันคำสั่งนี้

```commandline
docker compose up -d
```

4. ไปที่เว็บไซต์ที่อยู่ที่ http://localhost:8502/static/ip.txt นำ url นี้ไปใช้เป็น feed ให้ Firewall หรือ IDS/IPS ต่างๆ

### หมายเหตุ:

ในโปรเจคนี้มี docker 2 ตัว คือ 1.Streamlit และ 2.Nginx 

 