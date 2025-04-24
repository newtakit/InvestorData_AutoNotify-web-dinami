from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe
from google.oauth2.service_account import Credentials
import time

# Function for web scraping
def scrape_tfex_data():
    driver = webdriver.Chrome()
    driver.get('https://www.tfex.co.th/th/home')

    try:
        # Click button to display the desired data
        element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Investor Types')]"))
        )
        element.click()
        print("Button clicked successfully!")
    except Exception as e:
        print(f"Error while clicking button: {e}")
    
    # Extract HTML from the data table element
    time.sleep(10)  # Wait for data to load
    try:
        element = driver.find_element(By.XPATH, '/html/body/div/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div[2]/div/div[2]/div/div/div[3]/div[2]')
        partial_html = element.get_attribute('outerHTML')  # Extract HTML
        data_df = pd.read_html(partial_html)[0]  # Convert HTML to DataFrame
        print("Data extracted successfully!")
        print(data_df.head(12))  # Preview data
    except Exception as e:
        print(f"Error while extracting data: {e}")
        data_df = pd.DataFrame()  # Return an empty DataFrame in case of error
    
    driver.quit()  # Close the WebDriver
    return data_df

# Function for storing data into Google Sheets
def save_to_google_sheets(dataframe, sheet_id, worksheet_name, credentials_path):
    scopes = ['', '']
    credentials = Credentials.from_service_account_file(credentials_path, scopes=scopes)

    gc = gspread.authorize(credentials)
    try:
        # Open Google Sheets
        gs = gc.open_by_key(sheet_id)
        worksheet = gs.worksheet(worksheet_name)

        # Upload DataFrame to Google Sheets
        set_with_dataframe(worksheet, dataframe)
        print("Data uploaded to Google Sheets successfully!")
    except Exception as e:
        print(f"Error while uploading data: {e}")

# Main script execution
if __name__ == "__main__":
    # Scrape data
    data = scrape_tfex_data()
    
    if not data.empty:  # Proceed only if data was extracted successfully
        # Save to Google Sheets
        sheet_id = ''
        worksheet_name = 'Sheet1'
        credentials_path = r''
        
        save_to_google_sheets(data, sheet_id, worksheet_name, credentials_path)
    else:
        print("No data extracted, skipping Google Sheets upload.")
