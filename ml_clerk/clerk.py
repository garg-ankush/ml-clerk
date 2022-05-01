import os
import pandas as pd
import time
import pygsheets
from dotenv import load_dotenv
load_dotenv()


class Clerk:
    def __init__(self, excel_mode: bool = True, google_sheets_mode: bool = False):
        self.excel_mode = excel_mode
        self.google_sheets_mode = google_sheets_mode

        self.file_path = None
        self.sheet_name = None

        self.workbook = None
        self.sheet = None
        self.data = None

        self._is_setup_complete = False

        if not self.excel_mode and not self.google_sheets_mode:
            raise ValueError("Either excel model or google sheets mode needs to be on for clerk to start recording.")

        if self.excel_mode and self.google_sheets_mode:
            self.excel_mode = False

    def _excel_setup(self, file_path, sheet_name):
        if '.xlsx' not in file_path:
            raise Exception('Filepath must be an excel file with `.xlsx` extension.')
        try:
            self.df = pd.read_excel(file_path, sheet_name)
        except Exception:
            print("Either the workbook or the sheet doesn't exist. So creating and setting up a new workbook.")
            df = pd.DataFrame()
            df.to_excel(file_path)

    def _google_sheets_setup(self, file_path: str, sheet_name: str):
        if self.google_sheets_mode is not None:
            try:
                self.authorize = pygsheets.authorize(service_file=os.getenv("PATH_TO_TOKEN_JSON_FOR_GOOGLE_SHEETS"))
            except Exception as error:
                print(error)
                print("Are you authorized to make entries to this google sheet? "
                      "Check the READme file for further directions.")
                return

            try:
                self.workbook = self.authorize.open_by_url(file_path)
                self.sheet = self.workbook.worksheet_by_title(sheet_name)
            except Exception:
                print("Either the workbook or the sheet doesn't exist.")

    def set_up(self, file_path: str, sheet_name: str):
        self.file_path = file_path
        self.sheet_name = sheet_name

        if self.excel_mode:
            self._excel_setup(self.file_path, self.sheet_name)

        if self.google_sheets_mode:
            self._google_sheets_setup(self.file_path, self.sheet_name)

        self._is_setup_complete = True

    def _write(self, df):
        if self.excel_mode:
            df.to_excel(self.file_path, index=False)

        if self.google_sheets_mode:
            self.sheet.set_dataframe(df, (1, 1), extend=True)

    def record(self, **kwargs):
        if not self._is_setup_complete:
            print("Clerk needs a workbook to record. Workbook setup not complete.")
            return

        if not kwargs:
            print("You must pass in something for the clerk to record.")
            return

        dataframe_of_records = pd.DataFrame([kwargs])
        dataframe_of_records['timestamp'] = time.time()

        if self.excel_mode:
            self.data = pd.read_excel(self.file_path)
            # Append the new data to the existing data
            df = self.data.append(dataframe_of_records)
            # Write the entire dataframe again
            df.to_excel(self.file_path, index=False)

        if self.google_sheets_mode:
            # Get the data that currently exists in the sheet
            self.data = self.sheet.get_as_df(self.file_path)
            # Append the new data to the existing data
            df = self.data.append(dataframe_of_records)
            # Write the entire dataframe again
            self.sheet.set_dataframe(df, (1, 1), extend=True)

        print("Clerk recorded some data ...")
