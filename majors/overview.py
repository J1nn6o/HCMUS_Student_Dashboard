from majors.database_handler import DatabaseHandler
from utils.sankey import SankeyDiagram
from utils.preprocessing import PreProcessingUtils
from utils.donut import Donut
from utils.barchart import BarChart

# -----------------------------------------------------------------------------------
class Overview(DatabaseHandler):
    def __init__(self, db_params):
        super().__init__(db_params)

    def get_data(self, sql_query):
        """Truy vấn dữ liệu từ cơ sở dữ liệu."""
        return self.query(sql_query)
    
    def get_value(self, sql_query):
        return self.query_scalar(sql_query)
    
    def draw_donut(self, total_student, total_math_student, total_kdl_student):
        return Donut.create_donut_chart(total_student, total_math_student, total_kdl_student)
    
    def get_gpa_column(self, df):
        return BarChart.get_gpa_columns(df)
    
    def process_gpa_columns(self, df, gpa_columns_list: list):
        return BarChart.process_gpa_columns(df, gpa_columns_list)
    
    def draw_horizontal_bar_chart(self, df, application_id, groupby_column, filtered_value, color_scale_bar_chart, height, width):
        return BarChart.draw_horizontal_bar_chart(df, application_id, groupby_column, filtered_value, color_scale_bar_chart, height, width)
   
    def df_to_dict(self, foa_df):
        return PreProcessingUtils.df_to_dict(foa_df)

    def process_overview_data(self, df, selected_columns, drop):
        return SankeyDiagram.process_data(df, selected_columns, drop)
    
    def find_overview_unique_mapping(self, df, df1):
        return SankeyDiagram.find_unique_mapping(df, df1)

    def draw_overview_sankey(self, df, df_dict, final_dict, unique_source_target, color_list, mapping_dict, selected_columns, height=320, width=930):
        return SankeyDiagram.draw_sankey(df, df_dict, final_dict, unique_source_target, color_list, mapping_dict, selected_columns, height, width)
