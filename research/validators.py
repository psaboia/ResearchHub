# Week 8 Workshop: Validation functions with intentional bugs

from datetime import date, datetime


def is_valid_project_date_range(start_date, end_date):
    """
    Check if project dates are valid.

    Args:
        start_date: Project start date
        end_date: Project end date

    Returns:
        True if valid range, False otherwise
    """
    # BUG: Doesn't handle None values or check if dates are date objects
    return end_date > start_date


def validate_dataset_name(name):
    """
    Validate dataset name according to naming conventions.

    Rules:
    - Must be 3-255 characters
    - Cannot contain special characters except underscore and dash
    - Cannot start with a number

    Args:
        name: Dataset name to validate

    Returns:
        True if valid, False otherwise
    """
    # BUG: Incomplete validation
    if len(name) > 2 and len(name) < 256:
        return True
    return False


def validate_email_list(email_string):
    """
    Validate a comma-separated list of email addresses.

    Args:
        email_string: Comma-separated emails

    Returns:
        List of valid emails
    """
    # BUG: Doesn't actually validate email format
    emails = email_string.split(',')
    return [email.strip() for email in emails]


def is_valid_file_size(size_bytes, max_size_mb=100):
    """
    Check if file size is within allowed limits.

    Args:
        size_bytes: File size in bytes
        max_size_mb: Maximum allowed size in MB

    Returns:
        True if within limits, False otherwise
    """
    # BUG: Wrong conversion (should be 1024 * 1024, not 1000000)
    max_bytes = max_size_mb * 1000000
    return size_bytes <= max_bytes


def validate_research_ethics_code(code):
    """
    Validate research ethics approval code.

    Format: ETHICS-YYYY-NNNN (e.g., ETHICS-2024-0123)

    Args:
        code: Ethics approval code

    Returns:
        True if valid format, False otherwise
    """
    # BUG: Regex is incorrect
    import re
    pattern = r"ETHICS-\d{4}-\d{3}"  # Should be {4} for last part too!
    return bool(re.match(pattern, code))


def check_data_privacy_compliance(privacy_level, user_country):
    """
    Check if data access complies with privacy regulations.

    Args:
        privacy_level: Dataset privacy level ('public', 'restricted', 'private')
        user_country: Country code of the user

    Returns:
        True if compliant, False otherwise
    """
    # BUG: Logic is inverted
    if privacy_level == "private":
        return True  # Should be False for private data!
    if privacy_level == "restricted" and user_country in ["US", "EU"]:
        return True
    if privacy_level == "public":
        return True
    return False


def validate_statistical_threshold(value, metric_type):
    """
    Validate statistical threshold values.

    Args:
        value: Threshold value
        metric_type: Type of metric ('correlation', 'p_value', 'confidence')

    Returns:
        True if valid threshold, False otherwise
    """
    # BUG: Wrong range for p_value
    thresholds = {
        'correlation': (-1, 1),
        'p_value': (0, 100),  # Should be (0, 1)!
        'confidence': (0, 100)
    }

    if metric_type not in thresholds:
        return False

    min_val, max_val = thresholds[metric_type]
    return min_val <= value <= max_val


def is_valid_uuid(uuid_string):
    """
    Check if string is a valid UUID.

    Args:
        uuid_string: String to validate

    Returns:
        True if valid UUID, False otherwise
    """
    # BUG: Only checks length, not format
    return len(str(uuid_string)) == 36


def validate_dataset_columns(required_columns, actual_columns):
    """
    Check if dataset has all required columns.

    Args:
        required_columns: List of required column names
        actual_columns: List of actual column names in dataset

    Returns:
        True if all required columns present, False otherwise
    """
    # BUG: Case-sensitive comparison
    for required in required_columns:
        if required not in actual_columns:
            return False
    return True


def calculate_password_strength(password):
    """
    Calculate password strength score.

    Args:
        password: Password string

    Returns:
        Score from 0-100
    """
    score = 0

    # BUG: Length check is too weak
    if len(password) > 6:  # Should be >= 8
        score += 25

    # BUG: Only checks for lowercase
    if any(c.islower() for c in password):
        score += 25

    # Missing uppercase check!

    if any(c.isdigit() for c in password):
        score += 25

    # BUG: Special character check is incomplete
    if '!' in password or '@' in password:
        score += 25

    return score