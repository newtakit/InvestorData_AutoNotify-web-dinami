# InvestorData-AutoNotify-web-dinami

![head](images/head.jpg)


# อธิบายเป้าหมาย 
"ทำการสกัดข้อมูลหน้าเว็บ SET และ TFEX ที่ใช้ในการเเจ้งเตือนนักลงทุน ทุกเย็นผ่าน line OA โดยการเขียน CODE ผ่าน python และนำข้อมูลที่ได้ ไป เก็บใช้ google sheet และส่งการข้อมูลที่ได้รับเเจ้งเตือนผ่าน line OA  "


 # Tools
Python (ในตัวอย่างจะใช้ Version 3.13.1 / ระบบปฏิบัติการ windows 11)
Library ที่ต้องลงเพิ่ม
 - selenium
 - pandas 
 - spread 
 - time
- Visual Studio Code

# Process

 1: ดึงข้อมูลจากหน้าเว็บ
 2: นำข้อมูลไปเก็บใน Google Sheets
 3: เข้าไปสร้าง app sheets และเขียนคำสั่งให้แจ้งผ่าน line


```python
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

```






3: เข้าไปสร้าง app sheets และเขียนคำสั่งให้แจ้งผ่าน line

 
```python



    const LINE_ACCESS_TOKEN = 'YOUR_NEW_LINE_CHANNEL_ACCESS_TOKEN'; // ใส่ Access Token ใหม่
    const GROUP_ID = 'YOUR_GROUP_ID'; // ใส่ Group ID ของกลุ่ม
  
    // เปิด Google Sheet และดึงข้อมูลทั้งหมดจาก Sheet
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();  // ใช้ Active Sheet
    const data = sheet.getDataRange().getValues();  // ดึงข้อมูลทั้งหมดใน Sheet
  
    let message = " รายงานสุทธิ:\n\n";  // เริ่มต้นข้อความด้วยหัวข้อ
    
    // ดึงวันที่จากแถวแรก (แถวที่ 1 คือข้อมูลจริงๆ)
    const rawDate = data[0][0];  // วันที่ในแถวแรก (แถวที่ 0)
    
    // ใช้ formatDate เพื่อแสดงแค่วันที่ (ไม่รวมเวลา)
    const formattedDate = Utilities.formatDate(rawDate, Session.getScriptTimeZone(), 'yyyy-MM-dd');  // รูปแบบที่ไม่มีเวลา
  
    // เพิ่มวันที่ในข้อความ
    message += `วันที่: ${formattedDate}\n\n`;
  
    // สร้างข้อความจากข้อมูลใน Google Sheet
    for (let i = 1; i < data.length; i++) {  // เริ่มจากแถวที่ 2 เพราะแถวแรกเป็นหัวข้อ
      const category = data[i][0];  // คอลัมน์ที่ 1 (เช่น สถาบัน, ต่างประเทศ, ในประเทศ)
      const netAmount = data[i][1]; // คอลัมน์ที่ 2 (สุทธิ)
  
      // สร้างข้อความในรูปแบบที่ต้องการ
      message += `${category}        ${netAmount}\n`;  // เพิ่มข้อมูลในข้อความ
    }
  
    const url = 'https://api.line.me/v2/bot/message/push';
  
    const payload = {
      to: GROUP_ID,
      messages: [{
        type: 'text',
        text: message  // ข้อความที่ส่งมาจาก Google Sheet
      }]
    };
  
    const options = {
      method: 'post',
      contentType: 'application/json',
      headers: {
        Authorization: 'Bearer ' + LINE_ACCESS_TOKEN
      },
      payload: JSON.stringify(payload)
    };
  
    // ส่งข้อความไปยัง LINE Group
    const response = UrlFetchApp.fetch(url, options);
    Logger.log(response.getContentText());  // เช็คผลลัพธ์
  }
  
    
