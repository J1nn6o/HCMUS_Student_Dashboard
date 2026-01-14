import pandas as pd
from majors.database_handler import DatabaseHandler
from utils.sankey import SankeyDiagram
from utils.preprocessing import PreProcessingUtils
from utils.radarchart import RadarChart
from utils.barchart import BarChart
from utils.table import Table

# -----------------------------------------------------------------------------------
class DataScience(DatabaseHandler):
    def __init__(self, db_params):
        super().__init__(db_params)

    def get_data(self, sql_query):
        """Truy vấn dữ liệu từ cơ sở dữ liệu."""
        return self.query(sql_query)

    def get_value(self, sql_query):
        return self.query_scalar(sql_query)

    def preprocessing_data(self, df, df1, field_name):
        return PreProcessingUtils.preprocessing_data(df, df1, field_name)

    def process_kdl_data(self, df, selected_columns, drop):
        return SankeyDiagram.process_data(df, selected_columns, drop)
    
    def find_kdl_unique_mapping(self, df, df1):
        return SankeyDiagram.find_unique_mapping(df, df1)

    def draw_kdl_sankey(self, df, df_dict, final_dict, unique_source_target, color_list, mapping_dict, selected_columns, height=150, width=1200):
        return SankeyDiagram.draw_sankey(df, df_dict, final_dict, unique_source_target, color_list, mapping_dict, selected_columns, height, width)

    def merge_df_radar(self, radar_kdl_df, total_course_num_df):
        return RadarChart.merge_course_num_and_create_new_column(radar_kdl_df, total_course_num_df)
    
    def draw_radar(self, kdl_df: pd.DataFrame, student_ids):
        return RadarChart.plot_students_radar_chart(kdl_df, student_ids)

    def create_table(self, df: pd.DataFrame, student_ids: list, column_translation):
        df = Table.rename_columns(df, column_translation)
        student_dict = Table.df_to_dict(df, student_ids)
        return student_dict

    def preprocess_data_for_bar_chart(self, df, student_ids: list, course_group, total_count_course):
        return BarChart.df_to_dict(df, student_ids, course_group, total_count_course)
    
    def draw_bar_chart(self, total_course_num_df, total_course_num_per_student_dict, student_ids: list, height, width):
        return BarChart.plot_course_bar_chart(total_course_num_df, total_course_num_per_student_dict, student_ids, height, width)