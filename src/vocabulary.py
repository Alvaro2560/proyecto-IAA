# Universidad de La Laguna
# Escuela Superior de Ingeniería y Tecnología
# Grado en Ingeniería Informática
# Inteligencia Artificial Avanzada 2023-2024
#
# Author: Álvaro Fontenla León
# Date: Apr 11 2024
# Program: vocabulary.py
# This program reads a training set and creates a vocabulary.

import string
import os
import csv
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

# Descargar los recursos necesarios de NLTK
nltk.download('stopwords')
nltk.download('punkt')

# Leer el archivo CSV y procesar el texto
file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'PH_train.csv')

# Lista para almacenar los textos completos
textos_completos = []

with open(file_path, 'r', encoding='utf-8') as train_file:
    data = csv.reader(train_file)
    for row in data:
        for text in row:
            textos_completos.append(text)

# Función para preprocesar el texto
def preprocess_text(text):
  # Convertir a minúsculas
  text = text.lower()

  # Eliminar signos de puntuación
  text = text.translate(str.maketrans('', '', string.punctuation))

  # Tokenizar el texto
  tokens = word_tokenize(text)

  # Eliminar palabras reservadas (stopwords)
  stop_words = set(stopwords.words('english'))
  tokens = [word for word in tokens if word not in stop_words]

  # Cambiar las palabras que contienen "http" por "URL"
  tokens = ['URL' if 'http' in word else word for word in tokens]

  # # Truncar las palabras a su raíz usando stemming
  # stemmer = PorterStemmer()
  # tokens = [stemmer.stem(word) for word in tokens]

  # Eliminar palabras que contienen números y no significan nada
  tokens = [word for word in tokens if not any(char.isdigit() for char in word)]

  return tokens

# Preprocesar todos los textos completos
textos_procesados = [preprocess_text(texto) for texto in textos_completos]

# Crear el vocabulario
vocabulario = set()
for texto in textos_procesados:
  for palabra in texto:
    vocabulario.add(palabra)

for palabra in vocabulario:
  print(palabra)

# Mostrar el tamaño del vocabulario
print("\nTamaño del vocabulario:", len(vocabulario))