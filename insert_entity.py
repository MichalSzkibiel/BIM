# -*- coding: cp1250 -*-
import psycopg2
from subprocess import call
def insert_entity(ifc_name,element):
    if ifc_name[element]["is_in_table"]:
        return
    print (element)
    conn = psycopg2.connect("dbname=postgres user=postgres password=Qjr567*_+")
    cur = conn.cursor()
    if "parent" in ifc_name[element]:
        if ifc_name[element]["parent"] !=None:
            if not (ifc_name[ifc_name[element]["parent"]]["is_in_table"]):#I) Sprawdzamy, czy rodzic jest odznaczony
                insert_entity(ifc_name,ifc_name[element]["parent"])
            cur.execute("CREATE TABLE IF NOT EXISTS " + element + "() INHERITS ( " + ifc_name[element]["parent"]+ ") WITH (OIDS=TRUE);")
				#jedna tabela dla kazdego entity i jedna kolumna dla kazdego atrybutu
        else:
                cur.execute("CREATE TABLE IF NOT EXISTS " + element + "() WITH (OIDS=TRUE)", [element])
    for i in ifc_name[element]["attributes"]:# i to klucz a pod wartoscia jest tryb
		#2. Robimy procedure pod 2.a.i: Zaladowanie strony klasy
        ifc_name1= ifc_name[element]["attributes"][i]
        print(i)
        print(ifc_name1)
        if not "SET" in ifc_name1:
            if ifc_name1 in ifc_name:
                ifc_name1 = ifc_name[ifc_name1]
            else:
                ifc_name1 = "TEXT"
        elif not "SET_SET" in ifc_name1:
            ifc_name1 = ifc_name[ifc_name1.replace("SET_", "")]
            if type(ifc_name1) != type(""):
                ifc_name1='TEXT[]'
            else:
                ifc_name1 = ifc_name1 + "[]"
        else:
            ifc_name1 = "TEXT"
        if type(ifc_name1) != type(""):
            ifc_name1='TEXT'
        try:
            cur.execute("ALTER TABLE " + element + " ADD " + i + " " + ifc_name1)
        except:
            print("Nie udało się wstawić")
        
    conn.commit()
    cur.close()
    conn.close()
    ifc_name[element]["is_in_table"]=True#III Odznaczamy klasę		
	#c) Ustawienie kluczy obcych
