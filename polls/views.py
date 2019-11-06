from django.http import HttpResponse, Http404
from django.shortcuts import render
import xlrd
# Create your views here.
from polls.models.News import News
from polls.utils.Getlist import get_list

page_size = 300


def index(request):
    return render(request, 'index.html')


def search(request):
    # Reading an excel file using Python
    query = request.GET["query"]
    page_number = int(request.GET["page_number"])
    # Give the location of the file
    loc = ("polls/IR-F19-Project01-Input.xlsx")

    # To open Workbook
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)

    # For row 0 and column 0
    sheet.cell_value(0, 0)

    # put index list here!
    index_list = [12, 3, 2, 41,4]
    if (page_number)*page_size >= len(index_list):
        raise Http404("Question does not exist")
    list = get_list(index_list)
    """-1 if (page_number+1)*page_size >= len(index_list)-1 else"""
    lastIndex = (page_number+1)*page_size
    page_count =  len(index_list)/page_size + 1
    start = page_number + 1 if page_number >= 1 else page_number
    current = page_number + 1
    end = page_number + 2 if page_number + 2 !=lastIndex else page_number+1
    return render(request, 'search.html', {'list': list[page_number*page_size:lastIndex]
                                           ,'range':range(start,end)
                                           ,'current':current})
