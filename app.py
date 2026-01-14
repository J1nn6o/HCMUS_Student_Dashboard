import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output

from pages.callback import register_callbacks  
from pages.home import get_sidebar, layout 
from pages.about import get_about_page
from majors.database_handler import DatabaseHandler
from majors.overview import Overview
from majors.mathematics import Mathematics
from majors.datascience import DataScience
from pages.config_vie import column_translation

from utils.constant import *
import traceback


db_params = {
    "dbname": "test_db",       
    "user": "root",             
    "password": "root",             
    "host": "localhost",             
    "port": 5432                      
}

overview = Overview(db_params)
math = Mathematics(db_params)
kdl = DataScience(db_params)

try:
    #Process data for Overview
    overview_df = overview.get_data(OVERVIEW_QUERY)
    total_input_student = overview.get_value(TOTAL_STUDENTS)
    foa_df = overview.get_data(FOA_TABLE)
    foa_dict = overview.df_to_dict(foa_df)
    
    selected_columns_overview = ['application_id', 'field_name', 'subfield_name', 'major_name', 'graduated_status']
    grouped_df, final_df = overview.process_overview_data(overview_df, selected_columns_overview, drop='NGHỈ HỌC')
    unique_source_target, df_dict, final_dict, mapping_dict = overview.find_overview_unique_mapping(grouped_df, final_df)
    sankey_fig_overview = overview.draw_overview_sankey(
        overview_df,
        df_dict,
        final_dict,
        unique_source_target,
        COLOR_LIST,
        mapping_dict,
        selected_columns_overview,
        350,  # Positional argument for height
        950  # Positional argument for width
    )

    #Process data for Math 
    df_drop = math.get_data(QUERY_DROP)
    selected_columns = ['field_name', 'first_gpa_status','second_gpa_status', 'third_gpa_status', 'fourth_gpa_status']
    
    math_df = math.get_data(TTH_SQL_QUERY)
    total_math_input_student = math.get_value(TOTAL_MATH_STUDENT)
    math_df = math.preprocessing_data(math_df, df_drop, 'Nhóm ngành Toán học')
    grouped_df_math, final_df_math = math.process_math_data(math_df, selected_columns, drop='NGHI_HOC')
    unique_source_target_math, df_dict_math, final_dict_math, mapping_dict_math = math.find_math_unique_mapping(grouped_df_math, final_df_math)
    sankey_fig_math = math.draw_math_sankey(
        math_df,
        df_dict_math,
        final_dict_math,
        unique_source_target_math,
        COLOR_LIST,
        mapping_dict_math,
        selected_columns,
        160,  # Positional argument for height
        1200  # Positional argument for width
    )
    #Radar chart for THH
    total_math_course_num_df = math.get_data(TOTAL_MATH_COURSE_NUM)
    radar_math_df = math.get_data(RADAR_TTH_QUERY)
    radar_math_df = math.merge_df_radar(radar_math_df, total_math_course_num_df)
    default_math_student_ids = ['21110013', '21110020']
    radar_chart_math = math.draw_radar(radar_math_df, default_math_student_ids)
    
    #Dataframe table for TTH
    student_df = math.get_data(STUDENT_DF)
    math_student_dict = math.create_table(student_df, default_math_student_ids, column_translation) 
    
    #Process data for KDL
    kdl_df = kdl.get_data(KDL_SQL_QUERY)
    total_kdl_input_student = kdl.get_value(TOTAL_KDL_STUDENT)
    kdl_df = kdl.preprocessing_data(kdl_df, df_drop, 'Ngành Khoa học dữ liệu')
    grouped_df_kdl, final_df_kdl = kdl.process_kdl_data(kdl_df, selected_columns, drop='NGHI_HOC')
    unique_source_target_kdl, df_dict_kdl, final_dict_kdl, mapping_dict_kdl = kdl.find_kdl_unique_mapping(grouped_df_kdl, final_df_kdl)
    sankey_fig_kdl = kdl.draw_kdl_sankey(
        kdl_df,
        df_dict_kdl, 
        final_dict_kdl, 
        unique_source_target_kdl, 
        COLOR_LIST, 
        mapping_dict_kdl, 
        selected_columns, 
        150, 
        1200)
    
    # Radar for KDL
    total_kdl_course_num_df = kdl.get_data(TOTAL_KDL_COURSE_NUM)
    radar_kdl_df = kdl.get_data(RADAR_KDL_QUERY)
    radar_kdl_df = kdl.merge_df_radar(radar_kdl_df, total_kdl_course_num_df)
    default_kdl_student_ids = ['21280054', '21280030']
    radar_chart_kdl = kdl.draw_radar(radar_kdl_df, default_kdl_student_ids)
    
    # Dataframe table for KDL
    kdl_student_dict = kdl.create_table(student_df, default_kdl_student_ids, column_translation)

    # Donut chart
    donut_chart = overview.draw_donut(total_input_student, total_math_input_student, total_kdl_input_student)

    # Bar chart
    gpa_foa_df = overview.get_data(GPA_BAR_CHART)
    gpa_foa_df, gpa_columns_list = overview.get_gpa_column(gpa_foa_df)
    gpa_status_dict = overview.process_gpa_columns(gpa_foa_df, gpa_columns_list)
    default_gpa_status = '2021-2025'
    default_filtered_value = 'gpa>=7_and_<8.5'
    overview_bar_chart = overview.draw_horizontal_bar_chart(gpa_foa_df, 'application_id', default_gpa_status, default_filtered_value, COLOR_SCALE_BAR_CHART, height=400, width=920)
    
    # Bar chart for TTH
    total_course_num_per_student_df = math.get_data(STUDENT_TOTAL_COURSE_NUM)
    total_course_num_per_math_student_dict = math.preprocess_data_for_bar_chart(total_course_num_per_student_df, default_math_student_ids, 'course_group', 'total_count_course')
    math_bar_chart = math.draw_bar_chart(total_math_course_num_df, total_course_num_per_math_student_dict, default_math_student_ids, height=340, width=650)

    # Bar chart for KDL
    total_course_num_per_kdl_student_dict = kdl.preprocess_data_for_bar_chart(total_course_num_per_student_df, default_kdl_student_ids, 'course_group', 'total_count_course')
    kdl_bar_chart = kdl.draw_bar_chart(total_kdl_course_num_df, total_course_num_per_kdl_student_dict, default_kdl_student_ids, height=340, width=650)

    # Create the Dash app
    app = dash.Dash(
        __name__,
        external_stylesheets=[
            dbc.themes.BOOTSTRAP,
            'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css'
        ],
        show_undo_redo=False,
        suppress_callback_exceptions=True  # Cho phép callback với các thành phần không nằm trong layout ban đầu
    )

    # Layout for the app
    app.layout = html.Div([
        dcc.Location(id="url", refresh=False),
        html.Div(id="page-content") 
    ])

    # Callback để điều hướng giữa các trang
    @app.callback(
        Output("page-content", "children"),
        [Input("url", "pathname")]
    )
    def display_page(pathname):
        if pathname == "/about":
            return get_about_page(active_item='about')
        else:
            return layout(
                donut_chart,
                overview_bar_chart,
                gpa_columns_list,
                foa_dict,
                sankey_fig_overview,
                sankey_fig_math, 
                sankey_fig_kdl,
                radar_chart_math,               
                radar_math_df,
                math_bar_chart,
                radar_chart_kdl,
                radar_kdl_df,
                kdl_bar_chart,
                math_student_dict,
                kdl_student_dict
            )

    # Register callbacks
    register_callbacks(app, overview, math, gpa_foa_df, COLOR_SCALE_BAR_CHART, gpa_status_dict, radar_math_df, kdl, radar_kdl_df, total_math_course_num_df, total_kdl_course_num_df, total_course_num_per_student_df, student_df)

    if __name__ == '__main__':
        app.run(debug=True)

except Exception as e:
    print(e)
    print(traceback.format_exc()) 

# Đóng kết nối        
finally:
    overview.close()
    math.close()
    kdl.close()