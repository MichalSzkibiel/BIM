import psycopg2
from subprocess import call


#tab1=["Foreign_key_list","Value"]
#tab2=["Integer_list","Value"]
#tab3=["Real_list","Value"]
#tab4=["String_list","Value"]
ifc_name1={"nazwa_typu" : "INTEGER", "nazwa_entity":{"parent":"nazwa_parent", "attribute_list":[{"name":"nazwa_typu"},{"ifc_class":[{"set":[{"klucz":"INTEGER"},{"TYPE":"Tip_a_Type"},{"ENTITY":"Foreign_key_list"}]},
"NO_set":[{"TYPE":"tip_a_Type"},{"ENTITY":"Foreign_key_String"}]]}], "is_in_database":False}, "nazwa_enum" : ["string1", "string2"]}
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
    else
       if not (ifc_name1[ifc_name1[element]["parent"]]["is_in_table"]):#I) Sprawdzamy, czy rodzic jest odznaczony
           insert_entity(ifc_name1,element)
           #ciag dalszy w funkcji insert_entity
        
