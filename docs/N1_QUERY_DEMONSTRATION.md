# Complete Step-by-Step N+1 Query Demonstration

## Prerequisites
Run the setup command before starting:
```bash
docker compose exec web python manage.py setup_test_data
```
This creates all necessary data including the "Multi-Dataset Research Collaboration" project with 10 datasets.

## Note on Scripts
Instead of copying code into the Django shell, we'll use pre-made scripts for cleaner execution.
All scripts are in the `workshop_scripts/` directory.

## The Scenario

**Dashboard Performance Issue**
Users report the ResearchHub dashboard takes 5+ seconds to load when displaying project data. The DevOps team noticed database CPU usage spikes whenever the dashboard is accessed. This started happening after the platform grew from 10 to 100+ datasets per project.

**Your Task:** Investigate why the dashboard is slow and implement a fix.

## Step 1: Review the Data Structure

```bash
# First, let's understand what data the dashboard is displaying
docker compose exec web python workshop_scripts/n1_step1_review_data.py
```

This script will show:
- The Multi-Dataset Research Collaboration project structure
- 10 datasets with their relationships
- How accessing relationships in a loop causes the N+1 problem

## Steps 2-3: Investigate the Performance Issue

```bash
# Time to investigate! Let's diagnose what's causing the slowdown
docker compose exec web python workshop_scripts/n1_investigate_dashboard_performance.py
```

This investigation script will:
- Simulate a user accessing the dashboard
- Enable SQL query logging to see what's happening
- Measure actual execution time
- Show the performance impact at scale
- Identify the root cause of the slowdown

**Expected Output:**
```
🚨 INVESTIGATION RESULTS
📊 PERFORMANCE METRICS:
  • Execution time: ~50ms
  • Total queries executed: 32
  • Queries per dataset: 3.0

📈 IMPACT AT SCALE:
  Current (10 datasets): 32 queries, ~50ms
  With 100 datasets: ~302 queries, ~500ms (~0.5 seconds)
  With 1000 datasets: ~3002 queries, ~5000ms (~5.0 seconds) ⏰ TIMEOUT!

⚠️ PROBLEM IDENTIFIED: N+1 QUERY PATTERN
```

## Step 4: Prepare Your Cursor Context

> **💡 CURSOR CONTEXT MANAGEMENT:**
> Cursor automatically includes all open files and terminal output in the AI's context.
> Setting this up properly will dramatically improve the AI's ability to help you!

### Set Up Your IDE for Optimal AI Assistance:

**1. Open Multiple Relevant Files:**
- Open `research/views.py` → Navigate to `get_project_dashboard` (lines 31-48)
- Open `research/models.py` → So AI understands the model relationships
- Keep terminal visible with the investigation output (showing 32 queries)

**2. Arrange Your Cursor Windows:**
```
┌─────────────────┬──────────────────┐
│   views.py      │    models.py     │
│ (dashboard      │  (Dataset,       │
│  function)      │   ResearchProject)│
├─────────────────┴──────────────────┤
│         Terminal Output             │
│    (32 queries for 10 datasets)    │
└─────────────────────────────────────┘
```

> **📝 Instructor Note:**
> 1. **Demo Cursor's context display** - Show participants where Cursor shows included context
> 2. **Explain automatic inclusion** - "Everything you see open, the AI sees too"
> 3. **Point out relationships in models.py** - ForeignKey and ManyToMany matter for N+1
> 4. **Terminal context is crucial** - The performance metrics guide the AI

### Why This Context Setup Matters:
- **views.py alone**: AI might suggest generic optimizations
- **+ models.py**: AI understands the relationships causing N+1
- **+ terminal output**: AI sees the exact problem (32 queries)
- **= Perfect solution**: AI can now suggest precise select_related/prefetch_related

### The Problematic Code (for instructor reference):
```python
@api_view(['GET'])
def get_project_dashboard(request, project_id):
    project = ResearchProject.objects.get(id=project_id)

    datasets = project.datasets.all()

    dataset_info = []
    for dataset in datasets:  # Loop starts here - this is where N+1 happens
        info = {
            'id': str(dataset.id),
            'name': dataset.name,
            'uploaded_by': dataset.uploaded_by.username,  # ← N+1: fetches user
            'processing_jobs': dataset.processing_jobs.count(),  # ← N+1: counts jobs
            'access_requests': dataset.access_requests.filter(status='approved').count(),  # ← N+1: filter + count
        }
        dataset_info.append(info)

    return Response({'project': project.title, 'datasets': dataset_info})
```

**Analyzing the Problem Together:**
- **Line 42**: `dataset.uploaded_by.username` → Triggers 1 query per dataset (10 queries)
- **Line 43**: `dataset.processing_jobs.count()` → Triggers 1 query per dataset (10 queries)
- **Line 44**: `dataset.access_requests.filter(...).count()` → Triggers 1 query per dataset (10 queries)
- **Total**: 32 queries for 10 datasets (should be only 4-5 with optimization!)

## Step 5: Use AI to Generate the Fix (Workshop Exercise)

### Leveraging Cursor's Context for Progressive Improvement

> **🎯 PRE-PROMPT CHECKLIST:**
> □ views.py open at get_project_dashboard function
> □ models.py open showing Dataset and ResearchProject models
> □ Terminal visible with "32 queries" output
> □ Fresh conversation if previous attempts cluttered
> □ Check context limit indicator

> **📝 Instructor Note:**
> - **Start with minimal context** - Close models.py and terminal for Level 1
> - **Progressively add context** - Open files one by one to show improvement
> - **Let Cursor's automatic context work** - Don't copy/paste code!
> - **Point out context indicator** - Show what Cursor includes with each level

**Level 1 - Minimal Context (Only Prompt):**
*Setup: Close models.py and terminal, only views.py open*
```
"Fix the performance issue"
```
*AI sees: Just the function in views.py*
*Expected: Generic suggestions - caching, indexing, pagination*

**Level 2 - Single File Context:**
*Setup: views.py open at dashboard function*
```
"Fix the N+1 query problem in this function"
```
*AI sees: The function with the loop and relationships*
*Expected: Mentions select_related/prefetch_related but may miss details*

**Level 3 - Multi-File Context:**
*Setup: Open models.py alongside views.py*
```
"Fix the N+1 query problem. The terminal shows 32 queries for 10 datasets."
```
*AI sees: Function + model definitions + relationships*
*Expected: Better understanding of which fields need optimization*

**Level 4 - Full Context:**
*Setup: views.py + models.py + terminal with investigation output visible*
```
"Fix the N+1 query problem in get_project_dashboard.
Optimize the database queries for uploaded_by, processing_jobs, and access_requests."
```
*AI sees: Complete context - code, models, and performance metrics*
*Expected: Perfect solution with all optimizations correctly applied*

### The Power of Cursor's Automatic Context:
- **No copy/paste needed** - Cursor includes all open files
- **Terminal matters** - Error messages and output guide the AI
- **Models are crucial** - Relationships determine the optimization strategy
- **Fresh conversations** - Start new when context gets cluttered

> **📝 What to do with AI's solution:**
> - **Review** the code from each prompt level
> - **Choose** the best solution (probably Level 4)
> - **Apply** the changes to your `research/views.py` file
> - **Test** your AI-generated fix with the same investigation script (Step 5b below)

## Step 5b: Test YOUR AI-Generated Solution

```bash
# Test if your AI's solution actually fixed the problem
docker compose exec web python workshop_scripts/n1_investigate_dashboard_performance.py
```

> **📝 Success Criteria:**
> - Query count should drop from 32 to around 4-5
> - If it's still showing 32 queries, your solution didn't work
> - Try a better prompt or check the AI's code for errors

## Step 6: Compare with Reference Solution

```bash
# If your solution didn't work perfectly, compare with this reference
docker compose exec web python workshop_scripts/n1_step3_fixed_version.py
```

> **📝 Purpose of this step:**
> - **Shows a working solution** if your AI's fix had issues
> - **Demonstrates best practices** for Django ORM optimization
> - **Learning opportunity** - compare your solution with the reference
> - **Note:** This script contains its own fixed function, doesn't modify your file

This reference script will:
- Run a pre-made optimized version that definitely works
- Show the expected ~4-5 queries (vs original 32)
- Display all optimization techniques properly implemented
- Help you understand what the AI should have generated

**Expected Output:**
```
Total queries executed: 4-5
(1 for project with relations + 1 for datasets with users + 1 for processing_jobs + 1 for access_requests)
```

## Step 7: Performance Comparison Summary (Optional)

```bash
# Run the comparison script to see both versions side by side
docker compose exec web python workshop_scripts/n1_step4_compare_performance.py
```

This script will:
- Run both the original and optimized versions
- Show the dramatic difference in query count
- Provide a clear summary of the optimization techniques

> **📝 Instructor Note:**
> - **Celebrate the improvement!** - From 32 to 4-5 queries
> - **Emphasize the scale impact** - "Imagine with 1000 datasets!"
> - **Reinforce the lesson** - "Better context to AI = Better solutions"
> - **Participants keep their fix** - They've successfully optimized production code!
> - **Time check** - This section should wrap up the N+1 exercise (~2 minutes)

## Key Takeaways for Participants

### 🎯 The Problem:
- **N+1 Query Pattern**: 1 query for the collection + N queries for each item's relationships
- **Real Impact**: 10 datasets = 32 queries, 1000 datasets = 3002 queries!
- **User Experience**: Dashboard goes from instant to timing out

### 🔧 The Solution:
- **select_related()**: For ForeignKey relationships (SQL JOIN)
- **prefetch_related()**: For reverse ForeignKey and ManyToMany
- **annotate() + Count()**: For aggregations instead of .count() in loops
- **Prefetch objects**: For filtered relationships

### 📚 The Lesson:
**Context Quality Determines Solution Quality**
- Vague prompt → Generic advice
- Specific problem → Targeted solution
- Complete context → Production-ready code

### Django ORM Optimization Quick Reference:
```python
# BEFORE (N+1 Problem):
for dataset in project.datasets.all():
    print(dataset.uploaded_by.username)  # N queries

# AFTER (Optimized):
datasets = project.datasets.select_related('uploaded_by')
for dataset in datasets:
    print(dataset.uploaded_by.username)  # 0 additional queries
```

