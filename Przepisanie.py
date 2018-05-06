import psycopg2
from subprocess import call


tab1=["Foreign_key_list","Value"]
tab2=["Integer_list","Value"]
tab3=["Real_list","Value"]
tab4=["String_list","Value"]
ifc_name1={"nazwa_typu" : "INTEGER", "nazwa_entity":{"parent":"nazwa_parent", "attribute_list":[{"name":"nazwa_typu"},{"ifc_class":[{"set":[{"klucz":"INTEGER"},{"TYPE":"Tip_a_Type"},{"ENTITY":"Foreign_key_list"}]},
"NO_set":[{"TYPE":"tip_a_Type"},{"ENTITY":"Foreign_key_String"}]]}], "is_in_database":False}, "nazwa_enum" : ["string1", "string2"]}
for element in ifc_name1:
    if ifc_name1[element] =="nazwa_typu"#nie wiem jak sprawdzic odznaczenie
        return
    else#NIE JEST
       if ifc_class=="parent"#I) Sprawdzamy, czy rodzic jest odznaczonym, pewnie zle...
            return
        else#NIE JEST
            ifc_class="parent"#1. Ustawiamy obecną klasę na rodzica
            call(["python", "ifc_model_reader.py"])# bo trzeba przywolas funkcje z innego skryptu
            read_schemas()#2. Robimy procedurę pod 2.a.i: Załadowanie strony klasy
            return ifc_class #3. Wracamy do obecnej klasy (? Czy to to?)
    #II Wstawiamy tabelę dla danej klasy
    #Pewnie trzeba bedzie sprawdzic, do jakiego typu.
    if ifc_class == tab1
        return ifc_class
    elif ifc_class == tab2
        return ifc_class
    elif ifc_class == tab3
        return ifc_class
    elif ifc_class == tab4
    else
        print "tej klasy nie da sie dopasowac do zadnej typu tabeli "
			"""III Odznaczamy klasę- tego kompletnie nie wiem
	c) Ustawienie kluczy obcych- na razie to zostawiam"""