import urllib.request

def read_schemas():
        ifc_dict = {}
        link = r"http://www.steptools.com/stds/ifc/html/"
        fp = urllib.request.urlopen(link + "schema.html")
        mybytes = fp.read()
        mystr = mybytes.decode("utf8")
        fp.close()
        array = mystr.split(";")
        for el in array:
            el = el.strip()
            if (el[:4] == "TYPE"):
                first_split = el.split(">")
                second_split = first_split[1].split("<")
                print(second_split[0])
