import pandas as pd
from bs4 import BeautifulSoup

def extract_excel_to_html(sheet_name):
    # Read Excel file, skip the first row and set the first row as header
    excel_data = pd.read_excel('ExamSeatArrangement.xlsx', sheet_name=sheet_name, skiprows=1, header=None)
    # Get the number of columns in the Excel file
    num_columns = len(excel_data.columns)
    # Initialize an empty string to store HTML table
    html_table = '<table>'  # Initialize the HTML table variable with the opening <table> tag
    header_row = '<tr><th>Seat No.</th><th>Name</th><th>Roll No.</th><th>Att. Status</th></tr>'
    # Add the header row to the HTML table
    html_table += header_row
    # Iterate through the columns in chunks of 4
    for i in range(0, num_columns, 4):
        # Read data from the current chunk of 4 columns
        chunk_data = excel_data.iloc[:, i:i+4]
        # Iterate through the rows of the chunk data
        for index, row in chunk_data.iterrows():
            row_value_list = row.tolist()
            row_tag = '<tr>'
            for value in row_value_list:
                row_tag += f'<td>{value}</td>'
            row_tag += '</tr>'
            # Add the header row to the HTML table
            html_table += row_tag
        
    # Close the table tag
    html_table += '</table>'

    table_soup = BeautifulSoup(html_table, 'html.parser')
    # Find all td tags with text 'Absent'
    absent_cells = table_soup.find_all('td', text='Absent')
    # Set class attribute to 'has-text-danger'
    for cell in absent_cells:
        cell['class'] = 'has-text-danger has-text-weight-bold'
    # Find all td tags with text 'Absent'
    present_cells = table_soup.find_all('td', text='Present')
    # Set class attribute to 'has-text-danger'
    for cell in present_cells:
        cell['class'] = 'has-text-success'
    
    return table_soup.prettify()