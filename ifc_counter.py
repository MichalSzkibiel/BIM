import redis
import pymongo

class ifc_counter:
    #Klasa wczytujaca plik .ifc i przechowujaca funkcje do zadan 
    def __init__(self, fileIFC, fileAttr = ""):
        #Otwarcie pliku .ifc i podzial na pojedyncze linijki
        stream = open(fileIFC, 'r')
        self.lines = stream.readlines()
        #Przyciecie poczatkowych i koncowych bialych znakow
        for i in self.lines:
            i = i.strip()
        #Jesli nie podano pliku z nazwami atrybutow, to konstruktor konczy dzialanie
        if fileAttr == "":
            return
        #Wczytanie pliku z nazwami atrybutow i podzial na linijki
        stream = open(fileAttr, 'r')
        linesAttr = stream.readlines()
        #Uzupelnianie slownika
        self.attr_dict = {}
        for i in linesAttr:
             #Podzial, przed dwukropkiem sa nazwy klas, po sa nazwy atrybutow
             firstDiv = i.split(':')
             #Atrybuty sa wymienione od przecinka
             secDiv = firstDiv[1].split(',')
             #Uzupelnianie tabeli atrybutow
             attr_array = []
             for attr in secDiv:
                 attr_array.append(attr.strip())
             #Przypisanie tabeli do nazwy klasy
             self.attr_dict[firstDiv[0].strip()] = attr_array
    def count(self):
        #Funkcja zliczajaca obiekty, czyli wszystkie linie zaczynajace sie od "#"
        sum = 0
        for i in self.lines:
            if i[0] == "#":
                sum += 1
        return sum
    def class_extract(self, i):
        #Funkcja, ktora z definicji obiektu wyciaga nazwe klasy obiektu, czyli wszystko pomiedzy pierwszym "I", a "("
        beg = 0
        while i[beg] != "I":
           beg += 1
        end = beg
        while i[end] != "(":
            end += 1
        return i[beg:end].strip()
    def count_class(self, token):
        #Funkcja zliczajaca obiekty typu "token"
        sum = 0
        for i in self.lines:
            if i[0] == "#":
               line_class = self.class_extract(i)
               if line_class == token:
                   sum += 1
        return sum
    def class_lister(self):
        #Funkcja zapisujaca wykorzystane w modelu klasy obiektow
        #Struktura danych set przechowuje unikalne wartosci
        list = set()
        for i in self.lines:
            if i[0] == "#":
               line_class = self.class_extract(i)
               list.add(line_class)
        #Sortowanie przed zwroceniem
        list = sorted(list)
        return list
    def count_all_class(self):
        #Funkcja zliczajaca wystapienia wszystkich uzytych klas obiektow
        #Struktura danych dict przechowuje dane klucz:wartosc, klasa:liczba
        sums = dict()
        for i in self.lines:
             if i[0] == "#":
               line_class = self.class_extract(i)
               if line_class in sums:
                   sums[line_class] += 1
               else:
                   sums[line_class] = 1
        return sums
    def redis_writer(self, db):
        #Funkcja zapisujaca dane do bazy danych w srodowisku redis
        for i in self.lines:
            #Pominiecie linijek bez "#" na poczatku
            if i[0] != "#":
                continue
            #Podzial linijki na klucz i wartosc wedlug znaku rownosci
            keyend = 0
            while i[keyend] != '=':
                keyend += 1
            ifcobjectkey = i[:keyend].strip()
            #Na koncu linijki jest niepotrzebny srednik
            ifcobjectval = i[keyend + 1:len(i) - 1].strip()
            db.set(ifcobjectkey, ifcobjectval)
        #Zwraca rozmiar bazy danych
        return db.dbsize()
    def keyfinder(self, key):
        #Funkcja znajdujaca klucz w pliku tekstowym
		#Zwraca wartosc pod kluczem albo nic jezeli klucza nie ma
        for i in self.lines:
            m = len(key)
            if i[:m] == key and (i[m] == "=" or i[m] == " "):
                while i[m] != "=":
                    m += 1
                return i[m + 1:].strip()[:-1]
        return None

    def strToArray(self, i):
        #Funkcja konwertujaca string na tabele
        it = 1
        values = []
        
        while i[it] != ')':
                 #Wyciaganie atrybutu
                 arr = self.atribute_extractor(i, it)
                 #Dopisane do tabeli szykowanej do json_generatora
                 it2 = arr[0]
                 typ = arr[1]
                 values.append([i[it:it2], typ])
                 it = it2 + 1
                 if i[it2] == ')':
                     break
        #uzycie json_generatora do przypisania wartosci do wyjsciowej tabeli
        json = self.json_generator(values, 0)
        array = list(json.values())
        return array
  
    def json_generator(self, values, begVals = 2):
        #Funkcja, ktora tworzy slownik za pomoca tabeli o formacie [string, typ]
        #Przypadek klasy niezaleznej
        if begVals == 2:
             json = {'ifcId': values[0][0],
                     'ifcClass': values[1][0]}
        #Przypadek klasy niezaleznej
        elif begVals == 1:
             json = {'ifcClass': values[0][0]}
        #Przypadek tabeli
        else:
             json = {}
        #Ustalenie nazw atrybutow
        attr_names = []
        #Gdy klasa widnieje w slowniku atrybutow, to pobierane sa nazwy atrybutow ze slownika
        if begVals > 0 and json['ifcClass'] in self.attr_dict:
             attr_names = self.attr_dict[json['ifcClass']]
        #W przeciwnym razie atrybuty sa generowane automatycznie
        else:
            for i in range(begVals, len(values)):
                attr_names.append('Atr' + str(i - begVals + 1))
        num = 0 
        for i in values[begVals:]:
           #Przypadek numeryczny
           if i[1] == "int":
               json[attr_names[num]] = float(i[0])
           #Przypadek stringa
           elif i[1] == "string":
               json[attr_names[num]] = i[0].strip().replace('\'', '')
           #Przypadek tabeli, uruchomienie konwersji na tabele
           elif i[1] == "array":
               json[attr_names[num]] = self.strToArray(i[0])
           #Przypadek klasy zaleznej
           elif i[1] == "class":
               #Ekstrakcja nazwy klasy
               values = [[self.class_extract(i[0]), 'string']]
               it = 0
               #Dojscie do nawiasu otwierajacego
               while i[0][it] != "(":
                  it += 1
               it += 1
               while i[0][it] != ')':
                 #Ekstrakcja atrybutu
                 it2, typ = self.atribute_extractor(i[0], it)
                 values.append([i[0][it:it2], typ])
                 it = it2 + 1
                 if i[0][it2] == ')':
                     break
               #Generacja jsona
               json[attr_names[num]] = self.json_generator(values, 1)
               
           num += 1
        return json

    def atribute_extractor(self, line, it):
        #Funkcja wyciagajaca wartosc atrybutu zaczyhajacego sie na pozycji it
        array_deg = 0
        string = False
        typ = "string"
        for i in range(it, len(line)):
            #Jesli jestesmy poza stringiem, poza tablica i natrafiamy na przecinek lub nawias
            if array_deg == 0 and not string and (line[i] == ',' or line[i] == ')'):
                    #Sprawdzamy, czy atrybut jest liczba
                    try:
                        float(line[it:i])
                        typ = "int"
                    except:
                        pass
                    return list((i, typ))
            #Jesli natrafia na pojedynczy cudzyslow, przelaczenie stringa
            elif line[i] == '\'':
               string = not string
            #Jesli jestesmy poza stringiem i natrafiamy na nawias otwierajacy
            elif not string and line[i] == '(':
               #Zwiekszamy stopien tablicy
               array_deg += 1
               #Jesli to pierwszy napotkany znak, to typ tabela
               if it == i:
                    typ = "array"
               #Jesli nie, i nie jest to juz tabela, to typ klasa
               elif typ != "array":
                    typ = "class"
            #Jak jestesmy poza stringiem, i napotykamy nawias zamykajacy, zmniejszamy stopien tabeli
            elif not string and line[i] == ')':
               array_deg -= 1
        #Zwrot wartosci, gdy nie uda sie znalezc konca
        return [it, "string"]
          

    def json_getter(self):
         json = []
         for i in self.lines:
            #Pominiecie linijek bez "#" na poczatku
            if i[0] != "#":
                continue
            #Podzial linijki na klucz i wartosc wedlug znaku rownosci
            it = 0
            while i[it] != '=':
                it += 1
            #Zainicjowanie tabeli do json_generatora
            values = [[i[:it].strip(), "string"], [self.class_extract(i), "string"]]
            #Dojscie do nawiasu otwierajacego
            while i[it] != '(':
                it += 1
            it += 1
            while i[it] != ')':
                 #Ekstrakcja atrybutu
                 arr = self.atribute_extractor(i, it)
                 it2 = arr[0]
                 typ = arr[1]
                 values.append([i[it:it2], typ])
                 it = it2 + 1
                 if i[it2] == ')':
                     break
            #Generacja jsona
            json.append(self.json_generator(values))
         #Zwraca rozmiar bazy danych
         return json