# Week 8 Workshop: Participant Setup Guide

## 🚀 Initial Setup (Do this before or at start of workshop)

### Step 1: Clone the Repository
```bash
# Clone the ResearchHub repository
git clone https://github.com/psaboia/ResearchHub.git

# Navigate to the repository
cd ResearchHub

# Switch to the workshop branch
git checkout week8-presentation
```

### Step 2: Install Requirements
```bash
# Install pytest for running tests
pip install pytest pytest-mock
```

### Step 3: Navigate to Workshop Directory
```bash
# Go to the workshop folder
cd week8_workshop
```

### Step 4: Verify Setup
```bash
# Check that the bug exists (this is intentional!)
python -c "from slide_examples import add; print('add(2,3) =', add(2,3))"
# Should output: add(2,3) = 4  (That's the bug!)

# Try running the exercises (some will pass when they shouldn't!)
pytest exercises.py::TestAddFunction::test_add -v
# Should show: PASSED (but the function is broken!)
```

---

## 📁 Files You'll Use

- **`exercises.py`** - Your main work file (fix the bad tests here!)
- **`slide_examples.py`** - Functions with bugs to test
- **`test_solutions.py`** - Reference solutions (check after each exercise)
- **`PARTICIPANT_HANDOUT.md`** - Quick reference for principles

---

## 🎯 Your Workflow For Each Exercise

### 1️⃣ Find the Exercise
Open `exercises.py` and look for the exercise number matching the current slide.

### 2️⃣ Read the FIXME
Each exercise has a `FIXME` comment explaining what's wrong.

### 3️⃣ Follow the TODO
The `TODO` comments guide you on how to fix it.

### 4️⃣ Run Your Test
```bash
# Run specific exercise (replace TestClassName)
pytest exercises.py::TestClassName -v
```

### 5️⃣ Compare with Solution
After fixing, check `test_solutions.py` for the best practice approach.

---

## 🛠️ Helpful Commands

```bash
# Run a specific test class
pytest exercises.py::TestAddFunction -v

# Run all exercises
pytest exercises.py -v

# See why tests fail
pytest exercises.py --tb=short

# Run solutions to see correct approach
pytest test_solutions.py -v

# Get help on pytest
pytest --help
```

---

## 📝 Quick Tips

1. **Tests should FAIL first** - If fixing bugs, your test should fail to prove the bug exists
2. **Read the comments** - FIXME and TODO guide you
3. **Less is more** - Use minimal test data
4. **Mock boundaries only** - Don't mock your own logic
5. **One test, one thing** - Each test should verify one behavior

---

## ❓ Troubleshooting

**Import Error?**
- Make sure you're in the `week8_workshop` directory
- Check that `slide_examples.py` exists

**All tests passing?**
- That might be the problem! Bad tests pass when they shouldn't
- Your job is to make them fail (to reveal bugs) or test properly

**Can't find exercise?**
- Exercises are numbered to match the flow
- Ask instructor which exercise we're on

---

## 🎓 Ready to Start!

You're all set! Follow along with the instructor and remember:
- **Experience the problem first** (run the bad test)
- **Fix it yourself** (learn by doing)
- **Compare with best practice** (check solutions after)

Good luck and happy testing! 🚀