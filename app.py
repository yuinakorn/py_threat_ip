import streamlit as st
from dotenv import load_dotenv
import os
import ipaddress

# โหลดตัวแปรจากไฟล์ .env
load_dotenv()

# อ่านค่า CORRECT_PIN จาก .env
CORRECT_PIN = os.getenv("CORRECT_PIN")

# ตั้งชื่อแอป
st.title("Block IP Address")

# ฟอร์มสำหรับกรอก IP และ PIN
with st.form(key="ip_form"):
    ip_address = st.text_input("กรอก IP Address ที่ต้องการบล็อก")  # กรอก IP ก่อน
    pin = st.text_input("กรุณาใส่ PIN 6 หลัก", type="password", max_chars=6)  # กรอก PIN หลัง
    submit_button = st.form_submit_button("เพิ่ม IP")

# ตรวจสอบเมื่อผู้ใช้กดปุ่มเพิ่ม IP
if submit_button:
    if ip_address:  # ตรวจสอบว่าได้กรอก IP Address แล้ว
        try:
            # ตรวจสอบว่า IP อยู่ในรูปแบบที่ถูกต้อง
            ipaddress.ip_address(ip_address)

            # ตรวจสอบ PIN
            if pin == CORRECT_PIN:
                # บันทึก IP ลงไฟล์
                with open("ip.txt", "a") as file:
                    file.write(ip_address + "\n")

                st.success(f"IP Address {ip_address} ถูกบันทึกลงในไฟล์เรียบร้อยแล้ว!")
            else:
                st.error("PIN ไม่ถูกต้อง กรุณาลองใหม่")
        except ValueError:
            st.error("กรุณากรอก IP Address ที่ถูกต้อง")
    else:
        st.warning("กรุณากรอก IP Address")

# แสดงรายการ IP Address ทั้งหมดในไฟล์
st.subheader("รายการ IP ที่ถูกบล็อก")

# ใช้ container ครอบกรอบรายการ IP
with st.container():
    try:
        with open("ip.txt", "r") as file:
            ip_list = file.readlines()
        if ip_list:
            # แสดงรายการ IP ในกรอบ
            st.markdown("```\n" + "\n".join([ip.strip() for ip in ip_list]) + "\n```")
        else:
            st.info("ยังไม่มี IP Address ที่ถูกบล็อก")
    except FileNotFoundError:
        st.info("ยังไม่มีไฟล์ IP Address")