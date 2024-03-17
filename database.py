import sqlite3

def creat_database_tables():
    connect = sqlite3.connect("data.db")
    cur = connect.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS medias(media_id int(250),mid int(250))")
    connect.commit()
    connect.close()



def insert_media(media_id,mid):
    connect = sqlite3.connect("data.db")
    cur = connect.cursor()
    cur.execute(f"insert into medias (media_id,mid) values ('{media_id}',{mid})")
    connect.commit()
    connect.close()

def use_media(media_id):
    connect = sqlite3.connect("data.db")
    cur = connect.cursor()
    cur.execute(f"select * from medias where media_id='{media_id}'")
    dict_info=cur.fetchall()
    connect.commit()
    connect.close()
    return dict_info

creat_database_tables()