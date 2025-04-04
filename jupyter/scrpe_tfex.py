from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# เริ่มต้น WebDriver
driver = webdriver.Chrome()

# เปิดหน้าเว็บ
driver.get('https://www.tfex.co.th/th/home')

try:
    # รอให้ปุ่มหรือข้อความที่ต้องการพร้อมสำหรับการคลิก
    element = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Investor Types')]"))
    )
    element.click()
   
    print("คลิกสำเร็จ!")
except Exception as e:
    print(f"เกิดข้อผิดพลาด: {e}")
time.sleep(10)  # รอให้หน้าเว็บโหลดเสร็จ

# ดึง HTML จากองค์ประกอบที่ต้องการ (เช่น div ที่มี class เฉพาะ)
element = driver.find_element(By.XPATH, '/html/body/div/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div[2]/div/div[2]/div/div/div[3]/div[2]')
partial_html = element.get_attribute('outerHTML')  # ดึง HTML ทั้งหมดขององค์ประกอบนั้น
data_df2 = pd.read_html(partial_html)[0]  # เลือกตารางแรก
# แสดง HTML ที่ดึงมา
print(data_df2.head(12))  # แสดง 12 แถวแรกของ DataFrame
# ปิด WebDriver
driver.quit()