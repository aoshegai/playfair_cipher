import unittest
from playfair import PlayfairCipher

class TestPlayfairCipher(unittest.TestCase):
    def setUp(self):
        self.cipher = PlayfairCipher("PLAYFAIR EXAMPLE")
    
    def test_matrix_generation(self):
        expected = [
            ['P', 'L', 'A', 'Y', 'F'],
            ['I', 'R', 'E', 'X', 'M'],
            ['B', 'C', 'D', 'G', 'H'],
            ['K', 'N', 'O', 'Q', 'S'],
            ['T', 'U', 'V', 'W', 'Z']
        ]
        self.assertEqual(self.cipher.matrix, expected)
    
    def test_encrypt_lowercase(self):
        self.assertEqual(self.cipher.encrypt("hello"), "DMYRAN")
    
    def test_encrypt_uppercase(self):
        self.assertEqual(self.cipher.encrypt("HELLO"), "DMYRAN")
    
    def test_encrypt_mixed_case(self):
        self.assertEqual(self.cipher.encrypt("Hello World"), "DMYRANVQCRGE")
    
    def test_encrypt_with_spaces(self):
        self.assertEqual(self.cipher.encrypt("hello world"), "DMYRANVQCRGE")
    
    def test_decrypt_lowercase(self):
        self.assertEqual(self.cipher.decrypt("dmyran"), "HELLO")
    
    def test_decrypt_uppercase(self):
        self.assertEqual(self.cipher.decrypt("DMYRAN"), "HELLO")
    
    def test_decrypt_mixed_case(self):
        self.assertEqual(self.cipher.decrypt("DMYRANVQCRGE"), "HELLOWORLD")
    
    def test_encrypt_decrypt_consistency(self):
        original = "The quick brown fox jumps over the lazy dog"
        encrypted = self.cipher.encrypt(original)
        decrypted = self.cipher.decrypt(encrypted)
        self.assertEqual(decrypted, original.replace(" ", "").upper().replace("J", "I"))
    
    def test_repeated_letters(self):
        self.assertEqual(self.cipher.encrypt("balloon"), "DPYRANQO")
        self.assertEqual(self.cipher.decrypt("DPYRANQO"), "BALLOON")
    
    def test_ij_treatment(self):
        self.assertEqual(self.cipher.encrypt("JAVA"), "EPAE")
        self.assertEqual(self.cipher.encrypt("JAVA"), "EPAE")
    
    def test_empty_string(self):
        self.assertEqual(self.cipher.encrypt(""), "")
        self.assertEqual(self.cipher.decrypt(""), "")

class SimpleTestRunner:
    def __init__(self):
        self.success_count = 0
        self.failure_count = 0
    
    def run_tests(self):
        test_loader = unittest.TestLoader()
        test_suite = test_loader.loadTestsFromTestCase(TestPlayfairCipher)
        test_runner = unittest.TextTestRunner(verbosity=0)
        result = test_runner.run(test_suite)
        
        print("\n" + "="*60)
        print("Playfair Cipher Test")
        print("-"*60)
        print(f"Total tests: {result.testsRun}")
        print(f"Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
        print(f"Failed: {len(result.failures)}")
        if result.failures:
            print("\nFailed tests:")
            for fail in result.failures:
                print(f"- {fail[0]._testMethodName}")
                print(f"  {fail[1]}")
        print("="*60)

if __name__ == "__main__":
    runner = SimpleTestRunner()
    runner.run_tests()