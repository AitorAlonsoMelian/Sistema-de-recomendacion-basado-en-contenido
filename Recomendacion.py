import argparse
from math import log10, sqrt
from tabulate import tabulate
import sys

def exists(array, target):
    for x in array:
        if (x == target):
            return True
    return False

def sim(documento1, documento2, TFIDF, index1, index2):
    equals = []
    num = 0
    den1 = 0
    den2 = 0
    for i in range(len(documento1)):
        for j in range(len(documento2)):
            if ((documento1[i] == documento2[j]) and (exists(equals, documento1[i]) == False)):
                num = num + (TFIDF[index1][i] * TFIDF[index2][j])
    
    for i in range(len(documento1)):
        den1 = den1 + (TFIDF[index1][i])**2
    for i in range(len(documento2)):
        den2 = den2 + (TFIDF[index2][i])**2    

    result = round(num/(sqrt(den1) * sqrt(den2)),3)

    return result

parser = argparse.ArgumentParser(description="Programa de sistemas de recomendación")
parser.add_argument('file', type=argparse.FileType('r'))
parser.add_argument('-o', '--out', type=argparse.FileType('w', encoding='utf-8'))
args = parser.parse_args()
documents = args.file.readlines()

if args.out is not None:
    sys.stdout = args.out


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
    terms.append([])
    for j in i.split():
        if ((exists(terms[it],j) == False) and (j not in stopwords)):
            terms[it].append(j)
    it = it+1

TF = []
IDF = []
TFIDF = []
it = 0
for i in terms:
    TF.append([])
    IDF.append([])
    TFIDF.append([])
    it2 = 0
    for j in i:
        TF[it].append(documents[it].count(j))
        N = len(documents)
        dfx = 0
        for x in terms:
            if (exists(x,j)):
                dfx = dfx + 1
        IDF[it].append(round(log10(N/dfx),3))
        TFIDF[it].append(TF[it][it2] * IDF[it][it2])
        it2 = it2 + 1
    it = it+1

tabla = []
for i in range(len(terms)):
    tabla.append(["Indice", "Termino", "TF", "IDF", "TF-IDF"])
    for j in range(len(terms[i])):
        tabla.append([j, terms[i][j], TF[i][j], IDF[i][j], TFIDF[i][j]])
    print("Tabla del Documento " + str(i))
    print(tabulate(tabla, headers="firstrow", tablefmt="fancy_grid"))
    tabla = []

sim_matrix = []
for i in range(len(terms)):
    sim_matrix.append([])
    sim_matrix[i].append("Documento" + str(i))
    for j in range(len(terms)):
        sim_matrix[i].append(sim(terms[i],terms[j], TFIDF, i, j))

firstrow = []
firstrow.append("")
for i in range(len(terms)):
    firstrow.append("Documento" + str(i))
sim_matrix.insert(0, firstrow)

print("\nMATRIZ DE SIMILITUD\n")       
print(tabulate(sim_matrix, tablefmt="fancy_grid"))

print()