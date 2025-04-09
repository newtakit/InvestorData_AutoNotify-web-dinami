/ TOKEN และข้อมูลชีต
const CHANNEL_ACCESS_TOKEN = "xxxx";
const SHEET_ID = "xxxx";
const SHEET_NAME = "Data"; // ชื่อชีตที่เก็บข้อมูล


/**
 * ฟังก์ชันสำหรับตอบกลับคำสั่งของผู้ใช้
 * หากผู้ใช้ส่งคำว่า "รายงาน" จะดึงข้อมูลวันที่ปัจจุบันจากชีต Data และส่งกลับ
 */
function doPost(e) {
  try {
    const requestJSON = e.postData.contents;
    const requestObj = JSON.parse(requestJSON).events[0];
    const token = requestObj.replyToken;
    const userMessage = requestObj.message?.text || "";


    if (!token || !userMessage) {
      Logger.log("Invalid request data");
      return;
    }


    Logger.log("User Message: " + userMessage);


    if (userMessage === "รายงาน") { // ตรวจสอบคำสั่ง "รายงาน"
      const today = getTodayDate(); // วันที่ปัจจุบัน
      const report = generateReport(today);
      sendMessageToLine(token, report);
    } else {
      sendMessageToLine(token, "ขออภัย ไม่พบคำสั่งที่คุณต้องการ");
    }
  } catch (error) {
    Logger.log("Error in doPost: " + error.message);
  }
}


/**
 * ฟังก์ชันสร้างรายงานตามวันที่
 */
function generateReport(date) {
  try {
    const sheet = SpreadsheetApp.openById(SHEET_ID).getSheetByName(SHEET_NAME);
    if (!sheet) throw new Error("Sheet not found: " + SHEET_NAME);


    const data = sheet.getDataRange().getValues(); // ดึงข้อมูลทั้งหมดจากชีต
    const headers = data[0]; // หัวข้อคอลัมน์ (แถวแรก)


    // กรองข้อมูลเฉพาะวันที่
    const filteredRows = data.slice(1).filter(row => {
      const sheetDate = formatDateToYYYYMMDD(row[0]); // แปลงวันที่ในชีต
      return sheetDate === date; // เปรียบเทียบกับวันที่
    });


    if (filteredRows.length === 0) {
      return `ไม่พบข้อมูลสำหรับวันที่ ${date}`;
    }


    let report = `รายงานข้อมูลวันที่ ${date}:\n`;
    filteredRows.forEach((row) => {
      report += headers.map((header, i) => `${header}: ${row[i] || "-"}`).join("\n") + "\n\n";
    });


    return report.trim();
  } catch (error) {
    Logger.log("Error in generateReport: " + error.message);
    return "เกิดข้อผิดพลาดในการสร้างรายงาน";
  }
}


/**
 * ฟังก์ชันส่งข้อความตอบกลับไปยังผู้ใช้
 */
function sendMessageToLine(replyToken, message) {
  try {
    const url = "https://api.line.me/v2/bot/message/reply";
    const postData = {
      replyToken: replyToken,
      messages: [{ type: "text", text: message }],
    };
    const options = {
      method: "post",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + CHANNEL_ACCESS_TOKEN,
      },
      payload: JSON.stringify(postData),
    };
    UrlFetchApp.fetch(url, options);
  } catch (error) {
    Logger.log("Error in sendMessageToLine: " + error.message);
  }
}


/**
 * ฟังก์ชันตรวจสอบเวลาและเรียกฟังก์ชันส่งรายงาน
 * Trigger นี้จะทำงานทุกนาที และตรวจสอบว่าเวลาปัจจุบันคือ 08:00 AM หรือไม่
 */
function checkAndRunReport() {
  const now = new Date();
  const currentHour = now.getHours();
  const currentMinute = now.getMinutes();


  // ตรวจสอบว่าเวลาปัจจุบันคือ 08:00 PM
  if (currentHour === 22 && currentMinute === 30) {
    autoSendReport(); // เรียกฟังก์ชันส่งรายงานอัตโนมัติ
  }
}


/**
 * ฟังก์ชันส่งรายงานอัตโนมัติไปยัง LINE Broadcast
 */
function autoSendReport() {
  const sheet = SpreadsheetApp.openById(SHEET_ID).getSheetByName(SHEET_NAME);
  if (!sheet) throw new Error("Sheet not found: " + SHEET_NAME);


  const today = getTodayDate(); // วันที่ปัจจุบัน
  const properties = PropertiesService.getScriptProperties();
  const lastSentDate = properties.getProperty("lastSentDate");


  // หากส่งรายงานในวันนี้ไปแล้ว จะไม่ส่งซ้ำ
  if (lastSentDate === today) {
    Logger.log(`รายงานของวันที่ ${today} ได้ถูกส่งไปแล้ว`);
    return;
  }


  const data = sheet.getDataRange().getValues();
  const headers = data[0];


  // กรองข้อมูลเฉพาะวันที่ปัจจุบัน
  const filteredRows = data.slice(1).filter(row => {
    const sheetDate = formatDateToYYYYMMDD(row[0]);
    return sheetDate === today;
  });


  if (filteredRows.length === 0) {
    Logger.log(`ไม่พบข้อมูลสำหรับวันที่ ${today}`);
    return;
  }


  let report = `รายงานข้อมูลวันที่ ${today}:\n`;
  filteredRows.forEach((row) => {
    report += headers.map((header, i) => `${header}: ${row[i] || "-"}`).join("\n") + "\n\n";
  });


  const message = report.trim();
  sendBroadcastMessage(message); // ส่งข้อความ Broadcast


  // บันทึกวันที่ส่งรายงาน
  properties.setProperty("lastSentDate", today);
  Logger.log(`รายงานของวันที่ ${today} ได้ถูกส่งแล้ว`);
}


/**
 * ฟังก์ชันส่งข้อความแบบ Broadcast
 */
function sendBroadcastMessage(message) {
  try {
    const url = "https://api.line.me/v2/bot/message/broadcast";
    const postData = {
      messages: [{ type: "text", text: message }],
    };
    const options = {
      method: "post",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + CHANNEL_ACCESS_TOKEN,
      },
      payload: JSON.stringify(postData),
    };
    UrlFetchApp.fetch(url, options);
    Logger.log("ข้อความถูกส่งสำเร็จ");
  } catch (error) {
    Logger.log("Error in sendBroadcastMessage: " + error.message);
  }
}


/**
 * ฟังก์ชันแปลงวันที่ปัจจุบันให้เป็น YYYY-MM-DD
 */
function getTodayDate() {
  const now = new Date();
  const yyyy = now.getFullYear();
  const mm = String(now.getMonth() + 1).padStart(2, '0');
  const dd = String(now.getDate()).padStart(2, '0');
  return `${yyyy}-${mm}-${dd}`;
}


/**
 * ฟังก์ชันแปลง Date Object เป็น YYYY-MM-DD
 */
function formatDateToYYYYMMDD(date) {
  if (date instanceof Date) {
    return Utilities.formatDate(date, "Asia/Bangkok", "yyyy-MM-dd");
  }
  return date;