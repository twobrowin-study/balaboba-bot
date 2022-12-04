import pandas as pd

from sheet import AbstractSheetAdapter

class PhrasesClass(AbstractSheetAdapter):
    def _get_df(self) -> pd.DataFrame:
        full_df = pd.DataFrame(self.wks.get_all_records())
        if full_df.empty:
            return full_df
        valid = full_df.loc[
            (full_df['Фраза'] != '') &
            (full_df['Тип'] != '')
        ]
        return valid
    
    def get_random_phrase_and_type(self) -> tuple[str, int]:
        for ans in self.valid.sample(n = 1).itertuples(index=False, name=None):
            return (ans[0], int(ans[1]))