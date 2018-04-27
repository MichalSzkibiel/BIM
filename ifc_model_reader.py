import urllib.request

def read_schemas():
        ifc_dict = {}
        link = r"http://www.steptools.com/stds/ifc/html/"
        fp = urllib.request.urlopen(link + "schema.html")
        html_bytes = fp.read()
        html_str = html_bytes.decode("utf8")
        fp.close()
        html_schema = html_str.split(";")
        for el in html_schema:
            el = el.strip()
            if (el[:4] == "TYPE" or el[:6] == "ENTITY"):
                    class_link = el.split(r"'")[1]
                    fp = urllib.request.urlopen(link + class_link)
                    html_bytes = fp.read()
                    html_str = html_bytes.decode("utf8")
                    fp.close()
                    html_class = html_str.split("*)")
        
				
