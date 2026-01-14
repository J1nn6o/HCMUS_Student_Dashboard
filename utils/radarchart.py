from typing import List
import plotly.graph_objects as go
import pandas as pd

class RadarChart:
    @staticmethod
    def merge_course_num_and_create_new_column(df1, df2):
        merged_df = pd.merge(df1, df2[['course_group', 'course_num']], on='course_group', how='left')
        return merged_df

    @staticmethod
    def filter_student_data(df, student_id: int):
        """Lọc dữ liệu của một sinh viên dựa trên student_id."""
        student_data = df[df['student_id'] == student_id]
        if student_data.empty:
            print(f"Student ID {student_id} không tồn tại trong dữ liệu.")
        return student_data

    @staticmethod
    def prepare_radar_data(student_data):
        """Chuẩn bị dữ liệu cho biểu đồ radar, đảm bảo đóng vòng tròn."""
        # categories = student_data['course_group_num'].tolist()
        categories = student_data['course_group'].to_list()
        values = student_data['weighted_score'].tolist()
        categories += [categories[0]]
        values += [values[0]]
        return categories, values

    @staticmethod
    def add_trace(fig, categories, values, student_id, fillcolor, linecolor):
        """Thêm một trace vào biểu đồ radar."""
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=f'Sinh viên {student_id}',
            fillcolor=fillcolor,
            line=dict(color=linecolor, width=1.5)
        ))

    @staticmethod
    def configure_radar_chart():
        """Cấu hình chung cho biểu đồ radar."""
        return dict(
            polar=dict(
                bgcolor='white',
                gridshape='linear',
                radialaxis=dict(
                    visible=True,
                    range=[0, 10],
                    showline=True,
                    linewidth=1,
                    gridcolor='black',
                    linecolor='black',
                    tickfont=dict(color='black', size=10, family='Tahoma')
                ),
                angularaxis=dict(
                    gridcolor='black',
                    tickfont=dict(color='black', size=12, family='Tahoma'),
                    
                )
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=True,
            legend=dict(
                font=dict(color='black', size=10, family='Tahoma'),
                y=1
            ),
            margin=dict(
                l=10,  
                r=10,
                b=10 
            ),
            title=dict(
                text=f"<b>Biểu đồ radar</b>",
                font=dict(
                    family="Tahoma",
                    size=15,
                    color="black"
                )
            ),
            height=340,
            width=570
        )

    @staticmethod
    def plot_students_radar_chart(df, student_ids: List[int]):
        """Vẽ biểu đồ radar cho tối đa hai sinh viên."""
        if len(student_ids) == 0:
            raise ValueError("Danh sách student_ids không được để trống.")

        student_data_1 = RadarChart.filter_student_data(df, student_ids[0])

        if student_data_1.empty:
            raise ValueError(f"Dữ liệu của sinh viên {student_ids[0]} không tồn tại.")

        categories_1, values_1 = RadarChart.prepare_radar_data(student_data_1)

        fig = go.Figure()

        RadarChart.add_trace(fig, categories_1, values_1, student_ids[0], 'rgba(52, 102, 165, 0.4)', '#3466A5')

        if len(student_ids) > 1:
            student_data_2 = RadarChart.filter_student_data(df, student_ids[1])
            if student_data_2.empty:
                raise ValueError(f"Dữ liệu của sinh viên {student_ids[1]} không tồn tại.")
            categories_2, values_2 = RadarChart.prepare_radar_data(student_data_2)
            RadarChart.add_trace(fig, categories_2, values_2, student_ids[1], 'rgba(200, 54, 30, 0.4)', '#c41e32')

        fig.update_layout(**RadarChart.configure_radar_chart())

        return fig


