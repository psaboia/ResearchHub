# Workshop Guide - Week 3: Context-Aware Prompt Engineering

## Overview
Today you'll learn how to effectively communicate with AI coding assistants using a production-like codebase. You'll work with ResearchHub, a scientific data management platform, to fix performance and security issues using AI assistance.

## Setup Instructions

### 1. Clone and Setup
```bash
git clone https://github.com/psaboia/ResearchHub.git
cd ResearchHub

# Start services
docker compose up -d
docker compose exec web python manage.py migrate
docker compose exec web python manage.py setup_test_data

# Verify setup
docker compose exec web python workshop_scripts/verify_setup.py
# Should show: ✅ SETUP COMPLETE - Ready for workshop!
```

### 2. Access the Application
- Admin interface: http://localhost:8000/admin/
- Login: admin / admin123
- Test users: alice, bob, charlie / testpass123

## The ResearchHub Platform

ResearchHub is a platform where researchers from universities worldwide:
- Upload and share research datasets (CSV, Excel files)
- Collaborate on projects across institutions (MIT, Stanford, Oxford)
- Request access to sensitive data with proper authorization
- Track data processing jobs and quality metrics
- Monitor usage statistics and generate reports

The platform has grown from 10 to 1000+ datasets and now has performance and security issues that need fixing.

## Workshop Exercises

### Part 1: Documentation Generation

**Objective:** Learn the codebase through documentation while practicing context-aware prompting.

**Your Task:**
1. Open `research/views.py` in your AI IDE
2. Find the `calculate_data_quality_metrics` function (around line 183)
3. This function lacks documentation - use AI to generate comprehensive documentation

**Progressive Prompting Exercise:**
- Start with vague prompts and observe the output quality
- Gradually add more context and specificity
- Compare the results at each stage

**Success Criteria:**
- AI-generated documentation explains the function's purpose
- Documents all parameters and return values
- Includes usage examples
- Explains the quality scoring algorithm

### Part 2: Bug Identification & Fixing

You'll work on one of three bug scenarios. Each follows the same pattern: investigate → understand → fix → test.

#### Option A: Performance Crisis - N+1 Query Problem

**The Scenario:**
Users report the ResearchHub dashboard takes 5+ seconds to load when displaying project data. The DevOps team noticed database CPU usage spikes whenever the dashboard is accessed. This started after the platform grew from 10 to 100+ datasets per project.

**Step 1: Investigate the Performance Issue**
```bash
# First, understand the data structure
docker compose exec web python workshop_scripts/n1_step1_review_data.py

# Then investigate the performance problem
docker compose exec web python workshop_scripts/n1_investigate_dashboard_performance.py
```

**Expected Investigation Results:**
```
📊 PERFORMANCE METRICS:
  • Execution time: ~50ms
  • Total queries executed: 32
  • Queries per dataset: 3.0

📈 IMPACT AT SCALE:
  Current (10 datasets): 32 queries, ~50ms
  With 100 datasets: ~302 queries, ~500ms
  With 1000 datasets: ~3002 queries, ~5000ms ⏰ TIMEOUT!

⚠️ PROBLEM IDENTIFIED: N+1 QUERY PATTERN
```

**Step 2: Set Up Your Context for AI Assistance**
1. **Open `research/views.py`** → Navigate to `get_project_dashboard` function (lines 29-46)
2. **Open `research/models.py`** → So AI understands Dataset/ResearchProject relationships
3. **Keep terminal visible** → AI needs to see the "32 queries" problem

**Step 3: Fix with AI**
Use progressively specific prompts:
- Basic: "Fix the performance issue in this function"
- Better: "Optimize the N+1 query problem in get_project_dashboard"
- Best: "Fix the N+1 queries by using select_related/prefetch_related for uploaded_by, processing_jobs, and access_requests"

**Step 4: Test Your Fix**
```bash
# Re-run investigation - should show ~4-5 queries instead of 32
docker compose exec web python workshop_scripts/n1_investigate_dashboard_performance.py
```

**Step 5: Compare with Reference Solution (Optional)**
```bash
# See a working reference implementation to compare approaches
docker compose exec web python workshop_scripts/n1_step3_fixed_version.py
```

**Why compare?**
- **If your solution works perfectly**: See if there are additional optimizations or approaches you missed
- **If your solution partially works**: Identify what needs to be improved
- **Learning opportunity**: Understanding different ways to solve the same problem

#### Option B: Cache Disaster - Stale Statistics

**The Scenario:**
During a board meeting, the CEO notices the dashboard shows only 15 downloads for the flagship dataset. However, the analytics team confirms the database has 35 downloads - recent conference activity isn't reflected. Statistics cache isn't invalidated when new downloads occur.

**Step 1: Demonstrate the Cache Problem**
```bash
docker compose exec web python workshop_scripts/cache_demonstrate_problem.py
```

**Expected Investigation Results:**
```
📊 DISCREPANCY ANALYSIS:
  Dashboard shows: 15 downloads
  Database has: 35 downloads
  MISSING: 20 downloads not shown!
  ERROR RATE: 57.1% of data hidden

💰 BUSINESS IMPACT:
  • CEO's credibility damaged in board meeting
  • Investors questioning data accuracy
  • Conference success not reflected in metrics
```

**Step 2: Set Up Your Context for AI Assistance**
1. **Open `research/views.py`** → Find both `get_dataset_statistics` (lines 135-161) and `download_dataset` (lines 49-69)
2. **Keep terminal visible** → AI needs to see the cache discrepancy (35 in DB, 15 in cache)

**Step 3: Fix with AI**
Use progressively specific prompts:
- Basic: "Fix the cache issue"
- Better: "The statistics cache isn't being invalidated when datasets are downloaded"
- Best: "Add cache invalidation to download_dataset to clear the dataset_stats cache when data changes"

**Step 4: Test Your Fix**
```bash
docker compose exec web python workshop_scripts/cache_test_your_fix.py
```

**Step 5: Compare with Reference Solution (Optional)**
```bash
# See a working reference implementation to compare approaches
docker compose exec web python workshop_scripts/cache_fixed_version.py
```

#### Option C: Data Breach - Missing Authorization

**The Scenario:**
A security audit reveals that any logged-in user can download private research datasets, including confidential drug trials and patient data. A researcher from a competing institution could access proprietary research worth millions just by creating an account.

**Step 1: Demonstrate the Security Breach**
```bash
docker compose exec web python workshop_scripts/security_demonstrate_breach.py
```

**Expected Investigation Results:**
```
🎯 TARGET DATASET:
  Name: Confidential Drug Trial Results
  Privacy Level: PRIVATE
  Owner: bob

🔍 CHECKING LEGITIMATE ACCESS:
  ✓ Is dataset owner? False
  ✓ Is project collaborator? False
  ✓ Has approved access request? False
  ✓ Is dataset public? False

📊 VERDICT: User SHOULD have access? NO

❌❌❌ CRITICAL SECURITY BREACH CONFIRMED! ❌❌❌
```

**Step 2: Set Up Your Context for AI Assistance**
1. **Open `research/views.py`** → Navigate to `download_dataset` function (lines 49-69)
2. **Open `research/models.py`** → AI needs to understand Dataset, DataAccessRequest, ResearchProject relationships
3. **Keep terminal visible** → AI needs to see the unauthorized access confirmation

**Step 3: Fix with AI**
Use progressively specific prompts:
- Basic: "Add security to this function"
- Better: "Add authorization checks to prevent unauthorized dataset downloads"
- Best: "Add permission checks: user must be dataset owner, project collaborator, have approved access request, or dataset must be public. Raise PermissionDenied if unauthorized."

**Step 4: Test Your Fix**
```bash
docker compose exec web python workshop_scripts/security_test_your_fix.py
```

**Step 5: Compare with Reference Solution (Optional)**
```bash
# See a working reference implementation to compare approaches
docker compose exec web python workshop_scripts/security_fixed_version.py
```

### Part 3: Discussion & Reflection

**Group Discussion Topics:**
- What surprised you most about the context quality differences?
- How will you change your AI workspace setup after today?
- What context management strategies will you use in your own projects?
- Which bug scenario taught you the most and why?

**Success Criteria Review:**
Verify your Part 2 solutions achieved these goals:
- **Performance**: Query count drops from 32 to ~4-5 queries
- **Cache**: Statistics update immediately after downloads
- **Security**: Unauthorized access is properly blocked with clear error messages

## Key Learning Points

### Context-Aware Prompting Best Practices

1. **Start with the Right Files Open**
   - Open relevant source files in your IDE
   - AI sees all open files automatically
   - Include related models, not just the problem function

2. **Include Terminal Output**
   - Show AI any error messages or logs
   - Include performance metrics or test results
   - Add terminal context using @Add context in Cursor

3. **Be Specific in Your Requests**
   - Instead of "fix this bug" → "optimize these database queries to avoid N+1 problem"
   - Instead of "add security" → "add authorization checks to verify user can download this dataset"
   - Instead of "document this" → "write comprehensive documentation including parameters, return values, and usage examples"

4. **Iterate and Refine**
   - Start with basic prompts to understand the problem
   - Add more context and specificity in follow-up prompts
   - Don't hesitate to ask for clarification or improvements

### Technical Concepts Covered

- **N+1 Query Problem:** Understanding and fixing inefficient database queries
- **Django ORM Optimization:** Using select_related() and prefetch_related()
- **Cache Invalidation:** Proper cache management in web applications
- **Authorization vs Authentication:** Implementing proper access controls
- **Performance Profiling:** Using tools to identify bottlenecks

## Wrap-up

By the end of this workshop, you should understand how providing better context to AI coding assistants leads to more accurate, specific, and useful solutions. The key is to arrange your development environment strategically so the AI has all the information it needs to help you effectively.

## Additional Resources

**Essential Tools:**
- **[Django Debug Toolbar](https://django-debug-toolbar.readthedocs.io/)** - Identify N+1 queries in development
- **[Cursor Documentation](https://docs.cursor.com/)** - Official docs for AI-powered coding
- **[Cursor Concepts](https://cursor.com/docs/get-started/concepts)** - Core concepts for working with Cursor AI

**Further Learning:**
- **[Cursor Context](https://cursor.com/learn/context)** - Cursor context management
- **[Cursor Tool Calling](https://cursor.com/learn/tool-calling)** - Advanced Cursor AI capabilities
- **[Context Engineering: Bringing Engineering Discipline to Prompts](https://addyo.substack.com/p/context-engineering-bringing-engineering)** - Systematic approach to prompt engineering
- **[Django Database Optimization](https://docs.djangoproject.com/en/stable/topics/db/optimization/)** - select_related & prefetch_related guide
- **[Django Security Guide](https://docs.djangoproject.com/en/stable/topics/security/)** - Authorization and security best practices
- **[OpenAI Prompt Engineering](https://platform.openai.com/docs/guides/prompt-engineering)** - Improve your AI prompting skills