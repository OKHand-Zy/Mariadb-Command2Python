import mysql.connector
from mysql.connector import Error
import numpy
import pandas as pd

import os
import sys
import signal

def signal_handler(signal,frame):
    sys.exit(0)

# Database
def show_databases():
    global connection,cursor
    cursor.execute(f"show databases;")
    databases_info = cursor.fetchall()
    for i in range(0, len(databases_info) ):
        print( databases_info[i][0]  )

def create_database(database_name):
    global connection,cursor
    cursor.execute(f"CREATE DATABASE {database_name};")
    connection.commit()

def delete_database(database_name):
    global connection,cursor
    cursor.execute(f"DROP DATABASE {database_name};")
    connection.commit()

def change_database(c2database):
    global connection,cursor
    cursor.execute(f"use {c2database};")

# Table
def show_tables():
    global connection,cursor
    cursor.execute(f"show tables;")
    table_info = cursor.fetchall()
    for i in range(0, len(table_info) ):
        print( table_info[i][0]  )

def show_table_info(table):
    global connection,cursor
    cursor.execute(f"SHOW INDEX FROM {table};")
    table_info = cursor.fetchall()
    labels = ['Table', 'Non_unique', 'Key_name', 'Seq_in_index', 'Column_name', 'Collation', 'Cardinality', 'Sub_part', 'Packed', 'Null', 'Index_type', 'Comment', 'Index_comment', 'Ignored']
    pd_table = pd.DataFrame.from_records(table_info, columns=labels)
    print(pd_table)

def create_table_db(table,parm):
    global connection,cursor
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table}({parm});")
    connection.commit()

def delete_table(table):
    global connection,cursor
    cursor.execute(f"Drop TABLE {table};")
    connection.commit()

# column
def show_column_info(table):
    global connection,cursor
    cursor.execute(f"desc {table};")
    table_info = cursor.fetchall()
    labels = ['Field', 'Type', 'Null', 'Key', 'Default', 'Extra']
    desc_table = pd.DataFrame.from_records(table_info, columns=labels)
    print(desc_table)

def show_column_db(table,s_column='*',filte=''): 
    global connection,cursor
    cursor.execute(f"SELECT {s_column} FROM {table} {filte};")
    if s_column != '*':
        table_list= s_column.split(',')
        row_data = cursor.fetchall()
        datalist = pd.DataFrame.from_records(row_data,columns=table_list)
        print(datalist)
    else:
        row_data = cursor.fetchall()
        for count in range(len(row_data)):
            print(row_data[count])

def delete_column(table,D_column_name,D_values):
    global connection,cursor
    cursor.execute(f"DELETE FROM {table} WHERE {D_column_name}={D_values};")
    connection.commit()

def insert_db(table,names,rows):
    global connection,cursor
    values = ''.join(map(str, rows))
    cursor.execute(f"INSERT INTO {table} ({names}) VALUES {values};")
    connection.commit() # Update to datebase

def update_db(table,fl_column_name,fl_column_value,find_column,find_column_value):
    global connection,cursor
    cursor.execute(f"UPDATE {table} SET {fl_column_name}={fl_column_value} WHERE {find_column}={find_column_value};")
    connection.commit()

def show_processlist():
    global connection,cursor
    cursor.execute(f"show processlist;")
    table_info = cursor.fetchall()
    labels = ['Id', 'User', 'HOST', 'db', 'Command', 'Time', 'State', 'Info','Progress']
    processlist = pd.DataFrame.from_records(table_info, columns=labels)
    #processlist = pd.DataFrame(table_info, columns=labels)   
    print(processlist)

def help():
    print("\nSystem Command : " )
    print("Now User => whoiam \n")
    
    print("DataBase Command : ")
    print("Show Databases  => database?")
    print("Change Database => change_db <database_name>")
    print("Create new Database => create_db <new_database_name>")
    print("Delete a Datadase => delete_db <delete_database_name> \n")
    
    print("Table Command : ")
    print("Show Tables  => table?")
    print("Show Table info => column_info <table_name>")
    print("Create new Table => create_table <new_table_name> <column_name column_type>")
    print("=> Ex: create_table pytest name varchar(10) ")
    print("Delete a Table => delete_table <table_name>\n")
    
    print("Column Command : ")
    print("Show column info => column_info <table_name>")
    print("Show_column_data => column_db? <table_name> <column_name,column_name ....> <filte>"+"  [default: column = '*' filte = '']")
    print("=> Ex: column_db? inventory ")
    print("=> Ex: column_db? inventory id,name Where name='Frank' ")
    print("Add new data => add_data <table_name> <names> <rows>")
    print("=> Ex: add_data inventory name,quantity ('apple',20)")
    print("Delete data => delete_data <table_name> <column_name> <column_value>")
    print("=> Ex: delete_data inventory name Frank")
    print("Update data => update_db <table_name> <update_column_name> <update_column_valu> <find_column> <find_column_value>")
    print("=> Ex: update_db inventory name,quantity ('Orange',50)")   
    

if __name__ == '__main__':
    #os.system('cls')    
    host = input("input host:")
    user = input("input user:")
    password = input("input password:")
    database = input("into database:")
    
    signal.signal(signal.SIGINT,signal_handler) # ctrl+c the process.

    try:
        # 連接 MySQL/MariaDB 資料庫
        connection = mysql.connector.connect(
            host=host,              # 主機名稱 'localhost'
            database=database,      # 資料庫名稱 'example'
            user=user,              # 帳號
            password=password)      # 密碼

        if connection.is_connected():
            cursor = connection.cursor()
            while 1==1 :
                input_txt = input(f"[{database}] Input you Command : ")
                if input_txt != '':
                    input_option = input_txt.split(' ',1)
                    input_option[0] = input_option[0].lower()
                    if input_option[0] == 'exit' :
                        sys.exit(0)
                    elif input_option[0] == 'help':
                        help()
                        print("====== \n")
                    elif input_option[0] == 'whoiam':
                        cursor.execute(f"SELECT USER();")
                        print(cursor.fetchone()[0])
                    elif input_option[0] == 'processlist':
                        show_processlist()
                        print("====== \n")
                    # DataBase
                    elif input_option[0] == 'database?':
                        show_databases()
                        print("====== \n")
                    elif input_option[0] == 'change_db':
                        change_database(c2database=input_option[1])
                        database = input_option[1]
                        print("====== \n")
                    elif input_option[0] == 'create_db' :
                        create_database(database_name=input_option[1])
                        print("====== \n")
                    elif input_option[0] == 'delete_db' :
                        delete_database(database_name=input_option[1])
                        print("====== \n")
                    
                    # Table
                    elif input_option[0] == 'table?':
                        show_tables()
                        print("====== \n")
                    elif input_option[0] == 'table_info' :
                        show_table_info(table=input_option[1])
                        print("====== \n")
                    elif input_option[0] == 'create_table' :
                        input_txt=input_option[1].split(' ',1)
                        create_table_db(table=input_txt[0],parm=input_txt[1])
                        print("====== \n")
                    elif input_option[0] == 'delete_table' :
                        delete_table(input_option[1])
                        print("====== \n")

                    # column
                    elif input_option[0] == 'column_info' :
                        show_column_info(table=input_option[1])
                        print("====== \n")
                    elif input_option[0] == 'column_db?' :  #print not good 
                        input_txt=input_option[1].split(' ',2)
                        if (len(input_txt)) == 1:
                            show_column_db(table=input_txt[0])
                        elif (len(input_txt)) == 2:
                            show_column_db(table=input_txt[0],s_column=input_txt[1])
                        elif (len(input_txt)) == 3:
                            show_column_db(table=input_txt[0],s_column=input_txt[1],filte=input_txt[2])
                        else:
                            print( "I don't know this command , can use help" ) 
                        print("====== \n")
                    elif input_option[0] == 'add_data' : 
                        input_txt=input_option[1].split(' ',2)
                        insert_db(table=input_txt[0],names=input_txt[1],rows=input_txt[2])
                        print("====== \n")
                    elif input_option[0] == 'delete_data' :
                        input_txt=input_option[1].split(' ',2)
                        delete_column(table=input_txt[0],D_column_name=input_txt[1],D_values=input_txt[2])
                        print("====== \n")
                    elif input_option[0] == 'update_db' :
                        input_txt=input_option[1].split(' ',2)
                        update_db(table=input_txt[0],fl_column_name=input_txt[1],fl_column_value=input_txt[2],find_column=input_txt[3],find_column_value=input_txt[4])
                        print("====== \n")
                    else:
                        print( "I don't know this command , can use help" ) 


            
            # do some thing
            #help()
            #====================================#
            # Mysql : show databases();
            #show_databases()

            #====================================#
            # Mysql : use {c2database};
            #change_database(c2database='cy')

            #====================================#
            # Mysql : show tables();
            #show_tables()
            
            #====================================#
            # Mysql : desc {s_table};
            #show_table_db(s_table='createst')
            
            #====================================#
            # Mysql : CREATE TABLE IF NOT EXISTS {table}({parm});
            #create_table_column(table='createst',parm="ID int NOT NULL AUTO_INCREMENT PRIMARY KEY,Name varchar(20),Height int(6),Weight int(6)")
            
            #====================================#
            # Mysql : DELETE FROM {table} WHERE {D_column_name}={D_values};
            #delete_column(table="inventory",D_column_name="name",D_values="'Vicky'")
            
            #====================================#
            # Mysql : UPDATE {table} SET {filter_table_name}={filter_table_value} WHERE {find_column}={find_column_value};
            #update_db(table="inventory",fl_column_name="quantity",fl_column_value=888,find_column="name",find_column_value="'Vicky'")
            
            #====================================#
            # Mysql : INSERT INTO {table} ({tables_names}) VALUES {tables_values};
            #rows=[("AD",7), ("AP",8), ("FD",9)]
            #insert_db(table="inventory",names="name, quantity",rows=rows) #OK
            
            #====================================#
            # Mysql : SELECT column_name,column_name FROM table_name [WHERE Clause][LIMIT N][ OFFSET M];
            #read_table_db(db_table="cy.inventory") # database.table and no print data   

            #====================================#
            # Mysql : show processlist;
            #show_processlist()
    except Error as e:
        #print("Connet_Error:", e)
        print("Have error bye~bye~")

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            #print("Connect_Close")


# Refrence
#insert:
#https://learn.microsoft.com/zh-tw/azure/mysql/single-server/connect-python
#https://www.w3schools.com/python/python_mysql_insert.asp