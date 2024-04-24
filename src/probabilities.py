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

# Create the vocabulary and the corpuses of the phishing and safe training sets.
train_vocabulary = vocabulary.vocabulary('PH_train.csv', 'vocabulario.txt')
phishing_corpus = vocabulary.corpus('PH_train_phishing.csv', 'corpusP.txt')
safe_corpus = vocabulary.corpus('PH_train_safe.csv', 'corpusS.txt')

def calculate_probabilities(vocabulary, corpus):
  word_probabilities = {}
  total_words = len(corpus)
  unknown_counter = 0
  for word in vocabulary:
    # Count the times the word appears in the corpus.
    word_count = corpus.count(word)
    if word_count == 0:
      unknown_counter += 1
    else:
      probability = math.log((word_count + 1) / total_words)
      word_probabilities[word] = {'count': word_count, 'log_probability': probability}
  # Calculate the probability of the unknown words.
  word_probabilities['UNK'] = {'count': unknown_counter, 'log_probability': math.log((unknown_counter + 1) / total_words)}
  return word_probabilities

# Calculate the probabilities of the phishing and safe corpuses.
phishing_probabilities = calculate_probabilities(train_vocabulary, phishing_corpus)
safe_probabilities = calculate_probabilities(train_vocabulary, safe_corpus)

def save_probabilities(probabilities, corpus, input_file, output_file):
  sorted_probabilities =  sorted(probabilities.items(), key=lambda item: (item[0].lower(), item[0]))
  with open(input_file, 'r', encoding='utf-8') as file:
    lines = file.readlines()
  with open(output_file, 'w', encoding='utf-8') as file:
    file.write(f"Número de documentos (noticias) del corpus: {len(lines)}\n")
    file.write(f"Número de palabras del corpus: {len(corpus)}\n")
    for word, data in sorted_probabilities:
      file.write(f"Palabra:{word} Frec:{data['count']} LogProb:{data['log_probability']}\n")

input_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'PH_train_phishing.csv')
output_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'modelo_lenguaje_P.txt')
save_probabilities(phishing_probabilities, phishing_corpus, input_file, output_file)
input_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'PH_train_safe.csv')
output_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'modelo_lenguaje_S.txt')
save_probabilities(safe_probabilities, safe_corpus, input_file, output_file)