import shlex
import re

from polls.utils.Normalizer import Normalize
from polls.utils.lemmatizer import Lemmatizer


class Search:

    def __init__(self, query):
        self.query = query
        self.tokenize()

    def tokenize(self):
        lemmatizer = Lemmatizer()
        normalizer = Normalize(punctuation_spacing=False)
        TAG_RE = re.compile(r'[,\.?\'،\\\]\[؛ًٌ]')
        self.query = TAG_RE.sub(' ', self.query)
        self.query = normalizer.normalize(self.query)
        self.tokens = shlex.split(self.query)
        for i in range(len(self.tokens)):
            print(self.tokens[i])
            if self.tokens[i][0] == '!':
                self.tokens[i] = '!' + lemmatizer.lemmatize(self.tokens[i][1:])
            if ' ' in self.tokens[i]:
                sent = self.tokens[i].split()
                for j in range(len(sent)):
                    sent[j] = lemmatizer.lemmatize(sent[j])
                self.tokens[i] = ' '.join(sent)
            else:
                self.tokens[i] = lemmatizer.lemmatize(self.tokens[i])
        return self.tokens

    def tokenize_by_word(self):
        lemmatizer = Lemmatizer()
        normalizer = Normalize()
        TAG_RE = re.compile(r'[,\.?\"\'،\\\]\[؛ًٌ]')
        self.query = TAG_RE.sub(' ', self.query)
        self.query = normalizer.normalize(self.query)
        self.tokens = shlex.split(self.query)
        for i in range(len(self.tokens)):
            self.tokens[i] = lemmatizer.lemmatize(self.tokens[i])
        return self.tokens
s = Search('"شهادت حضرت رقیه"')
print(s.tokenize())