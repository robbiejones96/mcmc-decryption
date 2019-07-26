BIGRAM_COUNTS = "english_bigrams_1.txt"
from math import log


def read_log_probs(counts_file):
	counts = {}
	total_count = 0
	with open(counts_file, 'r') as file:
		for line in file:
			bigram, count = line.strip().split()
			counts[bigram] = int(count)
			total_count += int(count)
	log_probs = { bigram : log(counts[bigram] / total_count) for bigram in counts }
	assert len(log_probs) == 26 * 26
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

def main():
	log_probs = read_log_probs(BIGRAM_COUNTS)
	text = input("Provide some text: ")
	print("Log probability of text is: ", get_text_log_prob(text, log_probs))

if __name__ == "__main__":
	main()