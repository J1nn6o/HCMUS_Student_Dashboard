TOTAL_STUDENTS = """
    select count(distinct(student_id)) from student; 
"""

TOTAL_MATH_STUDENT = """
    select count(distinct(student_id))
    from student
    where student_id LIKE '2111%%';
"""

TOTAL_KDL_STUDENT = """
    select count(distinct(student_id))
    from student
    where student_id LIKE '2128%%';
"""

FOA_TABLE = """
    select * from form_of_application;
"""

OVERVIEW_QUERY = """
    SELECT 
        foa.application_id,
        s.student_id, 
        f.field_name,
        COALESCE(sf.subfield_name, 'NGHỈ HỌC (CSN)') AS subfield_name,
        COALESCE(m.major_name, 'NGHỈ HỌC (CN)') AS major_name,
        CASE
            WHEN sp.school_year = '2025-2026' AND sp.status = 'TOTNGHIEP' THEN 'TỐT NGHIỆP'
            /*WHEN sf.subfield_name IS NULL OR m.major_name IS NULL THEN 'NGHỈ HỌC' */
            ELSE 'CÒN HỌC TIẾP'
        END AS graduated_status
    FROM student s
    JOIN form_of_application foa ON foa.application_id = s.application_id
    LEFT JOIN field f ON f.field_id = s.field_id
    LEFT JOIN subfield sf ON sf.subfield_id = s.subfield_id
    LEFT JOIN major m ON m.major_id = s.major_id
    LEFT JOIN (
        SELECT * FROM student_performance
        WHERE school_year = '2025-2026'
    ) sp ON sp.student_id = s.student_id;
    """


TTH_SQL_QUERY = """
    DROP FUNCTION IF EXISTS calculate_gpa(VARCHAR, VARCHAR);

    CREATE OR REPLACE FUNCTION calculate_gpa(
        school_year_param VARCHAR[],
        student_pattern VARCHAR
    )
    RETURNS TABLE(
        student_id CHAR(8), 
        gpa FLOAT, 
        gpa_status VARCHAR
    ) 
    LANGUAGE plpgsql
    AS $$
    BEGIN
        RETURN QUERY 
        SELECT 
            g.student_id,
            ROUND(SUM(g.final_score * c.credits) / SUM(c.credits), 2)::FLOAT AS gpa,
            (CASE 
                WHEN ROUND(SUM(g.final_score * c.credits) / SUM(c.credits), 2)::FLOAT < 5.0 
                    THEN ARRAY_TO_STRING(school_year_param, ', ') || '_gpa<5'
                WHEN ROUND(SUM(g.final_score * c.credits) / SUM(c.credits), 2)::FLOAT >= 5.0 
                    AND ROUND(SUM(g.final_score * c.credits) / SUM(c.credits), 2)::FLOAT < 7.0
                    THEN ARRAY_TO_STRING(school_year_param, ', ') || '_gpa>=5_and_<7'
                WHEN ROUND(SUM(g.final_score * c.credits) / SUM(c.credits), 2)::FLOAT >= 7.0 
                    AND ROUND(SUM(g.final_score * c.credits) / SUM(c.credits), 2)::FLOAT < 8.5
                    THEN ARRAY_TO_STRING(school_year_param, ', ') || '_gpa>=7_and_<8.5'
                ELSE ARRAY_TO_STRING(school_year_param, ', ') || '_gpa>=8.5'
            END)::VARCHAR AS gpa_status
        FROM grade g
        LEFT JOIN course c 
            ON c.course_id = g.course_id AND c.optional_11 != 'NO'
        WHERE g.student_id LIKE student_pattern 
        AND g.school_year = ANY(school_year_param) -- Kiểm tra nhiều năm học
        GROUP BY g.student_id;
    END;
    $$; 

    /*DROP VIEW IF EXISTS gpa_tth;

    CREATE VIEW gpa_tth AS*/
    SELECT 
        first.student_id AS student_id,
        first.gpa AS first_gpa,
        first.gpa_status as first_gpa_status,
        second.gpa AS second_gpa,
        second.gpa_status AS second_gpa_status,
        third.gpa AS third_gpa,
        third.gpa_status AS third_gpa_status,
        fourth.gpa AS fourth_gpa,
        fourth.gpa_status AS fourth_gpa_status
    FROM 
        calculate_gpa(ARRAY['2021-2022'] ,'2111%%') AS first
    LEFT JOIN 
        calculate_gpa(ARRAY['2021-2022', '2022-2023'], '2111%%') AS second
        ON first.student_id = second.student_id
    LEFT JOIN
        calculate_gpa(ARRAY['2021-2022', '2022-2023', '2023-2024'],'2111%%') AS third
        ON first.student_id= third.student_id
    LEFT JOIN
        calculate_gpa(ARRAY['2021-2022', '2022-2023', '2023-2024', '2024-2025'], '2111%%') AS fourth
        ON first.student_id = fourth.student_id;
    """

QUERY_DROP = """
    select s.student_id, sp.school_year
    from student s
    left join student_performance sp on s.student_id = sp.student_id
    where sp.status != 'DANGHOC' AND sp.school_year != '2025-2026';
    """

KDL_SQL_QUERY = """
    DROP FUNCTION IF EXISTS calculate_gpa(VARCHAR, VARCHAR);

    CREATE OR REPLACE FUNCTION calculate_gpa(
        school_year_param VARCHAR[],
        student_pattern VARCHAR
    )
    RETURNS TABLE(
        student_id CHAR(8), 
        gpa FLOAT, 
        gpa_status VARCHAR
    ) 
    LANGUAGE plpgsql
    AS $$
    BEGIN
        RETURN QUERY 
        SELECT 
            g.student_id,
            ROUND(SUM(g.final_score * c.credits) / SUM(c.credits), 2)::FLOAT AS gpa,
            (CASE 
                WHEN ROUND(SUM(g.final_score * c.credits) / SUM(c.credits), 2)::FLOAT < 5.0 
                    THEN ARRAY_TO_STRING(school_year_param, ', ') || '_gpa<5'
                WHEN ROUND(SUM(g.final_score * c.credits) / SUM(c.credits), 2)::FLOAT >= 5.0 
                    AND ROUND(SUM(g.final_score * c.credits) / SUM(c.credits), 2)::FLOAT < 7.0
                    THEN ARRAY_TO_STRING(school_year_param, ', ') || '_gpa>=5_and_<7'
                WHEN ROUND(SUM(g.final_score * c.credits) / SUM(c.credits), 2)::FLOAT >= 7.0 
                    AND ROUND(SUM(g.final_score * c.credits) / SUM(c.credits), 2)::FLOAT < 8.5
                    THEN ARRAY_TO_STRING(school_year_param, ', ') || '_gpa>=7_and_<8.5'
                ELSE ARRAY_TO_STRING(school_year_param, ', ') || '_gpa>=8.5'
            END)::VARCHAR AS gpa_status
        FROM grade g
        LEFT JOIN course c 
            ON c.course_id = g.course_id AND c.optional_28 != 'NO'
        WHERE g.student_id LIKE student_pattern 
        AND g.school_year = ANY(school_year_param) -- Kiểm tra nhiều năm học
        GROUP BY  g.student_id;
    END;
    $$; 

    /* As we have already create view table so we don't really need to inject these code*/
    /*DROP VIEW IF EXISTS gpa_kdl;*/

    /*CREATE VIEW gpa_kdl AS*/
    SELECT 
        first.student_id AS student_id,
        first.gpa AS first_gpa,
        first.gpa_status as first_gpa_status,
        second.gpa AS second_gpa,
        second.gpa_status AS second_gpa_status,
        third.gpa AS third_gpa,
        third.gpa_status AS third_gpa_status,
        fourth.gpa AS fourth_gpa,
        fourth.gpa_status AS fourth_gpa_status
    FROM 
        calculate_gpa(ARRAY['2021-2022'] ,'2128%%') AS first
    LEFT JOIN 
        calculate_gpa(ARRAY['2021-2022', '2022-2023'], '2128%%') AS second
        ON first.student_id = second.student_id
    LEFT JOIN
        calculate_gpa(ARRAY['2021-2022', '2022-2023', '2023-2024'],'2128%%') AS third
        ON first.student_id = third.student_id
    LEFT JOIN
        calculate_gpa(ARRAY['2021-2022', '2022-2023', '2023-2024', '2024-2025'], '2128%%') AS fourth
        ON first.student_id = fourth.student_id;
    """

VIEW_TABLE_GPA_BAR_CHART = """
    /*DROP VIEW IF EXISTS bar_chart;

    CREATE VIEW bar_chart AS*/
    select tth.student_id,
        tth.first_gpa_status,
        tth.second_gpa_status,
        tth.third_gpa_status,
        tth.fourth_gpa_status,
        foa.application_id
    from gpa_tth tth
    left join student s on tth.student_id = s.student_id
    left join form_of_application foa on s.application_id = foa.application_id
    UNION
    select kdl.student_id,
        kdl.first_gpa_status,
        kdl.second_gpa_status,
        kdl.third_gpa_status,
        kdl.fourth_gpa_status,
        foa.application_id
    from gpa_kdl kdl
    left join student s on kdl.student_id = s.student_id
    left join form_of_application foa on s.application_id = foa.application_id;

    SELECT application_id, 
        first_gpa_status, count(first_gpa_status) as total_first_status,
        second_gpa_status, count(second_gpa_status) as total_second_status,
        third_gpa_status, count(third_gpa_status) as total_third_status,
        fourth_gpa_status, count(fourth_gpa_status) as total_fourth_status 
    FROM bar_chart
    group by application_id, first_gpa_status, second_gpa_status, third_gpa_status, fourth_gpa_status;
"""

GPA_BAR_CHART = """
    SELECT * FROM bar_chart;
"""

COLOR_SCALE_BAR_CHART = [     
    'rgba(230, 235, 240, 1)',  # Nhạt nhất
    'rgba(205, 217, 225, 1)',
    'rgba(180, 198, 210, 1)',
    'rgba(155, 179, 196, 1)',
    'rgba(130, 159, 181, 1)',
    'rgba(105, 140, 166, 1)',
    'rgba(56, 84, 109, 1)'     # Đậm nhất
    ]

COLOR_LIST = [
      "rgba(31, 119, 180, 0.8)",
      "rgba(255, 127, 14, 0.8)",
      "rgba(44, 160, 44, 0.8)",
      "rgba(214, 39, 40, 0.8)",
      "rgba(148, 103, 189, 0.8)",
      "rgba(140, 86, 75, 0.8)",
      "rgba(227, 119, 194, 0.8)",
      "rgba(127, 127, 127, 0.8)",
      "rgba(188, 189, 34, 0.8)",
      "rgba(23, 190, 207, 0.8)",
      "rgba(255, 99, 71, 0.8)",    
      "rgba(255, 69, 0, 0.8)",     # OrangeRed
      "rgba(34, 139, 34, 0.8)",    # ForestGreen
      "rgba(30, 144, 255, 0.8)",   # DodgerBlue
      "rgba(147, 112, 219, 0.8)",  # MediumPurple
      "rgba(255, 215, 0, 0.8)",    # Gold
      "rgba(0, 255, 255, 0.8)",    # Cyan
      "rgba(0, 128, 128, 0.8)",    # Teal
      "rgba(199, 21, 133, 0.8)",   # MediumVioletRed
      "rgba(218, 165, 32, 0.8)",   # GoldenRod
      "rgba(240, 128, 128, 0.8)",  # LightCoral
      "rgba(255, 160, 122, 0.8)",  # LightSalmon
      "rgba(60, 179, 113, 0.8)",   # MediumSeaGreen
      "rgba(106, 90, 205, 0.8)",   # SlateBlue
      "rgba(123, 104, 238, 0.8)",  # MediumSlateBlue
      "rgba(244, 164, 96, 0.8)",   # SandyBrown
      "rgba(25, 25, 112, 0.8)",    # MidnightBlue
      "rgba(255, 99, 132, 0.8)",   # Light Red
      "rgba(255, 206, 86, 0.8)",   # Yellow-Orange
      "rgba(75, 192, 192, 0.8)",   # Light Aqua
      "rgba(153, 102, 255, 0.8)",  # Light Purple
      "rgba(233, 30, 99, 0.8)",    # Deep Pink
      "rgba(76, 175, 80, 0.8)",    # Green
      "rgba(255, 235, 59, 0.8)",   # Yellow
      "rgba(0, 150, 136, 0.8)",    # Teal Green
      "rgba(3, 169, 244, 0.8)",    # Light Blue
      "rgba(63, 81, 181, 0.8)",    # Blue Gray
      "rgba(156, 39, 176, 0.8)",   # Violet
      "rgba(255, 87, 34, 0.8)",    # Dark Orange
      "rgba(205, 92, 92, 0.8)"]    # IndianRed

RADAR_TTH_QUERY = """
    WITH course_totals AS (
        SELECT 
            course_group,
            SUM(credits) AS total_credits
        FROM 
            course
        WHERE 
            course_group IS NOT NULL 
            AND optional_11 != 'NO'
        GROUP BY 
            course_group
    )
    SELECT 
        g.student_id, 
        c.course_group,
        ROUND(SUM(g.final_score * c.credits) / ct.total_credits, 2) AS weighted_score
    FROM grade g 
    LEFT JOIN course c ON c.course_id = g.course_id AND c.optional_11 != 'NO' 
    LEFT JOIN course_totals ct ON c.course_group = ct.course_group
    WHERE g.student_id LIKE '2111%' and c.course_group IS NOT NULL
    GROUP BY g.student_id, c.course_group, ct.total_credits
    ORDER BY g.student_id;
"""

TOTAL_MATH_COURSE_NUM = """
    select course_group, count(course_id) as course_num
    from course
    where course_group is not null and optional_11 != 'NO'
    group by course_group;
"""

STUDENT_TOTAL_COURSE_NUM = """
    select s.student_id, c.course_group, count(c.course_group) as total_count_course
    from student s
    left join grade g on g.student_id = s.student_id
    left join course c on g.course_id = c.course_id
    where c.course_group is not null
    group by s.student_id, c.course_group
    order by s.student_id;
"""

STUDENT_DF = """
    select s.student_id, 
		s.gender,
		s.academic_degree,
		f.field_name,
        case 
            when sb.subfield_name is null then ' '
            else sb.subfield_name
        end,
        case 
            when m.major_name is null then ' '
            else m.major_name
        end,
		foa.application_name,
		s.honor_program,
		s.school_year
    from student s
    left join field f on s.field_id = f.field_id
    left join subfield sb on sb.subfield_id = s.subfield_id
    left join major m on m.major_id = s.major_id
    left join form_of_application foa on foa.application_id = s.application_id;
    """

RADAR_KDL_QUERY = """
    WITH course_totals AS (
        SELECT 
            course_group,
            SUM(credits) AS total_credits
        FROM 
            course
        WHERE 
            course_group IS NOT NULL 
            AND optional_28 != 'NO'
        GROUP BY 
            course_group
    )
    SELECT 
        g.student_id, 
        c.course_group,
        ROUND(SUM(g.final_score * c.credits) / ct.total_credits, 2) AS weighted_score
    FROM grade g 
    LEFT JOIN course c ON c.course_id = g.course_id AND c.optional_28 != 'NO' 
    LEFT JOIN course_totals ct ON c.course_group = ct.course_group
    WHERE g.student_id LIKE '2128%' and c.course_group IS NOT NULL
    GROUP BY g.student_id, c.course_group, ct.total_credits
    ORDER BY g.student_id;
"""

TOTAL_KDL_COURSE_NUM = """
    select course_group, count(course_id) as course_num
    from course
    where course_group is not null and optional_28 != 'NO'
    group by course_group;
"""