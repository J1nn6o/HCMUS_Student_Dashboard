from dash import html
from pages.home import get_sidebar

def get_about_page(active_item="about"):
    return html.Div(
        children=[
            get_sidebar(active_item=active_item),
            html.Div(
                children=[
                    html.H3("Our Team", className="text-center mt-5"),
                    html.Ul(
                        children=[
                            html.Li("Trịnh Minh Anh - 21280005"),
                            html.Li("Lê Hồ Hoàng Anh - 21280085"),
                        ],
                        className="list-unstyled text-center",
                    )
                ],
                className="about-content", 
            ),
        ],
    )
