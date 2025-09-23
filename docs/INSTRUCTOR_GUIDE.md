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

**DEMONSTRATION 1: Show how business context improves documentation**

Open `research/views.py` line 184 in Cursor, and show these prompts live:

*First attempt (NO context):*
```
Prompt: "Document this function"
```
*Show the AI response - it will be generic and miss business meaning*

*Second attempt (WITH context):*
```
Prompt: "Document the calculate_data_quality_metrics function. This is used in a 
research platform where scientists upload datasets. The function validates data 
quality before researchers share data across institutions. Include what the 
quality grades A-D mean for research data sharing decisions."
```
*Show how AI now includes research-specific context in the documentation*

**DEMONSTRATION 2: Iterative refinement**

Stay with the same function and show this progression:

*Iteration 1:*
```
Prompt: "What does this function do?"
AI Response: [vague overview]
```

*Iteration 2:*
```
Prompt: "What does this function do? Focus on the validation_rules parameter"
AI Response: [better, but still missing details]
```

*Iteration 3:*
```
Prompt: "Explain the validation_rules parameter in calculate_data_quality_metrics.
Show me an example of validation_rules dict that would check:
- Temperature values between -50 and 50
- Email format for researcher_email field"
AI Response: [now gives concrete example you can use]
```

**DEMONSTRATION 3: Importance of output format**

Show the difference:

*Without format specification:*
```
Prompt: "Document this function"
Result: Random format, maybe paragraphs
```

*With format specification:*
```
Prompt: "Document this function with:
- One-line summary
- Args section with parameter types
- Returns section with example output
- Usage example with real values"
Result: Structured, usable documentation
```

**LIVE CODING TIP:** 
- Split your screen: Cursor on left, browser with Django admin on right
- Show the actual models in Django admin while discussing the code
- Copy-paste the AI responses into a new file so participants can see the evolution

### 🐛 Part 2: Bug Identification & Fixing (30 minutes)

**Objective:** Use context to identify and fix bugs

**1. Demonstrate context-aware debugging (10 min)**

**STEP-BY-STEP N+1 QUERY DEMONSTRATION:**

**Step 1: Show the problem**
```bash
# First, in terminal, show Django logging:
docker-compose exec web python manage.py shell
>>> import logging
>>> logging.basicConfig(level=logging.DEBUG)
```

**Step 2: Open the buggy code**
Open `research/views.py` lines 31-49 in Cursor

**Step 3: Try a poor prompt first**
```
Instructor says: "Let's try a vague prompt first"
Type in Cursor: "Fix the performance issue"

Show result: AI gives generic performance tips, misses the actual N+1 problem
```

**Step 4: Add some context**
```
Instructor says: "Now let's add information about what this code does"
Type: "Fix the performance issue in get_project_dashboard. It's too slow when 
we have many datasets"

Show result: AI might mention database queries but not specific solution
```

**Step 5: Provide full context - THE GOOD PROMPT**
```
Instructor says: "Now let's give the AI everything it needs"
Type: "Analyze the get_project_dashboard view for N+1 query problems:
1. Look at line 43 where we access dataset.uploaded_by.username
2. Look at line 44 where we access dataset.uploaded_by.profile.institution.name  
3. Look at line 45 where we call dataset.processing_jobs.count()
4. Check the models in research/models.py to understand relationships
5. Fix using Django's select_related for ForeignKeys and prefetch_related for reverse ForeignKeys
6. Show the complete fixed code"

Show result: AI now provides exact fix with select_related and prefetch_related
```

**Step 6: Test the fix**
```python
# Show the before/after query count:
# Before: 50+ queries for 10 datasets
# After: 3 queries total

# Paste the fixed code and demonstrate the improvement
```

**KEY INSTRUCTOR MOMENTS:**
- Pause after each prompt to discuss what was missing
- Ask participants: "What context would help here?"
- Show the Django Debug Toolbar query count if possible
- Emphasize the progression from vague to specific

**2. Guided practice with different bugs (20 min)**

**INSTRUCTOR SETUP:**
Divide class into 3 groups based on experience level. Walk around and help each group.

**GROUP A - Beginner: Cache Invalidation Bug**

*Location:* `research/views.py` lines 137-162 (get_dataset_statistics)

*What to tell them:*
```
"Your bug: Statistics are cached but never updated when data changes.
Start with: 'Why are my download statistics not updating?'
Build up to include: cache keys, invalidation triggers, Django cache framework"
```

*Expected progression:*
1. "Fix the cache bug" → Too vague
2. "The cache in get_dataset_statistics never updates" → Better
3. "Fix the cache invalidation in get_dataset_statistics. When a dataset is downloaded (line 62), the cache should be cleared. Use cache.delete() with the correct key pattern" → Good!

**GROUP B - Intermediate: Security Bug**

*Location:* `research/views.py` lines 52-70 (download_dataset)

*What to tell them:*
```
"Your bug: Any logged-in user can download any dataset, even private ones.
Start by looking at the models.py to understand the privacy levels.
Think about: Who should access what?"
```

*Expected progression:*
1. "Add security check" → Too vague
2. "Check if user can download dataset" → Better
3. "Add permission check in download_dataset: verify if request.user is the dataset.uploaded_by OR is a collaborator on the project OR has an approved DataAccessRequest. Check the models.py for relationships" → Good!

**GROUP C - Advanced: Race Condition Bug**

*Location:* `research/views.py` lines 73-99 (process_uploaded_file)

*What to tell them:*
```
"Your bug: When two users upload 'data.csv' at the same time, one overwrites the other.
Think about: Unique filenames, timestamps, UUID"
```

*Expected progression:*
1. "Fix the file upload" → Too vague
2. "Make filenames unique" → Better  
3. "Fix race condition in process_uploaded_file: Use UUID or timestamp in filename. Import uuid, change line 80 to: filename = f'{project_id}_{uuid.uuid4()}_{file.name}'. Also ensure directory exists with os.makedirs()" → Good!

**INSTRUCTOR CHECKPOINTS:**
Every 5 minutes, ask each group:
- "What context did you add to your prompt?"
- "What information from models.py helped?"
- "Show me your prompt evolution"

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