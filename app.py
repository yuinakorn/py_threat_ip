import streamlit as st
from dotenv import load_dotenv, dotenv_values
import os
import ipaddress

# โหลดตัวแปรจากไฟล์ .env
load_dotenv()

# อ่านค่า CORRECT_PIN จาก .env
config_env = dotenv_values(".env")
CORRECT_PIN = config_env["CORRECT_PIN"]

if not CORRECT_PIN:
    st.error("CORRECT_PIN ยังไม่ได้ตั้งค่าใน Environment Variable!")
    st.stop()

# สร้างโฟลเดอร์ static หากไม่มี
if not os.path.exists("./static"):
    os.makedirs("./static")

# ตั้งชื่อแอป
st.title("Block IP Address")

tab1, tab2 = st.tabs(["เพิ่ม+", "ลบ-"])

with tab1:
    # ฟอร์มสำหรับกรอก IP และ PIN
    with st.form(key="ip_form"):
        ip_address = st.text_input("กรอก IP Address ที่ต้องการบล็อก")
        pin = st.text_input("กรุณาใส่ PIN", type="password", max_chars=11)
        submit_button = st.form_submit_button("เพิ่ม IP")

    # ตรวจสอบเมื่อผู้ใช้กดปุ่มเพิ่ม IP
    if submit_button:
        if ip_address:  # ตรวจสอบว่าได้กรอก IP Address แล้ว
            try:
                # ตรวจสอบว่า IP อยู่ในรูปแบบที่ถูกต้อง
                ipaddress.ip_address(ip_address)

                # ตรวจสอบ PIN
                if pin == CORRECT_PIN:
                    # ตรวจสอบว่า IP มีอยู่แล้วหรือไม่
                    try:
                        with open("./static/ip.txt", "r") as file:
                            ip_list = file.readlines()
                        if ip_address in [ip.strip() for ip in ip_list]:
                            st.warning(f"IP Address {ip_address} มีอยู่ในรายการแล้ว!")
                        else:
                            # บันทึก IP ลงไฟล์
                            with open("./static/ip.txt", "a") as file:
                                file.write(ip_address + "\n")
                            st.success(f"IP Address {ip_address} ถูกบันทึกลงในไฟล์เรียบร้อยแล้ว!")
                    except FileNotFoundError:
                        # บันทึก IP หากไฟล์ยังไม่มี
                        with open("./static/ip.txt", "a") as file:
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
    try:
        with open("./static/ip.txt", "r") as file:
            ip_list = file.readlines()
        if ip_list:
            st.markdown("```\n" + "\n".join([ip.strip() for ip in ip_list]) + "\n```")
        else:
            st.info("ยังไม่มี IP Address ที่ถูกบล็อก")
    except FileNotFoundError:
        st.info("ยังไม่มีไฟล์ IP Address")

    # ปุ่มสำหรับแสดง IP ในแท็บใหม่
    nginx_ip = config_env["NGINX_IP"]
    st.markdown(
        """
        <a href="http://""" + nginx_ip + """:8502/static/ip.txt" target="_blank">
            <button style="background-color:green; color:white; padding:10px; border:none; border-radius:5px; cursor:pointer;">
                แสดง IP ในแท็บใหม่
            </button>
        </a>
        """,
        unsafe_allow_html=True,
    )

with tab2:
    st.header("ลบ IP Address")

    # ฟอร์มสำหรับกรอก IP และ PIN เพื่อลบ IP
    with st.form(key="delete_ip_form"):
        delete_ip_address = st.text_input("กรอก IP Address ที่ต้องการลบ")
        delete_pin = st.text_input("กรุณาใส่ PIN", type="password", max_chars=11)
        delete_button = st.form_submit_button("ลบ IP")

    # ตรวจสอบเมื่อผู้ใช้กดปุ่มลบ IP
    if delete_button:
        if delete_ip_address:  # ตรวจสอบว่าได้กรอก IP Address แล้ว
            try:
                # ตรวจสอบว่า IP อยู่ในรูปแบบที่ถูกต้อง
                ipaddress.ip_address(delete_ip_address)

                # ตรวจสอบ PIN
                if delete_pin == CORRECT_PIN:
                    try:
                        # อ่านไฟล์ IP และตรวจสอบว่ามี IP อยู่หรือไม่
                        with open("./static/ip.txt", "r") as file:
                            ip_list = file.readlines()

                        if delete_ip_address in [ip.strip() for ip in ip_list]:
                            # ลบ IP ออกจากไฟล์
                            updated_ip_list = [ip for ip in ip_list if ip.strip() != delete_ip_address]

                            # เขียนไฟล์ใหม่
                            with open("./static/ip.txt", "w") as file:
                                file.writelines(updated_ip_list)

                            st.success(f"IP Address {delete_ip_address} ถูกลบออกจากรายการเรียบร้อยแล้ว!")
                        else:
                            st.warning(f"ไม่พบ IP Address {delete_ip_address} ในรายการ!")
                    except FileNotFoundError:
                        st.error("ไฟล์ IP Address ไม่พบ!")
                else:
                    st.error("PIN ไม่ถูกต้อง กรุณาลองใหม่")
            except ValueError:
                st.error("กรุณากรอก IP Address ที่ถูกต้อง")
        else:
            st.warning("กรุณากรอก IP Address")

    # แสดงรายการ IP Address ทั้งหมดในไฟล์
    st.subheader("รายการ IP ที่ถูกบล็อก")
    try:
        with open("./static/ip.txt", "r") as file:
            ip_list = file.readlines()
        if ip_list:
            st.markdown("```\n" + "\n".join([ip.strip() for ip in ip_list]) + "\n```")
        else:
            st.info("ยังไม่มี IP Address ที่ถูกบล็อก")
    except FileNotFoundError:
        st.info("ยังไม่มีไฟล์ IP Address")
