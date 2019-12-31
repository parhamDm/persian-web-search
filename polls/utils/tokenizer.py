import re
class Tokenizer:
    def __init__(self,text):
        self.text = text
    def remove_tags(self, text):
        TAG_RE = re.compile(r'<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});|[،.؛:()_\-@#{}\[\]!«»",]')
        return TAG_RE.sub(' ', text)
    def tokenize_word(self):
        clean_text = self.remove_tags(self.text)
        try:
            self.tokens = clean_text.split()
        except:
            print("error occured")
        return self.tokens