# Week 8 Workshop: Effective Testing with LLM Coding Assistants
## Participant Handout

---

## 🎯 Key Concept
**Python + LLMs = Double Uncertainty**

Tests are your reality check - they verify what the LLM assumed matches what actually runs.

---

## 🔍 Workshop Exercises

### Exercise 1: The Add Function Trap
```python
def add(a, b):
    return 4  # Bug!

# Your test here:
```

**Question:** Does one passing test mean the function works?

---

### Exercise 2: Don't Test the Framework
```python
@dataclass
class ResearchUser:
    email: str
    age: int

    def __post_init__(self):
        self.email = self.email.strip().lower()
        # More validation...

# Write a test for YOUR logic, not Python's dataclass:
```

---

### Exercise 3: TDD - Format Citation
```python
def format_citation(author, year, title, journal=None):
    """
    Format research citation in APA style.
    Book: "Smith, J. (2023). Research Methods."
    Journal: "Smith, J. (2023). New Discovery. Nature."
    """
    pass  # Implement using TDD

# Step 1: Write failing test first
# Step 2: Implement minimal code
# Step 3: Refactor if needed
```

---

### Exercise 4: Bug Hunt
Find the bugs by writing comprehensive tests:

```python
def calculate_h_index(citations_list):
    """h-index = largest h where h papers have ≥h citations"""
    citations_list.sort(reverse=True)  # BUG: What if list is empty?
    h_index = 0
    for i, citations in enumerate(citations_list):
        if citations >= i + 1:
            h_index = i + 1
    return h_index

def parse_publication_date(date_string):
    """Parse dates from various formats"""
    from datetime import datetime
    return datetime.strptime(date_string, "%Y-%m-%d")  # BUG: Only one format!

def check_plagiarism_score(text1, text2):
    """Calculate text similarity percentage"""
    words1 = set(text1.split())  # BUG: Case sensitive!
    words2 = set(text2.split())
    overlap = len(words1.intersection(words2))
    total = len(words1.union(words2))
    return (overlap / total) * 100
```

---

## ✅ The 6 Principles of Good Testing

### 1. Don't Test the Framework
❌ **Bad:** Testing that Python/libraries work
✅ **Good:** Testing YOUR business logic

### 2. Focus on Behavior, Not Implementation
❌ **Bad:** Mock everything, test nothing
✅ **Good:** Test what it does, not how

### 3. Beware Over-Mocking
❌ **Bad:** Mock your own logic
✅ **Good:** Mock only external dependencies

### 4. Single Responsibility Principle
❌ **Bad:** One mega test for everything
✅ **Good:** One test per behavior

### 5. Use Minimal Test Data
❌ **Bad:** 100 items to test max()
✅ **Good:** 2 items prove it works

### 6. Red-Green-Refactor
🔴 **Red:** Write failing test first
🟢 **Green:** Make it pass
♻️ **Refactor:** Improve the code

---

## 🤖 AI Prompting Strategies

### ❌ Bad Prompts:
- "Write tests for this function"
- "Add unit tests"
- "Test this code"

### ✅ Good Prompts:

**For finding bugs:**
```
"Write a comprehensive test that checks edge cases like empty lists,
zero values, and None inputs"
```

**For testing YOUR logic:**
```
"Write tests for my email validation logic. Don't test that the
dataclass initializes - test that emails are normalized to lowercase
and invalid formats are rejected"
```

**For behavior testing:**
```
"Write tests that verify the behavior of this function using real files,
not mocks. The test should survive refactoring from open() to Path.read_text()"
```

**For minimal data:**
```
"Write a test using the minimum data needed to prove the max() function
works correctly - just 2 items, not a large dataset"
```

**For TDD:**
```
"Write a failing test first for a function that formats citations in APA style.
Then show the minimal implementation to make it pass."
```

**For mocking correctly:**
```
"Write a test that mocks only the database connection, but actually runs
my email validation logic to ensure academic domains are required"
```

---

## 🛠️ Quick Commands

### Run Tests:
```bash
# Run all tests
pytest test_examples.py -v

# Run specific test
pytest test_examples.py::TestAddFunction -v

# See why tests fail
pytest test_examples.py --tb=short
```

### Test Organization:
```python
class TestFeatureName:
    def test_handles_normal_case(self):
        # Happy path

    def test_handles_edge_case(self):
        # Empty, None, zero

    def test_rejects_invalid_input(self):
        # Error conditions
```

---

## 📝 Notes Section

### Key Takeaways:

1. _________________________________

2. _________________________________

3. _________________________________

### My Action Items:

- [ ] ______________________________

- [ ] ______________________________

- [ ] ______________________________

---

## 🎓 Remember

**Tests are not optional when using LLMs.**

They're your safety net in a world of double uncertainty.

Write failing tests first, then make them pass!