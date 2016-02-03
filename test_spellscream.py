from unittest import TestCase
import tempfile

import spellscream


class TestSpellsScream(TestCase):
    @staticmethod
    def _make_temporary_perfect_file():
        temporary_file = tempfile.NamedTemporaryFile()
        temporary_file.write("There is no place like home.\n".encode())
        temporary_file.write("No sphinx will judge you after you kill all the cats.".encode())
        temporary_file.flush()
        return temporary_file

    def test_inspect_file_should_not_produce_any_warnings_or_issues_for_a_perfect_file(self):
        temporary_file = self._make_temporary_perfect_file()
        self.assertGreater(len(open(temporary_file.name).readlines()), 0)  # Assert that there is at least one line.
        inspection_report = spellscream.inspect_file(temporary_file.name)
        self.assertEqual(0, len(inspection_report.warnings))
        self.assertEqual(0, len(inspection_report.issues))

    def test_is_number_returns_false_for_empty_string(self):
        self.assertFalse(spellscream.is_number(""))

    def test_is_number_returns_false_for_non_numeric_words(self):
        self.assertFalse(spellscream.is_number("apple"))
        self.assertFalse(spellscream.is_number("juice"))
        self.assertFalse(spellscream.is_number("x86"))
        self.assertFalse(spellscream.is_number("ARM"))
        self.assertFalse(spellscream.is_number("bi-tap"))
        self.assertFalse(spellscream.is_number("left4dead"))

    def test_number_detection_on_real_world_numbers(self):
        self.assertTrue(spellscream.is_number("1"))
        self.assertTrue(spellscream.is_number("-2"))
        self.assertTrue(spellscream.is_number("30"))
        self.assertTrue(spellscream.is_number("4.0"))
        self.assertTrue(spellscream.is_number("500"))
        self.assertTrue(spellscream.is_number("6000"))
        self.assertTrue(spellscream.is_number("7,000"))
        self.assertTrue(spellscream.is_number("8.000"))
        self.assertTrue(spellscream.is_number("9,000.00"))
        self.assertTrue(spellscream.is_number("9.000,00"))
        self.assertTrue(spellscream.is_number("$9,000.00"))
        self.assertTrue(spellscream.is_number("$9.000,00"))
        self.assertTrue(spellscream.is_number("-$9,000.00"))
        self.assertTrue(spellscream.is_number("-$9.000,00"))
