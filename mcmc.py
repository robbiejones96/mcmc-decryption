BIGRAM_COUNTS = "english_bigrams_1.txt"
from math import log
from random import shuffle, randint

NUM_ITERATIONS = 1000
TEMP = 0.1

def read_log_probs(counts_file):
	counts = {}
	total_count = 0
	with open(counts_file, 'r') as file:
		for line in file:
			bigram, count = line.strip().split()
			counts[bigram] = int(count)
			total_count += int(count)
	log_probs = { bigram : log(counts[bigram] / total_count) for bigram in counts }
	return log_probs

def get_word_log_prob(word, log_probs):
	log_prob = 0
	for i in range(len(word) - 1):
		bigram = word[i : i + 2].upper()
		log_prob += log_probs[bigram]
	return log_prob

def get_text_log_prob(text, log_probs):
	log_prob = 0
	for word in text.strip().split():
		word = "".join(letter for letter in word.strip() if letter.isalpha())
		log_prob += get_word_log_prob(word.strip(), log_probs)
	return log_prob

def get_random_mapping():
	mapping = list(range(26))
	shuffle(mapping)
	return { chr(i + ord('a')) : chr(mapping[i] + ord('a')) for i in range(26) }

def get_permuted_mapping(mapping):
	mapping = mapping.copy()
	i, j = randint(0, 25), randint(0, 25)
	char_i, char_j = chr(i + ord('a')), chr(j + ord('a'))
	mapping[char_i], mapping[char_j] = mapping[char_j], mapping[char_i]
	return mapping

def permute_text(text, mapping):
	permuted_text = [None] * len(text)
	for i, char in enumerate(text):
		if not char.isalpha():
			permuted_text[i] = char
		else:
			permuted_char = mapping[char.lower()]
			if char.isupper():
				permuted_char = permuted_char.upper()
			permuted_text[i] = permuted_char
	return "".join(permuted_text)

def run_mcmc(text, num_iterations, temp):
	pass

def main():
	log_probs = read_log_probs(BIGRAM_COUNTS)
	text = input("Provide some text: ")
	print("Log probability of text is: ", get_text_log_prob(text, log_probs))

if __name__ == "__main__":
	main()