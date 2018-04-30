import urllib.request

link = r"http://www.steptools.com/stds/ifc/html/"
simple = {"REAL":"REAL", "BINARY":"BYTEA", "BOOLEAN":"BOOLEAN", "INTEGER":"INTEGER", "NUMBER":"INTEGER", "STRING":"TEXT", "LOGICAL":"BOOLEAN"}

def type_extract(class_link):
                fp = urllib.request.urlopen(link + class_link)
                html_bytes = fp.read()
                html_str = html_bytes.decode("utf8")
                fp.close()
                html_class = html_str.split("*)")[1]
                html_class = html_class.split("END_TYPE")[0]
                html_class = html_class.replace("<A>", "")
                html_class = html_class.replace("</A>", "")
                html_class = html_class.replace("<B>", "")
                html_class = html_class.replace("</B>", "")
                html_class = html_class.replace("<PRE>", "")
                html_class = html_class.replace("</PRE>", "")
                name = html_class.split("\"")[1]
                name = name.replace("IFC4.", "")
                after_eq = html_class.split("=")[2]
                after_eq_arr = after_eq.strip().split(" ")
                after_eq = after_eq_arr[0]
                after_eq = after_eq.replace(";", "")
                after_eq = after_eq.split("(")[0]
                after_eq = after_eq.strip()
                if after_eq in simple:
                        return [name, simple[after_eq]]
                elif after_eq == "ARRAY":
                        array_type = after_eq_arr[3].strip().replace(";", "")
                        return [name, simple[array_type] + "[]"]
                elif after_eq == "<A":
                        class_link = (html_class.split("=")[3]).split("\'")[1]
                        parent_type = type_extract(class_link)
                        return [name, parent_type[1]]
                elif after_eq == "SET":
                        class_name = ((html_class.split("=")[3].split("<")[0]).split(">")[1]).replace(";", "").strip()
                        return [name, "SET_" + class_name]
                elif after_eq == "ENUMERATION":
                        html_class = html_class.replace("IFC4.", "")
                        names = html_class.split("\"")
                        names = names[3::2]
                        return [name, names]
                elif after_eq == "LIST":
                        if not (html_class.split("=")[2]).find("href") == -1:
                                class_name = ((html_class.split("=")[3].split("<")[0]).split(">")[1]).replace(";", "").strip()
                                return [name, "SET_" + class_name]
                        else:
                                array_type = after_eq_arr[3].strip().replace(";", "")
                                return [name, simple[array_type] + "[]"]
                elif after_eq == "SELECT":
                        return [name, "IfcRoot"]

def list_extractor(el):
        after_list = el.split(":")[2]
        if (not after_list.find("SET") == -1) or (not after_list.find("LIST") == -1):
                idx = el.find(":")
                list_type = list_extractor(el[idx + 1:])
        else:
             try:
                list_type = (after_list.split(">")[1]).strip()
             except:
                list_type = el.split(" ")[-1]
        return "SET_" + list_type

def entity_extract(class_link):
        fp = urllib.request.urlopen(link + class_link)
        html_bytes = fp.read()
        html_str = html_bytes.decode("utf8")
        fp.close()
        html_class = html_str.split("*)")[1]
        html_class = html_class.split("END_ENTITY")[0]
        html_class = html_class.replace("<A>", "")
        html_class = html_class.replace("</A>", "")
        html_class = html_class.replace("<B>", "")
        html_class = html_class.replace("</B>", "")
        html_class = html_class.replace("<PRE>", "")
        html_class = html_class.replace("</PRE>", "")
        html_class = html_class.replace("IFC4.", "")
        name = html_class.split("\"")[1]
        parent = None
        idx = html_class.find("SUBTYPE")
        if not idx == -1:
                parent = (html_class[idx:].split(">")[1]).split(")")[0]
        try:
                attributes_str = html_class.split(";")[1:]
        except:
                attributes_str = ""
        attributes = {}
        for el in attributes_str:
                if (not (el.find("WHERE") == -1 and el.find("INVERSE") == -1 and el.find("DERIVE") == -1)) or el.strip() == "":
                        break
                key = el.split("\"")[1]
                key = key.replace(name + ".", "")
                if (not el.find("SET") == -1) or (not el.find("LIST") == -1):
                    value = list_extractor(el)
                else:
                    try:
                            value = (el.split(">")[2]).strip()
                    except:
                            value = el.split(" ")[-1]
                attributes[key] = value
        return [name, parent, attributes]

def read_schemas():
        ifc_dict = {}
        fp = urllib.request.urlopen(link + "schema.html")
        html_bytes = fp.read()
        html_str = html_bytes.decode("utf8")
        fp.close()
        html_schema = html_str.split(";")
        possibilities = set(())
        i = 0
        for el in html_schema:
                i = i + 1
                if (i%10 == 0):
                        print (str(float(i/len(html_schema))*100.0) + "%")
                el = el.strip()
                if (el[:4] == "TYPE" and el.find("Enum") == -1 ):
                        class_link = el.split(r"'")[1]
                        key, value = type_extract(class_link)
                        ifc_dict[key] = value
                elif (el[:6] == "ENTITY"):
                        class_link = el.split(r"'")[1]
                        key, parent, attributes = entity_extract(class_link)
                        ifc_dict[key] = {"parent":parent, "attributes":attributes, "is_in_table":False}
        return ifc_dict
                        
                        
                        
            
                            
                            
                    
                    
                    
                    
        
				
