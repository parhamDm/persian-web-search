import xlrd
import csv
import collections


class Word:
    def __init__(self):
        print()


    def detect_charachters(self):
        loc = "database/IR-F19-Project01-Input.xlsx"
        wb = xlrd.open_workbook(loc)
        self.sheet = wb.sheet_by_index(0)
        self.characters = {}
        for i in range(0,1000) :
            for c in self.sheet.cell_value(i,5):
                if c in self.characters:
                    self.characters[c] = 1 + self.characters[c]
                else:
                    self.characters[c] =0
        self.characters = collections.OrderedDict(sorted(self.characters.items()))
        with open('dict.csv', 'w', newline="",encoding="utf8") as csv_file:
            writer = csv.writer(csv_file)
            for key, value in self.characters.items():
                writer.writerow([key, value,key.encode("unicode_escape")])

        print(self.characters)

    def read_map(self):
        with open('normalizer4.csv',encoding="utf8") as csv_file:
            reader = csv.reader(csv_file)
            self.mydict = dict(reader)
        print(self.mydict)

    def convert(self, string):
        stringBuffer = ""
        for s in string:
            if s in self.mydict:
                stringBuffer = stringBuffer + self.mydict[s]
        return stringBuffer