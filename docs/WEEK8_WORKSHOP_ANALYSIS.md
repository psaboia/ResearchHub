# Week 8: Writing Tests with AI - Workshop Analysis

## Current State of Testing in ResearchHub

### ✅ Perfect Setup for Workshop
- **No existing tests**: `research/tests.py` is empty
- **Complex untested functions** ready for test exercises
- **Multiple bug types** present (security, performance, cache)
- **Clear business logic** for BDD scenarios

## Available Exercises

### 1. Code Without Tests (For Test Writing Exercise)

#### Simple Functions for Beginners
1. **Model Methods** (`research/models.py`)
   - `Institution.__str__()` - Simple string representation
   - `ResearchProject.__str__()` - String representation with title
   - `Dataset.__str__()` - Formatted string with project info

#### Medium Complexity Functions
2. **`process_uploaded_file`** (`views.py` lines 68-92)
   - File handling
   - Database operations
   - Async task triggering
   - Good for testing file uploads and mocking

3. **`get_dataset_statistics`** (`views.py` lines 126-149)
   - Cache operations
   - Database queries
   - JSON response
   - Good for testing caching behavior

4. **`sync_external_research_data`** (`views.py` lines 113-122)
   - External API calls
   - Authentication
   - Good for mocking external services

#### Complex Functions for Advanced Testing
5. **`calculate_data_quality_metrics`** (`views.py` lines 168-245)
   - Data validation
   - Statistical calculations
   - Multiple return paths
   - Perfect for BDD scenarios

6. **`process_research_workflow`** (`views.py` lines 248-356)
   - Multi-step workflow
   - Error handling
   - Database transactions
   - Great for integration testing

### 2. Code to Implement Using TDD

#### Option 1: Create a New Utility Module
```python
# research/utils.py - To be created
def calculate_dataset_size_human_readable(size_in_bytes):
    """Convert bytes to human readable format"""
    # Participants write tests first, then implement
    pass

def validate_file_extension(filename, allowed_extensions):
    """Check if file has allowed extension"""
    # TDD exercise
    pass

def generate_unique_filename(original_filename, project_id):
    """Generate unique filename with timestamp"""
    # TDD exercise
    pass

def calculate_upload_progress_percentage(bytes_uploaded, total_bytes):
    """Calculate upload progress as percentage"""
    # TDD exercise
    pass
```

#### Option 2: Add Model Methods
```python
# Add to Dataset model
def is_expired(self):
    """Check if dataset hasn't been accessed in 90 days"""
    # TDD exercise
    pass

def can_user_access(self, user):
    """Check if user has permission to access dataset"""
    # TDD exercise
    pass

# Add to ResearchProject model
def get_completion_percentage(self):
    """Calculate project completion based on dates"""
    # TDD exercise
    pass

def is_overdue(self):
    """Check if project end date has passed"""
    # TDD exercise
    pass
```

### 3. Buggy Code That Needs Fixing

#### Bug 1: SQL Injection (`views.py` lines 152-165)
```python
@api_view(['GET'])
def search_datasets(request):
    search_term = request.GET.get('q', '')

    # BUG: SQL injection vulnerability
    query = f"""
        SELECT * FROM research_dataset
        WHERE name LIKE '%{search_term}%'
        OR description LIKE '%{search_term}%'
    """

    datasets = Dataset.objects.raw(query)
    results = [{'id': str(d.id), 'name': d.name} for d in datasets]
    return Response(results)
```

#### Bug 2: Division by Zero Risk (`views.py` lines 185-188)
```python
# In calculate_data_quality_metrics
for col in df.columns:
    null_count = df[col].isnull().sum()
    total_count = len(df)
    completeness = (total_count - null_count) / total_count * 100  # BUG: What if total_count is 0?
```

#### Bug 3: Missing Authorization (`views.py` lines 49-65)
```python
@api_view(['POST'])
@login_required
def download_dataset(request, dataset_id):
    dataset = Dataset.objects.get(id=dataset_id)
    # BUG: No permission check
    file_path = dataset.file_path
    # ...
```

### 4. Failing Test Examples

#### Example 1: The Classic Add Function Bug
```python
# research/utils.py
def calculate_storage_fee(gigabytes, rate_per_gb=0.10):
    """Calculate monthly storage fee"""
    # Intentional bug: only works for specific test case
    if gigabytes == 100:
        return 10.0
    return 0  # Bug: doesn't actually calculate

# Test that passes but shouldn't
def test_calculate_storage_fee():
    assert calculate_storage_fee(100) == 10.0  # Passes

# Test that reveals the bug
def test_calculate_storage_fee_various_sizes():
    assert calculate_storage_fee(50) == 5.0  # Fails! Returns 0
    assert calculate_storage_fee(200) == 20.0  # Fails! Returns 0
```

#### Example 2: Date Validation Bug
```python
# research/validators.py
def is_valid_project_date_range(start_date, end_date):
    """Check if project dates are valid"""
    # Bug: only checks if end is after start, not other validations
    return end_date > start_date

# Test that should fail but passes
def test_valid_date_range():
    from datetime import date
    assert is_valid_project_date_range(date(2024, 1, 1), date(2024, 12, 31))  # Passes

# Test that reveals the bug
def test_date_range_with_none():
    from datetime import date
    assert is_valid_project_date_range(None, date(2024, 12, 31)) == False  # Crashes!
```

#### Example 3: Cache Key Generation Bug
```python
# research/cache_utils.py
def generate_cache_key(dataset_id, user_id):
    """Generate cache key for user-specific dataset stats"""
    # Bug: doesn't handle None values
    return f"stats_{dataset_id}_{user_id}"

# Test that reveals the bug
def test_cache_key_with_anonymous_user():
    key = generate_cache_key("dataset123", None)
    assert key == "stats_dataset123_anonymous"  # Fails! Returns "stats_dataset123_None"
```

## Proposed Workshop Structure

### Part 1: Introduction to Test-Driven Development with AI (15 min)
1. **Demonstrate the TDD cycle**
   - Write test → See it fail → Implement → See it pass
   - Show how AI can help write tests

2. **Context progression for test prompts**
   - Level 1: "Write a test for this function"
   - Level 2: "Write unit tests covering edge cases"
   - Level 3: "Write BDD-style tests with Given/When/Then"
   - Level 4: Full context with business requirements

### Part 2: Writing Tests for Existing Code (20 min)
**Exercise Options:**
- Beginners: Test model methods
- Intermediate: Test `get_dataset_statistics` with cache mocking
- Advanced: Test `calculate_data_quality_metrics` with pandas data

**AI Prompting Practice:**
- Start with vague prompt → generic test
- Add business context → better test coverage
- Include edge cases → comprehensive test suite

### Part 3: Test-Driven Implementation (15 min)
**Choose one function to implement:**
- `calculate_dataset_size_human_readable`
- `validate_file_extension`
- `is_expired` model method

**Process:**
1. Write tests first (with AI help)
2. Run tests → see them fail
3. Implement function (with AI help)
4. Run tests → see them pass
5. Refactor if needed

### Part 4: Finding and Fixing Bugs with Tests (10 min)
**Use the failing test examples:**
1. Show test that passes incorrectly
2. Write comprehensive test that fails
3. Fix the bug
4. Verify all tests pass

## Key Teaching Points

1. **Context matters for test generation**
   - Business requirements → better test scenarios
   - Edge cases → more robust tests
   - Performance requirements → appropriate test types

2. **Different test types need different prompts**
   - Unit tests: "Test this function in isolation"
   - Integration tests: "Test the workflow end-to-end"
   - BDD tests: "Write Given/When/Then scenarios"

3. **AI helps but doesn't replace thinking**
   - AI generates boilerplate quickly
   - Humans add business logic understanding
   - Review AI-generated tests for completeness

## Success Metrics

Participants should be able to:
- ✅ Generate unit tests using AI with proper context
- ✅ Follow TDD cycle with AI assistance
- ✅ Write tests that reveal bugs
- ✅ Mock external dependencies in tests
- ✅ Distinguish between test types (unit, integration, BDD)