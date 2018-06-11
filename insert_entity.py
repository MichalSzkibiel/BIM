# -*- coding: cp1250 -*-
def insert_entity(ifc_name,element):
    if ifc_name[[element]["is_in_table"]]:
        return
    if "parent" in ifc_name[element]:
            if not (ifc_name[ifc_name[element]["parent"]]["is_in_table"]):#I) Sprawdzamy, czy rodzic jest odznaczony
                 insert_entity(ifc_name,ifc_name[element]["parent"])
    conn = psycopg2.connect("dbname=postgres user=Karol Jakub")
    cur = conn.cursor()
    cur.execute("CREATE TABLE %s INHERITS (%s) WITH (OIDS=TRUE) );", [ifc_name,element,ifc_name[ifc_name[element]["parent"]]])#jedna tabela dla kazdego entity i jedna kolumna dla kazdego atrybutu
    for i in ifc_name[element][attributes]:# i to klucz a pod wartoscia jest tryb
		#2. Robimy procedure pod 2.a.i: Zaladowanie strony klasy
        ifc_name1= ifc_name[ifc_name[element][attributes][i]]
        if ifc_name1!=ifc_name[[element]["String"]]:
            ifc_name1='TEXT'
            cur.execute("ALTER TABLE %s ADD %s text;", [ifc_name, i])
        else:
            cur.execute("ALTER TABLE %s ADD %s %s", [ifc_name, i, ifc_name1]) 
    conn.commit()
    cur.close()
    conn.close()
    conn1 = psycopg2.connect("dbname=postgres user=postgres")
    cur1 = conn1.cursor()
    ifc_name1[[element]["is_in_table"]]=True#III Odznaczamy klasę		
	#c) Ustawienie kluczy obcych
