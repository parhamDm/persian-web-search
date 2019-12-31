import xlrd

workbook = xlrd.open_workbook("database/IR-F19-Project01-Input.xlsx")

def InstanciateExcel():
    global workbook
    loc = ("database/IR-F19-Project01-Input.xlsx")
    workbook = xlrd.open_workbook(loc)