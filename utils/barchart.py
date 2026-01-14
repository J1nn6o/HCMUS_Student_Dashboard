import plotly.graph_objects as go
import plotly.express as px
# import pandas as pd

class BarChart:
    @staticmethod
    def get_gpa_columns(df):
        """
        Returns:
            list: Danh sách tên các cột chứa ký tự 'gpa_status' với tên cột đã được cập nhật.
        """
        gpa_mapping = {
            'first_gpa_status': '2021-2022',
            'second_gpa_status': '2021-2023',
            'third_gpa_status': '2021-2024',
            'fourth_gpa_status': '2021-2025'
        }
        
        df.columns = [gpa_mapping.get(col, col) if 'gpa_status' in col else col for col in df.columns]
        updated_columns = [col for col in df.columns if col not in ['student_id', 'application_id']]

        return df, updated_columns

    
    @staticmethod
    def process_gpa_columns(df, gpa_columns):
        result = {}
        for col in gpa_columns:
            df[col] = df[col].str.extract(r'(gpa.*)')[0]
            result[col] = df[col].dropna().unique().tolist()
        return result
    
    
    @staticmethod
    def draw_horizontal_bar_chart(df, x_column, groupby_column, filtered_value, color_scale_bar_chart, height, width):
        filtered_df = df[df[groupby_column] == filtered_value]

        grouped_df = (
            filtered_df.groupby([x_column, groupby_column])
            .size()
            .reset_index(name='count')
        )

        grouped_df = grouped_df.sort_values(by='count', ascending=True).reset_index(drop=True)

        num_colors = len(color_scale_bar_chart)
        grouped_df['color'] = [color_scale_bar_chart[i % num_colors] for i in range(len(grouped_df))]

        grouped_df = grouped_df.sort_values(by='count', ascending=True)

        fig = px.bar(
            grouped_df,
            x='count',
            y=x_column,
            orientation='h',
            labels={
                'count': 'Số lượng sinh viên',
                x_column: x_column.capitalize()
            },
        )

        fig.update_traces(marker=dict(color=grouped_df['color'].tolist()))

        fig.update_layout(
            xaxis_title="Số lượng sinh viên",
            yaxis_title="Phương thức xét tuyển (PTXT)",
            xaxis=dict(
                title=dict(
                    text="Số lượng sinh viên",
                    font=dict(
                        size=13, 
                        color="black"
                    )
                )
            ),
            yaxis=dict(
                title=dict(
                    text=x_column.capitalize(),
                    font=dict(
                        size=13,  
                        color="black"
                    )
                )
            ),
            legend_title=groupby_column.capitalize(),
            title=dict(
                text=f"<b>Tổng số lượng SV có ĐTB tích lũy: {filtered_value} trong năm học {groupby_column}</b>",
                font=dict(
                    family="Tahoma",
                    size=15,
                    color="black"
                )
            ),
            template="plotly_white",
            showlegend=True,
            font=dict(
                family="Tahoma",
                color='black',
                size=13
            ),
            height=height,
            width=width
        )

        return fig

    
    @staticmethod
    def df_to_dict(df, student_ids: list, course_group=None, total_count_course=None):
        filtered_df = df[df[df.columns[0]].isin(student_ids)]
        result = {}
        for _, row in filtered_df.iterrows():
            student_id = row['student_id']
            if student_id not in result:
                result[student_id] = []
            if course_group is not None and total_count_course is not None:
                result[student_id].append([row[course_group], row[total_count_course]])

        return result
    
    @staticmethod
    def plot_course_bar_chart(total_course_num_df, total_course_num_per_student_dict, student_ids:list, height, width):
        if len(student_ids) > 2:
            raise ValueError("Số lượng student_ids không được vượt quá 2 phần tử.")
        
        total_course_num_df = total_course_num_df.sort_values(by='course_num', ascending=False)

        course_groups = total_course_num_df['course_group']
        total_course_num = total_course_num_df['course_num']

        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=course_groups,
            y=total_course_num,
            name="Tổng số môn trong 1 nhóm",
            marker_color='rgba(211, 169, 211, 0.9)' 
        ))

        for idx, student_id in enumerate(student_ids):
            student_data = total_course_num_per_student_dict.get(student_id, [])
            
            student_values = []
            for group in course_groups:
                matching_values = [value for course, value in student_data if course == group]
                student_values.append(matching_values[-1] if matching_values else 0)
            
            student_color = 'rgba(52, 102, 165, 0.89)' if idx == 0 else 'rgba(200, 54, 30, 0.89)'

            fig.add_trace(go.Bar(
                x=course_groups,
                y=student_values,
                name=f"Sinh viên {student_id}",
                marker_color=student_color 
            ))

        fig.update_layout(
            xaxis_title="Các nhóm môn học",
            yaxis_title="Tổng số lượng môn",
            template="plotly_white",
            title=dict(
                text=f"<b>Số lượng môn học của sinh viên theo các nhóm</b>",
                font=dict(
                    family="Tahoma",
                    size=15,
                    color="black"
                )
            ),
            showlegend=True,
            font=dict(
                family="Tahoma",
                color='black',
                size=10
            ),
            legend=dict(
                orientation="h",  # Đặt legend theo chiều ngang
                yanchor="bottom",  # Căn legend phía trên của chart
                y=1.05,  # Đặt vị trí của legend ở trên trục x
                xanchor="center",  # Căn giữa legend
                x=0.5  # Đặt legend ở giữa
            ),
            margin=dict(
                l=30,  
                r=30,
                b=10 
            ),
            height=height,
            width=width,
            barmode='group'
        )

        return fig

    

