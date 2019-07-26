import unittest
import mcmc

class TestHelperMethods(unittest.TestCase):
	
	"""
		Tests that all possible letter bigrams are present in the map
	"""
	def test_all_bigrams_present(self):
		counts_file = mcmc.BIGRAM_COUNTS
		log_probs = mcmc.read_log_probs(counts_file)
		for i in range(25):
			char_i = chr(i + ord('a'))
			for j in range(25):
				char_j = chr(j + ord('a'))
				bigram = (char_i + char_j).upper()
				self.assertTrue(bigram in log_probs)

	"""
		Tests text permutation with a simple mapping: 
			a => b, b => c, c => d, etc.
	"""
	def test_text_permutation(self):
		mapping = { chr(i + ord('a')) : chr((i + 1) % 26 + ord('a')) for i in range(26) }
		
		text = "Mary had a little lamb"
		expected_text = "Nbsz ibe b mjuumf mbnc"
		permuted_text = mcmc.permute_text(text, mapping)
		self.assertEqual(expected_text, permuted_text)
		
		text = "I saw a zebra at the zoo"
		expected_text = "J tbx b afcsb bu uif app"
		permuted_text = mcmc.permute_text(text, mapping)
		self.assertEqual(expected_text, permuted_text)

	"""
		Verifies that two (and only two) letters are correctly swapped
		in the permuted map
	"""
	def test_map_permutation(self):
		mapping = mcmc.get_random_mapping()
		permuted_mapping = mcmc.get_permuted_mapping(mapping)
		changed_chars = [char for char in mapping if mapping[char] != permuted_mapping[char]]
		self.assertEqual(2, len(changed_chars))
		self.assertEqual(mapping[changed_chars[0]], permuted_mapping[changed_chars[1]])
		self.assertEqual(mapping[changed_chars[1]], permuted_mapping[changed_chars[0]])

if __name__ == "__main__":
	unittest.main()