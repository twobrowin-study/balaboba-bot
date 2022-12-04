import pandas as pd

from sheet import AbstractSheetAdapter

class GroupsClass(AbstractSheetAdapter):
    def _get_df(self) -> pd.DataFrame:
        full_df = pd.DataFrame(self.wks.get_all_records())
        if full_df.empty:
            return full_df
        valid = full_df.loc[
            (full_df['Id'] != '') &
            (full_df['Описание'] != '') &
            (full_df['Активно'] != '')
        ]
        return valid
    
    def get_id_list(self) -> list[str]:
        return self.valid[self.valid['Активно'] == "Да"]['Id'].to_list()