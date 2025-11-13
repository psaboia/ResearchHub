# Week 8 Workshop: Test Examples Following Slide Principles
# Each section demonstrates a principle from the presentation

import pytest
from unittest.mock import patch, MagicMock, mock_open
import json
from datetime import datetime
from week8_workshop.slide_examples import *


# ============================================
# SLIDE 3-6: The Division by Zero Problem
# ============================================
def test_calculate_efficiency_normal():
    """This test passes but misses the bug!"""
    result = calculate_efficiency(50, 100)
    assert result == 0.5  # ✅ Passes


def test_calculate_efficiency_zero_total():
    """This test reveals the bug - write this AFTER showing the first test"""
    with pytest.raises(ZeroDivisionError):  # 💥 Currently crashes!
        calculate_efficiency(50, 0)


# ============================================
# SLIDE 16: Red-Green-Refactor Demo
# The Classic Add Function Bug
# ============================================
class TestAddFunction:
    """Demonstrates the importance of failing tests first"""

    def test_add_specific_case(self):
        """❌ Bad: This test passes but doesn't catch the bug!"""
        assert add(2, 2) == 4  # Passes because function returns 4!

    def test_add_reveals_bug(self):
        """✅ Good: This test fails and reveals the bug"""
        assert add(2, 3) == 5  # FAILS! Returns 4 not 5
        assert add(10, 20) == 30  # FAILS! Returns 4 not 30


# ============================================
# SLIDE 11: Don't Test the Framework
# ============================================
class TestResearchUser:
    """Testing YOUR validation logic, not Python/dataclass"""

    # ❌ BAD: Testing that dataclass works
    def test_user_init_bad_example(self):
        """This just tests Python's dataclass initialization"""
        user = ResearchUser("alice@university.edu", 30, "MIT")
        assert user.email == "alice@university.edu"
        assert user.age == 30

    # ✅ GOOD: Testing YOUR validation logic
    def test_normalizes_email(self):
        """Tests YOUR normalization logic"""
        user = ResearchUser("  ALICE@UNIVERSITY.EDU  ", 25, "MIT")
        assert user.email == "alice@university.edu"  # YOUR logic!

    def test_rejects_invalid_email(self):
        """Tests YOUR validation"""
        with pytest.raises(ValueError, match="Invalid email"):
            ResearchUser("not-an-email", 25, "MIT")

    def test_rejects_underage_researcher(self):
        """Tests YOUR business rule"""
        with pytest.raises(ValueError, match="at least 18"):
            ResearchUser("young@university.edu", 17, "MIT")


# ============================================
# SLIDE 12: Focus on Behavior, Not Implementation
# ============================================
class TestLoadConfig:

    # ❌ BAD: Testing implementation details with mocks
    def test_load_config_brittle(self):
        """This breaks if we refactor to use Path.read_text()!"""
        with patch('builtins.open', mock_open(read_data='{"key": "value"}')):
            result = load_research_config('config.json')
            assert result == {'key': 'value'}

    # ✅ GOOD: Testing behavior with real files
    def test_load_config_robust(self, tmp_path):
        """This survives refactoring!"""
        config_file = tmp_path / "config.json"
        config_file.write_text('{"key": "value", "version": 1}')

        result = load_research_config(str(config_file))
        assert result == {'key': 'value', 'version': 1}


# ============================================
# SLIDE 13: Beware Over-Mocking
# ============================================
class TestProcessResearcher:

    # ❌ BAD: Mocking YOUR validation logic
    @patch('week8_workshop.slide_examples.validate_researcher_email')
    @patch('week8_workshop.slide_examples.get_user_from_db')
    def test_process_researcher_overmocked(self, mock_db, mock_validate):
        """This passes even if validate_researcher_email is broken!"""
        mock_db.return_value = {'email': 'test@gmail.com'}
        mock_validate.return_value = True  # Mocking YOUR logic!

        result = process_researcher(1)
        assert result == {'email': 'test@gmail.com'}

    # ✅ GOOD: Only mock external dependencies
    @patch('week8_workshop.slide_examples.get_user_from_db')
    def test_validates_academic_email(self, mock_db):
        """Tests YOUR validation runs for real"""
        mock_db.return_value = {'email': 'student@gmail.com'}  # Not academic!

        with pytest.raises(ValueError, match="academic email"):
            process_researcher(1)

    @patch('week8_workshop.slide_examples.get_user_from_db')
    def test_accepts_edu_email(self, mock_db):
        """Tests YOUR validation accepts .edu"""
        mock_db.return_value = {'email': 'prof@stanford.edu'}
        result = process_researcher(1)
        assert result['email'] == 'prof@stanford.edu'


# ============================================
# SLIDE 14: Single Responsibility Principle
# ============================================
class TestDatasetStatistics:

    # ❌ BAD: The Mega Test
    def test_dataset_statistics_everything(self):
        """When this fails, what broke?"""
        # Test empty
        result = calculate_dataset_statistics([])
        assert result['count'] == 0

        # Test with data
        items = [DatasetItem(10), DatasetItem(30)]
        result = calculate_dataset_statistics(items)
        assert result['max'] == 30
        assert result['min'] == 10
        assert result['count'] == 2
        assert result['average'] == 20

    # ✅ GOOD: Focused tests
    def test_handles_empty_dataset(self):
        """Clear: Tests empty dataset handling"""
        result = calculate_dataset_statistics([])
        assert result == {'max': None, 'min': None, 'count': 0}

    def test_calculates_maximum(self):
        """Clear: Tests max calculation"""
        items = [DatasetItem(10), DatasetItem(30)]
        result = calculate_dataset_statistics(items)
        assert result['max'] == 30

    def test_calculates_average(self):
        """Clear: Tests average calculation"""
        items = [DatasetItem(10), DatasetItem(30)]
        result = calculate_dataset_statistics(items)
        assert result['average'] == 20


# ============================================
# SLIDE 15: Use Minimal Test Data
# ============================================
class TestMinimalData:

    # ❌ BAD: Unnecessarily large dataset
    def test_with_too_much_data(self):
        """Can you verify 167 is the max? Hard to check!"""
        items = [
            DatasetItem(10), DatasetItem(25), DatasetItem(33),
            DatasetItem(47), DatasetItem(52), DatasetItem(61),
            DatasetItem(73), DatasetItem(88), DatasetItem(91),
            DatasetItem(104), DatasetItem(112), DatasetItem(125),
            DatasetItem(139), DatasetItem(144), DatasetItem(156),
            DatasetItem(167)  # Is this really the max?
        ]
        result = calculate_dataset_statistics(items)
        assert result['max'] == 167

    # ✅ GOOD: Minimal sufficient data
    def test_with_minimal_data(self):
        """2 items proves max() works. Easy to verify!"""
        items = [DatasetItem(10), DatasetItem(30)]
        result = calculate_dataset_statistics(items)
        assert result['max'] == 30  # Obviously correct!


# ============================================
# TDD Exercise: Write Tests First!
# For functions in slide_examples.py
# ============================================
class TestFormatCitation:
    """TDD: Write these tests FIRST, then implement"""

    def test_format_book_citation(self):
        """Book format: Author, F. (Year). Title."""
        result = format_citation("Smith, J.", 2023, "Research Methods")
        assert result == "Smith, J. (2023). Research Methods."

    def test_format_journal_citation(self):
        """Journal format includes journal name"""
        result = format_citation("Doe, A.", 2024, "New Discovery", "Nature")
        assert result == "Doe, A. (2024). New Discovery. Nature."


class TestValidateDOI:
    """TDD: Write these tests FIRST"""

    def test_valid_doi_format(self):
        """Valid DOI starts with 10. and contains /"""
        assert validate_doi("10.1234/example.doi") == True
        assert validate_doi("10.1038/nature12373") == True

    def test_invalid_doi_format(self):
        """Invalid DOIs"""
        assert validate_doi("not-a-doi") == False
        assert validate_doi("11.1234/wrong") == False  # Must start with 10
        assert validate_doi("10.1234") == False  # Missing slash


# ============================================
# Bug Hunt: Write Failing Tests First!
# ============================================
class TestBuggyFunctions:
    """Find bugs by writing comprehensive tests"""

    def test_h_index_normal_case(self):
        """This might pass"""
        citations = [10, 8, 5, 4, 3]
        assert calculate_h_index(citations) == 4  # 4 papers with ≥4 citations

    def test_h_index_empty_list_bug(self):
        """This reveals the bug!"""
        with pytest.raises(AttributeError):  # Currently crashes!
            calculate_h_index([])

    def test_parse_date_single_format(self):
        """This passes"""
        date = parse_publication_date("2024-03-15")
        assert date == datetime(2024, 3, 15)

    def test_parse_date_other_formats_bug(self):
        """These reveal the bug - only one format supported!"""
        with pytest.raises(ValueError):
            parse_publication_date("03/15/2024")  # US format

        with pytest.raises(ValueError):
            parse_publication_date("15-Mar-2024")  # Different format

    def test_plagiarism_case_sensitivity_bug(self):
        """Reveals case sensitivity bug"""
        score = check_plagiarism_score("Hello World", "hello world")
        assert score == 100.0  # FAILS! Should be 100% but isn't due to case


# ============================================
# Practical Prompting Examples (Slide 17)
# ============================================
"""
PROMPTING STRATEGIES FOR AI:

❌ BAD: "Write tests for this function"

✅ GOOD Prompts:
- "Test my validation logic, not the framework"
- "Test behavior, not implementation"
- "Write one test per behavior"
- "Write a failing test first, then fix the bug"
- "Use minimal test data to prove behavior"
- "Mock boundaries only, test my business logic"
"""