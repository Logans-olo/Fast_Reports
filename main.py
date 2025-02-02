import numpy as np
import pandas as pd
from docx import Document
from sqlalchemy import create_engine
import sqlite3
def main(): 
    name = input("What is your name: ")
    document = doc_init(name)
    document.save(name + ".docx")
    
    db_init()
    
    
def doc_init(name):
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

def db_init(): 
    connection = sqlite3.connect("OBHR.db") # Using a SQL database that is going to insert from the connected CSV
    crsr = connection.cursor()
    print ("connection established to the database")
    #Reading from the CSV and establishing a new table
    df = pd.read_csv('OBHR330-2025Spring_T1Survey_0_deidentified.csv', nrows=3)
    print(' we did this')
    engine = create_engine('sqlite:///OBHR.db')
    print(df)
    df.to_sql('OBHR', con = engine, if_exists='replace', index=False)
    # sql_command = """"" 
    # CREATE TABLE
    # """
        
        
        
if __name__ == "__main__":
    main()