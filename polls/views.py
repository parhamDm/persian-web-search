from django.http import HttpResponse, Http404
from django.shortcuts import render
import xlrd
# Create your views here.
from polls.models.News import News
from polls.utils.Getlist import get_list
from polls.utils.Search import Search
from polls.utils.Indexer import Index
from polls.utils.Normalizer import Normalize
from polls.utils.tfidf import TfIdf
from polls.utils.global_excel import workbook
page_size = 300


def index(request):
    return render(request, 'index.html')


def search(request):
    # Reading an excel file using Python
    query = request.GET["q"]
    page_number = int(request.GET["page_number"])
    # Give the location of the file
    loc = ("polls/IR-F19-Project01-Input.xlsx")

    i = Index("database/IR-F19-Project01-Input.xlsx", "database/stopwords.xlsx", 'database/dictionary.txt')
    s = Search(query)
    index_list = i.process(s.tokens)
    tfidf = TfIdf()

    word_list = s.tokenize_by_word()
    index_list = tfidf.get_similarity_list(word_list, index_list)
    # To open Workbook
    sheet = workbook.sheet_by_index(0)

    # For row 0 and column 0
    sheet.cell_value(0, 0)

    # if (page_number)*page_size >= len(index_list):
    #     raise Http404("Question does not exist")
    list = get_list(index_list, s.tokens)
    # """-1 if (page_number+1)*page_size >= len(index_list)-1 else"""
    # lastIndex = (page_number+1)*page_size
    # page_count =  len(index_list)/page_size + 1
    # start = page_number + 1 if page_number >= 1 else page_number
    # current = page_number + 1
    # end = page_number + 2 if page_number + 2 !=lastIndex else page_number+1
    # return render(request, 'search.html', {'list': list[page_number*page_size:lastIndex]
    #                                        ,'range':range(start,end)
    #                                        ,'current':current})
    return render(request, 'search.html', {'list': list})


def news(request):
    id = request.GET["id"]
    item = get_list([int(id)], [])[0]
    return render(request, 'news.html', {'item': item})


def getChars(request):
    # charGeneralizer = Word()
    # charGeneralizer.read_map()
    # charGeneralizer.convert("خانه‌ها")
    tfidf = TfIdf()
    # list = tfidf.get_tfidf(['جعفر', 'پناهی', 'نیا', 'محمدی'])
    tfidf.index()
    return "Sss"
