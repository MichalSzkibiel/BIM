# -*- coding: cp1250 -*-
def insert_entity(ifc_name,element):
    if ifc_name1[[element]["is_in_table"]]:
        return
    if not (ifc_name1[ifc_name1[element]["parent"]]["is_in_table"]):
        insert_entity(ifc_name,ifc_name1[element]["parent"]) #1. Ustawiamy obecna… klasa na rodzica
        conn = psycopg2.connect("dbname=postgres user=Karol Jakub")
        cur = conn.cursor()
        cur.execute("CREATE TABLE entity(id enumeration PRIMARY KEY, ifc_name1 bigint);")
        for i in ifc_name1[element]:
            cur.execute("INSERT INTO entity  VALUES (%s)",i)#2. Robimy procedure pod 2.a.i: Zaladowanie strony klasy
        conn.commit()
        cur.close()
        conn.close()
        conn1 = psycopg2.connect("dbname=postgres user=Karol Jakub")
        cur1 = conn1.cursor()
        cur1.execute("CREATE TABLE class(id serial PRIMARY KEY, ifc_name1 bigint);")#3. Wracamy do obecnej klasy
        cur1.execute(SQL("INSERT INTO {} VALUES (%s)").format(Identifier(ifc_name1)),i)#II Wstawiamy tabelę dla danej klasy
        "is_in_table"=True#III Odznaczamy klasę		
	#c) Ustawienie kluczy obcych
