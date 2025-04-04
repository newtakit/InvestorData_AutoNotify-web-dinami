import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe
from google.oauth2.service_account import Credentials
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive 
scopes = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']

credentials = Credentials.from_service_account_file(r'C:/Users/newta/OneDrive/Desktop/new-git-test/web-dinami/credentials.json', scopes=scopes)

gc = gspread.authorize(credentials)

gauth = GoogleAuth()
drive = GoogleDrive(gauth)

# open a google sheet
gs = gc.open_by_key('your_google_sheet_key')  # replace with your Google Sheet key
# select a work sheet from its name
worksheet1 = gs.worksheet('Sheet1')