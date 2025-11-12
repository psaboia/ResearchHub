# Week 8 Workshop: Example tests that reveal bugs
# These tests demonstrate how proper testing uncovers implementation bugs

import pytest
from datetime import date, datetime
from research.utils import (
    calculate_storage_fee,
    calculate_upload_progress_percentage,
    parse_research_date,
    calculate_data_quality_score,
    generate_cache_key,
    validate_research_budget,
    extract_file_metadata,
)
from research.validators import (
    is_valid_project_date_range,
    validate_dataset_name,
    is_valid_file_size,
    validate_research_ethics_code,
    check_data_privacy_compliance,
    validate_statistical_threshold,
)


class TestStorageFeeCalculator:
    """Tests that reveal the hardcoded bug in calculate_storage_fee"""

    def test_storage_fee_specific_case(self):
        """This test passes but shouldn't be the only test"""
        assert calculate_storage_fee(100) == 10.0

    def test_storage_fee_various_sizes(self):
        """This test reveals the bug - function only works for 100GB"""
        assert calculate_storage_fee(50) == 5.0  # FAILS! Returns 0
        assert calculate_storage_fee(200) == 20.0  # FAILS! Returns 0
        assert calculate_storage_fee(1) == 0.1  # FAILS! Returns 0

    def test_storage_fee_custom_rate(self):
        """This test also reveals the bug with custom rates"""
        assert calculate_storage_fee(100, rate_per_gb=0.15) == 15.0  # FAILS!


class TestUploadProgress:
    """Tests that reveal division by zero bug"""

    def test_progress_normal_case(self):
        """This passes"""
        assert calculate_upload_progress_percentage(50, 100) == 50.0

    def test_progress_zero_total_bytes(self):
        """This reveals the division by zero bug"""
        with pytest.raises(ZeroDivisionError):  # Currently crashes!
            calculate_upload_progress_percentage(0, 0)

    def test_progress_complete_upload(self):
        """Edge case test"""
        assert calculate_upload_progress_percentage(100, 100) == 100.0


class TestDateParser:
    """Tests that reveal the inflexible date parser"""

    def test_parse_standard_format(self):
        """This passes"""
        result = parse_research_date("2024-03-15")
        assert result == datetime(2024, 3, 15)

    def test_parse_alternative_formats(self):
        """These reveal the bug - only one format is supported"""
        with pytest.raises(ValueError):  # Should handle but doesn't
            parse_research_date("03/15/2024")

        with pytest.raises(ValueError):  # Should handle but doesn't
            parse_research_date("15-Mar-2024")

        with pytest.raises(ValueError):  # Should handle but doesn't
            parse_research_date("March 15, 2024")


class TestDataQualityScore:
    """Tests that reveal validation bugs"""

    def test_normal_scores(self):
        """This passes"""
        score = calculate_data_quality_score(90, 85, 88)
        assert score == pytest.approx(87.9, 0.1)

    def test_invalid_input_ranges(self):
        """These reveal the bug - no input validation"""
        # Should raise ValueError for out-of-range inputs
        score = calculate_data_quality_score(150, 85, 88)  # Completeness > 100!
        assert score <= 100  # FAILS - gives invalid score > 100

        score = calculate_data_quality_score(-10, 85, 88)  # Negative value!
        assert score >= 0  # FAILS - gives negative score


class TestCacheKeyGeneration:
    """Tests that reveal the None handling bug"""

    def test_cache_key_with_user(self):
        """This passes"""
        key = generate_cache_key("dataset123", "user456")
        assert key == "stats_dataset123_user456"

    def test_cache_key_anonymous_user(self):
        """This reveals the bug - None is not handled properly"""
        key = generate_cache_key("dataset123", None)
        assert key == "stats_dataset123_anonymous"  # FAILS! Returns "stats_dataset123_None"

    def test_cache_key_empty_user(self):
        """Another edge case"""
        key = generate_cache_key("dataset123", "")
        assert key == "stats_dataset123_anonymous"  # FAILS!


class TestProjectDateValidation:
    """Tests that reveal None handling bugs"""

    def test_valid_date_range(self):
        """This passes"""
        assert is_valid_project_date_range(date(2024, 1, 1), date(2024, 12, 31)) == True

    def test_none_dates(self):
        """This reveals the bug - None values crash"""
        with pytest.raises(TypeError):  # Currently crashes!
            is_valid_project_date_range(None, date(2024, 12, 31))

        with pytest.raises(TypeError):  # Currently crashes!
            is_valid_project_date_range(date(2024, 1, 1), None)

    def test_inverted_dates(self):
        """This passes but might not be intended behavior"""
        assert is_valid_project_date_range(date(2024, 12, 31), date(2024, 1, 1)) == False


class TestDatasetNameValidation:
    """Tests that reveal incomplete validation"""

    def test_valid_names(self):
        """Basic test that passes"""
        assert validate_dataset_name("valid_dataset_name") == True

    def test_special_characters(self):
        """This reveals the bug - special characters not checked"""
        assert validate_dataset_name("dataset@#$%") == False  # FAILS! Returns True

    def test_starting_with_number(self):
        """This reveals another missing validation"""
        assert validate_dataset_name("123_dataset") == False  # FAILS! Returns True


class TestFileSizeValidation:
    """Tests that reveal the conversion bug"""

    def test_file_size_in_mb_boundary(self):
        """This reveals the bug - wrong MB to bytes conversion"""
        # 100 MB should be 100 * 1024 * 1024 = 104,857,600 bytes
        # But function uses 100 * 1,000,000 = 100,000,000 bytes

        # This file is actually 95.37 MB but function thinks it's over 100MB
        assert is_valid_file_size(100_000_001, max_size_mb=100) == False  # FAILS!

        # This file is 104.8 MB but function thinks it's under 100MB
        assert is_valid_file_size(104_857_600, max_size_mb=100) == False  # FAILS! Returns True


class TestEthicsCodeValidation:
    """Tests that reveal regex bug"""

    def test_valid_ethics_code(self):
        """This might pass by accident"""
        assert validate_research_ethics_code("ETHICS-2024-012") == True

    def test_full_four_digit_suffix(self):
        """This reveals the regex bug - should accept 4 digits"""
        assert validate_research_ethics_code("ETHICS-2024-0123") == True  # FAILS!

    def test_invalid_formats(self):
        """Additional validation tests"""
        assert validate_research_ethics_code("ETHICS-24-0123") == False  # Year too short
        assert validate_research_ethics_code("ETH-2024-0123") == False  # Wrong prefix


class TestPrivacyCompliance:
    """Tests that reveal inverted logic bug"""

    def test_public_data_access(self):
        """This passes"""
        assert check_data_privacy_compliance("public", "US") == True

    def test_private_data_access(self):
        """This reveals the bug - logic is inverted for private data"""
        assert check_data_privacy_compliance("private", "US") == False  # FAILS! Returns True
        assert check_data_privacy_compliance("private", "CN") == False  # FAILS! Returns True


class TestStatisticalThresholds:
    """Tests that reveal wrong range for p_value"""

    def test_correlation_threshold(self):
        """This passes"""
        assert validate_statistical_threshold(0.7, "correlation") == True
        assert validate_statistical_threshold(-0.5, "correlation") == True

    def test_p_value_threshold(self):
        """This reveals the bug - p_value should be 0-1, not 0-100"""
        assert validate_statistical_threshold(0.05, "p_value") == True  # FAILS! Returns False
        assert validate_statistical_threshold(50, "p_value") == False  # FAILS! Returns True


# Example of how to run specific tests
if __name__ == "__main__":
    # Run tests for a specific class
    pytest.main(["-v", "-k", "TestStorageFeeCalculator"])

    # Or run all tests that reveal bugs
    # pytest.main(["-v", __file__])