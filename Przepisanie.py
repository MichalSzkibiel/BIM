import psycopg2
from subprocess import call
from insert_entity import insert_entity
from ifc_dict import ifc_dict

ifc_name1=ifc_dict
conn = psycopg2.connect("dbname=postgres user=postgres password=Qjr567*_+")
cur = conn.cursor()
#cur.execute("CREATE TABLE set_real (id text PRIMARY KEY, values real[]);")
#cur.execute("CREATE TABLE set_integer (id text PRIMARY KEY, values integer[]);")
#cur.execute("CREATE TABLE set_entity (id text PRIMARY KEY, values text[]);")
conn.commit()
conn.close()
for element in ifc_name1:
    if type(ifc_name1[element]) == type("string"):#sprawdzamy typy
        continue
    elif type(ifc_name1[element]) == type([]):
        conn = psycopg2.connect("dbname=postgres user=postgres password=Qjr567*_+")
        cur = conn.cursor()
        conn = psycopg2.connect("dbname=postgres user=postgres password=Qjr567*_+")
        cur = conn.cursor()
        cur.execute("select exists(select * from information_schema.tables where table_name=%s)", (element,))
        if bool(cur.rowcount):
            continue
        cur.execute("CREATE TABLE " + element + " (id text PRIMARY KEY);")
        for i in ifc_name1[element]:
            cur.execute("INSERT INTO " + element + "  VALUES (%s)", [i])
        conn.commit()
        cur.close()
        conn.close()    
    else:
        insert_entity(ifc_name1,element)
                #ciag dalszy w funkcji insert_entity
             
