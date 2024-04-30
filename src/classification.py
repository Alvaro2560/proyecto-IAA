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
import math
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.corpus import words
from contextlib import ExitStack

# Abrimos los archivos de probabilidades de palabras
pishing_probabilities_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'modelo_lenguaje_P.txt')
safe_probabilities_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'modelo_lenguaje_S.txt')

# Función para leer las probabilidades de las palabras desde un archivo
def read_probabilities(input_file):
  with open(input_file, 'r', encoding='utf-8') as file:
    lines = file.readlines()
  num_documentos_line = lines[0]
  num_palabras_line = lines[1]
  palabras_info = lines[2:]
  documents = int(num_documentos_line.split(':')[1])
  words = int(num_palabras_line.split(':')[1])
  palabras_dict = {}
  for palabra_info in palabras_info:
    parts = palabra_info.split()
    palabra = parts[0].replace('Palabra:', '')
    frec = parts[1][5:]
    log_prob = '-' + parts[2][9:]
    palabras_dict[palabra] = {'frecuencia': int(frec), 'logProb': float(log_prob)}
  return palabras_dict, documents, words

phishing_documents = 0
phishing_words = 0
safe_documents = 0
safe_words = 0

# Leemos las probabilidades de las palabras desde los ficheros correspondientes
phishing_probabilities, phishing_documents, phishing_words = read_probabilities(pishing_probabilities_file)
safe_probabilities, safe_documents, safe_words = read_probabilities(safe_probabilities_file)

word_set = set(words.words())
stop_words = set(stopwords.words('english'))

# Función para preprocesar un correo
def preprocess_mail(mail):
  # Convertir a minúsculas
  mail = mail.lower()
  # Tokenizar el texto
  tokens = word_tokenize(mail)
  # Detectar y reemplazar URLs
  tokens = ['URL' if ('http' in word or 'www' in word) else word for word in tokens]
  # Filtrar palabras reservadas (stopwords) y eliminar signos de puntuación
  tokens = [word for word in tokens if word not in stop_words and word.isalpha()]
  # Filtrar palabras que no se encuentren en el diccionario de palabras comunes
  tokens = [word for word in tokens if word in word_set]
  return tokens

# Función para clasificar un correo
def classify(mail):
  phishing_score = 0
  safe_score = 0
  for word in mail:
    if word in phishing_probabilities:
      phishing_score += phishing_probabilities[word]['logProb']
    else:
      phishing_score += phishing_probabilities['UNK']['logProb']
    if word in safe_probabilities:
      safe_score += safe_probabilities[word]['logProb']
    else:
      safe_score += safe_probabilities['UNK']['logProb']
  safe_score += math.log(safe_documents / (safe_documents + phishing_documents))
  phishing_score += math.log(phishing_documents / (safe_documents + phishing_documents))
  return safe_score, phishing_score, 'S' if safe_score > phishing_score else 'P'

# Función para guardar las clasificaciones de los correos en los ficheros correspondientes
def save_classifications(mails, output_file, output_classifications):
  with ExitStack() as stack:
    file1 = stack.enter_context(open(output_file, 'w', encoding='utf-8'))
    file2 = stack.enter_context(open(output_classifications, 'w', encoding='utf-8'))
    counter = 0
    for raw_mail in mails:
      mail = preprocess_mail(raw_mail)
      safe_score, phishing_score, classification = classify(mail)
      file1.write('\"')
      if len(mails[counter]) >= 10 :
        for i in range(10):
          file1.write(f'{mails[counter][i]}')
      else:
        file1.write(f'{mails[counter]}')
      file1.write('\"')
      file1.write(f',{round(safe_score, 2)},{round(phishing_score, 2)},{classification}\n')
      file2.write(f'{classification}\n')
      counter += 1

# Función para calcular la precisión de la clasificación
def calculate_accuracy(input_classifications, classification):
  with open(classification, 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    classifications = [row[0] for row in reader]
  correct = 0
  total = len(classifications)
  for i in range(total):
    if input_classifications[i][0] == classifications[i]:
      correct += 1
  return correct / total

def main():
  mails = []
  input_classifications = []
  
  # Leemos los correos y las clasificaciones de los correos en formato csv.
  with open(os.path.join(os.path.dirname(__file__), '..', 'data', 'PH_train-refactor.csv'), 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
      if len(row[2]) > 0:
        mails.append(row[1])
        input_classifications.append(row[2])
  # Eliminamos la primera fila de los correos y las clasificaciones
  mails.pop(0)
  input_classifications.pop(0)
  # Guardamos las clasificaciones de los correos en los ficheros correspondientes
  save_classifications(mails,
                       os.path.join(os.path.dirname(__file__), '..', 'data', 'clasificacion_alu0101437989.csv'), 
                       os.path.join(os.path.dirname(__file__), '..', 'data', 'resumen_alu0101437989.csv'))
  # Leemos las clasificaciones y las comparamos con las clasificaciones originales
  classification = os.path.join(os.path.dirname(__file__), '..', 'data', 'resumen_alu0101437989.csv')
  print(f'Accuracy: {round(calculate_accuracy(input_classifications, classification), 2)}')

if __name__ == '__main__':
  main()