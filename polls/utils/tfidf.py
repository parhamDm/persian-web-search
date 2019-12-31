import collections
import heapq
import json
import pickle
from math import log

import norm
import numpy as np
import xlrd
import re

from polls.utils.Normalizer import Normalize
from polls.utils.global_excel import workbook
from polls.utils.Indexer import Index
from polls.utils.lemmatizer import Lemmatizer
from polls.utils.wordTokenizer import WordTokenizer


class TfIdf:

    def __init__(self):
        self.wb = workbook
        self.sheet = self.wb.sheet_by_index(0)
        self.doc_count = self.sheet.nrows

    def index(self):
        global content_tokens
        doc_list = []
        idf = {}
        lemmatizer = Lemmatizer()
        normalizer = Normalize()
        tokenizer = WordTokenizer(join_verb_parts=True)

        list = []
        for i in range(1, self.sheet.nrows):  # self.sheet.nrows):
            print(i)
            content = self.sheet.cell_value(i, 5)
            content = self.remove_tags(content)
            content = normalizer.normalize(content)
            content_tokens = tokenizer.tokenize(content)
            try:
                content_tokens = content.split()
                tf = {}

            except:
                print("error occured")
            # print(content_tokens)
            for j in content_tokens:
                if j == 'ها' or j == 'می':
                    continue
                    # print('this can be: ' + content_tokens[j])
                j = lemmatizer.lemmatize(j)
                #j = normalizer.convert(j)
                # print('this cannot be: ' + content_tokens[j])
                if (j in idf) and (j not in tf):
                    idf[j] += 1
                elif (j not in tf):
                    idf[j] = 1

                if j in tf:
                    tf[j] += 1
                else:
                    tf[j] = 1

            tf = collections.OrderedDict(sorted(tf.items()))
            doc_list.append(tf)

        for doc in doc_list:
            for tf in doc:
                doc[tf] = (1 + log(doc[tf],10)) * log(self.doc_count / idf[tf],10)

        with open('database/tfidf.json', 'w', encoding="utf8") as f:
            json.dump(doc_list, f)
        with open('database/wordfreq.pkl', 'wb') as f:
            pickle.dump(idf, f,pickle.HIGHEST_PROTOCOL)

    def remove_tags(self, text):
        TAG_RE = re.compile(r'<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});|[،.؛:()_\-@#{}\[\]!«»",]')
        return TAG_RE.sub(' ', text)

    def read_from_file(self):
        # with open('database/tfidf.txt',encoding="utf8") as f:
        #     lines = collections.OrderedDict(f.readlines())
        # return (lines)
        list = []
        with open('database/tfidf.json', encoding="utf8") as fp:
            data = json.load(fp)
        return data

    def get_similarity_list(self, list_of_words, list_of_docs):
        data = self.read_from_file()
        list_of_similarities = []
        tfidf_input = self.get_tfidf(list_of_words)
        # every doc
        for i in range(len(list_of_docs)):
            # document i
            sum = 0
            j =list_of_docs[i] - 1
            document_tfidf = data[list_of_docs[i] - 1]
            for item in list_of_words:
                if item in document_tfidf and item in tfidf_input:
                    sum += document_tfidf[item]*tfidf_input[item]
            sum = sum/(np.linalg.norm(list(document_tfidf.values())))
            list_of_similarities.append(DocSum(list_of_docs[i], sum))
        heapq.heapify(list_of_similarities)
        list_of_similarities = heapq.nlargest(20, list_of_similarities)
        return_list =[]
        for item in list_of_similarities:
            return_list.append(item.docId)
        return return_list


    def get_tfidf(self,list_words):
        tf ={}
        for j in list_words:
            if j in tf:
                tf[j] += 1
            else:
                tf[j] = 1

        with open('database/wordfreq.pkl','rb') as f:
            idf = pickle.load(f)
        for i in tf:
            if i in idf:
                tf[i] = (1 + log(tf[i],10)) * log( self.doc_count / idf[i],10)
        return tf

class DocSum:
    def __init__(self, docId, sum):
        self.docId = docId
        self.sum = sum

    def __lt__(self, other):
        return self.sum < other.sum
