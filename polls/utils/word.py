class Word:
    def addNewWord(self, word, index, position):
        self.word = word
        self.index = [index]
        self.freq = [1]
        self.position = [[position]]

    def addFromFile(self, word, index, freq, position):
        self.word = word
        self.index = index
        self.freq = freq
        self.position = position

    def add_to_index(self, index, position):
        if (index not in self.index):
            self.index.append(index)
            self.freq.append(1)
            self.position.append([position])
        else:
            i = self.index.index(index)
            self.position[i].append(position)
            self.freq[i] += 1
        self.freq = [x for (y, x) in sorted(zip(self.index, self.freq), key=lambda pair: pair[0])]
        self.position = [x for (y, x) in sorted(zip(self.index, self.position), key=lambda pair: pair[0])]
        self.index = [y for y in sorted(self.index)]