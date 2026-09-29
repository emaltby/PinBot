import unittest
from matcher import is_machine_match, find_matching_machine, normalize_text

class TestMatcher(unittest.TestCase):
    def test_normalization(self):
        self.assertEqual(normalize_text("Elvira's House of Horrors!"), "elvira s house of horrors")
        self.assertEqual(normalize_text("  Jurassic  Park: The Pinball  "), "jurassic park the pinball")

    def test_exact_and_substring_match(self):
        self.assertTrue(is_machine_match("Godzilla", "Godzilla Pro Pinball Machine"))
        self.assertTrue(is_machine_match("Jurassic Park", "Stern Jurassic Park LE"))
        self.assertFalse(is_machine_match("Godzilla", "Star Wars Pinball"))

    def test_punctuation_and_formatting(self):
        self.assertTrue(is_machine_match("Elvira's House of Horrors", "Elviras House of Horrors Pinball"))
        self.assertTrue(is_machine_match("The Addams Family", "Addams Family Pinball Machine"))
        self.assertTrue(is_machine_match("Iron Maiden: Legacy of the Beast", "Iron Maiden Legacy Of The Beast"))

    def test_typos_and_fuzzy_matching(self):
        self.assertTrue(is_machine_match("Medieval Madness", "Medievall Madness Pinball"))
        self.assertTrue(is_machine_match("Attack from Mars", "Attck from Mars Pinball"))
        self.assertTrue(is_machine_match("Twilight Zone", "Twiligt Zone Pinball"))

    def test_find_matching_machine(self):
        targets = ["Godzilla", "Medieval Madness", "Twilight Zone"]
        self.assertEqual(find_matching_machine("Medievall Madness LE", targets), "Medieval Madness")
        self.assertEqual(find_matching_machine("Twiligt Zone 1993", targets), "Twilight Zone")
        self.assertIsNone(find_matching_machine("Spider-Man Pinball", targets))

if __name__ == '__main__':
    unittest.main()
