import xlrd

from polls.models.News import News


def get_list(indexList,tokens):
    loc = ("polls/IR-F19-Project01-Input.xlsx")

    # To open Workbook
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)

    # For row 0 and column 0
    sheet.cell_value(0, 0)

    list = []

    for i in indexList:
        news = News()
        news.id = i

        news.publish_date = sheet.cell_value(i, 0)
        news.title = sheet.cell_value(i, 1)
        news.url = sheet.cell_value(i, 2)
        news.summery = sheet.cell_value(i, 3)
        news.meta_tags = sheet.cell_value(i, 4)
        news.content = sheet.cell_value(i, 5)
        news.thumbnail = sheet.cell_value(i, 6)
        list.append(news)
    return list


