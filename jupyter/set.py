import pandas as pd

pd.read_html('https://coinmarketcap.com/')
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# เริ่มต้น WebDriver
driver = webdriver.Chrome()
driver.get('https://www.tfex.co.th/th/market-data/historical-data/trading-by-investor-types')
time.sleep(5)  # รอให้หน้าเว็บโหลดเสร็จ

# ดึง HTML จากองค์ประกอบที่ต้องการ (เช่น div ที่มี class เฉพาะ)
element = driver.find_element(By.XPATH, '/html/body/div/div/div/div[2]/div[2]/div/div/div[2]/div/table')
partial_html = element.get_attribute('outerHTML')  # ดึง HTML ทั้งหมดขององค์ประกอบนั้น

# แสดง HTML ที่ดึงมา
print(partial_html)

# ปิด WebDriver
driver.quit()