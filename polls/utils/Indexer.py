import xlrd
import re
import ast
from pathlib import Path

from .tokenizer import Tokenizer
from .lemmatizer import Lemmatizer
from .word import Word
from .Normalizer import Normalize
from .wordTokenizer import WordTokenizer


class Index:
    content_index = 5
    doc_count = 10

    def read_file(self, address):
        loc = (address)
        wb = xlrd.open_workbook(loc)
        self.sheet = wb.sheet_by_index(0)
        self.doc_count = self.sheet.nrows - 1
        # for i in range(sheet.ncols):
        #     print(sheet.cell_value(0, 0))
        # print(sheet.ncols)

    def intersection(self, l1, l2):
        return [val for val in l1 if val in l2]

    def find_freq(self, token, index):
        for w in self.word_index:
            if w.word == token and index in w.index:
                return w.freq[w.index.index(index)]
        return -1

    def find_pos(self, token, index):
        for w in self.word_index:
            if w.word == token and index in w.index:
                return w.position[w.index.index(index)]
        return []

    def find_text(self, text):
        index_list = []
        freq_list = []
        for i in range(len(self.word_index)):
            try:
                if self.word_index[i].word == text:
                    index_list = self.word_index[i].index
                    break
            except:
                print("error!")
        return index_list

    def find_not_text(self, text):
        text = text[1:]
        list = [x for x in range(1, self.doc_count)]
        not_list = []
        for i in range(len(self.word_index)):
            try:
                if self.word_index[i].word == text:
                    not_list = self.word_index[i].index
            except:
                print("error!")
        for i in not_list:
            if i in list:
                list.remove(i)
        return list

    def find_specified_text(self, text):
        tokens = text.split()
        # print(tokens)
        index_list = []
        freq_list = []
        position_list = []
        # print(tokens)
        for x in range(len(tokens)):
            for i in range(len(self.word_index)):
                if self.word_index[i].word == tokens[x]:
                    index_list.append(self.word_index[i].index)
                    freq_list.append(self.word_index[i].freq)
                    position_list.append(self.word_index[i].position)
                    break
        index_list = list(set.intersection(*map(set, index_list)))

        freq_list = []
        position_list = []
        # print(index_list)
        for token in tokens:
            freq_list.append([])
            position_list.append([])
            for i in index_list:
                freq_list[-1].append(self.find_freq(token, i))
                position_list[-1].append(self.find_pos(token, i))
        # print(position_list)
        for i in range(1, len(position_list)):
            l = position_list[i]
            # print(l)
            for k in range(len(l)):
                for j in range(len(l[k])):
                    l[k][j] -= 1
            for k in range(len(l)):
                for j in range(len(l[k])):
                    if l[k][j] not in position_list[i - 1][k]:
                        index_list[k] = -index_list[k]
                    elif index_list[k] < 0 :
                        index_list[k] = -index_list[k]
        index_list = [value for value in index_list if value > 0]
        index_list.sort()
        # print(index_list)
        return index_list

    def index_from_file(self, path):
        with open(path, encoding='utf-8') as f:
            first_line = f.readline()[:-1]
            while first_line != '':
                w = Word()
                try:
                    w.addFromFile(first_line, ast.literal_eval(f.readline()[:-1]), ast.literal_eval(f.readline()[:-1]),
                                  ast.literal_eval(f.readline()[:-1]))
                except:
                    #todo fix error!
                    print("An exception occurred")
                    # print(w)
                self.word_index.append(w)
                first_line = f.readline()[:-1]
    def remove_tags(self, text):
        TAG_RE = re.compile(r'<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});|[،.؛:()_\-@#{}\[\]!«»",]')
        return TAG_RE.sub(' ', text)

    def index(self, path):
        list = []
        normalizer = Normalize()
        lemmatizer = Lemmatizer()
        tokenizer = WordTokenizer(join_verb_parts=True)

        for i in range(1, self.sheet.nrows):  # ):
            content = self.sheet.cell_value(i, self.content_index)
            content = self.remove_tags(content)
            content = normalizer.normalize(content)
            content_tokens = tokenizer.tokenize(content)

            print(i)
            for j in range(len(content_tokens)):
                if content_tokens[j] == 'ها' or content_tokens[j] == 'می':
                    continue
                #print('this can be: ' + content_tokens[j])
                content_tokens[j] = lemmatizer.lemmatize(content_tokens[j])
                #print('this cannot be: ' + content_tokens[j])
                try:
                    li = list.index(content_tokens[j])
                except ValueError:
                    li = -1
                if li > -1:
                    self.word_index[li].add_to_index(i, j)
                elif content_tokens[j] not in self.stopwords:
                    w = Word()
                    w.addNewWord(content_tokens[j], i, j)
                    self.word_index.append(w)
                    list.append(content_tokens[j])
        self.save_to_file(path)

    def process(self, tokens):
        indexes = []
        for x in tokens:
            if x[0:4] == 'cat:':
                print('cat')
                continue
            if x[0:4] == 'url:':
                print('url')
                continue
            if x[0:7] == 'source:':
                print('source')
                continue
            if x[0] == '!':
                indexes.append(self.find_not_text(x))
                continue
            if ' ' in x:
                indexes.append(self.find_specified_text(x))
            else:
                indexes.append(self.find_text(x))
        return list(set.intersection(*map(set, indexes)))
        # print(indexes)
        # print(list(set.intersection(*map(set,indexes))))

    def print_list(self):
        for i in self.word_index:
            print('word: ' + i.word)
            print(i.index)
            print(i.freq)
            print(i.position)

    def read_stopwords(self, address):
        loc = (address)
        wb = xlrd.open_workbook(loc)
        stopwords_sheet = wb.sheet_by_index(0)
        for i in range(stopwords_sheet.nrows):
            self.stopwords.append(stopwords_sheet.cell_value(i, 0))

    def save_to_file(self, path):
        with open(path, 'w', encoding="utf-8") as f:
            for item in self.word_index:
                f.write("%s\n" % item.word)
                f.write("%s\n" % item.index)
                f.write("%s\n" % item.freq)
                f.write("%s\n" % item.position)

    def __init__(self, address, stopword_address, destPath):
        self.stopwords = []
        self.read_stopwords(stopword_address)
        self.word_index = []
        if not (Path(destPath).is_file()):
            self.read_file(address)
            self.index(destPath)
        self.index_from_file(destPath)
