from google.oauth2.service_account import Credentials
import gspread
scopes = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']

sheet_id = '******'

credentials = Credentials.from_service_account_file('path_json', scopes=scopes)

gc = gspread.authorize(credentials)
gs = gc.open_by_key(sheet_id)
gs.values_append(
    'SET',  # ชื่อ Sheet
    {'valueInputOption': 'USER_ENTERED'},
    {'values': [data_df2]}
)