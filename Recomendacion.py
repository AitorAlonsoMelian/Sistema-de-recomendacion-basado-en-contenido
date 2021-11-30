import argparse

def exists(array, target):
    for x in array:
        if (x == target):
            return True
    return False

parser = argparse.ArgumentParser(description="Programa de sistemas de recomendación")

parser.add_argument('file', type=argparse.FileType('r'))

args = parser.parse_args()

documents = args.file.readlines()
terms = []
stopwords = []
s = open("stopwords.txt", 'r')

for i in s.readlines():
    i = i.replace("\n","")
    if (exists(stopwords,i) == False):
        stopwords.append(i)

for i in documents:
    i = i.replace(",","")
    i = i.replace(".","")
    i = i.lower()
    for j in i.split():
        if (exists(terms,j) == False):
            terms.append(j)

p = [t for t in terms if t not in stopwords]

#print(p)
#print(terms)


