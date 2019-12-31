import shlex
import re

from polls.utils.Normalizer import Normalize
from polls.utils.lemmatizer import Lemmatizer


class Search:

    def __init__(self, query):
        self.query = query
        self.tokens = self.tokenize()

    def tokenize(self):
        lemmatizer = Lemmatizer()
        normalizer = Normalize()
        TAG_RE = re.compile(r'[,\.!?\'،\\\]\[؛ًٌ]')
        self.query = TAG_RE.sub(' ', self.query)
        self.query = normalizer.normalize(self.query)
        self.tokens = shlex.split(self.query)
        for i in range(len(self.tokens)):
            self.tokens[i] = lemmatizer.lemmatize(self.tokens[i])
        return self.tokens

    def tokenize_by_word(self):
        lemmatizer = Lemmatizer()
        normalizer = Normalize()
        TAG_RE = re.compile(r'[,\.!?\"\'،\\\]\[؛ًٌ]')
        self.query = TAG_RE.sub(' ', self.query)
        self.query = normalizer.normalize(self.query)
        self.tokens = shlex.split(self.query)
        for i in range(len(self.tokens)):
            self.tokens[i] = lemmatizer.lemmatize(self.tokens[i])
        return self.tokens