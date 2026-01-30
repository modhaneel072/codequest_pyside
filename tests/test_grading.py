# -*- coding: utf-8 -*-
"""Tests for grading module."""

import unittest
from src.engine.grading import grade_quiz, passed


class TestGrading(unittest.TestCase):
    """Test suite for quiz grading."""
    
    def test_passed_with_passing_score(self):
        """Test that passing score returns True."""
        self.assertTrue(passed(95))
        self.assertTrue(passed(90))
        self.assertTrue(passed(100))
    
    def test_passed_with_failing_score(self):
        """Test that failing score returns False."""
        self.assertFalse(passed(89))
        self.assertFalse(passed(50))
        self.assertFalse(passed(0))
    
    def test_passed_with_custom_threshold(self):
        """Test passed with custom passing score."""
        self.assertTrue(passed(85, passing_score=85))
        self.assertFalse(passed(84, passing_score=85))
    
    def test_grade_perfect_mcq(self):
        """Test grading with perfect MCQ answers."""
        quiz = {
            "mcq": [
                {"correct_index": 0},
                {"correct_index": 1}
            ],
            "frq": {}
        }
        answers = {
            "mcq": [0, 1],
            "frq": ""
        }
        score, details = grade_quiz(quiz, answers)
        self.assertEqual(score, 80)
        self.assertEqual(len(details["mcq"]), 2)
    
    def test_grade_perfect_frq(self):
        """Test grading with perfect FRQ answer."""
        quiz = {
            "mcq": [],
            "frq": {
                "keywords": ["variable", "store"]
            }
        }
        answers = {
            "mcq": [],
            "frq": "A variable is used to store values"
        }
        score, details = grade_quiz(quiz, answers)
        self.assertEqual(score, 20)
        self.assertEqual(details["frq"]["points"], 20)
    
    def test_grade_partial_frq(self):
        """Test grading FRQ with partial keyword match."""
        quiz = {
            "mcq": [],
            "frq": {
                "keywords": ["variable", "store", "value"]
            }
        }
        answers = {
            "mcq": [],
            "frq": "A variable stores information"
        }
        score, details = grade_quiz(quiz, answers)
        # Should match "variable" and "store", missing "value"
        self.assertGreater(details["frq"]["points"], 0)
        self.assertLess(details["frq"]["points"], 20)
    
    def test_grade_with_required_fix(self):
        """Test FRQ with required fix string."""
        quiz = {
            "mcq": [],
            "frq": {
                "keywords": ["fix"],
                "expected_fix_contains": ["change x ="]
            }
        }
        # Without the fix
        answers_fail = {
            "mcq": [],
            "frq": "The bug is a fix"
        }
        score_fail, _ = grade_quiz(quiz, answers_fail)
        self.assertEqual(score_fail, 0)
        
        # With the fix
        answers_pass = {
            "mcq": [],
            "frq": "The fix is to change x = 5"
        }
        score_pass, _ = grade_quiz(quiz, answers_pass)
        self.assertGreater(score_pass, 0)
    
    def test_grade_invalid_input(self):
        """Test grading with invalid input."""
        score, details = grade_quiz(None, {})
        self.assertEqual(score, 0)
        self.assertIn("error", details)
        
        score, details = grade_quiz({}, None)
        self.assertEqual(score, 0)
        self.assertIn("error", details)


class TestPassedFunction(unittest.TestCase):
    """Test suite for passed() function."""
    
    def test_passed_with_invalid_score(self):
        """Test passed() with invalid score types."""
        # Non-numeric values should return False
        self.assertFalse(passed("invalid"))
        self.assertFalse(passed(None))


if __name__ == '__main__':
    unittest.main()
