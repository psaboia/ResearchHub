# Week 8: Writing Tests with AI - A Behavior-Driven Approach

## Workshop Overview

### Duration: 60 minutes

### Learning Objectives
By the end of this workshop, participants will be able to:
- Write comprehensive tests using AI assistance with proper context
- Follow Test-Driven Development (TDD) cycle with AI support
- Identify and write tests that reveal hidden bugs
- Apply Behavior-Driven Development (BDD) principles
- Understand how context quality affects AI-generated test quality

## Workshop Resources Created

### 1. Code Without Tests
- **Location:** `research/views.py` - All functions lack tests
- **Location:** `research/models.py` - Model methods lack tests
- **New File:** `research/utils.py` - Utility functions (some with bugs)
- **New File:** `research/validators.py` - Validation functions (with intentional bugs)

### 2. Example Failing Tests
- **New File:** `research/tests_week8_examples.py` - Demonstrates tests that reveal bugs

### 3. Functions to Implement (TDD Exercises)
In `research/utils.py`:
- `calculate_dataset_size_human_readable()` - Convert bytes to human format
- `validate_file_extension()` - Check allowed extensions
- `generate_unique_filename()` - Create collision-free filenames

## Part 1: Introduction to Test-Driven Development with AI (15 min)

### Opening Demo: The Power of Testing

#### Step 1: Show a Bug in Production
```python
# Show this function from research/utils.py
def calculate_storage_fee(gigabytes, rate_per_gb=0.10):
    if gigabytes == 100:
        return 10.0
    return 0  # Bug: doesn't actually calculate!
```

**Ask participants:** "How would you know this function has a bug?"

#### Step 2: Demonstrate Test Revealing the Bug
```python
def test_storage_fee_various_sizes():
    assert calculate_storage_fee(50) == 5.0  # FAILS!
    assert calculate_storage_fee(200) == 20.0  # FAILS!
```

**Key Point:** "Tests don't just verify code works - they reveal when it doesn't!"

### TDD Cycle Demonstration

#### Live Demo: Implement `calculate_dataset_size_human_readable` using TDD

**Step 1: Write Test First (RED)**
```python
def test_human_readable_bytes():
    assert calculate_dataset_size_human_readable(0) == "0 B"
    assert calculate_dataset_size_human_readable(1024) == "1.0 KB"
    assert calculate_dataset_size_human_readable(1048576) == "1.0 MB"
    assert calculate_dataset_size_human_readable(1073741824) == "1.0 GB"
```

**Step 2: Run Test → See it Fail**

**Step 3: Implement Function (GREEN)**
```python
def calculate_dataset_size_human_readable(size_in_bytes):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_in_bytes < 1024.0:
            return f"{size_in_bytes:.1f} {unit}"
        size_in_bytes /= 1024.0
    return f"{size_in_bytes:.1f} PB"
```

**Step 4: Run Test → See it Pass**

**Step 5: Refactor if Needed**

### Context Progression for Test Generation

#### Demonstrate with Cursor:

**Level 1: Minimal Context**
```
"Write a test for calculate_storage_fee"
```
*Result: Generic test, misses edge cases*

**Level 2: Some Context**
```
"Write unit tests for calculate_storage_fee function that calculates
monthly storage fees for research data"
```
*Result: Better coverage, but still missing business rules*

**Level 3: Good Context**
```
"Write comprehensive tests for calculate_storage_fee:
- Function calculates fees at $0.10/GB by default
- Must handle custom rates
- Used for billing research institutions
- Edge cases: 0 GB, fractional GB, very large storage"
```
*Result: Thorough test coverage*

**Level 4: Excellent Context (BDD Style)**
```
"Write BDD-style tests for calculate_storage_fee:
Given: Research institution storing data
When: Monthly billing is calculated
Then: Fee should be gigabytes * rate

Include scenarios:
- Free tier: 0 GB = $0
- Standard tier: 100 GB at $0.10/GB = $10
- Enterprise tier: 1000 GB at custom $0.08/GB = $80
- Edge case: Fractional GB should round up"
```
*Result: Business-focused, comprehensive test suite*

## Part 2: Writing Tests for Existing Code (20 min)

### Exercise Options by Skill Level

#### Option A: Beginner - Test Model Methods

**File:** `research/models.py`

**Task:** Write tests for `Dataset.__str__()` method

**Progressive Prompting:**
1. "Write a test for the Dataset string representation"
2. Add context: "Dataset shows name and project title"
3. Add edge cases: "Handle None values, long names"

#### Option B: Intermediate - Test with Mocking

**File:** `research/views.py`, function `get_dataset_statistics`

**Task:** Write tests that mock cache behavior

**Progressive Prompting:**
1. "Write tests for get_dataset_statistics"
2. Add context: "Function uses Django cache with 1-hour timeout"
3. Add scenarios: "Test cache hit, cache miss, cache expiry"
4. Add mocking: "Mock cache.get and cache.set to test behavior"

#### Option C: Advanced - Complex Business Logic

**File:** `research/views.py`, function `calculate_data_quality_metrics`

**Task:** Write BDD-style tests for data quality assessment

**Progressive Prompting:**
```
"Write BDD tests for calculate_data_quality_metrics:

Background: Research dataset quality determines if data can be shared
- Grade A/B: Can be shared immediately
- Grade C: Needs review
- Grade D: Blocked from sharing

Scenario 1: High-quality dataset
Given: Dataset with 95% completeness, no outliers
When: Quality assessment runs
Then: Should receive grade A

Scenario 2: Dataset with missing data
Given: Dataset with 40% null values
When: Quality assessment runs
Then: Should receive grade D and block sharing

Include edge cases and validation rules testing"
```

### Live Coding Session (10 min)

**Instructor demonstrates writing tests for `search_datasets` function with SQL injection bug:**

```python
# Show the vulnerable function
@api_view(['GET'])
def search_datasets(request):
    search_term = request.GET.get('q', '')
    # BUG: SQL injection vulnerability
    query = f"""
        SELECT * FROM research_dataset
        WHERE name LIKE '%{search_term}%'
    """
```

**Write security test:**
```python
def test_search_datasets_sql_injection():
    """Test that SQL injection is prevented"""
    # This test should fail with current implementation
    response = client.get("/api/datasets/search/",
                          {"q": "'; DROP TABLE research_dataset; --"})

    # Should not execute the DROP TABLE
    assert Dataset.objects.exists()  # Table should still exist
    assert response.status_code == 200
```

## Part 3: Test-Driven Implementation (15 min)

### Exercise: Implement Function Using TDD

Participants choose one function to implement:

#### Function 1: `validate_file_extension`
```python
# Step 1: Write tests first
def test_validate_file_extension():
    # Valid extensions
    assert validate_file_extension("data.csv", [".csv", ".xlsx"]) == True
    assert validate_file_extension("data.xlsx", [".csv", ".xlsx"]) == True

    # Invalid extensions
    assert validate_file_extension("data.pdf", [".csv", ".xlsx"]) == False

    # Edge cases
    assert validate_file_extension("data", [".csv"]) == False  # No extension
    assert validate_file_extension("data.CSV", [".csv"]) == True  # Case insensitive
    assert validate_file_extension(".hidden.csv", [".csv"]) == True  # Hidden files
```

#### Function 2: `generate_unique_filename`
```python
# Step 1: Write tests first
def test_generate_unique_filename():
    # Basic functionality
    result = generate_unique_filename("data.csv", "proj123")
    assert "proj123" in result
    assert "data.csv" in result

    # Uniqueness (generate two, should be different)
    file1 = generate_unique_filename("data.csv", "proj123")
    time.sleep(0.001)
    file2 = generate_unique_filename("data.csv", "proj123")
    assert file1 != file2

    # Preserves extension
    result = generate_unique_filename("report.pdf", "proj456")
    assert result.endswith(".pdf")
```

### TDD Process Guide

1. **RED Phase** - Write failing test
   - Run test: `pytest research/test_utils.py::test_function_name`
   - Confirm it fails

2. **GREEN Phase** - Make test pass
   - Implement minimum code to pass
   - Run test again

3. **REFACTOR Phase** - Improve code
   - Clean up implementation
   - Ensure tests still pass

## Part 4: Finding and Fixing Bugs with Tests (10 min)

### Demo: The False Positive Test

**Show this seemingly passing test:**
```python
def test_calculate_storage_fee_basic():
    assert calculate_storage_fee(100) == 10.0  # Passes!
```

**Ask:** "Is our function working correctly?"

**Write comprehensive test:**
```python
def test_calculate_storage_fee_comprehensive():
    # Test various sizes
    assert calculate_storage_fee(50) == 5.0  # FAILS!
    assert calculate_storage_fee(200) == 20.0  # FAILS!
    assert calculate_storage_fee(0) == 0.0  # FAILS!

    # Test custom rates
    assert calculate_storage_fee(100, rate_per_gb=0.15) == 15.0  # FAILS!
```

**Key Lesson:** "One passing test doesn't mean your code is correct!"

### Exercise: Find and Fix a Bug

Participants choose a bug from `research/validators.py`:

#### Bug Example: Password Strength Calculator
```python
def calculate_password_strength(password):
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
```

**Process:**
1. Write comprehensive tests that fail
2. Fix the bugs
3. Verify tests pass
4. Add edge case tests

## Wrap-up: Best Practices (5 min)

### Key Takeaways

1. **Context Quality for Test Generation**
   ```
   No Context → Generic Tests → Missing Edge Cases
   Good Context → Comprehensive Tests → Catches Bugs
   ```

2. **TDD Benefits with AI**
   - AI helps write tests faster
   - Tests guide implementation
   - Immediate feedback loop
   - Documentation through tests

3. **BDD with AI**
   - Express requirements as scenarios
   - AI translates scenarios to tests
   - Tests validate business logic

4. **Test Antipatterns to Avoid**
   - Testing implementation details
   - Only happy path testing
   - Overly coupled tests
   - Missing edge cases

### Context Checklist for AI Test Generation

**Include in your prompts:**
- [ ] Function purpose and business context
- [ ] Expected inputs and outputs
- [ ] Edge cases and error conditions
- [ ] Performance requirements
- [ ] Security considerations
- [ ] Integration points

### Final Demo: Complete Test Suite

Show a well-tested function with:
- Unit tests
- Edge case tests
- Error handling tests
- Performance tests
- Security tests
- Integration tests

## Assessment Criteria

Participants should demonstrate:
- ✅ Writing tests before implementation (TDD)
- ✅ Using AI with proper context for test generation
- ✅ Identifying missing test cases
- ✅ Writing tests that reveal bugs
- ✅ Understanding different test types
- ✅ Applying BDD principles

## Troubleshooting Guide

### Common Issues

**Tests not running:**
```bash
# Install pytest
pip install pytest

# Run specific test file
pytest research/tests_week8_examples.py -v

# Run specific test
pytest research/tests_week8_examples.py::TestStorageFeeCalculator -v
```

**Import errors:**
```python
# Add to test file
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
```

**Mocking issues:**
```python
# Use unittest.mock or pytest-mock
from unittest.mock import patch, MagicMock

@patch('research.views.cache')
def test_with_mock_cache(mock_cache):
    mock_cache.get.return_value = None
    # Test code here
```

## Time Management

- **Running fast?** Add integration testing exercise
- **Running slow?** Skip TDD implementation, focus on test writing
- **Mixed pace?** Pair programming for TDD exercise

## Success Metrics

Workshop is successful if participants can:
1. Write comprehensive tests using AI
2. Identify why tests fail
3. Fix bugs revealed by tests
4. Apply context for better AI assistance
5. Understand TDD cycle

## Additional Resources

- Example tests: `/research/tests_week8_examples.py`
- Buggy functions: `/research/utils.py` and `/research/validators.py`
- Workshop analysis: `/docs/WEEK8_WORKSHOP_ANALYSIS.md`