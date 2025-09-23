# Instructor Guide - Week 3: Context-Aware Prompt Engineering Workshop

## Pre-Workshop Setup (15 min before)
- Ensure all participants have:
  - Cursor IDE or similar AI coding tool installed
  - Docker Desktop running
  - GitHub account
  - Terminal/command line access

## Workshop Flow (90 minutes total)

### 🎯 Introduction (10 minutes)

**1. Welcome & Context Setting**
```
"Today we'll learn how to effectively communicate with AI coding assistants. 
You'll work with a real production-like codebase that has intentional bugs.
The goal is to learn how providing better context leads to better AI responses."
```

**2. Explain the Scenario**
```
"ResearchHub is a scientific data management platform used by multiple universities.
It has real-world problems: performance issues, security bugs, and missing documentation.
Your job is to use AI to understand and fix these issues."
```

**3. Quick Demo**
Show the difference between:
- Poor prompt: "Fix the bug"
- Good prompt: "Analyze the get_project_dashboard function for N+1 query issues considering Django ORM relationships"

### 🚀 Setup Phase (10 minutes)

**Have participants run:**
```bash
# 1. Clone repository
git clone https://github.com/psaboia/ResearchHub.git
cd ResearchHub

# 2. Start services
docker-compose up -d

# 3. Create database
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate

# 4. Load test data
docker-compose exec web python manage.py setup_test_data
```

**Verify everyone can access:**
- http://localhost:8000/admin/ (login: admin/admin123)

### 📚 Part 1: Documentation Generation (30 minutes)

**Objective:** Learn the codebase by generating documentation

**1. Introduce the task (5 min)**
```
"First, we need to understand this codebase. We'll use AI to generate documentation
for complex functions. This helps us learn the system before fixing bugs."
```

**2. Guide first documentation attempt (10 min)**

Have them open `research/views.py` in Cursor and try:

**Poor prompt example:**
```
"Document this function"
```

**Better prompt example:**
```
"Generate comprehensive documentation for the calculate_data_quality_metrics function 
including:
- Purpose and business context
- Parameter descriptions with types
- Return value structure with example
- How it fits into the research data workflow"
```

**3. Let them practice (15 min)**

Assign each participant a function to document:
- Group A: `calculate_data_quality_metrics` (lines 184-261)
- Group B: `process_research_workflow` (lines 265-375)
- Group C: `get_project_dashboard` (lines 31-49)

**Key Teaching Points:**
- Show how including "business context" improves documentation
- Demonstrate iterative refinement
- Explain importance of specifying output format

### 🐛 Part 2: Bug Identification & Fixing (30 minutes)

**Objective:** Use context to identify and fix bugs

**1. Demonstrate context-aware debugging (10 min)**

Show the N+1 query problem together:

```python
# File: research/views.py, lines 31-49
# This is the buggy code with N+1 problem
```

**Poor prompt:**
```
"Fix the performance issue"
```

**Good prompt:**
```
"Analyze the get_project_dashboard view for N+1 query problems. 
Consider:
- The Django models in research/models.py
- How datasets relate to projects and users
- Django ORM optimization techniques like select_related and prefetch_related
Show the fixed code with explanation."
```

**2. Guided practice with different bugs (20 min)**

Assign bugs to groups:
- **Beginner**: Cache invalidation bug (lines 137-162)
  - Prompt hint: "Check when cache should be invalidated after data access"
  
- **Intermediate**: Security bug (lines 52-70)
  - Prompt hint: "Consider multi-institutional access controls from the models"
  
- **Advanced**: Race condition (lines 73-99)
  - Prompt hint: "Think about concurrent uploads with same filename"

### 🎨 Part 3: Iterative Refinement (15 minutes)

**Objective:** Practice improving prompts based on AI responses

**Exercise: The Refinement Challenge**

Start with vague prompt:
1. "Fix the search function"

Guide them to refine:
2. "Fix the SQL injection vulnerability in search_datasets"

Further refine:
3. "Fix the SQL injection vulnerability in search_datasets function on lines 166-180. Use Django ORM's Q objects for safe queries instead of raw SQL"

**Key Points:**
- Each iteration adds more context
- Specific line numbers help
- Mentioning the solution approach guides AI better

### 📊 Wrap-up & Best Practices (10 minutes)

**1. Review key learnings:**
- Context is crucial (surrounding code, business logic, frameworks used)
- Be specific about what you want
- Iterate and refine your prompts
- Reference specific files and line numbers

**2. Show the prompt evolution:**
```
Vague → Specific → Contextual → Prescriptive
```

**3. Real-world application:**
```
"In your daily work:
- Always provide business context
- Include error messages completely
- Reference related files
- Specify desired output format"
```

## Facilitator Tips

### Common Issues & Solutions

**Docker not starting:**
```bash
# Check if ports are in use
lsof -i :8000
lsof -i :5432
# Kill processes if needed
```

**Can't access admin:**
- Ensure migrations were run
- Check docker-compose logs web

**AI not giving good responses:**
- Encourage adding more context
- Show them the models.py file for relationships
- Suggest including error messages

### Discussion Prompts

**After Documentation Phase:**
"What information did the AI need to create good documentation?"

**After Bug Fixing:**
"How did understanding the models help with fixing bugs?"

**After Refinement:**
"What pattern do you see in effective prompts?"

### Assessment Ideas

**Quick Check:** Have participants fix one bug independently and share their prompts

**Advanced Challenge:** Give them a new bug not in the guide:
- Create a new API endpoint
- Add validation to existing function
- Optimize a database query

### Key Messages to Reinforce

1. **Context includes:**
   - File structure
   - Related models
   - Business requirements
   - Framework conventions

2. **Good prompts are:**
   - Specific about the problem
   - Include relevant context
   - Specify desired output
   - Reference exact locations

3. **Iteration is normal:**
   - First prompt rarely perfect
   - Each response teaches you what to add
   - Refine based on AI's questions

## Time Management

- **Too fast?** Add the SQL injection bug fix exercise
- **Too slow?** Skip the refinement exercise, focus on main bugs
- **Mixed pace?** Pair faster participants with slower ones

## Success Metrics

Participants should be able to:
✅ Generate meaningful documentation using context
✅ Identify the importance of providing file relationships
✅ Fix at least one bug using context-aware prompts
✅ Demonstrate prompt iteration and refinement

## Post-Workshop

Share these resources:
- GitHub repo link
- This guide for reference
- Encourage practicing with their own codebases
- Suggest creating a "prompt library" for common tasks