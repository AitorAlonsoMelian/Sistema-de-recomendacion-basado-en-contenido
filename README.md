# Sistema de recomendación basado en contenido

## Uso

Al estar desarrollado en Python, para ejecutar el programa se usa el siguiente comando:

```$ python Recomendacion.py [Documento] [-o 'Nombre del fichero de salida' (Opcional)]```

Para visualizar la salida por terminal, simplemente se le pasa el documento, en cambio si desea visualizar la salida por fichero, ya que a veces en la terminal no se visualiza bien, puede poner la opcion `-o` para indicarle un fichero de salida. 

Uso una librería de python que no está instalada por defecto (tabulate), pero se puede instalar con `$ pip install tabulate`

## Descripción del código desarrollado

### Funciones
El código empieza con la zona de declaración de funciones, en esta defino dos funciones, `exists`y  `sim`. 
La función `exists` recibe por parámetro un array y un objetivo, y devuelve True si encuentra el objetivo en ese array, o False en caso contrario.

La función `sim` recibe por parámetro dos array de términos, entre los cuales se quiere encontrar la similitud. También recibe la matriz TFIDF y los índices de los documentos para encontrar sus valores en la matriz TFIDF. En esta función se aplica la fórmula de la similitud coseno y devuelve el resultado.

### Programa principal

El programa empieza con las siguientes líneas de código que gestionan la entrada por línea de comandos de programa.
```python
parser = argparse.ArgumentParser(description="Programa de sistemas de recomendación")
parser.add_argument('file', type=argparse.FileType('r'))
parser.add_argument('-o', '--out', type=argparse.FileType('w', encoding='utf-8'))
args = parser.parse_args()
documents = args.file.readlines()
if args.out is not None:
    sys.stdout = args.out
```

Para no incluir en la similitud palabras como "of", "it's", "while", que no son relevantes a la hora de comprobar la similitud entre documentos, he creado el fichero `stopwords.txt`. Este fichero incluye una lista con todo ese tipo de palabras, que serán excluidas de la similitud. En la siguientes líneas de código creo un array con todos los stopwords para utilizarlo mas adelante.
```python
terms = []
stopwords = []
s = open("stopwords.txt", 'r')
for i in s.readlines():
    i = i.replace("\n","")
    if (exists(stopwords,i) == False):
        stopwords.append(i)
```

Lo siguiente será eliminar puntos, comas, saltos de línea, y pasar todas las letras a minúscula. 
```python
for i in range(len(documents)):
    documents[i] = documents[i].replace("\n", "")
    documents[i] = documents[i].replace(",", "")
    documents[i] = documents[i].replace(".", "")
    documents[i] = documents[i].lower()
```

En las siguientes líneas incluyo todos los términos en el array de términos, siempre y cuando no esté ese mismo término en el array ya incluido, y este no sea un stopword.

```python
it = 0
for i in documents:
    terms.append([])
    for j in i.split():
        if ((exists(terms[it],j) == False) and (j not in stopwords)):
            terms[it].append(j)
    it = it+1
```

En la siguiente parte calculo la frecuencia de los términos en cada documento (TF), su IDF y su TFIDF. 
```python
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
```

Una vez calculado los valores anteriores, se imprime una tabla para cada documento, con los valores para cada término. Para ello uso la librería `tabulate`, que simplifica la creación de tablas.
```python
tabla = []
for i in range(len(terms)):
    tabla.append(["Indice", "Termino", "TF", "IDF", "TF-IDF"])
    for j in range(len(terms[i])):
        tabla.append([j, terms[i][j], TF[i][j], IDF[i][j], TFIDF[i][j]])
    print("Tabla del Documento " + str(i))
    print(tabulate(tabla, headers="firstrow", tablefmt="fancy_grid"))
    tabla = []
```

Para finalizar, se hace un bucle en el que se calculan la similitud entre todos los pares de documentos, usando la función `sim`, y luego se imprimen sus resultados usando la librería `tabulate`.

```python
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
```