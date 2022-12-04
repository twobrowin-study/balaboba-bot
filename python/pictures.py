import pandas as pd

from sheet import AbstractSheetAdapter

from datetime import datetime

class PicturesClass(AbstractSheetAdapter):
    def _get_df(self) -> pd.DataFrame:
        full_df = pd.DataFrame(self.wks.get_all_records())
        if full_df.empty:
            return full_df
        valid = full_df.loc[
            (full_df['Дата'] != '') &
            (full_df['Картинка'] != '')
        ]
        valid['Дата'] = valid['Дата'].apply(lambda s: datetime.strptime(s, "%d.%m.%Y").date())
        return valid
        
    def get_today_image(self) -> str:
        for _,row in self.valid[self.valid['Дата'] == datetime.today().date()].iterrows():
            return row['Картинка']
