import pdfkit
from flask import Flask, send_file
from io import BytesIO
from bs4 import BeautifulSoup
from college_details import college_name, college_address

def create_attendance_report(html_table, class_room, exam_name="CIE-III", subject_name="IOT", subject_code="18CS81", semester="VIII", date="22/04/2024", time="9:00AM - 11:00AM"):
    # HTML template for the PDF
    html = """
    <html>
    <head>
        <title>Attendance Sheet</title>
        <style>
            .header, .sub-header, .subject-details, .footer, .table th, .table td {{
                font-family: Arial, sans-serif;
            }}

            .header {{
                text-align: center;
                margin-top: 30px;
                font-weight: bold;
                font-size: 20px;
            }}
            .sub-header {{
                text-align: center;
                margin-top: 10px;
                font-weight: bold;
                font-size: 16px;
            }}
            .subject-details-container {{
                margin-top: 20px;
                overflow: hidden;
            }}

            .subject-details-left {{
                float: left;
                width: 70%; 
            }}

            .subject-details-right {{
                float: left;
                width: 30%; 
            }}
            .table {{
                border-collapse: collapse;
                width: 100%;
                margin-top: 20px;
                font-size: 12px;
            }}
            .table th, .table td {{
                border: 1px solid black;
                padding: 8px;
                text-align: left;
            }}
            .footer {{
                margin-top: 20px;
                font-weight: bold;
                font-size: 16px;
            }}
            .footer div {{
                margin-bottom: 10px; /* Increased gap between the two lines */
            }}
        </style>
    </head>
    <body>
        <div class="header">{}</div>
        <div class="sub-header">{}</div>
        <div class="sub-header">Attendance Sheet (Form B) - [{}]</div>

        <div class="subject-details-container">
            <div class="subject-details-left">
                <div><b>Subject Name:</b> {}</div>
                <div><b>Subject Code:</b> {}</div>
                <div><b>Semester:</b> {}</div>
            </div>
            <div class="subject-details-right">
                <div><b>Room No.:</b> {}</div>
                <div><b>Date:</b> {}</div>
                <div><b>Time:</b> {}</div>
            </div>
        </div>


        <table class="table">
            <tr>
                <th>Sl. No.</th>
                <th>Reg Number</th>
                <th>Name of the Student</th>
                <th>Attendance Status</th>
            </tr>
            <!-- Student data will be inserted here -->
        </table>

        <div class="footer">
            <div>Total</div>
            <div>No. of Students Present:</div>
        </div>
    </body>
    </html>
    """.format(college_name, exam_name, class_room, subject_name, subject_code, semester, class_room, date, time)

    students = []
    present_count = 0
    table_soup = BeautifulSoup(html_table, 'html.parser')
    tr_tags = table_soup.find_all('tr')
    for tr_tag in tr_tags[1:]:
        row_value_list = [td.text.strip() for td in tr_tag.find_all('td')]
        students.append(row_value_list)
        if row_value_list[3] == "Present":
            present_count += 1

    total_students = len(students)

    # Insert student data into HTML table
    student_rows = ""
    for student in students:
        student_rows += f"""
        <tr>
            <td>{student[0]}</td>
            <td>{student[2]}</td>
            <td>{student[1]}</td>
            <td>{student[3]}</td>
        </tr>
        """

    # Insert student rows into the HTML template
    html = html.replace("<!-- Student data will be inserted here -->", student_rows)

    # Update footer with total and present count
    html = html.replace("<div>Total</div>", f"<div>Total: {total_students}</div>")
    html = html.replace("<div>No. of Students Present:</div>", f"<div>No. of Students Present: {present_count}</div>")

    # Generate PDF from HTML
    pdf = pdfkit.from_string(html, False)

    return pdf