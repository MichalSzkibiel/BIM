from ifc_counter import ifc_counter
from ifc_model_reader import *
from ifc_dict import ifc_dict

ifc_dict2 = {}

for key in ifc_dict:
    keyU = key.upper()
    ifc_dict2[keyU] = ifc_dict[key]

class numerator:
    value = 1

class set_numerator:
    value = 1

def sqlize_set_set(list):
    first = list[0][0]
    try:
        int(first)
        type = "set_integer"
    except:
        try:
            float(first)
            type = "set_float"
        except:
            type = "set_entity"
    sql = []
    ids = []
    for el in list:
        id = "$" + str(set_numerator.value)
        set_numerator.value = set_numerator_value + 1
        sql = sql + ["INSERT INTO " + type + " VALUES (" + id + ", " + str(el).replace("[", "(").replace("]", ")")]
        ids.append(id)
    return sql, ids

def sqlize(object):
    sql = ["INSERT INTO " + object["ifcClass"] + " VALUES ("]
    for key in object:
        if key == "ifcId":
            sql[-1] = sql[-1] + "\'" + object[key] + "\'"
        elif key == "ifcClass":
            continue
        elif type(object[key]) == type({}):
            if type(ifc_dict2[object[key]["ifcClass"]]) == type(""):
                for key2 in object[key]:
                    value = key2
                try:
                  float(key2)
                  sql[-1] = sql[-1] + ", " + str(key2)
                except:
                  sql[-1] = sql[-1] + ", \'" + key2 + "\'"
            else:   
                object[key]["ifcId"] = "*" + str(numerator.value)
                sql[-1] = sql[-1] + ", *" + str(numerator.value)
                numerator.value = numerator.value + 1
                sql1 = sqlize(object[key])
                sql = sql1 + sql
        elif object[key] == "$" or object[key] == "*":
            sql[-1] = sql[-1] + ", NULL"
        elif type(object[key]) == type([]):
              first = object[key][0]
              if type(first) == type([]):
                  first = first[0]
                  sql1, ids = sqlize_set_set(object[key])
                  sql = sql1 + sql
                  sql[-1] = sql[-1] + ", " + str(ids).replace("[", "(").replace("]", ")")
              else:
                  sql[-1] = sql[-1] + ", " + str(object[key]).replace("[", "(").replace("]", ")")
        else:
              try:
                  float(object[key])
                  sql[-1] = sql[-1] + ", " + str(object[key])
              except:
                  sql[-1] = sql[-1] + ", \'" + object[key].replace(".", "") + "\'"
    sql[-1] = sql[-1] + ")"
    return sql

#ifc_model = ifc_model_reader.read_schemas()
counter  = ifc_counter("HITOS_Architectural_2006-10-25.ifc", "ifc_atributes.txt")
print("generowanie jsona")
json = counter.json_getter()
print("koniec")
conn = psycopg2.connect("dbname=postgres user=postgres password=Qjr567*_+")
cur = conn.cursor()
for el in json:
    sql = sqlize(el)
    for i in range(len(sql)):
        cur.execute(sql[i])
        #print (sql[i])
conn.close()
