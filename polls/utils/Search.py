import shlex


class Search:

    def __init__(self, query):
        self.query = query
        self.tokenize()

    def tokenize(self):
        self.tokens = shlex.split(self.query)
        return self.tokens
