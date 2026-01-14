import dash_bootstrap_components as dbc
import dash_molstar
from dash import dash_table
from dash import html, dcc
from pages.config_vie import *

def draw_sankey_plot(
    sankey_plot, 
    style={'marginLeft': '0', 'paddingTop': '0','paddingLeft': '0' }
):
    return dcc.Graph(
        figure=sankey_plot, 
        style=style
    )
    
    
def insert_image(src, alt='', width=50, height=40, className='mx-1'):
    return html.Img(
        src=src, 
        alt='', width=50, height=40, className='mx-1')
    

def get_sidebar(active_item="home"):
    nav = html.Nav(id="sidebar", children=[
        html.Div(className="custom-menu", children=[
            html.Button([
                html.I(className="fas fa-bars", style={'color': 'white'}) 
            ], type="button", id="sidebarCollapse", className="btn btn-primary")
        ]),
        html.Div(className="flex-column p-4 nav nav-pills", children=[
            html.A([
                html.Div([
                    insert_image('/assets/hcmus_khong_nen.png'),
                    insert_image('/assets/logo_khoa_toan_tin.ico'),
                ], className='d-flex align-items-left'),  
                html.Div([
                    html.H4("HCMUS", className='fs-4 mb-0'),
                    html.H4("Khoa Toán - Tin", className='fs-4'), 
                ], className='text-white text-left mt-2') 
            ], className='d-flex flex-column align-items-left mb-3 mb-md-0 me-md-auto text-decoration-none', href='/'),
            html.Hr(),
            dbc.NavItem(dbc.NavLink(dashboard, href="/", className='text-white', active=True if active_item=='home' else False)),
            dbc.NavItem(dbc.NavLink(about_us, href="/about", className='text-white', active=True if active_item=='about' else False))
        ])
    ])
    return nav


def create_banner():
   return dbc.Row([
        dbc.Col([
            html.Div(
                id="header-title",
                children=[
                    html.H2(
                        header_title, 
                        style={
                            'color': '#062C66',
                            'text-align': 'center',
                            'fontWeight': 'bold'
                        }
                    )            
                ]
            ),
        ]),
    ])
   

def create_dropdown_selection():
    return html.Div(
        [
            dbc.Label(training_course, html_for="year-dropdown", style={'fontWeight': 'bold', 'color':'#062C66'}),
            dcc.Dropdown(
                id="year-dropdown",
                options=[
                    {'label': 'Khóa 2021', 'value': 'K2021'},
                    {'label': 'Khóa 2022', 'value': 'K2022'},
                    {'label': 'Khóa 2023', 'value': 'K2023'}
                ],
                value='K21', 
                placeholder="Khóa 2021",
                clearable=False,
                style={'width': '150px', 'marginLeft': '10px'},
                maxHeight=600,
                optionHeight=40
            ),
        ],
        style={
            'display': 'flex',  
            'alignItems': 'center', 
            'justifyContent': 'center',  
            'marginBottom': '10px' 
        }
    )

def create_overview_section(donut_chart, bar_chart, gpa_columns_list):
    return html.Div(
        children=[
            # Container for both donut chart and bar chart
            html.Div(
                children=[
                    # Column 1: Donut Chart and Dropdowns with Submit Button
                    html.Div(
                        children=[
                            # Donut Chart
                            html.Div(
                                children=[
                                    html.P("Tổng số lượng SV đầu vào:", style={
                                        'textAlign': 'left',
                                        'fontWeight': 'bold',
                                        'color': 'black',
                                        'fontSize': '14px',
                                        'marginBottom': '0px'
                                    }),
                                    dcc.Graph(
                                        figure=donut_chart,
                                        config={"displayModeBar": False},
                                        style={'margin': '0 auto'}
                                    ),
                                ],
                                style={
                                    'backgroundColor': '#FFFFFF',
                                    'border': '1px solid rgba(0, 0, 0, 0.15)',
                                    'boxShadow': '9px 9px 9px rgba(0, 0, 0, 0.09)',
                                    'borderRadius': '5px',
                                    'width': '100%',
                                    'height': '200px',
                                    'marginBottom': '10px',
                                    'padding': '10px',
                                    'textAlign': 'center'
                                }
                            ),

                            # Dropdowns and Submit Button
                            html.Div(
                                children=[
                                    # Dropdown for selecting academic year
                                    html.Div(
                                        children=[
                                            html.Label("Chọn năm học:", style={'fontWeight': 'bold', 'fontSize': '14px'}),
                                            dcc.Dropdown(
                                                id='year-scale-dropdown',
                                                options=[{'label': year, 'value': year} for year in gpa_columns_list],
                                                placeholder="2021-2022",
                                                style={'width': '100%', 'marginBottom': '10px'}
                                            )
                                        ],
                                        style={'marginBottom': '10px'}
                                    ),

                                    # Dropdown for selecting GPA scale
                                    html.Div(
                                        children=[
                                            html.Label("Chọn thang điểm GPA:", style={'fontWeight': 'bold', 'fontSize': '14px'}),
                                            dcc.Dropdown(
                                                id='gpa-scale-dropdown',
                                                placeholder="gpa>=7_and_<8.5",
                                                style={'width': '100%'}
                                            )
                                        ],
                                        style={'marginBottom': '10px'}
                                    ),

                                    # Submit Button
                                    html.Button(
                                        submit,
                                        id='submit_button_overview',
                                        style={
                                            'padding': '5px 15px',
                                            'backgroundColor': '#062C66',
                                            'fontSize': '13px',
                                            'color': 'white',
                                            'border': 'none',
                                            'borderRadius': '5px',
                                            'width': '100px',
                                            'textAlign': 'center'
                                        }
                                    ),
                                ],
                                style={
                                    'backgroundColor': '#FFFFFF',
                                    'border': '1px solid rgba(0, 0, 0, 0.15)',
                                    'boxShadow': '9px 9px 9px rgba(0, 0, 0, 0.09)',
                                    'borderRadius': '5px',
                                    'width': '100%',
                                    'padding': '10px',
                                    'textAlign': 'center'
                                }
                            )
                        ],
                        style={
                            'width': '20%',
                            'display': 'inline-block',
                            'verticalAlign': 'top',
                            'margin': '10px',
                            'marginLeft': '30px'
                        }
                    ),

                    # Column 2: Bar Chart
                    html.Div(
                        children=[
                            dcc.Graph(
                                id='bar_chart',
                                figure=bar_chart,
                                style={'margin': '0 auto'}
                            ),
                        ],
                        style={
                            'backgroundColor': 'white',
                            'border': '1px solid rgba(0, 0, 0, 0.15)',
                            'boxShadow': '9px 9px 9px rgba(0, 0, 0, 0.07)',
                            'width': '75%',
                            'height': 'auto',
                            'borderRadius': '5px',
                            'margin': '10px',
                            'padding': '0px',
                            'display': 'inline-block',
                            'verticalAlign': 'top'
                        }
                    ),
                ],
                style={
                    'backgroundColor': 'rgba(0,0,0,0)',
                    'width': '100%',
                    'margin': '10px auto',
                    'padding': '0',
                    'display': 'flex',
                    'justifyContent': 'space-between',
                }
            ),
        ],
        style={
            'backgroundColor': 'rgba(0,0,0,0)',
            'width': '100%',
            'margin': '10px auto',
            'padding': '0',
        }
    )


def generate_table(foa_dict, sankey_plot):
    table_rows = []

    table_rows.append(
        html.Tr([
            html.Th("Chú thích", style={
                'textAlign': 'center',
                'padding': '0px',
                'fontSize': '13px',
                'borderBottom': '1px solid #ddd',
                'position': 'sticky',
                'top': '0',
                'zIndex': '1',
                'backgroundColor': '#FFFFFF',
                'width': '20%'
            }),
            html.Th("Tên PTXT", style={
                'textAlign': 'center',
                'padding': '0px',
                'fontSize': '13px',
                'borderBottom': '1px solid #ddd',
                'position': 'sticky',
                'top': '0',
                'zIndex': '1',
                'backgroundColor': '#FFFFFF',
                'width': '80%'
            })
        ], style={
            'borderBottom': '2px solid #ddd'}
        )
    )

    for key, value in foa_dict.items():
        table_rows.append(
            html.Tr([
                html.Td(key, style={
                    'textAlign': 'center',
                    'padding': '5px',
                    'fontSize': '13px',
                    'borderBottom': '1px solid #ddd'
                }),
                html.Td(value, style={
                    'textAlign': 'left',
                    'padding': '5px',
                    'fontSize': '13px',
                    'borderBottom': '1px solid #ddd'
                })
            ])
        )

    table = html.Table(
        children=table_rows,
        style={
            'width': '100%',
            'borderCollapse': 'collapse',
            'marginTop': '0px'
        }
    )

    return html.Div(
        children=[
            html.Div(
                children=table,
                style={
                    'backgroundColor': '#FFFFFF',
                    'borderTop': '1px solid rgba(0, 0, 0, 0.15)',
                    'borderLeft': '1px solid rgba(0, 0, 0, 0.15)',
                    'borderRight': '1px solid rgba(0, 0, 0, 0.15)',
                    'borderBottom': '1px solid rgba(0, 0, 0, 0.15)',
                    'boxShadow': '9px 9px 9px rgba(0, 0, 0, 0.07)',
                    'borderRadius': '5px',
                    'overflowY': 'scroll',
                    'height': '350px',
                    'width': '20%',
                    'margin': '10px',
                    'marginLeft': '30px',
                    'marginRight': '10px',
                    'padding': '0px',
                    'display': 'inline-block',
                    'verticalAlign': 'top'
                }
            ),
            html.Div(
                children=[
                    html.Label(
                        "Sự chuyển đổi về số lượng sinh viên qua từng giai đoạn: ",
                        style={
                            'fontWeight': 'bold',
                            'fontSize': '14px',
                            'textAlign': 'center',
                            'marginTop': '10px',
                            'display': 'flex',
                            'justifyContent': 'center',
                            'alignItems': 'center',
                        }
                    ),
                    html.Label(
                        "xét tuyển đầu vào, chọn ngành, cơ sở ngành (CSN), chuyên ngành (CN) và tốt nghiệp ",
                        style={
                            'fontWeight': 'bold',
                            'fontSize': '14px',
                            'textAlign': 'center',
                            'display': 'flex',
                            'justifyContent': 'center',
                            'alignItems': 'center',
                        }
                    ),
                    # Biểu đồ Sankey
                    draw_sankey_plot(
                        sankey_plot, 
                        style={'marginLeft': '0', 'marginTop': '0px','paddingTop': '0px', 'paddingLeft': '0', 'width': '100%'}
                    ),
                ],
                style={
                    'backgroundColor': 'white',
                    'border': '1px solid rgba(0, 0, 0, 0.15)',
                    'boxShadow': '9px 9px 9px rgba(0, 0, 0, 0.07)',
                    'width': '75%',
                    'height': '350px',  
                    'borderRadius': '5px',
                    'margin': '10px',
                    'marginRight': '10px',
                    'display': 'inline-block',
                    'verticalAlign': 'top'
                }
            ),
        ]
    )

def create_data_section(major, major_name, sankey_plot, radar_chart, radar_df, bar_chart, student_dict):
    # Lấy số lượng cột và header từ student_dict
    student_keys = list(student_dict.keys())
    columns = [
        {'name': student_dict[student_keys[0]][i][0], 'id': f'col_{i}'}
        for i in range(len(student_dict[student_keys[0]]))
    ]

    # Tạo dữ liệu bảng
    data = [
        {
            f'col_{i}': student_dict[student][i][1]
            for i in range(len(student_dict[student]))
        }
        for student in student_dict
    ]

    return html.Div(
        children=[
            # Tiêu đề
            html.P(major, style={
                'textAlign': 'center', 
                'fontWeight': 'bold',
                'backgroundColor': 'rgba(0,0,0,0)',
                'color': '#062C66', 
                'fontSize': '20px',
                'marginBottom': '0'
            }),
            html.Div(
                children=[
                    html.Label(
                        f"Dòng chảy về số lượng sinh viên {major} theo từng nhóm điểm GPA qua các năm học",
                        style={
                            'fontWeight': 'bold',
                            'fontSize': '14px',
                            'textAlign': 'center',
                            'marginTop': '10px',
                            'display': 'flex',
                            'justifyContent': 'center',
                            'alignItems': 'center',
                        }
                    ),
                    # Biểu đồ Sankey
                    draw_sankey_plot(
                        sankey_plot, 
                        style={'marginLeft': '0', 'paddingTop': '0', 'paddingLeft': '0', 'width': '100%'}
                    ),
                ],
                style={
                    'backgroundColor': 'white',
                    'border': '1px solid rgba(0, 0, 0, 0.15)',
                    'boxShadow': '9px 9px 9px rgba(0, 0, 0, 0.07)',
                    'width': '97.5%',
                    'marginLeft': '25px',
                    'marginRight': '15px',
                    'padding': '0',
                    'height': '180px',  
                    'borderRadius': '5px',
                    'marginBottom': '25px'
                }
            ),

            html.Div(
                children=[
                    dbc.Label(
                        input_2_student_ids,
                        html_for=f'student_id_1_{major_name}', 
                        style={
                            'fontWeight': 'bold', 
                            'color': '#062C66', 
                            'textAlign': 'right',
                            'gridColumn': '2 / 3', 
                            'alignSelf': 'center' 
                        }
                    ),
                    dcc.Dropdown(
                        id=f'student_id_1_{major_name}',
                        options=[{'label': student, 'value': student} for student in radar_df['student_id'].unique()],
                        placeholder="MSSV 1",
                        style={
                            'gridColumn': '3 / 4', 
                            'alignSelf': 'center'  
                        }
                    ),
                    dcc.Dropdown(
                        id=f'student_id_2_{major_name}',
                        options=[{'label': student, 'value': student} for student in radar_df['student_id'].unique()],
                        placeholder="MSSV 2",
                        style={
                            'gridColumn': '4 / 5',  
                            'alignSelf': 'center'  
                        }
                    ),
                    html.Button(
                        submit,
                        id=f'submit_button_{major_name}',
                        n_clicks=0,
                        style={
                            'padding': '5px 15px',
                            'backgroundColor': '#062C66',
                            'color': '#fff',
                            'border': 'none',
                            'borderRadius': '5px',
                            'gridColumn': '5 / 6', 
                            'alignSelf': 'center', 
                            'width': '100px', 
                            'textAlign': 'center' 
                        }
                    )
                ],
                style={
                    'display': 'grid',  
                    'gridTemplateColumns': 'repeat(6, 1fr)',  
                    'alignItems': 'center',  
                    'gap': '5px',  
                    'width': '99%'  
                }
            ),

            html.Div(
                children=[
                    dcc.Graph(
                        id=f'radar_chart_{major_name}',
                        figure=radar_chart,
                        style={'flex': 1, 'verticalAlign': 'top', 'marginRight': '-10px'}  
                    ),
                    dcc.Graph(
                        id=f'student_bar_chart_{major_name}',
                        figure=bar_chart,
                        style={'flex': 1, 'marginLeft': '0',  'marginTop': '0px'}  
                    ),
                ],
                style={'display': 'flex', 'justifyContent': 'space-between', 'marginLeft': '0'}
            ),

            # html.Div(
            #     children=[
            #         dash_table.DataTable(
            #             id=f'student_table_{major_name}',
            #             columns=columns,
            #             data=data,
            #             style_table={'overflowX': 'auto'},
            #             style_header={
            #                 'fontWeight': 'normal',
            #                 'backgroundColor': '#062C66',
            #                 'color': 'white',
            #                 'textAlign': 'center',
            #                 'fontFamily': 'Tahoma',
            #                 'fontSize': '13px',
            #             },
            #             style_cell={
            #                 'textAlign': 'center',
            #                 'padding': '10px',
            #                 'border': '1px solid #ddd',
            #                 'fontFamily': 'Tahoma',
            #                 'fontSize': '12px',
            #             }
            #         )
            #     ],
            # )
            html.Div(
                children=[
                    html.Div(
                        
                        children=[
                            dash_table.DataTable(
                                id=f'student_table_{major_name}',
                                columns=columns,
                                data=data,
                                style_table={
                                    'overflowX': 'auto'
                                    # 'width': '80%'
                                    
                                },
                                style_header={
                                    'fontWeight': 'normal',
                                    'backgroundColor': '#062C66',
                                    'color': 'white',
                                    'textAlign': 'center',
                                    'fontFamily': 'Tahoma',
                                    'fontSize': '13px',
                                },
                                style_cell={
                                    'textAlign': 'center',
                                    'padding': '5px',
                                    'border': '1px solid #ddd',
                                    'fontFamily': 'Tahoma',
                                    'whiteSpace': 'normal',  # Cho phép xuống dòng
                                    'overflow': 'hidden',
                                    'fontSize': '12px',
                                }
                            )
                        ],
                        style={
                            'width': '100%',
                            # 'height': '350px',  
                            'margin': '10px',
                            'marginRight': '10px',
                            'display': 'inline-block',
                            'verticalAlign': 'top'
                        },
                    )
                ]
            )

        ],
        style={
            'backgroundColor': 'rgba(0,0,0,0)',
            'width': '97%',
            'margin': '10px auto',
            'padding': '0',
            'height': '760px',  
            'marginBottom': '50px',
            'borderRadius': '0',
        }
    )

 

# def layout(donut_chart, overview_bar_chart, gpa_column_list,  foa_dict, sankey_fig_overview, sankey_fig_math, sankey_fig_kdl, radar_math_chart, radar_math_df, math_student_table, radar_kdl_chart, radar_kdl_df, kdl_student_table ):
def layout(donut_chart, overview_bar_chart, gpa_column_list,  foa_dict, sankey_fig_overview, sankey_fig_math, sankey_fig_kdl, radar_math_chart, radar_math_df, math_bar_chart, radar_kdl_chart, radar_kdl_df, kdl_bar_chart, math_student_dict, kdl_student_dict):
    banner = create_banner()
    dropdown_section = create_dropdown_selection()

    # Box chứa Sankey Overview
    foa_table_overview = generate_table(foa_dict, sankey_fig_overview)
    box_section_overview = create_overview_section(donut_chart, overview_bar_chart, gpa_column_list)

    # Box của TTH
    box_section_math = create_data_section("Nhóm Ngành Toán học", 'math', sankey_fig_math, radar_math_chart, radar_math_df, math_bar_chart, math_student_dict)
    
    # Box của KDL
    box_section_kdl = create_data_section("Ngành Khoa học Dữ liệu", 'kdl', sankey_fig_kdl, radar_kdl_chart, radar_kdl_df, kdl_bar_chart, kdl_student_dict)

    layout = [
        get_sidebar("home"),  # Đặt "Dashboard" ở trạng thái 'active' mặc định
        html.Div([ 
            dbc.Container(banner, fluid=True),
            dbc.Container(dropdown_section, fluid=True),  
            dbc.Container(foa_table_overview, fluid=True),
            dbc.Container(box_section_overview, fluid=True),
            dbc.Container(box_section_math, fluid=True),
            dbc.Container(box_section_kdl, fluid=True)
        ], className='content')
    ]

    return layout

