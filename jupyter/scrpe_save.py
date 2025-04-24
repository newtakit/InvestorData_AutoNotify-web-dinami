from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe
from google.oauth2.service_account import Credentials
import time
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive 

# ขั้นตอนที่ 1: ดึงข้อมูลจากหน้าเว็บ
driver = webdriver.Chrome()
driver.get('https://www.tfex.co.th/th/home')

try:
    # คลิกปุ่มเพื่อแสดงข้อมูลที่ต้องการ
    element = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Investor Types')]"))
    )
    element.click()
    print("คลิกสำเร็จ!")
except Exception as e:
    print(f"เกิดข้อผิดพลาด: {e}")

# ดึง HTML จากองค์ประกอบที่มีตารางข้อมูล
time.sleep(10)  # รอให้ข้อมูลปรากฏ
element = driver.find_element(By.XPATH, '/html/body/div/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div[2]/div/div[2]/div/div/div[3]/div[2]')
partial_html = element.get_attribute('outerHTML')  # ดึง HTML
data_df2 = pd.read_html(partial_html)[0]  # แปลง HTML เป็น DataFrame ด้วย pandas
print(data_df2.head(12))  # แสดงข้อมูลบางส่วนเพื่อความแน่ใจ

driver.quit()  # ปิด WebDriver

# ขั้นตอนที่ 2: นำข้อมูลไปเก็บใน Google Sheets
scopes = ['', '']
credentials = Credentials.from_service_account_file(
    r'C:/Users/newta/OneDrive/Desktop/new-git-test/web-dinami/credentials.json', scopes=scopes)

gc = gspread.authorize(credentials)

# เปิด Google Sheets
gs = gc.open_by_key('')
worksheet1 = gs.worksheet('Sheet1')

# อัปโหลดข้อมูลจาก DataFrame ไปยัง Google Sheets
set_with_dataframe(worksheet1, data_df2)
print("อัปโหลดข้อมูลสำเร็จ!")
