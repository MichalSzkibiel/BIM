from ifc_model_reader import read_schemas

ifc_dict = read_schemas()

file = open("ifc_dict.txt", "w")
file.write(str(ifc_dict))
file.close()
