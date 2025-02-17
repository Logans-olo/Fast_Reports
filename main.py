import numpy as np
from tkinter import *
import pandas as pd
from docx import Document
from sqlalchemy import create_engine
import sqlite3
from app import *


engine = create_engine('sqlite:///OBHR.db')
name = ""



#Spring 2025 OBHR 33000-008 LEC
def main(): 
    document = doc_init()
    app = QApplication()
# Create a Qt widget, which will be our window.
    window = MainWindow()
    window.show()  # IMPORTANT!!!!! Windows are hidden by default.

    # Start the event loop.
    app.exec()
    table_name = db_init()
    data = db_query(table_name, 'Sections', '\"Spring 2025 OBHR 33000-008 LEC\"')
    print(len(data))
    print(len(data[0]))
    table = document.add_table(len(data), 3)
    table.style = 'Colorful List'
    i = 0
    j = 0
    for row in data: 
        for column in range(1,4):
            cell = table.cell(i, j)
            cell.text = str(row[j])
            j = j + 1
        i = i + 1
    document.save(name + ".docx")

def doc_init():
    
    name = " "
    print(name)
    document = Document()
    document.add_heading
    document.add_heading(name, 0)

    p = document.add_paragraph('A plain paragraph having some ')
    p.add_run('bold').bold = True
    p.add_run(' and some ')
    p.add_run('italic.').italic = True

    document.add_heading(name, level=1)
    document.add_paragraph('Intense quote', style='Intense Quote')

    document.add_paragraph(
        'first item in unordered list', style='List Bullet'
    )
    
    return document

def  db_init(): 
    
    print ("connection established to the database")
    pathname = input("What is the name of the csv")
    #Reading from the CSV and establishing a new table
    df = pd.read_csv(pathname + '.csv', nrows = 3)
    print(' we did this')
    
    
    df.to_sql('OBHR', con = engine, if_exists='replace', index=False)
    
    return pathname


def db_query(table_name, table_column, where): 
    connection = sqlite3.connect("OBHR.db") # Using a SQL database that is going to insert from the connected CSV
    crsr = connection.cursor()
    sql_command = """
    SELECT * FROM OBHR """  + """ WHERE """ + table_column + """ = """ + where + """ ;
    """
    print(sql_command)
    crsr.execute(sql_command)
    data = crsr.fetchall()
    for i in data:
        print(i)
        
    return data
    #df = pd.read_sql(data, con = engine)
    #return df
if __name__ == "__main__":
    main()