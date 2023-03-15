import pymorphy2


class BooleanSearch:

    def __init__(self):
        self.resourcesPath = '/Users/angelina/PycharmProjects/InfSearch/resources/'
        self.invertedIndexFile = open(self.resourcesPath + 'invertedIndex.txt', 'r')
        self.infinitiveIndex = self.getInfinitiveIndexArray()
        self.morph = pymorphy2.MorphAnalyzer()

    def getInfinitiveIndexArray(self):
        d = dict()
        lines = self.invertedIndexFile.readlines()
        for line in lines:
            strings = line.split('\n')[0].split(': ')
            k = strings[0]
            other = strings[1].strip().split(' ')
            d[k] = []
            for i in other:
                d[k].append(int(i))
        self.invertedIndexFile.close()
        return d

    def getInfinitive(self, q):
        wordInfo = self.morph.parse(q)[0]
        normalForm = wordInfo.normal_form if wordInfo.normalized.is_known else q.lower()
        return normalForm

    def getInfinitiveIndex(self, q):
        q = self.getInfinitive(q)
        if q in self.infinitiveIndex.keys():
            return self.infinitiveIndex[q]
        else:
            list()

    def __and__(self, q1, q2):
        v1 = self.getInfinitiveIndex(q1)
        v2 = self.getInfinitiveIndex(q2)
        res = list()
        for i in v1:
            if i in v2:
                res.append(i)
        return res

    def __or__(self, q1, q2):
        v1 = self.getInfinitiveIndex(q1)
        v2 = self.getInfinitiveIndex(q2)
        return set(v1 + v2)

    def __not__(self, q1, q2):
        v1 = self.getInfinitiveIndex(q1)
        v2 = self.getInfinitiveIndex(q2)
        for i in v1:
            if i in v2:
                v1.remove(i)
        return v1


if __name__ == '__main__':
    bs = BooleanSearch()
    print(bs.__and__('почта', 'технический'))
    print(bs.__or__('значительный', 'джуда'))
    print(bs.__not__('значительный', 'джуда'))
