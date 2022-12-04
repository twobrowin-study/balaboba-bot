import pandas as pd

from sheet import AbstractSheetAdapter

from settings import SheetTiming
from log import Log

from datetime import datetime

class TimingClass(AbstractSheetAdapter):
    def _get_df(self) -> pd.DataFrame:
        full_df = pd.DataFrame(self.wks.get_all_records())
        if full_df.empty:
            return pd.DataFrame({
                'Ежедневное время': '',
                'Если дата не равна': '',
                'Изменить': 'Нет',
                'Изменено': 'Да'
            })
        valid = full_df.loc[
            (full_df['Ежедневное время'] != '') &
            (full_df['Если дата не равна'] != '') &
            (full_df['Изменить'].isin(["Да", "Нет"])) &
            (full_df['Изменено'].isin(["Да", "Нет"]))
        ]
        return valid
    
    def get_at_everyday_time(self) -> str:
        return datetime.strptime(self.valid.iloc[0]['Ежедневное время'], '%H:%M:%S').strftime('%H:%M')
    
    def get_until_date(self) -> str:
        return self.valid.iloc[0]['Если дата не равна']

    def check_if_should_change(self) -> bool:
        return not self.valid[(self.valid['Изменить'] == "Да") & (self.valid['Изменено'] == "Нет")].empty
    
    def write_changed(self) -> None:
        self.valid.iloc[0]['Изменено'] = 'Да'
        self.wks.update_cell(2, 4, 'Да')
        Log.info(f"Wrote to {self.name} df and wks")
        
Timing = TimingClass(SheetTiming, 'timing')