# -*- coding: cp1250 -*-
def insert_entity(ifc_dict, ifc_name,element):
    if ifc_name1[[element]["is_in_table"]]:
        return
    if not (ifc_name1[ifc_name1[element]["parent"]]["is_in_table"]):
        insert_entity(ifc_name,ifc_name1[element]["parent"]) #1. Ustawiamy obecna… klasa na rodzica
    conn = psycopg2.connect("dbname=postgres user=Karol Jakub")
    cur = conn.cursor()
    cur.execute("CREATE TABLE %s(id enumeration PRIMARY KEY, (%s) bigint );")#jedna tabela dla kazdego entity i jedna kolumna dla kazdego atrybutu
    for i in ifc_name1[element][attributes]:# i to klucz a pod wartoscia jest tryb
		#2. Robimy procedure pod 2.a.i: Zaladowanie strony klasy
        ifc_name= ifc_dict(ifc_name1[element][attributes][i])
        if ifc_name!=ifc_name1[[element]["String"]]:
            ifc_name='TEXT'
            cur.execute("ALTER TABLE %s ADD %s text;")
        else:
            cur.execute("ALTER TABLE %s ADD %s %s", ["ifc_name","attributes","type"]) 
    conn.commit()
    cur.close()
    conn.close()
    conn1 = psycopg2.connect("dbname=postgres user=Karol Jakub")
    cur1 = conn1.cursor()
    cur1.execute("CREATE TABLE %s(id serial PRIMARY KEY, %s bigint);")#3. Wracamy do obecnej klasy
    cur1.execute(SQL("INSERT INTO %s VALUES (%s)").format(Identifier(ifc_name1)),i)#II Wstawiamy tabelę dla danej klasy
    ifc_name1[[element]["is_in_table"]]=True#III Odznaczamy klasę		
	#c) Ustawienie kluczy obcych
