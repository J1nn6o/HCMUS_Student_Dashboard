import pandas as pd
import numpy as np
# from majors.database_handler import DatabaseHandler
import plotly.graph_objects as go
# import matplotlib.pyplot as plt
from utils.color_utils import lighten_color

class SankeyDiagram:
    @staticmethod
    def process_data(df, selected_columns, drop:str):
        drop = drop
        def groupby_df(selected_columns, df):
            dfs = []
            performance_order_academic = ['PT01', 'PT02', 'PT03', 'PT04', 'PT05', 'PT07', 'PT7B']
            performance_order_final = ['Ngành Toán học', 'Ngành Toán tin', 'Ngành Toán ứng dụng', 'Ngành Khoa học dữ liệu ', 'Drop subfield']
            for i in range(len(selected_columns) - 1):
                grouped_df = df.groupby([selected_columns[i], selected_columns[i + 1]])['student_id'].count().reset_index()
                grouped_df.columns = ['source', 'target', 'value']
                # Kiểm tra và sắp xếp cho từng categorical feature
                if selected_columns[i] == 'academic_performance':
                    grouped_df['source'] = pd.Categorical(grouped_df['source'], categories=performance_order_academic, ordered=True)

                if selected_columns[i] == 'final_academic_performance':
                    grouped_df['source'] = pd.Categorical(grouped_df['source'], categories=performance_order_final, ordered=True)

                if selected_columns[i + 1] == 'academic_performance':
                    grouped_df['target'] = pd.Categorical(grouped_df['target'], categories=performance_order_academic, ordered=True)

                if selected_columns[i + 1] == 'final_academic_performance':
                    grouped_df['target'] = pd.Categorical(grouped_df['target'], categories=performance_order_final, ordered=True)

                # Sắp xếp theo thứ tự đã định nghĩa cho cả source và target
                grouped_df = grouped_df.sort_values(by=['source', 'target'])
                
                dfs.append(grouped_df)

            overall_df = pd.concat(dfs, axis=0)
            final_df = dfs[-1]  
            return overall_df, final_df

        def set_drop_value(df, drop):
            if 'value' in df.columns:
                df.loc[
                    df['source'].str.contains(drop, case=False, na=False), 'value'] = 0
            return df

        grouped_df, final_df = groupby_df(selected_columns, df)
        grouped_df = set_drop_value(grouped_df, drop)
        final_df = set_drop_value(final_df, drop)
        return grouped_df, final_df

    @staticmethod
    def find_unique_mapping(df1, df2):
        unique_source_target = list(pd.unique(df1[['source', 'target']].values.ravel('K')))
        mapping_dict = {value: idx for idx, value in enumerate(unique_source_target)}

        df1['source'] = df1['source'].map(mapping_dict)
        df1['target'] = df1['target'].map(mapping_dict)
        df2['source'] = df2['source'].map(mapping_dict)
        df2['target'] = df2['target'].map(mapping_dict)

        df_dict = df1.to_dict(orient='list')
        final_dict = df2.to_dict(orient='list')

        return unique_source_target, df_dict, final_dict, mapping_dict

    @staticmethod
    def calculate_total_values_by_source(df_dict, mapping_dict):
        df_tempt = pd.DataFrame(df_dict)

        drop_values = [value for key, value in mapping_dict.items() if 'NGHI_HOC' in key or 'NGHỈ HỌC' in key]

        specific_rows = df_tempt[df_tempt['target'].isin(drop_values)]

        total_values_by_source = df_tempt[~df_tempt['source'].isin(drop_values)].groupby('source')['value'].sum()

        if not specific_rows.empty:
            total_values_by_target_for_specific = specific_rows.groupby('target')['value'].sum()
            total_values_by_source = pd.concat([total_values_by_source, total_values_by_target_for_specific]).to_dict()

        return total_values_by_source

    @staticmethod
    def calculate_total_values_by_target(final_df):
        df = pd.DataFrame(final_df)
        total_values_by_target = df.groupby('target')['value'].sum().to_dict()
        return total_values_by_target
    
    @staticmethod
    def calculate_custom_node_positions(df_dict, unique_source_target, selected_columns):
        x_positions = {}
        y_positions = {}

        

        # Giá trị y cố định cho từng node
        fixed_y_values = {
            'application_id':   [0.03,  # PT01
                                 0.13,  # PT02
                                 0.28,  # PT03
                                 0.42,  # PT04
                                 0.52,  # PT05
                                 0.62,  # PT07
                                 0.72], # PT7B
            'field_name': [0.62,           # Nhóm ngành Khoa học dữ liệu
                           0.22],          # Nhóm ngành Toán học
            'subfield_name': [0.75,         # Nghi học CSN
                              0.6,        # Ngành Khoa học dữ liệu
                              0.1,        # Ngành Toán học
                              0.25,         # Ngành Toán tin
                              0.4],       # Ngành Toán ứng dụng
                                  
            'major_name': [0.42,        # Cơ học
                           0.07,        # Giải tích
                           0.12,        # Giải tích số
                           0.7,        # KHDL
                           0.24,        # Khoa học dữ liệu 2
                           0.58,         # Ly luan
                           0.82,        # Nghi hoc
                           0.35,        # Phương pháp Toán trong Tin học
                           0.29,        # Toán tin ứng dụng
                           0.48,         # Toán tài chính
                           0.53,        # Tối ưu và hệ thống
                           0.18,        # Xác suất thống kê
                           0.02,        # Đại số
                           0.7],        # Nghỉ học (CN)
            'graduated_status': [0.75,      # CÒN HỌC TIẾP
                                 0.25,],     # TOT NGHIEP
            'field': [0.1,                 # 11
                      0.1],                # 28
            'first_gpa_status': [0.8,       # 1st_gpa >=5_and_<7
                                 0.4,       # 1st_gpa>=7_and_<8.5
                                 0.1,       # 1st_gpa>=8.5
                                 1],        # 
            'second_gpa_status': [0.75,      # >=5_and_<7
                                  0.4,     # >=7_and_<8.5
                                  0.1,      # >=8.5
                                  0.95,     # second_year_drop
                                  ],    
            'third_gpa_status': [0.75,      # >=5_and_<7
                                 0.4,       # >=7_and_<8.5
                                 0.05,      # >=8.5
                                 0.95],     # third_year_drop
            'fourth_gpa_status': [0.8,      # >=5_and_<7
                                  0.4,      # >=7_and_<8.5
                                  0.1,      # >=8.5
                                  0.9],     # drop

        }

        # Phân loại các node theo nhóm feature'application_id', 'field_name', 'subfield_name', 'major_name', 'graduated_status'
        feature_groups = {
            'application_id': [node for node in unique_source_target if node in ['PT01', 'PT02', 'PT03', 'PT04', 'PT05', 'PT07', 'PT7B']],
            'field_name': [node for node in unique_source_target if node in ['Ngành Khoa học dữ liệu', 'Nhóm ngành Toán học']],
            'subfield_name': [node for node in unique_source_target if node in ['NGHỈ HỌC (CSN)', 'Ngành Khoa học dữ liệu ', 'Ngành Toán học', 'Ngành Toán tin', 'Ngành Toán ứng dụng']],
            'major_name': [node for node in unique_source_target if node in ['Cơ học', 'Giải tích', 'Giải tích số', 'Khoa học dữ liệu 1', 'Khoa học dữ liệu 2', 
                                                                             'Lý luận và phương pháp giảng dạy môn Toán', 'NGHỈ HỌC (CN)', 'Phương pháp Toán trong Tin học', 
                                                                             'Toán tin ứng dụng', 'Toán tài chính', 'Tối ưu và hệ thống', 'Xác suất thống kê', 'Đại số']],
            'graduated_status': [node for node in unique_source_target if node in ['CÒN HỌC TIẾP', 'TỐT NGHIỆP']],
            'field_name': [node for node in unique_source_target if node in ['Nhóm ngành Toán học', 'Ngành Khoa học dữ liệu']],
            'first_gpa_status': [node for node in unique_source_target if node in ['1st_gpa>=5_and_<7', '1st_gpa>=7_and_<8.5', '1st_gpa>=8.5', '1st_gpa>=8.5']],
            'second_gpa_status': [node for node in unique_source_target if node in ['2nd_gpa>=5_and_<7', '2nd_gpa>=7_and_<8.5', '2nd_gpa>=8.5', 'NGHI_HOC_NAM_2']],
            'third_gpa_status': [node for node in unique_source_target if node in ['3rd_gpa>=5_and_<7', '3rd_gpa>=7_and_<8.5', '3rd_gpa>=8.5', 'NGHI_HOC_NAM_3']],
            'fourth_gpa_status': [node for node in unique_source_target if node in ['4th_gpa>=5_and_<7', '4th_gpa>=7_and_<8.5', '4th_gpa>=8.5', 'NGHI_HOC_NAM_4']],
        }

        # Tính toán vị trí x và y cho từng node trong từng nhóm feature
        for feature in selected_columns:
            nodes = feature_groups.get(feature, [])
            
            # Gán giá trị x cho nhóm feature
            num_features = len(selected_columns)
            if num_features > 0:
                # Điều chỉnh phạm vi x để rộng hơn (ví dụ: 0.05 đến 0.95)
                start_x = -0.01
                end_x = 1

                # Tính khoảng cách giữa các feature
                if num_features > 1:
                    spacing_first_three = (end_x - start_x) / (num_features * 0.9)  # Khoảng cách nhỏ hơn cho 3 feature đầu
                    spacing_others = (end_x - start_x) / (num_features * 0.6)  # Tăng khoảng cách cho các feature còn lại

                    # Tính x_position dựa trên index
                    index = selected_columns.index(feature)
                    if index == 0:
                        x_position = start_x
                    elif index == 1:
                        x_position = start_x + spacing_first_three
                    elif index == 2:
                        x_position = start_x + 2 * spacing_first_three
                    else:
                        x_position = (
                            start_x + 3 * spacing_first_three 
                            + (index - 3) * spacing_others
                        )
                else:
                    x_position = 0.5  # Giá trị mặc định nếu chỉ có 1 feature
            else:
                x_position = 0.5  # Giá trị mặc định nếu không có feature nào được chọn

            # Gán vị trí x cho tất cả các node trong nhóm
            x_positions.update({node: x_position for node in nodes})

            # Kiểm tra nếu có giá trị y cố định, nếu không có, chia đều vị trí y cho các node trong feature
            if feature in fixed_y_values:
                for i, node in enumerate(nodes):
                    y_positions[node] = fixed_y_values[feature][i]
            else:
                # Tính toán vị trí y mặc định (chia đều cho các node)
                num_nodes = len(nodes)
                y_step = 1 / (num_nodes + 1)  # chia đều khoảng cách giữa các node
                for i, node in enumerate(nodes):
                    y_positions[node] = y_step * (i + 1)

        return x_positions, y_positions

    @staticmethod
    def draw_sankey(df, df_dict, final_dict, unique_source_target, color_list, mapping_dict, selected_columns, height, width):
        
        # Ensure all selected_columns exist in df_dict
        missing_columns = [col for col in selected_columns if col not in df.columns]

        if missing_columns:
            raise ValueError(f"Missing columns in df_dict: {missing_columns}")
        
        total_values_by_source = SankeyDiagram.calculate_total_values_by_source(df_dict, mapping_dict)
        total_values_by_target = SankeyDiagram.calculate_total_values_by_target(final_dict)
        labeled_nodes = []
        x_positions, y_positions = SankeyDiagram.calculate_custom_node_positions(pd.DataFrame(df_dict), unique_source_target, selected_columns)
        for i, label in enumerate(unique_source_target):
            source_value = total_values_by_source.get(i)
            target_value = total_values_by_target.get(i)

            if source_value is not None:
                labeled_nodes.append(f"{label}: {source_value}")
            else:
                labeled_nodes.append(f"{label}: {target_value}")

        link_colors = [lighten_color(color_list[src % len(color_list)]) for src in df_dict['source']]
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                x=[x_positions[node] for node in unique_source_target],
                y=[y_positions[node] for node in unique_source_target],
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=labeled_nodes, 
                color=color_list[:len(unique_source_target)]  
            ),
            textfont=dict(
                color='black',
                size=10,
                family="Tahoma"
            ),
            link=dict(
                source=df_dict['source'],
                target=df_dict['target'],
                value=df_dict['value'],
                color=link_colors
            ))])

        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', 
            paper_bgcolor='rgba(0,0,0,0)',  
            margin=dict(
                l=50,  
                r=50,  
                t=20,  
                b=20   
            ),
            height=height,
            width=width
        )

        return fig