import psycopg2
from subprocess import call
from insert_entity import insert_entity

ifc_name1={"nazwa_typu" : "INTEGER", "nazwa_entity":{"parent":"nazwa_parent", "attribute_list":{"name":"nazwa_typu", "ifc_class":"nazwa_entity"}, "is_in_table":False}, "nazwa_enum" : ["string1","string2"]}
for element in ifc_name1:
    if type(ifc_name1[element]) == type("string"):#sprawdzamy typy
        continue
    elif type(ifc_name1[element]) == type([]):
        conn = psycopg2.connect("dbname=postgres user=Karol Jakub")
        cur = conn.cursor()
        cur.execute("CREATE TABLE element(id text PRIMARY KEY);")
        for i in ifc_name1[element]:
            cur.execute("INSERT INTO element  VALUES (%s)",i)
        conn.commit()
        cur.close()
        conn.close()    
    else:
        insert_entity(ifc_name1,element)
                #ciag dalszy w funkcji insert_entity
             
