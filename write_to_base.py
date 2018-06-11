from ifc_counter import ifc_counter
from ifc_model_reader import *
from ifc_dict import ifc_dict

ifc_dict2 = {}

for key in ifc_dict:
    keyU = key.upper()
    ifc_dict2[keyU] = ifc_dict[key]

class numerator:
    value = 1

def sqlize(object):
    sql = ["INSERT INTO %s VALUES ("]
    values = [[object["ifcClass"]]]
    for key in object:
        if key == "ifcId":
            sql[-1] = sql[-1] + "%s, "
            values[-1] = [values[-1][0]] + ["\'" + object[key] + "\'"] + values[-1][1:]
        elif key == "ifcClass":
            continue
        elif type(object[key]) == type({}):
            if type(ifc_dict2[object[key]["ifcClass"]]) == type(""):
                for key2 in object[key]:
                    value = key2
                try:
                  float(key2)
                  sql[-1] = sql[-1] + "%s, "
                  values[-1] = values[-1] + [key2]
                except:
                  sql[-1] = sql[-1] + "%s, "
                  values[-1] = values[-1] + ["\'" + key2 + "\'"]
            else:   
                object[key]["ifcId"] = "*" + str(numerator.value)
                sql[-1] = sql[-1] + "%s, "
                values[-1] = values[-1] + ["*" + str(numerator.value)]
                numerator.value = numerator.value + 1
                sql1, values1 = sqlize(object[key])
                sql = sql1 + sql
                values = values1 + values
        elif object[key] == "$" or object[key] == "*":
            sql[-1] = sql[-1] + "%s, "
            values[-1] = values[-1] + ["NULL"]
        elif type(object[key]) == type([]):
              first = object[key][0]
              try:
                  float(first)
                  sql[-1] = sql[-1] + "%s, "
                  values[-1] = values[-1] + [str(object[key]).replace("[", "(").replace("]", ")")]
              except:
                  sql[-1] = sql[-1] + "%s, "
                  values[-1] = values[-1] + [str(object[key]).replace("[", "(").replace("]", ")")]
        else:
              try:
                  float(object[key])
                  sql[-1] = sql[-1] + "%s, "
                  values[-1] = values[-1] + [object[key]]
              except:
                  sql[-1] = sql[-1] + "%s, "
                  values[-1] = values[-1] + ["\'" + object[key] + "\'"]
    sql[-1] = sql[-1][:-2] + ")"
    return sql, values

#ifc_model = ifc_model_reader.read_schemas()
counter  = ifc_counter("HITOS_Architectural_2006-10-25.ifc", "ifc_atributes.txt")
print("generowanie jsona")
json = counter.json_getter()
print("koniec")
for el in json:
    sql, values = sqlize(el)
    for i in range(len(sql)):
        print (sql[i] + ", " + str(values[i]))
print (str(numerator.value))
