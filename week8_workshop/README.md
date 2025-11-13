# Week 8 Workshop: Effective Testing in the World of LLM Coding Assistants

## 📚 Workshop Materials

This workshop teaches participants how to write effective tests when using AI coding assistants like GitHub Copilot, Cursor, or ChatGPT. Based on the presentation "Effective Testing in the World of LLM Coding Assistants".

### 🎯 Core Message
**Python + LLMs = Double Uncertainty**
- Python's dynamic nature means no compile-time guarantees
- LLMs make assumptions that might be wrong
- Tests are your reality check!

## 📁 Files Included

### For Instructors:
- **`INSTRUCTOR_GUIDE_PRESENTATION.md`** - Complete 60-minute workshop guide aligned with slides
- **`slides.pdf`** - The presentation slides (18 slides)

### For Participants:
- **`PARTICIPANT_HANDOUT.md`** - Quick reference and exercises
- **`slide_examples.py`** - Code examples (with intentional bugs!)
- **`test_examples.py`** - Test demonstrations (good vs bad approaches)

### Workshop Structure:
1. **Opening Hook** (5 min) - Division by zero bug
2. **The Add Function Trap** (10 min) - Why one test isn't enough
3. **Six Testing Principles** (30 min) - With hands-on exercises
4. **AI Prompting Strategies** (10 min) - Good vs bad prompts
5. **Wrap-up** (5 min) - Key takeaways

## 🚀 Quick Start

### Setup:
```bash
# Install pytest
pip install pytest pytest-mock

# Verify the famous bug works
python -c "from slide_examples import add; print(add(2,3))"
# Should print: 4 (that's the bug!)

# Run example tests
pytest test_examples.py -v
```

### For Instructors:
1. Review `INSTRUCTOR_GUIDE_PRESENTATION.md`
2. Open `slides.pdf` for presentation
3. Have `slide_examples.py` ready for live coding
4. Print `PARTICIPANT_HANDOUT.md` for attendees

### For Participants:
1. Follow along with `PARTICIPANT_HANDOUT.md`
2. Write tests in `test_examples.py`
3. Try the exercises in `slide_examples.py`

## 🎓 The 6 Principles

1. **Don't Test the Framework** - Test YOUR logic, not Python
2. **Focus on Behavior** - Test what it does, not how
3. **Beware Over-Mocking** - Mock boundaries only
4. **Single Responsibility** - One test, one behavior
5. **Use Minimal Test Data** - Just enough to prove it works
6. **Red-Green-Refactor** - Fail first, then fix

## 🤖 AI Prompting Cheat Sheet

### ❌ Bad Prompt:
```
"Write tests for this function"
```

### ✅ Good Prompts:
```
"Write a failing test that reveals the division by zero bug"
"Test my validation logic, not the dataclass framework"
"Use minimal test data - just 2 items to prove max() works"
"Mock only external dependencies, test my business logic"
```

## 📊 Workshop Success Metrics

Participants should leave being able to:
- [ ] Write tests that actually fail before fixing bugs
- [ ] Identify framework testing vs logic testing
- [ ] Create focused, single-behavior tests
- [ ] Use appropriate test data (not too much!)
- [ ] Apply Red-Green-Refactor cycle
- [ ] Write effective prompts for AI test generation

## 🔧 Troubleshooting

### Common Issues:
- **Import errors**: Make sure you're in the ResearchHub directory
- **Tests all passing**: Some are supposed to fail! (That's the point)
- **Can't find slides.pdf**: Check the root ResearchHub directory

### Emergency Backup:
All code examples are in the files - no need to type during workshop!

## 📚 Additional Resources

### Key Files to Reference:
- Bad test examples: See comments marked with ❌
- Good test examples: See comments marked with ✅
- Bugs to find: Look for comments with "BUG:"

### The Core Lesson:
When using LLMs to write code, tests aren't optional overhead - they're essential verification that what the AI assumed matches what actually runs.

**Not optional. Not overhead. Essential verification.**

---

## Questions?
This workshop was designed to be practical and hands-on. The best way to learn is to write tests that fail, then make them pass!

Remember: **Write failing tests first!** 🔴 → 🟢