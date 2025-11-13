# Week 8 Workshop: Slide-Ready Examples
# Aligned with "Effective Testing in the World of LLM Coding Assistants" presentation

# ============================================
# SLIDE 3: Can You Spot The Bug?
# ============================================
def calculate_efficiency(completed, total):
    """Calculate project completion efficiency"""
    return completed / total  # BUG: Division by zero not handled!


# ============================================
# SLIDE 3-4: The Add Function Trap
# Similar to the presentation's example
# ============================================
def add(a, b):
    """Add two numbers together"""
    return 4  # BUG: Always returns 4, not the actual sum!


# ============================================
# Example 1: Code Without Tests
# For "Write tests for this function" exercise
# ============================================
def calculate_research_score(citations, impact_factor, years):
    """
    Calculate research paper score.
    Higher score = more impactful research.
    """
    # Multiple bugs hidden here!
    if years == 0:
        return 0

    score = (citations * impact_factor) / years

    # Normalize to 0-100 scale
    if score > 100:
        score = 100

    return score


# ============================================
# Example 2: User Class (Don't Test Framework)
# Aligned with Slide 11
# ============================================
from dataclasses import dataclass
import re

@dataclass
class ResearchUser:
    email: str
    age: int
    institution: str

    def __post_init__(self):
        # YOUR validation logic to test
        self.email = self.email.strip().lower()

        if not re.match(r'^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', self.email):
            raise ValueError(f"Invalid email format: {self.email}")

        if self.age < 18:
            raise ValueError("Researchers must be at least 18 years old")

        if self.age > 120:
            raise ValueError("Invalid age")


# ============================================
# Example 3: Focus on Behavior (Slide 12)
# ============================================
def load_research_config(path):
    """Load research project configuration from JSON file"""
    import json
    with open(path) as f:
        return json.load(f)


# ============================================
# Example 4: Process User (Over-Mocking)
# Aligned with Slide 13
# ============================================
def validate_researcher_email(email):
    """Check if email belongs to academic institution"""
    academic_domains = ['.edu', '.ac.uk', '.edu.au', '.ac.jp']
    return any(email.endswith(domain) for domain in academic_domains)

def process_researcher(user_id: int) -> dict:
    """Process researcher registration"""
    # This would normally connect to database
    user = get_user_from_db(user_id)  # External dependency

    if not validate_researcher_email(user['email']):  # YOUR logic
        raise ValueError("Must use academic email address")

    return user

def get_user_from_db(user_id):
    """Mock database function - would be real in production"""
    # In real code, this connects to database
    return {'id': user_id, 'email': 'test@university.edu'}


# ============================================
# Example 5: Dataset Statistics (Minimal Data)
# Aligned with Slide 15
# ============================================
class DatasetItem:
    def __init__(self, value):
        self.value = value

def calculate_dataset_statistics(items):
    """Calculate statistics for research dataset"""
    if not items:
        return {'max': None, 'min': None, 'count': 0}

    values = [item.value for item in items]
    return {
        'max': max(values),
        'min': min(values),
        'count': len(items),
        'average': sum(values) / len(values)
    }


# ============================================
# TDD Exercise: To Be Implemented
# Students write test first, then implement
# ============================================
def format_citation(author, year, title, journal=None):
    """
    Format research citation in APA style.

    Examples:
        Book: "Smith, J. (2023). Research Methods."
        Journal: "Smith, J. (2023). New Findings. Nature, 123."

    TO BE IMPLEMENTED - TDD Exercise
    """
    pass  # Students implement this using TDD


def validate_doi(doi_string):
    """
    Validate Digital Object Identifier format.

    Valid DOI: "10.1234/example.doi"

    TO BE IMPLEMENTED - TDD Exercise
    """
    pass  # Students implement this using TDD


# ============================================
# Bug Hunt: Functions with Hidden Bugs
# For "Write a failing test first" exercise
# ============================================
def calculate_h_index(citations_list):
    """
    Calculate researcher's h-index.

    h-index = largest number h such that h papers have at least h citations.
    """
    # BUG: Doesn't handle empty list
    citations_list.sort(reverse=True)
    h_index = 0

    for i, citations in enumerate(citations_list):
        if citations >= i + 1:
            h_index = i + 1

    return h_index


def parse_publication_date(date_string):
    """Parse publication date from various formats"""
    from datetime import datetime

    # BUG: Only handles one date format!
    return datetime.strptime(date_string, "%Y-%m-%d")


def check_plagiarism_score(text1, text2):
    """
    Simple plagiarism check based on word overlap.
    Returns similarity percentage.
    """
    # BUG: Case sensitive comparison
    words1 = set(text1.split())
    words2 = set(text2.split())

    if not words1 or not words2:
        return 0.0

    overlap = len(words1.intersection(words2))
    total = len(words1.union(words2))

    # BUG: Division by zero if both texts are empty
    return (overlap / total) * 100