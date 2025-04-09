function sendLineNotifyToGroup() {
    const LINE_ACCESS_TOKEN = 'YOUR_NEW_LINE_CHANNEL_ACCESS_TOKEN'; // ใส่ Access Token ใหม่
    const GROUP_ID = 'YOUR_GROUP_ID'; // ใส่ Group ID ของกลุ่ม
  
    // เปิด Google Sheet และดึงข้อมูลทั้งหมดจาก Sheet
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();  // ใช้ Active Sheet
    const data = sheet.getDataRange().getValues();  // ดึงข้อมูลทั้งหมดใน Sheet
  
    let message = "📢 รายงานสุทธิ:\n\n";  // เริ่มต้นข้อความด้วยหัวข้อ
    
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
  