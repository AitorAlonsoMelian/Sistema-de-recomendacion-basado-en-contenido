import argparse
from math import log
from tabulate import tabulate

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

for i in range(len(documents)):
    documents[i] = documents[i].replace("\n", "")
    documents[i] = documents[i].replace(",", "")
    documents[i] = documents[i].replace(".", "")
    documents[i] = documents[i].lower()

it = 0
for i in documents:
    # i = i.replace(",","")
    # i = i.replace(".","")
    # i = i.lower()
    terms.append([])
    for j in i.split():
        if ((exists(terms[it],j) == False) and (j not in stopwords)):
            terms[it].append(j)
    it = it+1

TF = []
IDF = []
it = 0
#print("TERMINOS\n")
for i in terms:
    TF.append([])
    IDF.append([])
    #print(i)
    for j in i:
        TF[it].append(documents[it].count(j))
        N = len(documents)
        dfx = 0
        for x in terms:
            if (exists(x,j)):
                dfx = dfx + 1
        IDF[it].append(round(log(N/dfx),3))
    it = it+1

#print("\nTF\n")
#print(TF)

#print("\nIDF\n")
#print(IDF)


tabla = []
for i in range(len(terms)):
    tabla.append(["Indice", "Termino", "TF", "IDF", "TF-IDF"])
    for j in range(len(terms[i])):
        tabla.append([j, terms[i][j], TF[i][j], IDF[i][j], TF[i][j] * IDF[i][j]])
    print("Tabla del Documento " + str(i))
    print(tabulate(tabla, headers="firstrow", tablefmt="fancy_grid"))
    tabla = []


#p = [t for t in terms if t not in stopwords]
