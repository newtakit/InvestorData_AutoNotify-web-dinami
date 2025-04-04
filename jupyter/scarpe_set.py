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
# แก้ไขค่าของคอลัมน์ 'stock' ด้วยค่าที่เหมาะสม
data_df2[('นักลงทุนสถาบัน', 'stock')] = [
    "Futures", "Equity Index Futures", "Single Stock Futures", 
    "Precious Metal Futures", "Deferred Precious Metal", 
    "Currency Futures", "Interest Rate Futures", 
    "Agriculture Futures", "Options", "SET50 Index Call", 
    "SET50 Index Put", None  # หรือค่าอื่นๆ ที่เหมาะสม
]

print(data_df2)
# ปิด WebDriver
driver.quit()



