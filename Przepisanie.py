import psycopg2

tab1=["Foreign_key_list","Value"]
tab2=["Integer_list","Value"]
tab3=["Real_list","Value"]
tab4=["String_list","Value"]
ifc_name1={"nazwa_typu" : "INTEGER", "nazwa_entity":{"parent":"nazwa_parent", "attribute_list":[{"name":"nazwa_typu"},{"ifc_class":[{"set":[{"klucz":"INTEGER"},{"TYPE":"Tip_a_Type"},{"ENTITY":"Foreign_key_list"}]},
"NO_set":[{"TYPE":"tip_a_Type"},{"ENTITY":"Foreign_key_String"}]]}], "is_in_database":False}, "nazwa_enum" : ["string1", "string2"]}
for element in ifc_name1:
    