# Instructor Guide - Week 3: Context-Aware Prompt Engineering Workshop (Revised)

## Quick Links to Detailed Guides
- [Documentation Exercise](./DOCUMENTATION_EXERCISE.md) - Generating documentation
- [N+1 Query Demonstration](./N1_QUERY_DEMONSTRATION.md) - Performance optimization
- [Cache Bug Demonstration](./CACHE_BUG_DEMONSTRATION.md) - Cache invalidation
- [Security Bug Demonstration](./SECURITY_BUG_DEMONSTRATION.md) - Authorization vulnerability

## Workshop Structure

### 🎯 Introduction

#### Welcome & Context Setting (1 minute)
```
"Today we'll learn how to effectively communicate with AI coding assistants.
You'll work with a real production-like codebase that has intentional bugs.
The goal is to learn how providing better context leads to better AI responses.
While I explain the scenario, please start cloning the repository - you'll need it soon!"
```

#### The Scenario (2 minutes)
**ResearchHub**: A scientific data management platform where researchers from universities worldwide:
- Upload and share research datasets (CSV, Excel files with experimental data)
- Collaborate on projects across institutions (MIT, Stanford, Oxford, etc.)
- Request access to sensitive data with proper authorization
- Track data processing jobs and quality metrics
- Monitor usage statistics and generate reports

**The Challenge**: The platform has grown from 10 to 1000+ datasets, and now has:
- Performance bottlenecks causing dashboard timeouts
- Security vulnerabilities exposing private research data
- Cache invalidation issues showing incorrect statistics

#### 🚀 Setup & Verification Phase (10 minutes)

> **📝 Instructor Note:**
> - Run these commands 15 minutes before workshop to ensure everything works
> - Have mentors ready to help with setup issues
> - Display the setup checklist on screen

```bash
# If not already cloned (some may have done this beforehand):
git clone https://github.com/psaboia/ResearchHub.git
cd ResearchHub

# Start services if not running:
docker compose up -d
docker compose exec web python manage.py migrate
docker compose exec web python manage.py setup_test_data

# Verify setup is correct:
docker compose ps  # Should show 4 containers running

# Run verification script:
docker compose exec web python workshop_scripts/verify_setup.py
# Should show: ✅ SETUP COMPLETE - Ready for workshop!

# Open in your AI IDE (Cursor, VS Code, etc.)
```

### ✅ Setup Checklist:
- [ ] Docker containers running (4 containers)
- [ ] Verification script shows "✅ SETUP COMPLETE"
- [ ] Can access http://localhost:8000/admin/ (admin/admin123)
- [ ] Repository open in Cursor/AI IDE

#### Quick Cursor Context Demo (5 minutes)

> **📝 Live Demo - Show the Power of Context:**
> 1. **Open Cursor** with the ResearchHub repository
> 2. **See the context window:** ask `what do you have in your context window?`
> 3. **Ask vague question** with no files open: "How do I fix the performance issue?"
>    - Show how AI go search in the whole codebase, which can take long time and give a generic advice
> 4. **Open research/views.py** and ask same question
>    - Show how AI now mentions specific functions
> 5. **Open terminal** with error output and ask again (click on *`@Add context`* to add the *`terminal`* first)
>    - Show how AI now identifies the exact problem
> 5. **Key takeaway**: "The AI sees what you see - arrange your workspace strategically!"

**Cursor's Automatic Context Features:**
- **Open files** → AI reads them automatically
- **Terminal output** → AI sees errors and logs
- **Multiple tabs** → AI understands relationships
- **Linter errors** → AI knows what's broken

### 📚 Part 1: Documentation Generation (20 minutes)

**[Open DOCUMENTATION_EXERCISE.md](./DOCUMENTATION_EXERCISE.md)**

#### Objectives
- Learn the codebase through documentation
- Understand how context improves AI output
- Practice iterative prompt refinement

#### Structure
1. **Poor Documentation Demo** 
   - Show `calculate_data_quality_metrics` function
   - Use vague prompt: "Document this"
   - Analyze weak output together

2. **Progressive Context Building** 
   - Add business context
   - Include parameter details
   - Request examples
   - Show improvement at each step

3. **Complex Function Challenge** 
   - Groups document `process_research_workflow`
   - Compare different approaches
   - Share best results

#### Key Teaching Points
- Context transforms generic docs into useful guides
- Business understanding > technical details
- Examples make documentation actionable

### 🐛 Part 2: Bug Fixing Exercises (25-30 minutes)

> **📝 Key Teaching Strategy:** Each bug demonstration includes an **embedded context demo** at the critical moment!
>
> **The Pattern:**
> 1. Participants investigate the problem
> 2. **YOU demonstrate bad context** (vague prompt → generic AI response)
> 3. **YOU guide them to set up good context** (specific files + terminal)
> 4. **THEY use AI with good context** → get specific, actionable solution
>
> This just-in-time demonstration is much more impactful than a separate session.

> **📝 Instructor Note:** Participants choose ONE bug scenario to work on individually.
> All scenarios include the context demonstration at the natural teaching moment.

#### Available Bug Exercises:

##### 🔍 N+1 Query Problem (Performance)
**[Open N1_QUERY_DEMONSTRATION.md](./N1_QUERY_DEMONSTRATION.md)**
- **Time:** 15-20 minutes
- **Complexity:** Medium
- **Location:** `views.py` lines 30-46
- **Issue:** Dashboard makes 32 queries for 10 datasets, causing timeouts
- **Key Learning:** Django ORM optimization with select_related/prefetch_related
- **Best for:** Groups wanting to understand performance debugging

##### 💾 Cache Invalidation Bug
**[Open CACHE_BUG_DEMONSTRATION.md](./CACHE_BUG_DEMONSTRATION.md)**
- **Time:** 10-15 minutes
- **Complexity:** Lower
- **Location:** `views.py` lines 126-149
- **Issue:** Statistics show outdated data to users
- **Impact:** Researchers see wrong download counts for their papers
- **Key Learning:** Cache invalidation strategies
- **Best for:** Groups new to caching concepts

##### 🔒 Security Vulnerability (Authorization)
**[Open SECURITY_BUG_DEMONSTRATION.md](./SECURITY_BUG_DEMONSTRATION.md)**
- **Time:** 10-15 minutes
- **Complexity:** Medium
- **Location:** `views.py` lines 51-65
- **Issue:** Private research data accessible to unauthorized users
- **Impact:** HIPAA/GDPR violation risk, confidential data exposure
- **Key Learning:** Authentication vs Authorization
- **Best for:** Groups interested in security

### 🔄 Part 3: Discussion & Wrap-up (10-15 minutes)

> **📝 Instructor Note:** Keep this brief but impactful. Participants should leave with clear takeaways.

#### Guided Discussion Questions:
1. **"What surprised you most about the context demonstration?"**
2. **"How will you change your AI workspace setup after today?"**
3. **"What's one context strategy you'll use in your own projects?"**

#### Quick Success Review:
- **Ask participants:** "Did your Part 2 fixes work? Any issues?"
- **Verify success criteria:**
  - Performance: 32 queries → 4-5 queries
  - Cache: Statistics update immediately
  - Security: Unauthorized access blocked

> **📝 Additional Security Bug Note:**
> If time permits and participants are interested, mention the SQL injection vulnerability in `search_datasets` (lines 153-165):
> - **Problem:** `f"... WHERE name LIKE '%{search_term}%'"` - Direct string interpolation
> - **Fix:** Use Django ORM `.filter(name__icontains=search_term)` instead
> - **Context:** Same setup principles apply

### 📊 Wrap-up & Best Practices

#### Review the Context Progression

Draw on whiteboard:
```
No Context → Some Context → Good Context → Excellent Context
    ↓             ↓              ↓               ↓
 Useless      Generic         Helpful        Perfect
```

#### Cursor Context Management Mastery

**The Context Pyramid** (draw on board):
```
        🎯 PERFECT FIX
       /             \
      /   Full Context \
     /_________________\
    /   Multi-File +    \
   /    Terminal Output  \
  /_______________________\
 /    Single File Open    \
/_________________________\
    No Context (Just Prompt)
```

#### Key Takeaways

1. **Cursor's Automatic Context Magic**
   - **Open files** = AI knowledge base
   - **Terminal output** = Problem evidence
   - **Multiple tabs** = Relationship understanding
   - **Linter/errors** = Debugging hints
   - **No copy/paste** = Everything visible is included

2. **Context Components for Success**
   - File locations and line numbers
   - Related code and models
   - Business requirements
   - Framework conventions
   - Terminal output and errors

3. **Progressive Prompt Pattern**
   ```
   Vague → Specific → Located → Contextual → Complete
   ```

4. **Workspace Setup Best Practices**
   - Open relevant files before prompting
   - Keep terminal visible for errors/output
   - Arrange windows to show relationships
   - Start fresh conversations when context cluttered
   - Check context indicator before prompting

## Instructor Tips & Troubleshooting

### Time Management
- **Running Fast?** Add the SQL injection exercise or explore all three bugs
- **Running Slow?** Focus on N+1 and one other bug
- **Mixed Pace?** Pair faster with slower participants

### Common Issues & Solutions

#### Docker Problems
```bash
# Ports in use
lsof -i :8000
kill -9 [PID]

# Restart services
docker compose down
docker compose up -d
```

#### Database Issues
```bash
# Reset database
docker compose exec web python manage.py flush --no-input
docker compose exec web python manage.py migrate
docker compose exec web python manage.py setup_test_data
```

#### Can't Find Bug
- Direct them to line numbers
- Show them the comment markers "# BUG"
- Pair with another participant

### Discussion Prompts by Section

#### After Documentation
"What information did the AI need to create useful documentation?"

#### After Bug Fixing
"How did understanding the models help with fixing bugs?"

#### After Context Demo
"What difference did you notice when you added more files to your workspace?"

#### After Progressive Prompting
"Which level of context gave you the best results? Why?"

#### After Refinement
"What pattern do you see in effective prompts?"

## Assessment Checklist

Participants should be able to:
- [ ] Generate meaningful documentation using context
- [ ] Identify the importance of providing file relationships
- [ ] Fix at least one bug using context-aware prompts
- [ ] Demonstrate prompt iteration and refinement
- [ ] Explain difference between vague and contextual prompts

## Workshop Materials

### For Participants
- Repository: https://github.com/psaboia/ResearchHub
- Quick Start: [QUICKSTART.md](./QUICKSTART.md)
- Bug Guides: Share specific guides as needed

### For Instructors
- This guide
- Individual bug demonstration guides
- Test scripts in repository

## Post-Workshop

### Follow-up Resources
- Encourage practicing with own codebases
- Create a prompt library for common tasks
- Join AI coding communities

### Feedback Questions
1. Which bug was most instructive?
2. What context type was most valuable?
3. How will you apply this to your work?

## Quick Reference Card

### Prompt Quality Ladder
```
Level 1: "Fix bug"
Level 2: "Fix performance issue"
Level 3: "Fix N+1 query in dashboard view"
Level 4: "Fix N+1 in lines 31-49 using select_related"
Level 5: [Full context with models, examples, framework]
```

### Cursor Context Setup Checklist
□ **Open relevant files** - views.py, models.py, etc.
□ **Show terminal output** - Errors, logs, test results
□ **Arrange windows** - Both functions visible if needed
□ **Fresh conversation** - Start new if context cluttered
□ **Check context limit** - Look at indicator before prompting

### Context Categories
- **Location**: Files, line numbers, function names
- **Relationships**: Models, dependencies, imports
- **Business**: Purpose, requirements, constraints
- **Technical**: Framework, patterns, conventions
- **Examples**: Input/output, edge cases, errors
- **Evidence**: Terminal output, error messages

### Magic Phrases That Improve AI Responses
- "Show the complete fixed code"
- "Include all necessary imports"
- "The terminal shows..." (reference visible output)
- "Using the models shown in models.py..."
- "Consider edge cases like..."
- "Use [specific framework] best practices"

## Success Metrics

### Minimum Success (All Participants)
- Fix one bug with AI assistance
- Understand context importance
- Can iterate on prompts

### Good Success (Most Participants)
- Fix two different bug types
- Generate quality documentation
- Explain context categories

### Excellent Success (Some Participants)
- Fix all three bug types
- Help others with prompts
- Create own context templates