import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# เริ่มต้น WebDriver
driver = webdriver.Chrome()
driver.get('https://www.tfex.co.th/th/market-data/historical-data/trading-by-investor-types')
time.sleep(5)  # รอให้หน้าเว็บโหลดเสร็จ

# ดึง HTML จากองค์ประกอบที่ต้องการ (เช่น div ที่มี class เฉพาะ)
element = driver.find_element(By.XPATH, '/html/body/div/div/div/div[2]/div[2]/div/div/div[2]/div')
partial_html = element.get_attribute('outerHTML')  # ดึง HTML ทั้งหมดขององค์ประกอบนั้น

# แสดง HTML ที่ดึงมา
data_df2 = pd.read_html(partial_html)[0]  # เลือกตารางแรก
print(data_df2.head(12))  # แสดง 12 แถวแรกของ DataFrame

# ปิด WebDriver
driver.quit()



