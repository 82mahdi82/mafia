import mysql.connector
import time

def create_database():
    cnx = mysql.connector.connect(user='root', password='ioWJnL7vsHuiNieCO91d',host='datasps_db')
    cursor = cnx.cursor()
    # cursor.execute("DROP database IF EXISTS data")
    cursor.execute("create database if not exists data")
    cursor.execute("use data")
    cursor.execute("""CREATE TABLE if not exists profile (cid bigint PRIMARY KEY,
                photo VARCHAR(300) DEFAULT 'AgACAgQAAxkBAAI3wmYPvX4hkpjvxDYFKAQMF_Za41qaAALbxzEbi0x5UCNROuj45nOoAQADAgADbQADNAQ',
                name VARCHAR(25) DEFAULT 'وارد نشده',
                gender VARCHAR(25) DEFAULT 'وارد نشده',
                age VARCHAR(25) DEFAULT 'وارد نشده',
                education VARCHAR(25) DEFAULT 'وارد نشده',
                height VARCHAR(15) DEFAULT 'وارد نشده',
                weight VARCHAR(15) DEFAULT 'وارد نشده',
                job VARCHAR(15) DEFAULT 'وارد نشده',
                income VARCHAR(25) DEFAULT 'وارد نشده',
                province VARCHAR(15) DEFAULT 'وارد نشده',
                home VARCHAR(25) DEFAULT 'وارد نشده',
                car VARCHAR(15) DEFAULT 'وارد نشده',
                matrial VARCHAR(15) DEFAULT 'وارد نشده',
                validity int(100) DEFAULT 0,
                ID int(20))""")
    

    cursor.execute("""CREATE TABLE if not exists girlfriend (cid bigint PRIMARY KEY,
                ebout VARCHAR(300) DEFAULT 'وارد نشده',
                ebout_girl VARCHAR(25) DEFAULT 'وارد نشده',
                age_f VARCHAR(25) DEFAULT 'وارد نشده',
                post VARCHAR(25) DEFAULT 'no',
                shenase int(20),
                status VARCHAR(25),
                date VARCHAR(25))""")
    
    cursor.execute("""CREATE TABLE if not exists boyfriend (cid bigint PRIMARY KEY,
                ebout VARCHAR(300) DEFAULT 'وارد نشده',
                ebout_boy VARCHAR(25) DEFAULT 'وارد نشده',
                age_f VARCHAR(25) DEFAULT 'وارد نشده',
                post VARCHAR(25) DEFAULT 'no',
                shenase int(20),
                status VARCHAR(25),
                date VARCHAR(25))""")

    cursor.execute("""CREATE TABLE if not exists hhome (cid bigint PRIMARY KEY,
                ebout VARCHAR(300) DEFAULT 'وارد نشده',
                ebout_hhome VARCHAR(25) DEFAULT 'وارد نشده',
                ebout_home VARCHAR(25) DEFAULT 'وارد نشده',
                post VARCHAR(25) DEFAULT 'no',
                shenase int(20),
                status VARCHAR(25),
                date VARCHAR(25))""")  

    cursor.execute("""CREATE TABLE if not exists sugermommy (cid bigint PRIMARY KEY,
                ebout VARCHAR(300) DEFAULT 'وارد نشده',
                ebout_boy VARCHAR(25) DEFAULT 'وارد نشده',
                age_f VARCHAR(25) DEFAULT 'وارد نشده',
                post VARCHAR(25) DEFAULT 'no',
                shenase int(20),
                status VARCHAR(25),
                date VARCHAR(25))""")

    cursor.execute("""CREATE TABLE if not exists sugerdady (cid bigint PRIMARY KEY,
                ebout VARCHAR(300) DEFAULT 'وارد نشده',
                ebout_girl VARCHAR(25) DEFAULT 'وارد نشده',
                age_f VARCHAR(25) DEFAULT 'وارد نشده',
                post VARCHAR(25) DEFAULT 'no',
                shenase int(20),
                status VARCHAR(25),
                date VARCHAR(25))""")
     
    cursor.execute("""CREATE TABLE if not exists tompmarri (cid bigint PRIMARY KEY,
                ebout VARCHAR(300) DEFAULT 'وارد نشده',
                ebout_boy_girl VARCHAR(25) DEFAULT 'وارد نشده',
                age_f VARCHAR(25) DEFAULT 'وارد نشده',
                dowry VARCHAR(25) DEFAULT 'وارد نشده',
                post VARCHAR(25) DEFAULT 'no',
                shenase int(20),
                status VARCHAR(25),
                date VARCHAR(25))""") 
    
    cursor.execute("""CREATE TABLE if not exists marri (cid bigint PRIMARY KEY,
                ebout VARCHAR(300) DEFAULT 'وارد نشده',
                ebout_boy_girl VARCHAR(25) DEFAULT 'وارد نشده',
                age_f VARCHAR(25) DEFAULT 'وارد نشده',
                post VARCHAR(25) DEFAULT 'no',
                shenase int(20),
                status VARCHAR(25),
                date VARCHAR(25))""")

    cursor.execute("""CREATE TABLE if not exists partnerlang (cid bigint PRIMARY KEY,
                ebout VARCHAR(300) DEFAULT 'وارد نشده',
                ebout_you VARCHAR(25) DEFAULT 'وارد نشده',
                age_f VARCHAR(25) DEFAULT 'وارد نشده',
                post VARCHAR(25) DEFAULT 'no',
                shenase int(20),
                status VARCHAR(25),
                date VARCHAR(25))""") 

    cursor.execute("""CREATE TABLE if not exists partnerkoo (cid bigint PRIMARY KEY,
                ebout VARCHAR(300) DEFAULT 'وارد نشده',
                ebout_you VARCHAR(25) DEFAULT 'وارد نشده',
                age_f VARCHAR(25) DEFAULT 'وارد نشده',
                post VARCHAR(25) DEFAULT 'no',
                shenase int(20),
                status VARCHAR(25),
                date VARCHAR(25))""")
    
    cursor.execute("""CREATE TABLE if not exists teachlang (cid bigint PRIMARY KEY,
                ebout VARCHAR(300) DEFAULT 'وارد نشده',
                whatteach VARCHAR(25) DEFAULT 'وارد نشده',
                teach_exp VARCHAR(25) DEFAULT 'وارد نشده',
                cost VARCHAR(25) DEFAULT 'وارد نشده',
                post VARCHAR(25) DEFAULT 'no',
                shenase int(20),
                status VARCHAR(25),
                date VARCHAR(25))""")
    
    cursor.execute("""CREATE TABLE if not exists teachkoo (cid bigint PRIMARY KEY,
                ebout VARCHAR(300) DEFAULT 'وارد نشده',
                whatteach VARCHAR(25) DEFAULT 'وارد نشده',
                teach_exp VARCHAR(25) DEFAULT 'وارد نشده',
                cost VARCHAR(25) DEFAULT 'وارد نشده',
                post VARCHAR(25) DEFAULT 'no',
                shenase int(20),
                status VARCHAR(25),
                date VARCHAR(25))""")

    cursor.execute("""CREATE TABLE if not exists teachuniv (cid bigint PRIMARY KEY,
                ebout VARCHAR(300) DEFAULT 'وارد نشده',
                whatteach VARCHAR(25) DEFAULT 'وارد نشده',
                teach_exp VARCHAR(25) DEFAULT 'وارد نشده',
                cost VARCHAR(25) DEFAULT 'وارد نشده',
                post VARCHAR(25) DEFAULT 'no',
                shenase int(20),
                status VARCHAR(25),
                date VARCHAR(25))""")

    cursor.execute("""CREATE TABLE if not exists teachsys (cid bigint PRIMARY KEY,
                ebout VARCHAR(300) DEFAULT 'وارد نشده',
                whatteach VARCHAR(25) DEFAULT 'وارد نشده',
                teach_exp VARCHAR(25) DEFAULT 'وارد نشده',
                cost VARCHAR(25) DEFAULT 'وارد نشده',
                post VARCHAR(25) DEFAULT 'no',
                shenase int(20),
                status VARCHAR(25),
                date VARCHAR(25))""") 
    
    cursor.execute("""CREATE TABLE if not exists projectuinv (cid bigint PRIMARY KEY,
                ebout VARCHAR(300) DEFAULT 'وارد نشده',
                ecpertise VARCHAR(25) DEFAULT 'وارد نشده',
                post VARCHAR(25) DEFAULT 'no',
                shenase int(20),
                status VARCHAR(25),
                date VARCHAR(25))""") 
    
    cursor.execute("""CREATE TABLE if not exists projectwork (cid bigint PRIMARY KEY,
                ebout VARCHAR(300) DEFAULT 'وارد نشده',
                ecpertise VARCHAR(25) DEFAULT 'وارد نشده',
                post VARCHAR(25) DEFAULT 'no',
                shenase int(20),
                status VARCHAR(25),
                date VARCHAR(25))""") 

    print("created")
    cursor.close()
    cnx.commit()

#-------------------------------------------profile------------------------------------------------

def use_all_profile():
    cnx = mysql.connector.connect(user='root', password='ioWJnL7vsHuiNieCO91d',host='datasps_db',database="data")
    cursor = cnx.cursor(dictionary=True)
    cursor.execute(f"select * from profile")
    dict_product=cursor.fetchall()
    return dict_product
def use_profile_table(cid):
    cnx = mysql.connector.connect(user='root', password='ioWJnL7vsHuiNieCO91d',host='datasps_db',database="data")
    cursor = cnx.cursor(dictionary=True)
    cursor.execute(f"select * from profile where cid={cid}")
    dict_product=cursor.fetchall()
    return dict_product

def use_profile_id_table(id):
    cnx = mysql.connector.connect(user='root', password='ioWJnL7vsHuiNieCO91d',host='datasps_db',database="data")
    cursor = cnx.cursor(dictionary=True)
    cursor.execute(f"select * from profile where ID={id}")
    dict_product=cursor.fetchall()
    return dict_product

def add_validity(ID,validity):
    cnx = mysql.connector.connect(user='root', password='ioWJnL7vsHuiNieCO91d',host='datasps_db',database="data")
    cursor = cnx.cursor()
    cursor.execute(f"update profile set validity=validity+{validity} where ID={ID}")
    cursor.close()
    cnx.commit()

def sub_validity(ID,validity):
    cnx = mysql.connector.connect(user='root', password='ioWJnL7vsHuiNieCO91d',host='datasps_db',database="data")
    cursor = cnx.cursor()
    cursor.execute(f"update profile set validity=validity-{validity} where ID={ID}")
    cursor.close()
    cnx.commit()

def all_use_profile_table():
    cnx = mysql.connector.connect(user='root', password='ioWJnL7vsHuiNieCO91d',host='datasps_db',database="data")
    cursor = cnx.cursor(dictionary=True)
    cursor.execute(f"select * from profile")
    dict_product=cursor.fetchall()
    return dict_product

def insert_profile_first_table(cid,ID):
    cnx = mysql.connector.connect(user='root', password='ioWJnL7vsHuiNieCO91d',host='datasps_db',database="data")
    cursor = cnx.cursor()
    cursor.execute("insert into profile (cid,ID) values (%s,%s)",(cid,ID))
    cursor.close()
    cnx.commit()

def update_profile_one_table(cid,key,value):
    cnx = mysql.connector.connect(user='root', password='ioWJnL7vsHuiNieCO91d',host='datasps_db',database="data")
    cursor = cnx.cursor()
    cursor.execute(f"update profile set {key}='{value}' where cid={cid}")
    cursor.close()
    cnx.commit()

#--------------------------------------------------post---------------------------------------------------------------------

def insert_post_first_table(post,cid):
    cnx = mysql.connector.connect(user='root', password='ioWJnL7vsHuiNieCO91d',host='datasps_db',database="data")
    cursor = cnx.cursor()
    cursor.execute(f"insert into {post} (cid) values (%s)",(cid,))
    cursor.close()
    cnx.commit()

def use_post_table(post,cid):
    cnx = mysql.connector.connect(user='root', password='ioWJnL7vsHuiNieCO91d',host='datasps_db',database="data")
    cursor = cnx.cursor(dictionary=True)
    cursor.execute(f"select * from {post} where cid={cid}")
    dict_product=cursor.fetchall()
    return dict_product

def use_post_table_shenase(post,shenase):
    cnx = mysql.connector.connect(user='root', password='ioWJnL7vsHuiNieCO91d',host='datasps_db',database="data")
    cursor = cnx.cursor(dictionary=True)
    cursor.execute(f"select * from {post} where shenase={shenase}")
    dict_product=cursor.fetchall()
    return dict_product

def use_post_on_table(post):
    cnx = mysql.connector.connect(user='root', password='ioWJnL7vsHuiNieCO91d',host='datasps_db',database="data")
    cursor = cnx.cursor(dictionary=True)
    cursor.execute(f"select * from {post} where post='yes'")
    dict_product=cursor.fetchall()
    return dict_product

def use_post_one_table(post,row,cid):
    cnx = mysql.connector.connect(user='root', password='ioWJnL7vsHuiNieCO91d',host='datasps_db',database="data")
    cursor = cnx.cursor(dictionary=True)
    cursor.execute(f"select {row} from {post} where cid={cid}")
    dict_product=cursor.fetchall()
    return dict_product

def update_post_one_table(post,cid,key,value):
    cnx = mysql.connector.connect(user='root', password='ioWJnL7vsHuiNieCO91d',host='datasps_db',database="data")
    cursor = cnx.cursor()
    cursor.execute(f"update {post} set {key}='{value}' where cid={cid}")
    cursor.close()
    cnx.commit()

def update_post_last_table(post_name,post,shenase,status,date,cid):
    cnx = mysql.connector.connect(user='root', password='ioWJnL7vsHuiNieCO91d',host='datasps_db',database="data")
    cursor = cnx.cursor()
    cursor.execute(f"update {post_name} set post='{post}' ,shenase={shenase}, status='{status}', date='{date}' where cid={cid}")
    cursor.close()
    cnx.commit()



