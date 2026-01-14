import pandas as pd
import numpy as np

class PreProcessingUtils:
    @staticmethod
    def preprocessing_data(df, df1, field_name: str):
        mapping = {
            '2021-2022': '1st',
            '2021-2022, 2022-2023': '2nd',
            '2021-2022, 2022-2023, 2023-2024': '3rd',
            '2021-2022, 2022-2023, 2023-2024, 2024-2025': '4th'
        }
        
        df.insert(0, 'field_name', field_name)

        common_students_mask = df1[df1['student_id'].isin(df['student_id'])]
        gpa_status_cols = [col for col in df.columns if col.endswith('_gpa_status')]

        for _, row in common_students_mask.iterrows():
            student_id = row['student_id']
            school_year = row['school_year']
            
            for status_col in gpa_status_cols:
                mask = (df['student_id'] == student_id) & (df[status_col].str.contains(school_year, na=False))
                df.loc[mask, status_col] = [None]

        def replace_gpa_status(column):
            extracted = column.str.extract(r'^(.*)_gpa')[0]
            replaced = extracted.map(mapping)
            return replaced + column.str.extract(r'(_gpa.*)')[0]

        columns_to_replace = ['first_gpa_status', 'second_gpa_status', 'third_gpa_status', 'fourth_gpa_status']
        for col in columns_to_replace:
            df[col] = replace_gpa_status(df[col])

        df['second_gpa_status'] = df['second_gpa_status'].fillna('NGHI_HOC_NAM_2')
        df['third_gpa_status'] = df['third_gpa_status'].fillna('NGHI_HOC_NAM_3')
        df['fourth_gpa_status'] = df['fourth_gpa_status'].fillna('NGHI_HOC_NAM_4')

        return df
    
    @staticmethod
    def df_to_dict(df):
        if df.shape[1] < 2:
            raise ValueError("DataFrame phải có ít nhất 2 cột")
        
        return dict(zip(df.iloc[:, 0], df.iloc[:, 1]))
    

