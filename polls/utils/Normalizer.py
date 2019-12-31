import re

from polls.utils.filereader import fileReader
from polls.utils.defaults import maketrans
from polls.utils.lemmatizer import Lemmatizer
from polls.utils.wordTokenizer import WordTokenizer


compile_patterns = lambda patterns: [(re.compile(pattern), repl) for pattern, repl in patterns]
class Normalize:
    def __init__(self, remove_extra_spaces=True, persian_style=True, persian_numbers=True, remove_diacritics=True,
                 affix_spacing=True, token_based=False, punctuation_spacing=True,twofaced_words= True):
        self._punctuation_spacing = punctuation_spacing
        self._affix_spacing = affix_spacing
        self._token_based = token_based
        self._twofaced_words= True

        translation_src, translation_dst = ' ىكي“”', ' یکی""'
        if persian_numbers:
            translation_src += '0123456789%'
            translation_dst += '۰۱۲۳۴۵۶۷۸۹٪'
        self.translations = maketrans(translation_src, translation_dst)

        if self._token_based:
            lemmatizer = Lemmatizer()
            self.words = lemmatizer.words
            self.verbs = lemmatizer.verbs
            self.tokenizer = WordTokenizer(join_verb_parts=False)
            self.suffixes = {'ی', 'ای', 'ها', 'های', 'تر', 'تری', 'ترین', 'گر', 'گری', 'ام', 'ات', 'اش'}

        self.character_refinement_patterns = []

        if remove_extra_spaces:
            self.character_refinement_patterns.extend([
                (r' +', ' '),  # remove extra spaces
                (r'\n\n+', '\n\n'),  # remove extra newlines
                (r'[ـ\r]', ''),  # remove keshide, carriage returns
            ])

        if persian_style:
            self.character_refinement_patterns.extend([
                ('([\d+])\.([\d+])', r'\1٫\2'),  # replace dot with momayez
                (r' ?\.\.\.', ' …'),  # replace 3 dots
            ])

        if remove_diacritics:
            self.character_refinement_patterns.append(
                ('[\u064B\u064C\u064D\u064E\u064F\u0650\u0651\u0652]', ''),
                # remove FATHATAN, DAMMATAN, KASRATAN, FATHA, DAMMA, KASRA, SHADDA, SUKUN
            )

        self.character_refinement_patterns = compile_patterns(self.character_refinement_patterns)

        punc_after, punc_before = r'\.:!،؛؟»\]\)\}', r'«\[\(\{'
        if punctuation_spacing:
            self.punctuation_spacing_patterns = compile_patterns([
                ('" ([^\n"]+) "', r'"\1"'),  # remove space before and after quotation
                (' ([' + punc_after + '])', r'\1'),  # remove space before
                ('([' + punc_before + ']) ', r'\1'),  # remove space after
                ('([' + punc_after[:3] + '])([^ ' + punc_after + '\d۰۱۲۳۴۵۶۷۸۹])', r'\1 \2'),  # put space after . and :
                ('([' + punc_after[3:] + '])([^ ' + punc_after + '])', r'\1 \2'),  # put space after
                ('([^ ' + punc_before + '])([' + punc_before + '])', r'\1 \2'),  # put space before
            ])

        if affix_spacing:
            self.affix_spacing_patterns = compile_patterns([
                (r'([^ ]ه) ی ', r'\1‌ی '),  # fix ی space
                (r'(^| )(ن?می) ', r'\1\2‌'),  # put zwnj after می, نمی
                (
                r'(?<=[^\n\d ' + punc_after + punc_before + ']{2}) (تر(ین?)?|گری?|های?)(?=[ \n' + punc_after + punc_before + ']|$)',
                r'‌\1'),  # put zwnj before تر, تری, ترین, گر, گری, ها, های
                (r'([^ ]ه) (ا(م|یم|ش|ند|ی|ید|ت))(?=[ \n' + punc_after + ']|$)', r'\1‌\2'),
                # join ام, ایم, اش, اند, ای, اید, ات
            ])

    def normalize(self, text):
        text = self.character_refinement(text)
        if self._affix_spacing:
            text = self.affix_spacing(text)

        if self._token_based:
            tokens = self.tokenizer.tokenize(text.translate(self.translations))
            text = ' '.join(self.token_spacing(tokens))

        if self._punctuation_spacing:
            text = self.punctuation_spacing(text)
        if self._twofaced_words:
            text = self.twofaced(text)

        return text

    def twofaced(self,text):
        f = fileReader("database/twoface.xlsx")
        sheet = f.read_file()
        for i in range(sheet.nrows):
            if sheet.cell_value(i,1) in text:
                text = text.replace(sheet.cell_value(i,1),sheet.cell_value(i,0))
        return text
    def character_refinement(self, text):

        text = text.translate(self.translations)
        for pattern, repl in self.character_refinement_patterns:
            text = pattern.sub(repl, text)
        return text

    def punctuation_spacing(self, text):

        for pattern, repl in self.punctuation_spacing_patterns:
            text = pattern.sub(repl, text)
        return text

    def affix_spacing(self, text):

        for pattern, repl in self.affix_spacing_patterns:
            text = pattern.sub(repl, text)
        return text

    def token_spacing(self, tokens):

        result = []
        for t, token in enumerate(tokens):
            joined = False

            if result:
                token_pair = result[-1] + '‌' + token
                if token_pair in self.verbs or token_pair in self.words and self.words[token_pair][0] > 0:
                    joined = True

                    if t < len(tokens) - 1 and token + '_' + tokens[t + 1] in self.verbs:
                        joined = False

                elif token in self.suffixes and result[-1] in self.words:
                    joined = True

            if joined:
                result.pop()
                result.append(token_pair)
            else:
                result.append(token)

        return result
    # def detect_characters(self):
    #     loc = "database/IR-F19-Project01-Input.xlsx"
    #     wb = xlrd.open_workbook(loc)
    #     self.sheet = wb.sheet_by_index(0)
    #     self.characters = {}
    #     for i in range(0,1000) :
    #         for c in self.sheet.cell_value(i,5):
    #             if c in self.characters:
    #                 self.characters[c] = 1 + self.characters[c]
    #             else:
    #                 self.characters[c] =0
    #     self.characters = collections.OrderedDict(sorted(self.characters.items()))
    #     with open('dict.csv', 'w', newline="",encoding="utf8") as csv_file:
    #         writer = csv.writer(csv_file)
    #         for key, value in self.characters.items():
    #             writer.writerow([key, value,key.encode("unicode_escape")])
    #
    #     print(self.characters)
    #
    # def read_map(self):
    #     with open('normalizer4.csv',encoding="utf8") as csv_file:
    #         reader = csv.reader(csv_file)
    #         self.mydict = dict(reader)
    #     # print(self.mydict)
    #
    # def convert(self, string):
    #     self.read_map()
    #     stringBuffer = ""
    #     for s in string:
    #         if s in self.mydict:
    #             stringBuffer = stringBuffer + self.mydict[s]
    #     return stringBuffer
