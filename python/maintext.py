import pandas as pd

from sheet import AbstractSheetAdapter

class MainTextClass(AbstractSheetAdapter):
    def _get_df(self) -> pd.DataFrame:
        full_df = pd.DataFrame(self.wks.get_all_records())
        if full_df.empty:
            return full_df
        valid = full_df.loc[
            (full_df['Основной текст'] != '')
        ]
        return valid
        
    def get_main_text(self) -> str:
        for _,row in self.valid.iterrows():
            return row['Основной текст']
