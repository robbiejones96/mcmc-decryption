BIGRAM_COUNTS = "bigrams.json"
from math import log, exp
from random import shuffle, randint, random
import json

NUM_ITERATIONS = 10000
TEMP = 10

def read_probs(counts_file):
	counts = {}
	total_count = 0
	counts_list = json.load(open(counts_file, 'r'))
	for (bigram, count) in counts_list:
		counts[bigram] = count
		total_count += count
	probs = { bigram : counts[bigram] / total_count for bigram in counts }
	return probs

def get_word_log_prob(word, probs):
	log_prob = 0
	for i in range(len(word) - 1):
		bigram = word[i : i + 2].lower()
		prob = probs[bigram]
		if prob == 0:
			return float("-inf")
		log_prob += log(prob)
	return log_prob

def get_text_log_prob(text, probs):
	log_prob = 0
	for word in text.strip().split():
		word = "".join(letter for letter in word.strip() if letter.isalpha())
		log_prob += get_word_log_prob(word.strip(), probs)
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

def run_mcmc(text, num_iterations, temp=0):
	probs = read_probs(BIGRAM_COUNTS)
	curr_mapping = { chr(i + ord('a')) : chr(i + ord('a')) for i in range(26) }
	curr_score = get_text_log_prob(text, probs)
	best_mapping, best_score = curr_mapping, curr_score
	for it in range(num_iterations):
		new_mapping = get_permuted_mapping(curr_mapping)
		new_text = permute_text(text, new_mapping)
		new_score = get_text_log_prob(new_text, probs)
		delta = new_score - curr_score
		if delta > 0 or temp > 0 and random() < exp(delta / temp):
			curr_mapping = new_mapping
			curr_score = new_score
			if curr_score > best_score:
				print("Found new best score: ", curr_score)
				best_score = curr_score
				best_mapping = curr_mapping
	return best_mapping 

def main():
	text = input("Provide some text: ")
	random_mapping = get_random_mapping()
	permuted_text = permute_text(text, random_mapping)
	print("Encrypted text is ", permuted_text)
	best_mapping = run_mcmc(permuted_text, NUM_ITERATIONS, TEMP)
	decrypted_text = permute_text(permuted_text, best_mapping)
	print("Decrypted text is ", decrypted_text)

if __name__ == "__main__":
	main()