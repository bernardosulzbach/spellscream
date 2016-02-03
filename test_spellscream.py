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
