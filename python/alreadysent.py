import pandas as pd

from sheet import AbstractSheetAdapter

from datetime import datetime

from log import Log

class AlreadySentClass(AbstractSheetAdapter):
    def _get_df(self) -> pd.DataFrame:
        full_df = pd.DataFrame(self.wks.get_all_records())
        if full_df.empty:
            return full_df
        valid = full_df.loc[
            (full_df['Сообщение'] != '') &
            (full_df['Дата и время'] != '')
        ]
        valid['Дата и время'] = valid['Дата и время'].apply(lambda s: datetime.strptime(s, "%Y-%m-%d %H:%M").date())
        return valid

    def check_if_already_sent(self, text) -> bool:
        if self.valid.empty:
            return False
        return not self.valid[self.valid['Сообщение'] == text].empty
    
    def write_text(self, text) -> None:
        row = self._next_available_row()
        self.wks.update_cell(row, 1, text)
        self.wks.update_cell(row, 2, datetime.today().strftime("%Y-%m-%d %H:%M"))
        Log.info(f"Wrote to {self.name} wks")
        