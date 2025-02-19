from sqlalchemy import create_engine
import pandas as pd
import sqlite3
engine = create_engine('sqlite:///OBHR.db')

def print_table(data, table_name, table):
    data = db_query(table_name, 'Sections', '\"Spring 2025 OBHR 33000-008 LEC\"')
    print(len(data))
    print(len(data[0]))
    # table = document.add_table(len(data), 3)
    table.style = 'Colorful List'
    i = 0
    j = 0
    for row in data: 
        for column in range(1,4):
            cell = table.cell(i, j)
            cell.text = str(row[j])
            j = j + 1
        i = i + 1
        
def db_init(table_name, pathname): 
    
    print ("connection established to the database")
    # pathname = input("What is the name of the csv")
    #Reading from the CSV and establishing a new table
    df = pd.read_csv(pathname + '.csv', nrows = 3)
    print(' we did this')
    
    
    df.to_sql(table_name, con = engine, if_exists='replace', index=False)
    
    return pathname

def db_column(table_name):
    connection = sqlite3.connect("OBHR.db")
    crsr = connection.cursor()
    crsr.execute('PRAGMA table_info(' + table_name + ')')
    return crsr.fetchall()
def db_query(table_name, table_column, where): 
    connection = sqlite3.connect("OBHR.db") # Using a SQL database that is going to insert from the connected CSV
    crsr = connection.cursor()
    sql_command = """
    SELECT * FROM """ +  table_name    + """ WHERE """ + table_column + """ = """ + where + """ ;
    """
    print(sql_command)
    crsr.execute(sql_command)
    data = crsr.fetchall()
    for i in data:
        print(i)
        
    return data
    #df = pd.read_sql(data, con = engine)
    #return df