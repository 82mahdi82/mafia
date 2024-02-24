import sqlite3

def creat_database_tables():
    connect = sqlite3.connect("data.db")
    cur = connect.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS groups(cid int(25) PRIMARY KEY,title VARCHAR(250))")
    cur.execute("CREATE TABLE IF NOT EXISTS users(cid int(25) PRIMARY KEY, user_name VARCHAR(250))")
    cur.execute("CREATE TABLE IF NOT EXISTS games (name VARCHAR(100), link_game VARCHAR(500) PRIMARY KEY, id_image VARCHAR(500),number int(10),time VARCHAR(10),gruop_id VARCHAR(250),gruop_name VARCHAR(250),nazer VARCHAR(250),name_nazer VARCHAR(250))")
    connect.commit()
    connect.close()


def insert_users(cid,user_name):
    connect = sqlite3.connect("data.db")
    cur = connect.cursor()
    cur.execute(f"insert into users (cid,user_name) values ({cid},'{user_name}')")
    connect.commit()
    connect.close()


def insert_group(cid,title):
    connect = sqlite3.connect("data.db")
    cur = connect.cursor()
    cur.execute(f"insert into groups (cid,title) values ({cid},'{title}')")
    connect.commit()
    connect.close()

def use_table_admin_group():
    connect = sqlite3.connect("data.db")
    cur = connect.cursor()
    cur.execute(f"select * from groups")
    dict_info=cur.fetchall()
    connect.commit()
    connect.close()
    return dict_info


def insert_games(name,link_game,id_image,number,time,gruop_id,gruop_name,nazer,name_nazer):
    connect = sqlite3.connect("data.db")
    cur = connect.cursor()
    cur.execute(f"insert into games (name,link_game,id_image,number,time,gruop_id,gruop_name,nazer,name_nazer) values ('{name}','{link_game}','{id_image}',{number},'{time}','{gruop_id}','{gruop_name}','{nazer}','{name_nazer}')")
    connect.commit()
    connect.close()
    
def use_games():
    connect = sqlite3.connect("data.db")
    cur = connect.cursor()
    cur.execute(f"select * from games")
    dict_info=cur.fetchall()
    connect.commit()
    connect.close()
    return dict_info


def delete_games(link_game):
    connect = sqlite3.connect("data.db")
    cur = connect.cursor()
    cur.execute(f"delete from games where link_game='{link_game}'")
    connect.commit()
    connect.close()



def use_users():
    connect = sqlite3.connect("data.db")
    cur = connect.cursor()
    cur.execute(f"select * from users")
    dict_info=cur.fetchall()
    connect.commit()
    connect.close()
    return dict_info

# insert_games("شب س هم","http:\\efkmlksvmkvf.com","gfjxrlitkhndgnmhd,m xfl.bmnskz;mb c,slk;m c,mn xvm nb",6)