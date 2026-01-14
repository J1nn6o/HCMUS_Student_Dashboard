from dash import Input, Output, State
from pages.config_vie import column_translation

def register_callbacks(app, overview, math, gpa_foa_df, COLOR_SCALE_BAR_CHART, gpa_foa_dict, radar_math_df, kdl, radar_kdl_df, total_math_course_num_df, total_kdl_course_num_df, total_course_num_per_student_df, student_df):
    @app.callback(
        Output('sidebar', 'className'),
        Input('sidebarCollapse', 'n_clicks'),
        prevent_initial_call=True
    )
    def toggle_sidebar(n_clicks):
        if n_clicks is None or n_clicks % 2 == 0:
            return ''  # Ân sidebar
        else:
            return 'active'  # Hiển thị sidebar
        
    @app.callback(
        Output('gpa-scale-dropdown', 'options'),
        Input('year-scale-dropdown', 'value')
    )
    def update_gpa_scale_options(selected_year):
        if selected_year and selected_year in gpa_foa_dict:
            return [{'label': scale, 'value': scale} for scale in gpa_foa_dict[selected_year]]
        return []

    @app.callback(
        Output('bar_chart', 'figure'),
        Input('submit_button_overview', 'n_clicks'),
        [State('year-scale-dropdown', 'value'),
         State('gpa-scale-dropdown', 'value')],
        prevent_initial_call=True
    )
    def update_bar_chart(n_clicks, selected_year, scale):
        bar_chart = overview.draw_horizontal_bar_chart(
            df=gpa_foa_df, 
            application_id='application_id',
            groupby_column=selected_year,
            filtered_value=scale,
            color_scale_bar_chart=COLOR_SCALE_BAR_CHART, 
            height=400,
            width=920  
        )

        return bar_chart

    @app.callback(
        [
            Output('radar_chart_math', 'figure'),
            Output('student_bar_chart_math', 'figure'),
            Output('student_table_math', 'data'),
            Output('student_table_math', 'columns')
        ],
        Input('submit_button_math', 'n_clicks'),
        [
            State('student_id_1_math', 'value'),
            State('student_id_2_math', 'value')
        ],
        prevent_initial_call=True
    )
    def update_student_table(n_clicks, student_id_1_math, student_id_2_math):
        student_list = [student_id for student_id in [student_id_1_math, student_id_2_math] if student_id]

        if not student_list:
            return 'Vui lòng nhập ít nhất 1 sinh viên'
        
        student_list = [student_id for student_id in [student_id_1_math, student_id_2_math] if student_id]
        radar_math_chart = math.draw_radar(radar_math_df, student_list)
        total_course_num_per_math_student_dict = math.preprocess_data_for_bar_chart(total_course_num_per_student_df, student_list, 'course_group', 'total_count_course')
        student_bar_chart_math = math.draw_bar_chart(total_math_course_num_df, total_course_num_per_math_student_dict, student_list, height=340, width=650)

        student_dict = math.create_table(student_df, student_list, column_translation)
        student_keys = list(student_dict.keys())
        
        columns = [
            {'name': student_dict[student_keys[0]][i][0], 'id': f'col_{i}'}
            for i in range(len(student_dict[student_keys[0]]))
        ]

        data = [
            {
                f'col_{i}': student_dict[student][i][1]
                for i in range(len(student_dict[student]))
            }
            for student in student_dict
        ]
        
        return radar_math_chart, student_bar_chart_math, data, columns


    @app.callback(
        [
            Output('radar_chart_kdl', 'figure'),
            Output('student_bar_chart_kdl', 'figure'),
            Output('student_table_kdl', 'data'),
            Output('student_table_kdl', 'columns')
        ],
        Input('submit_button_kdl', 'n_clicks'),
        [
            State('student_id_1_kdl', 'value'),
            State('student_id_2_kdl', 'value')
        ],
        prevent_initial_call=True
    )
    def update_student_table(n_clicks, student_id_1_kdl, student_id_2_kdl):
        student_list = [student_id for student_id in [student_id_1_kdl, student_id_2_kdl] if student_id]
        
        if not student_list:
            return 'Vui lòng nhập ít nhất 1 sinh viên'

        radar_kdl_chart = kdl.draw_radar(radar_kdl_df, student_list)
        total_course_num_per_kdl_student_dict = kdl.preprocess_data_for_bar_chart(total_course_num_per_student_df, student_list, 'course_group', 'total_count_course')
        student_bar_chart_kdl = kdl.draw_bar_chart(total_kdl_course_num_df, total_course_num_per_kdl_student_dict, student_list, height=380, width=650)

        student_dict = math.create_table(student_df, student_list, column_translation)
        student_keys = list(student_dict.keys())
        
        columns = [
            {'name': student_dict[student_keys[0]][i][0], 'id': f'col_{i}'}
            for i in range(len(student_dict[student_keys[0]]))
        ]
        
        data = [
            {
                f'col_{i}': student_dict[student][i][1]
                for i in range(len(student_dict[student]))
            }
            for student in student_dict
        ]
        
        return radar_kdl_chart, student_bar_chart_kdl, data, columns
