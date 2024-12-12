################################################################################
##########################         import packages         #####################
################################################################################
import mysql.connector as MySQLdb
import sys
sys.path.insert(0,'../.')
import config

################################################################################
########################## Create Database on mysql server #####################
################################################################################
def create_db(mysql_user=config.mysql_user, mysql_password=config.mysql_password, mysql_host=config.mysql_host, db_name=config.db_name):
    try:
        conn = MySQLdb.connect(user=mysql_user, host=mysql_host, password=mysql_password)
        print('Connection to MySQL server done successfully.')
        try:
            cur = conn.cursor()
            cur.execute("CREATE DATABASE IF NOT EXISTS {} ;".format(db_name))
            conn.commit()
            print("Database created successfully.")
        finally:
            conn.close()
            print("Connection closed.")
    except Exception as e:
        print("I am unable to connect to the database:", e)

################################################################################
########################## Create Table for Classroom ###########################
################################################################################
def create_table(mysql_user=config.mysql_user, mysql_password=config.mysql_password, mysql_host=config.mysql_host, db_name=config.db_name, table_name=config.table_name):
    try:
        conn = MySQLdb.connect(user=mysql_user, host=mysql_host, password=mysql_password, database=db_name)
        print('Connection to MySQL server done successfully.')
        try:
            cur = conn.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS {} (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                classroom_no VARCHAR(20) NOT NULL
                            );""".format(table_name))
            conn.commit()
            print("Table created successfully.")
        finally:
            conn.close()
            print("Connection closed.")
    except Exception as e:
        print("I am unable to connect to the database:", e)

def insert_row(classroom_no, mysql_user=config.mysql_user, mysql_password=config.mysql_password, mysql_host=config.mysql_host, db_name=config.db_name, table_name=config.table_name):
    try:
        conn = MySQLdb.connect(user=mysql_user, host=mysql_host, password=mysql_password, database=db_name)
        print('Connection to MySQL server done successfully.')
        try:
            cur = conn.cursor()
            cur.execute("""INSERT INTO {} (classroom_no) VALUES ('{}');""".format(table_name, classroom_no))
            conn.commit()
            print('Row inserted successfully.')
        finally:
            conn.close()
            print("Connection closed.")
    except Exception as e:
        print("Error:", e)

################################################################################
##########################          Main Function          ######################
################################################################################
if __name__ == "__main__":
    create_db()
    create_table()
