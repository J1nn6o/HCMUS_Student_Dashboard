import pandas as pd

class Table:
    @staticmethod
    def rename_columns(df, translation_dict):
        return df.rename(columns=translation_dict)

    @staticmethod
    def df_to_dict(df, student_ids:list):
        filtered_df = df[df[df.columns[0]].isin(student_ids)]
        first_column_name = filtered_df.columns[0] 
        result = {}
        for _, row in filtered_df.iterrows():
            key = row[first_column_name]
            values = [[col_name, row[col_name]] for col_name in filtered_df.columns[0:]]
            result[key] = values
        return result
