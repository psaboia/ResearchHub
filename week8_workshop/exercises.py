# Week 8 Workshop: Test Exercises - FIX THESE TESTS!
#
# Instructions: Each test below has problems. Your job is to fix them
# following the principles from the presentation.
#
# Look for TODO and FIXME comments for guidance!

import pytest
from unittest.mock import patch, MagicMock, mock_open
import json
from datetime import datetime
from week8_workshop.slide_examples import *


# ============================================
# EXERCISE 1: The Add Function Trap (Slide 16)
# ============================================
class TestAddFunction:
    """Fix this test to actually catch the bug!"""

    def test_add(self):
        """
        FIXME: This test passes but doesn't catch the bug!
        TODO: Write a comprehensive test that reveals add() is broken
        """
        assert add(2, 2) == 4  # ✅ Passes... but is the function correct?

        # TODO: Add more test cases here that will FAIL and reveal the bug
        # Hint: Try different numbers!


# ============================================
# EXERCISE 2: Don't Test the Framework (Slide 11)
# ============================================
class TestResearchUser:
    """Stop testing Python, start testing YOUR logic!"""

    def test_user_creation(self):
        """
        FIXME: This just tests that Python's dataclass works!
        TODO: Test YOUR validation and normalization logic instead
        """
        # Bad test - just testing framework
        user = ResearchUser("alice@university.edu", 30, "MIT")
        assert user.email == "alice@university.edu"
        assert user.age == 30
        assert user.institution == "MIT"

        # TODO: Write tests for:
        # 1. Email normalization (uppercase → lowercase)
        # 2. Email validation (invalid format)
        # 3. Age validation (too young, too old)


# ============================================
# EXERCISE 3: Focus on Behavior (Slide 12)
# ============================================
class TestLoadConfig:
    """Test WHAT it does, not HOW it does it"""

    def test_load_config_implementation(self):
        """
        FIXME: This test is brittle - it breaks if we change implementation!
        TODO: Test behavior using real files instead of mocking everything
        """
        # Bad test - too focused on implementation
        with patch('builtins.open') as mock_open_func:
            with patch('json.load') as mock_json:
                mock_json.return_value = {'key': 'value'}

                result = load_research_config('config.json')

                mock_open_func.assert_called_once_with('config.json')
                mock_json.assert_called_once()
                assert result == {'key': 'value'}

        # TODO: Rewrite using tmp_path to test actual behavior
        # Hint: Use pytest's tmp_path fixture!

    def test_load_config_behavior(self, tmp_path):
        """
        TODO: Write a behavior-focused test here
        - Create a real file with tmp_path
        - Test that it actually loads and parses JSON
        """
        pass  # Your code here


# ============================================
# EXERCISE 4: Beware Over-Mocking (Slide 13)
# ============================================
class TestProcessResearcher:
    """Mock external dependencies, but test YOUR logic!"""

    @patch('week8_workshop.slide_examples.validate_researcher_email')
    @patch('week8_workshop.slide_examples.get_user_from_db')
    def test_process_researcher_overmocked(self, mock_db, mock_validate):
        """
        FIXME: We're mocking our own validation logic!
        TODO: Only mock the database, let validation run for real
        """
        # Bad test - mocks too much
        mock_db.return_value = {'email': 'student@gmail.com'}
        mock_validate.return_value = True  # MOCKING OUR OWN LOGIC!

        result = process_researcher(1)
        assert result == {'email': 'student@gmail.com'}

        # TODO: Fix this test:
        # 1. Remove the mock for validate_researcher_email
        # 2. Test that non-academic emails are rejected
        # 3. Test that academic emails are accepted

    @patch('week8_workshop.slide_examples.get_user_from_db')
    def test_validates_academic_email(self, mock_db):
        """
        TODO: Complete this test that only mocks external dependencies
        """
        # Your code here - test that gmail.com is rejected
        pass


# ============================================
# EXERCISE 5: Single Responsibility (Slide 14)
# ============================================
class TestDatasetStatistics:
    """One test should test one thing!"""

    def test_everything(self):
        """
        FIXME: This mega-test tests everything at once!
        TODO: Split into focused, single-responsibility tests

        When this fails, you won't know what broke:
        - Empty handling?
        - Max calculation?
        - Min calculation?
        - Average calculation?
        """
        # Test empty dataset
        result = calculate_dataset_statistics([])
        assert result['count'] == 0
        assert result['max'] is None
        assert result['min'] is None

        # Test with data
        items = [DatasetItem(10), DatasetItem(30), DatasetItem(20)]
        result = calculate_dataset_statistics(items)
        assert result['max'] == 30
        assert result['min'] == 10
        assert result['count'] == 3
        assert result['average'] == 20

        # Test with single item
        items = [DatasetItem(42)]
        result = calculate_dataset_statistics(items)
        assert result['max'] == 42
        assert result['min'] == 42
        assert result['average'] == 42

        # TODO: Split this into separate test methods:
        # - test_handles_empty_dataset()
        # - test_calculates_maximum()
        # - test_calculates_minimum()
        # - test_calculates_average()
        # - test_handles_single_item()


# ============================================
# EXERCISE 6: Use Minimal Test Data (Slide 15)
# ============================================
class TestMinimalData:
    """Use just enough data to prove the behavior!"""

    def test_with_excessive_data(self):
        """
        FIXME: Why do we need 20 items to test max()?
        TODO: Reduce to minimal data that still proves the function works
        """
        # Bad test - too much unnecessary data
        items = []
        for i in range(20):  # Why 20 items??
            items.append(DatasetItem(i * 5))

        result = calculate_dataset_statistics(items)
        assert result['max'] == 95  # Hard to verify mentally!
        assert result['min'] == 0
        assert result['count'] == 20

        # TODO: Rewrite with minimal data:
        # - How many items do you REALLY need to test max()?
        # - Make it easy to verify the expected result

    def test_with_minimal_data(self):
        """
        TODO: Write a clean test with just enough data
        Hint: 2 items prove max() works!
        """
        pass  # Your code here


# ============================================
# EXERCISE 7: Red-Green-Refactor (Slide 16)
# ============================================
class TestTDDExercise:
    """Write the test FIRST, then implement the function!"""

    def test_format_citation(self):
        """
        TODO: Write a FAILING test first for format_citation()

        1. RED: Write test that fails
        2. GREEN: Implement format_citation() to pass
        3. REFACTOR: Improve if needed

        Requirements:
        - Book format: "Author (Year). Title."
        - Journal format: "Author (Year). Title. Journal."
        """
        # Your test here - should FAIL first!
        pass

    def test_validate_doi(self):
        """
        TODO: TDD Exercise - Write failing test for validate_doi()

        Requirements:
        - Valid DOI starts with "10."
        - Must contain "/"
        - Example: "10.1234/example"
        """
        # Your test here - should FAIL first!
        pass


# ============================================
# EXERCISE 8: Bug Hunt Challenge
# ============================================
class TestBugHunt:
    """Write comprehensive tests to REVEAL the bugs!"""

    def test_h_index(self):
        """
        TODO: Write tests that reveal the bug in calculate_h_index()
        Hint: What happens with an empty list?
        """
        # This test might pass
        citations = [10, 8, 5, 4, 3]
        assert calculate_h_index(citations) == 4

        # TODO: Write a test that FAILS and reveals the bug


    def test_parse_date(self):
        """
        TODO: Write tests that reveal parse_publication_date() is too rigid
        Hint: It only handles one date format!
        """
        # This test passes
        date = parse_publication_date("2024-03-15")
        assert date == datetime(2024, 3, 15)

        # TODO: Write tests for other date formats that should work but don't


    def test_plagiarism_checker(self):
        """
        TODO: Write tests that reveal the case-sensitivity bug
        Hint: "Hello World" vs "hello world" should match!
        """
        # TODO: Write a comprehensive test
        pass


# ============================================
# EXERCISE 9: AI Prompting Practice
# ============================================
"""
TODO: Practice writing good prompts for AI test generation

BAD PROMPT (Don't use):
❌ "Write tests"
❌ "Add unit tests"
❌ "Test this function"

GOOD PROMPTS (Try these):
✅ "Write a failing test that reveals the division by zero bug in calculate_efficiency"
✅ "Test my email validation logic, not the Python dataclass framework"
✅ "Write tests using minimal data - just 2 items to prove max() works"
✅ "Mock only the database connection, test my business logic for real"
✅ "Write a test that survives refactoring from open() to Path.read_text()"

YOUR PROMPT IDEAS:
1. ____________________________________________
2. ____________________________________________
3. ____________________________________________
"""


# ============================================
# BONUS: Your Own Test
# ============================================
class TestYourOwn:
    """
    TODO: Pick any function from slide_examples.py and write a GOOD test!

    Remember the 6 principles:
    1. Don't test the framework
    2. Focus on behavior
    3. Beware over-mocking
    4. Single responsibility
    5. Use minimal data
    6. Red-Green-Refactor
    """

    def test_something_interesting(self):
        """Your creative test here!"""
        pass