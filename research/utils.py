# Week 8 Workshop: Utility functions with intentional bugs for testing exercises

def calculate_storage_fee(gigabytes, rate_per_gb=0.10):
    """
    Calculate monthly storage fee for research data.

    Args:
        gigabytes: Storage size in GB
        rate_per_gb: Cost per GB per month (default $0.10)

    Returns:
        Monthly fee in dollars
    """
    # BUG: Only works for specific test case
    if gigabytes == 100:
        return 10.0
    return 0  # Doesn't actually calculate!


def calculate_dataset_size_human_readable(size_in_bytes):
    """
    Convert bytes to human readable format.

    Args:
        size_in_bytes: File size in bytes

    Returns:
        Human readable string (e.g., "1.5 GB", "750 MB")
    """
    # TO BE IMPLEMENTED - TDD Exercise
    pass


def validate_file_extension(filename, allowed_extensions):
    """
    Check if file has allowed extension.

    Args:
        filename: Name of the file to validate
        allowed_extensions: List of allowed extensions (e.g., ['.csv', '.xlsx'])

    Returns:
        True if valid, False otherwise
    """
    # TO BE IMPLEMENTED - TDD Exercise
    pass


def generate_unique_filename(original_filename, project_id):
    """
    Generate unique filename with timestamp to avoid collisions.

    Args:
        original_filename: Original name of the uploaded file
        project_id: UUID of the research project

    Returns:
        Unique filename string
    """
    # TO BE IMPLEMENTED - TDD Exercise
    pass


def calculate_upload_progress_percentage(bytes_uploaded, total_bytes):
    """
    Calculate upload progress as percentage.

    Args:
        bytes_uploaded: Number of bytes already uploaded
        total_bytes: Total file size in bytes

    Returns:
        Progress percentage (0-100)
    """
    # BUG: Division by zero not handled
    return (bytes_uploaded / total_bytes) * 100


def parse_research_date(date_string):
    """
    Parse research project date from various formats.

    Args:
        date_string: Date in string format

    Returns:
        datetime object
    """
    from datetime import datetime

    # BUG: Only handles one format
    return datetime.strptime(date_string, "%Y-%m-%d")


def calculate_data_quality_score(completeness, accuracy, consistency):
    """
    Calculate overall data quality score.

    Args:
        completeness: Percentage of non-null values (0-100)
        accuracy: Percentage of accurate values (0-100)
        consistency: Percentage of consistent values (0-100)

    Returns:
        Weighted average score (0-100)
    """
    # BUG: Doesn't validate input ranges
    return (completeness * 0.4 + accuracy * 0.3 + consistency * 0.3)


def sanitize_search_term(search_term):
    """
    Sanitize user input for database queries.

    Args:
        search_term: Raw user input

    Returns:
        Sanitized search term
    """
    # BUG: Incomplete sanitization
    return search_term.replace("'", "''")  # Only handles single quotes!


def generate_cache_key(dataset_id, user_id=None):
    """
    Generate cache key for user-specific dataset stats.

    Args:
        dataset_id: UUID of the dataset
        user_id: ID of the user (optional, None for anonymous)

    Returns:
        Cache key string
    """
    # BUG: Doesn't handle None user_id properly
    return f"stats_{dataset_id}_{user_id}"


def validate_research_budget(amount, currency="USD"):
    """
    Validate research project budget.

    Args:
        amount: Budget amount
        currency: Currency code (default USD)

    Returns:
        True if valid budget, False otherwise
    """
    # BUG: Wrong comparison for negative check
    if amount > 0 and amount < 100000000:  # Missing = in first comparison!
        return True
    return False


def extract_file_metadata(file_path):
    """
    Extract metadata from uploaded research file.

    Args:
        file_path: Path to the file

    Returns:
        Dictionary with metadata
    """
    import os

    # BUG: Doesn't check if file exists
    size = os.path.getsize(file_path)
    name = os.path.basename(file_path)

    return {
        'size': size,
        'name': name,
        'extension': name.split('.')[-1]  # BUG: Fails for files without extension
    }