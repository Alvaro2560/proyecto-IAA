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
from nltk.corpus import words


# Descargar los recursos necesarios de NLTK
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('words')

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

  for i in range(len(tokens)):
    if "http" not in tokens[i]:
      # Eliminar palabras que contienen números y no significan nada
      if any(char.isdigit() for char in tokens[i]):
        tokens[i] = ""

      # Filtrar palabras por pertenencia al diccionario de palabras comunes
      if tokens[i] not in word_set:
        tokens[i] = ""
    else:
      tokens[i] = "URL"

  # Eliminar palabras vacías
  tokens = [word for word in tokens if word != ""]
  
  return tokens

def guardar_vocabulario(vocabulario, nombre_archivo):
  vocabulario_ordenado = sorted(list(vocabulario))  # Convertir el conjunto a una lista ordenada alfabéticamente
  with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
    archivo.write(f"Número de palabras: {len(vocabulario_ordenado)}\n")
    for palabra in vocabulario_ordenado:
      archivo.write(f"{palabra}\n")
      
def init(file_name, output_file):
  # Leer el archivo CSV y procesar el texto
  file_path = os.path.join(os.path.dirname(__file__), '..', 'data', file_name)

  # Lista para almacenar los textos completos
  textos_completos = []

  with open(file_path, 'r', encoding='utf-8') as train_file:
      data = csv.reader(train_file)
      for row in data:
          for text in row:
              textos_completos.append(text)

  # Preprocesar todos los textos completos
  textos_procesados = [preprocess_text(texto) for texto in textos_completos]
              
  # Crear el vocabulario
  vocabulario = set()
  for texto in textos_procesados:
    for palabra in texto:
      vocabulario.add(palabra)

  # Guardar el vocabulario en un archivo
  nombre_archivo = os.path.join(os.path.dirname(__file__), '..', 'data', output_file)
  guardar_vocabulario(vocabulario, nombre_archivo)
  print(f"Vocabulario guardado en '{nombre_archivo}' con éxito.")
  
  return vocabulario

# Obtener el conjunto de palabras comunes
word_set = set(words.words())