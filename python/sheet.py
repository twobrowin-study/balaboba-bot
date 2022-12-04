import gspread
import pandas as pd

from settings import SheetsSecret, SheetsName
from log import Log

gc = gspread.service_account(filename=SheetsSecret)
sh = gc.open(SheetsName)

class AbstractSheetAdapter():
    def __init__(self, sheet_name: str, name: str) -> None:
        self.wks = sh.worksheet(sheet_name)
        self.valid = self._get_df()
        self.name = name
        Log.info(f"Initialized {self.name} df")
        Log.debug(self.valid)
    
    def update(self) -> None:
        self.valid = self._get_df()
        Log.info(f"Updated {self.name} df")
        Log.debug(self.valid)

    def _get_df(self) -> pd.DataFrame:
        pass
    
    def _next_available_row(self):
        str_list = list(filter(None, self.wks.col_values(1)))
        return str(len(str_list)+1)