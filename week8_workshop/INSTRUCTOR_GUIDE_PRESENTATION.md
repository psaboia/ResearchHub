# Week 8: Effective Testing in the World of LLM Coding Assistants
## Instructor Guide - Presentation-Aligned Workshop

### Duration: 60 minutes
### Materials: `slides.pdf` + Live Coding Examples

---

## 🎯 Workshop Overview

This workshop teaches participants how to write effective tests when using LLM coding assistants, following the presentation "Effective Testing in the World of LLM Coding Assistants". The key message: **Python + LLMs = Double Uncertainty**, making tests essential for verification.

### Key Files
- **Presentation:** `slides.pdf` (18 slides)
- **Code Examples:** `week8_workshop/slide_examples.py`
- **Test Examples:** `week8_workshop/test_examples.py`

---

## 📊 Slide-by-Slide Workshop Flow

### **Opening Hook (5 minutes)**

#### 📽️ Slide 1: Title
- Welcome participants
- Set expectations: "We'll learn to write tests that actually catch bugs when using AI"

#### 📽️ Slide 2: "Why Spend So Much Effort on Testing?"
**Ask participants:** "Who here uses GitHub Copilot, Cursor, or ChatGPT for coding?"

#### 📽️ Slide 3: "Can You Spot The Bug?"
**Live Demo #1:**
```python
def calculate_efficiency(completed, total):
    return completed / total
```
**Ask:** "What's wrong with this code?"
- Let them spot it (or not)
- Run: `calculate_efficiency(50, 0)` → 💥 ZeroDivisionError

#### 📽️ Slides 4-6: Type Hints Don't Save You
- Show how even with `PositiveInt` type hints, Python can be monkey-patched
- **Key Point:** "Python has no bedrock of trust"

#### 📽️ Slide 5: "It's a Trap!"
**Transition:** "This is why we need comprehensive testing!"

---

### **Part 1: The Add Function Trap (10 minutes)**

#### 📽️ Slide 16: Red-Green-Refactor
**Live Demo #2: The Classic Bug**

```python
# Show this function
def add(a, b):
    return 4  # Bug!
```

**Interactive Exercise:**
1. Ask participant to write a test
2. They probably write: `assert add(2, 2) == 4` ✅ Passes!
3. **The Trap:** "Your test passes! Is the function correct?"
4. Write comprehensive test: `assert add(2, 3) == 5` ❌ Fails!

**Key Lesson:** "One passing test ≠ working code"

---

### **Part 2: Six Principles of Good Testing (30 minutes)**

#### 📽️ Slide 11: Don't Test the Framework
**Time: 5 minutes**

**Show Bad Example:**
```python
def test_user_init():
    user = ResearchUser("alice@uni.edu", 30, "MIT")
    assert user.email == "alice@uni.edu"  # Just testing Python!
```

**Show Good Example:**
```python
def test_normalizes_email():
    user = ResearchUser("  ALICE@UNI.EDU  ", 30, "MIT")
    assert user.email == "alice@uni.edu"  # Testing YOUR logic!
```

**Hands-on:** Participants write tests for email validation logic

---

#### 📽️ Slide 12: Focus on Behavior
**Time: 5 minutes**

**Demo with `load_research_config`:**
- Show brittle test with mocks
- Show robust test with tmp_path
- **Key Point:** "Test what it does, not how it does it"

---

#### 📽️ Slide 13: Beware Over-Mocking
**Time: 5 minutes**

**Live Coding:**
```python
# BAD: Mock everything including YOUR logic
mock_validator.return_value = True  # Your validation never runs!

# GOOD: Only mock external dependencies
mock_db.return_value = {'email': 'not-academic@gmail.com'}
# YOUR validation actually runs and catches this!
```

**Exercise:** Fix an over-mocked test together

---

#### 📽️ Slide 14: Single Responsibility Principle
**Time: 5 minutes**

**Show Mega Test vs Focused Tests:**
- When mega test fails: "What broke?"
- When focused test fails: "Immediately know!"

**Quick Exercise:** Break up a mega test into focused tests

---

#### 📽️ Slide 15: Use Minimal Test Data
**Time: 5 minutes**

**Interactive Question:**
"Does having 100 items prove max() works better than 2 items?"

**Demo:**
- Show test with 16 items → Hard to verify
- Show test with 2 items → Obviously correct!

---

#### 📽️ Slide 16: Red-Green-Refactor (Revisited)
**Time: 5 minutes**

**TDD Live Exercise:** Implement `format_citation` together
1. **RED:** Write failing test first
2. **GREEN:** Implement minimal code
3. **REFACTOR:** Improve implementation

---

### **Part 3: Practical AI Prompting (10 minutes)**

#### 📽️ Slide 17: Practical Prompting Strategies

**Bad Prompt Demo:**
```
"Write tests for this function"
```
Show generic, unhelpful tests from AI

**Good Prompts Demo:**
```
"Write a failing test that reveals the division by zero bug"
"Test my email validation logic, not the dataclass framework"
"Write minimal test data to prove max() works"
```
Show specific, valuable tests from AI

**Hands-on:** Participants prompt AI with good vs bad prompts, compare results

---

### **Part 4: Bug Hunt Challenge (10 minutes)**

#### Live Coding Challenge
**Functions with hidden bugs:**
1. `calculate_h_index` - Empty list bug
2. `parse_publication_date` - Single format bug
3. `check_plagiarism_score` - Case sensitivity bug

**Process:**
1. Groups write comprehensive tests
2. Tests reveal bugs
3. Fix bugs together
4. All tests pass!

---

### **Wrap-up (5 minutes)**

#### 📽️ Slide 18: Why Testing Matters

**Key Messages:**
- Python + LLMs = Double Uncertainty
- Tests are your reality check
- They verify what the LLM assumed matches what actually runs

**The Three Takeaways:**
1. **Write failing tests first** - Proves bugs exist and are fixed
2. **Test YOUR logic, not frameworks** - Focus on business value
3. **Use good prompts** - Get better tests from AI

---

## 🛠️ Setup Instructions

### Before Workshop:
```bash
# Create branch and setup
git checkout week8-presentation
mkdir week8_workshop

# Install dependencies
pip install pytest pytest-mock

# Verify setup
python -c "from week8_workshop.slide_examples import add; print(add(2,3))"
# Should print: 4 (the bug!)
```

### Quick Test Commands:
```bash
# Run specific slide examples
pytest week8_workshop/test_examples.py::TestAddFunction -v

# Run all tests
pytest week8_workshop/test_examples.py -v

# Show failures only
pytest week8_workshop/test_examples.py --tb=short
```

---

## 💡 Teaching Tips

### For Each Principle:
1. **Show the problem** (bad test)
2. **Explain why it's bad** (what could go wrong)
3. **Show the solution** (good test)
4. **Practice together** (hands-on exercise)

### Time Management:
- **Running Fast?** Add more TDD exercises
- **Running Slow?** Skip Slide 14 (Single Responsibility)
- **Mixed Pace?** Pair programming for exercises

### Common Questions:
- **"Why not just use type hints?"** → Show Slide 6-9 (monkey patching)
- **"Isn't mocking everything safer?"** → Show Slide 13 (miss real bugs)
- **"Why write tests if AI wrote the code?"** → Slide 18 (double uncertainty)

---

## 📝 Assessment Checklist

Participants should be able to:
- [ ] Write a test that actually fails before fixing a bug
- [ ] Identify when they're testing framework vs. their logic
- [ ] Create focused, single-behavior tests
- [ ] Use minimal test data effectively
- [ ] Write good prompts for AI test generation
- [ ] Apply Red-Green-Refactor cycle

---

## 🎯 Success Metrics

Workshop succeeds if participants:
1. Understand why "Python + LLMs = Double Uncertainty"
2. Can write tests that reveal hidden bugs
3. Know how to prompt AI for better test generation
4. Leave with practical strategies they'll actually use

---

## 🚀 Quick Reference

### The 6 Principles (One-Liners):
1. **Don't test the framework** - Test YOUR logic
2. **Focus on behavior** - Not implementation
3. **Beware over-mocking** - Mock boundaries only
4. **Single responsibility** - One test, one thing
5. **Minimal data** - Just enough to prove it
6. **Red-Green-Refactor** - Fail first, then fix

### Good AI Prompts:
- ✅ "Write a failing test that reveals the bug"
- ✅ "Test my validation logic, not the framework"
- ✅ "Use minimal test data"
- ✅ "Mock external dependencies only"
- ❌ "Write tests" (too vague!)

---

## 📚 Additional Resources

### Slides Alignment:
- Slides 3-6: Division by zero example
- Slide 11: Don't test framework
- Slide 12: Focus on behavior
- Slide 13: Beware over-mocking
- Slide 14: Single responsibility
- Slide 15: Minimal test data
- Slide 16: Red-Green-Refactor
- Slide 17: Practical prompting
- Slide 18: Why it matters

### Emergency Backup:
If live coding fails, all examples are in:
- `week8_workshop/slide_examples.py` (buggy code)
- `week8_workshop/test_examples.py` (good/bad tests)