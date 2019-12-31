import xlrd
class fileReader:
    def __init__(self,address):
        self.address = address
    def read_file(self):
        loc = (self.address)
        wb = xlrd.open_workbook(loc)
        sheet = wb.sheet_by_index(0)
        return sheet