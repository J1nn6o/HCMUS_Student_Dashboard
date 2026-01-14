import plotly.graph_objects as go
import pandas as pd

class Donut:
    @staticmethod
    def create_donut_chart(total_student, total_math_student, total_kdl_student):
        labels = ["TTH", "KDL"]
        values = [total_math_student, total_kdl_student]

        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.7,
            marker=dict(colors=["#015C92", "#88CDF6"]),
            textinfo="label+value",
            insidetextorientation="radial"
        )])

        fig.update_layout(
            annotations=[dict(
                text=f"<b>{total_student}</b>",
                font=dict(size=20, color="black", family="Tahoma"),
                showarrow=False
            )],
            
            margin=dict(t=0, b=0, l=0, r=0),
            height=150,
            width=230,
            showlegend=True,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
            # title = 'Tổng số lượng SV đầu vào'
        )
        return fig