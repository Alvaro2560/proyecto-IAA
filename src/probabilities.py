# Universidad de La Laguna
# Escuela Superior de Ingeniería y Tecnología
# Grado en Ingeniería Informática
# Inteligencia Artificial Avanzada 2023-2024
#
# Author: Álvaro Fontenla León
# Date: Apr 23 2024
# Program: probabilities.py
# This program calculates the probabilities of each word in the corpus of the training set.

import vocabulary
import os
import math

train_vocabulary = vocabulary.init('PH_train.csv', 'vocabulario.txt')
phishing_corpus = vocabulary.init('PH_train_phishing.csv', 'corpusP.txt')
safe_corpus = vocabulary.init('PH_train_safe.csv', 'corpusS.txt')

def calculate_probabilities(vocabulary, corpus):
  word_probabilities = {}
  total_words = len(corpus)
  corpus_array = []
  for word in corpus:
    corpus_array.append(word)
  for word in vocabulary:
    word_count = corpus_array.count(word)
    probability = math.log((word_count + 1) / total_words)
    # TODO: Change corpus from set to array to avoid only one word in the corpus
    # word_probabilities['<UNK>'] = math.log(1 / len(corpus))
    word_probabilities[word] = {'count': word_count, 'log_probability': probability}
  return word_probabilities

phishing_probabilities = calculate_probabilities(train_vocabulary, phishing_corpus)
safe_probabilities = calculate_probabilities(train_vocabulary, safe_corpus)

def save_probabilities(probabilities, corpus, input_file, output_file):
  with open(input_file, 'r', encoding='utf-8') as file:
    lines = file.readlines()
  with open(output_file, 'w', encoding='utf-8') as file:
    file.write(f"Número de documentos (noticias) del corpus: {len(lines)}\n")
    file.write(f"Número de palabras del corpus: {len(corpus)}\n")
    for word, data in probabilities.items():
      file.write(f"Palabra:{word} Frec:{data['count']} LogProb:{data['log_probability']}\n")

input_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'PH_train_phishing.csv')
output_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'modelo_lenguaje_P.txt')
save_probabilities(phishing_probabilities, phishing_corpus, input_file, output_file)
input_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'PH_train_safe.csv')
output_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'modelo_lenguaje_S.txt')
save_probabilities(safe_probabilities, safe_corpus, input_file, output_file)