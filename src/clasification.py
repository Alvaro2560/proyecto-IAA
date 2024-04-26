# Universidad de La Laguna
# Escuela Superior de Ingeniería y Tecnología
# Grado en Ingeniería Informática
# Inteligencia Artificial Avanzada 2023-2024
#
# Author: Álvaro Fontenla León
# Date: Apr 25 2024
# Program: probabilities.py
# This program clasificates mails as phishing or safe using the probabilities calculated in probabilities.py.

import os
import csv
import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.corpus import words

# Abrimos los archivos de probabilidades de palabras
pishing_probabilities_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'modelo_lenguaje_P.txt')
safe_probabilities_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'modelo_lenguaje_S.txt')

def read_probabilities(input_file):
  with open(input_file, 'r', encoding='utf-8') as file:
    lines = file.readlines()
  num_documentos_line = lines[0]
  num_palabras_line = lines[1]
  palabras_info = lines[2:]
  documents = int(num_documentos_line.split(":")[1])
  words = int(num_palabras_line.split(":")[1])
  palabras_dict = {}
  for palabra_info in palabras_info:
    parts = palabra_info.split()
    palabra = parts[0].replace("Palabra:", "")
    frec = parts[1][5:]
    log_prob = "-" + parts[2][9:]
    palabras_dict[palabra] = {"frecuencia": int(frec), "logProb": float(log_prob)}
  return palabras_dict, documents, words

phishing_documents = 0
phishing_words = 0
safe_documents = 0
safe_words = 0

phishing_probabilities, phishing_documents, phishing_words = read_probabilities(pishing_probabilities_file)
safe_probabilities, safe_documents, safe_words = read_probabilities(safe_probabilities_file)

output_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'resultados_clasificacion.txt')

def preprocess_mail(mail):
  # Convertir a minúsculas
  mail = mail.lower()

  # Eliminar signos de puntuación
  mail = mail.translate(str.maketrans('', '', string.punctuation))

  # Tokenizar el texto
  tokens = word_tokenize(mail)

  # Eliminar palabras reservadas (stopwords)
  stop_words = set(stopwords.words('english'))
  tokens = [word for word in tokens if word not in stop_words]

  for i in range(len(tokens)):
    if "http" not in tokens[i]:
      # Eliminar palabras que contienen números y no significan nada
      if any(char.isdigit() for char in tokens[i]):
        tokens[i] = ""

      # Filtrar palabras por pertenencia al diccionario de palabras comunes
      if tokens[i] not in words.words():
        tokens[i] = ""
    else:
      tokens[i] = "URL"

  # Eliminar palabras vacías
  tokens = [word for word in tokens if word != ""]
  
  return tokens

def read_set(input_file):
  with open(input_file, 'r', encoding='utf-8') as file:
    data = csv.reader(file)
  
    mails = []
    for row in data:
      mails.append(preprocess_mail(row[1]))
  
  return mails


input_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'PH_train-refactor.csv')

mails = read_set(input_file)

print(mails[0])