# Complete Step-by-Step Cache Invalidation Demonstration

## Prerequisites
Run the setup command before starting:
```bash
docker compose exec web python manage.py setup_test_data
```
This creates the "Research Analytics Dataset" and all necessary test data.

## Note on Scripts
Instead of copying code into the Django shell, we'll use pre-made scripts for cleaner execution.
All scripts are in the `workshop_scripts/` directory.

## The Scenario

**Cache Invalidation Issue**
During a board meeting, the CEO notices the dashboard shows only 15 downloads for the flagship dataset. However, the analytics team confirms the database actually has 35 downloads - the recent conference activity isn't reflected. The statistics cache isn't being invalidated when new downloads occur, causing decision-makers to see outdated metrics for up to an hour.

**Your Task:** Fix the cache invalidation bug so statistics update in real-time.

## Step 1: Present the Statistics Problem

```bash
# Let's demonstrate why the CEO's dashboard showed wrong numbers
docker compose exec web python workshop_scripts/cache_demonstrate_problem.py
```

This demonstration script will:
- Simulate the CEO checking the dashboard
- Show conference attendees downloading the dataset
- Demonstrate how the dashboard still shows old numbers
- Calculate the business impact of wrong metrics
- Identify the cache as the root cause

**Expected Output:**
```
📊 DEMONSTRATION: CEO's Dashboard Disaster
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

> **📝 Instructor Note:**
> 1. **Emphasize the business impact** - This isn't just a technical bug
> 2. **Point out the time sensitivity** - Board meeting follow-up at 2 PM!
> 3. **Ask participants** - "What would happen if this was your production system?"
> 4. **Connect to real world** - Similar to Twitter's view count caching issues

## Step 2: Context Quality Demonstration

> **📝 INSTRUCTOR DEMONSTRATION:**
> Before participants set up their context, show them why specific prompts work better!
> They just saw the cache problem (35 in DB, 15 in cache) - perfect timing to demonstrate context importance.

### Instructor Demo - Vague Context (2 minutes)

**Setup for Instructor:**
1. **Close all files** in your Cursor/IDE
2. **Clear or minimize terminal** so cache discrepancy isn't visible
3. **Start fresh AI conversation**

**Live Demo:**
- **Ask AI:** "Fix the cache issue"
- **Point out to participants:** Watch how the AI gives generic caching advice
- **Expected AI Response:** Generic suggestions about Redis config, TTL settings, cache warming
- **Say to participants:** "See? The AI doesn't know about our specific statistics cache or download function!"

**Key Teaching Point:**
> **"Without context, AI gives generic cache advice. But we need specific help with download invalidating statistics cache!"**

---

**Transition to Good Context:**
> **"Now let's give the AI the specific context it needs to solve OUR cache invalidation problem!"**

## Step 3: Prepare Your Cursor Context

> **💡 CURSOR CONTEXT MANAGEMENT:**
> Cursor automatically includes all open files and terminal output in the AI's context.
> Setting this up properly will dramatically improve the AI's ability to help you!

### Set Up Your IDE for Optimal AI Assistance:

**1. Open Multiple Relevant Files:**
- Open `research/views.py` → Navigate to `get_dataset_statistics` (lines 137-162)
- Keep `research/views.py` open → Also locate `download_dataset` (lines 53-70)
- Keep terminal visible with the demonstration output (showing cache discrepancy)

**2. Arrange Your Cursor Windows:**
```
┌─────────────────────────────────────┐
│         views.py                    │
│  - get_dataset_statistics (visible) │
│  - download_dataset (scroll to see) │
├─────────────────────────────────────┤
│         Terminal Output             │
│   (35 in DB, 15 in cache)          │
└─────────────────────────────────────┘
```

> **📝 Instructor Note:**
> 1. **Demo Cursor's context display** - Show participants where Cursor shows included context
> 2. **Explain automatic inclusion** - "Everything you see open, the AI sees too"
> 3. **Point out the two functions** - Both must be visible for AI to understand the fix
> 4. **Terminal context is crucial** - The cache discrepancy guides the AI

### Why This Context Setup Matters:
- **views.py alone**: AI might suggest generic cache improvements
- **+ terminal output**: AI sees the actual problem (35 vs 15)
- **+ both functions visible**: AI understands the connection between them
- **= Perfect solution**: AI can now suggest precise cache.delete() in the right place

## Step 4: Examine the Problematic Code

### The Problematic Code (for instructor reference):
```python
# In get_dataset_statistics (lines 137-162):
cache_key = f"dataset_stats_{dataset_id}"
stats = cache.get(cache_key)
if stats:
    return Response(stats)  # Returns stale data!

# ... expensive calculation ...

cache.set(cache_key, stats, timeout=3600)  # Caches for 1 hour

# In download_dataset (lines 53-70):
AuditLog.objects.create(...)  # Records download
# BUG: Never invalidates the cache!
```

**Analyzing the Problem Together:**
- **Line 160**: Sets cache with 1-hour timeout
- **Line 68**: Creates audit log for download
- **Missing**: No cache invalidation after download!
- **Impact**: Statistics stay stale for up to 1 hour

> **📝 Instructor Note:**
> 1. **Walk through together** - Point out cache.set on line 160
> 2. **Ask the key question** - "Where should we invalidate this cache?"
> 3. **Point to download_dataset** - "What happens after line 68?"

## Step 5: Use AI to Generate the Fix (Workshop Exercise)

### Leveraging Cursor's Context for Progressive Improvement

> **🎯 PRE-PROMPT CHECKLIST:**
> □ views.py open with BOTH functions visible
> □ Terminal visible with "35 in DB, 15 in cache" output
> □ Fresh conversation if previous attempts cluttered
> □ Check context limit indicator

> **📝 Instructor Note:**
> - **Start with minimal context** - Close terminal for Level 1
> - **Progressively add context** - Show terminal for Level 2+
> - **Let Cursor's automatic context work** - Don't copy/paste code!
> - **Point out context indicator** - Show what Cursor includes with each level

**Level 1 - Minimal Context (Only Prompt):**
*Setup: Close terminal, only views.py open*
```
"Fix the cache bug"
```
*AI sees: Just the code in views.py*
*Expected: Generic caching advice, might suggest wrong solutions*

**Level 2 - Single Focus Context:**
*Setup: views.py open at get_dataset_statistics function*
```
"The statistics cache isn't updating when new downloads happen"
```
*AI sees: The caching function with timeout=3600*
*Expected: AI identifies cache invalidation issue but might miss where to add it*

**Level 3 - Multi-Function Context:**
*Setup: views.py with both functions visible + terminal output*
```
"Fix the cache invalidation bug. The terminal shows 35 downloads in DB but cache shows 15.
The cache needs to be cleared in download_dataset after new downloads."
```
*AI sees: Both functions + the discrepancy evidence*
*Expected: AI suggests cache.delete() in the right place, might miss key format*

**Level 4 - Full Context:**
*Setup: views.py + terminal + scroll to show both functions clearly*
```
"Fix the cache invalidation bug in download_dataset.
After the audit log on line 68, invalidate the cache using the exact key format
from get_dataset_statistics (line 141): f'dataset_stats_{dataset_id}'
Import cache and show the complete fixed function."
```
*AI sees: Complete context - both functions, terminal evidence, exact locations*
*Expected: Perfect solution with correct key format and placement*

> **📝 What to do with AI's solution:**
> - **Review** the code from each prompt level
> - **Choose** the best solution (probably Level 4)
> - **Apply** the changes to your `research/views.py` file
> - **Test** your AI-generated fix with Step 5 below

### The Power of Cursor's Automatic Context:
- **No copy/paste needed** - Cursor includes all open files
- **Terminal matters** - Error messages and output guide the AI
- **Function proximity** - Having both functions visible helps AI connect them
- **Fresh conversations** - Start new when context gets cluttered

## Step 6: Test YOUR AI-Generated Solution

```bash
# Test if your AI's solution actually fixed the cache bug
docker compose exec web python workshop_scripts/cache_test_your_fix.py
```

> **📝 Success Criteria:**
> - Should show "✅ SUCCESS! Cache invalidation is working!"
> - If it shows "❌ FAIL!", your solution needs adjustment
> - Common issues: wrong cache key, missing import, syntax error

**Expected Output for Working Fix:**
```
🧪 TESTING YOUR CACHE FIX
✅ SUCCESS! Cache invalidation is working!
  • Before download: 35
  • After download: 36
  • Cache properly invalidated and refreshed
```

> **📝 Instructor Note:**
> - **If participants struggle** - Remind them about the cache key format
> - **Common mistake** - Forgetting to import cache
> - **Debugging tip** - Check if cache.delete() is called with correct key

## Step 7: Compare with Reference Solution (If Needed)

```bash
# If your solution didn't work, see the reference implementation
docker compose exec web python workshop_scripts/cache_fixed_version.py
```

> **📝 Purpose of this step:**
> - **Shows working solution** if participant's fix has issues
> - **Teaching moment** - Compare their approach with reference
> - **Demonstrates best practices** - Including updating last_accessed
> - **Not a failure** - Learning from reference is valuable too!

The reference will show:
- Correct import statements
- Proper cache key construction
- Complete invalidation logic
- Additional considerations for production

## Step 8: Verify Business Impact is Resolved

After applying the fix, let's verify the CEO's dashboard would now work:

```bash
# Run the demonstration again to confirm the fix works
docker compose exec web python workshop_scripts/cache_demonstrate_problem.py
```

> **📝 Final Verification:**
> - Statistics should now update immediately
> - No more embarrassing board meetings!
> - Real-time metrics for decision making

## Key Takeaways for Participants

### 🎯 The Problem:
- **Stale Cache**: Statistics cached for 1 hour, never invalidated
- **Business Impact**: Wrong metrics shown to board, damaged credibility
- **Root Cause**: Missing cache.delete() after data changes

### 🔧 The Solution:
- **Invalidate on change**: Add cache.delete() after any data modification
- **Correct key format**: Must match exactly: `f"dataset_stats_{dataset_id}"`
- **Import required**: `from django.core.cache import cache`
- **Consider all change points**: Downloads, uploads, deletions, etc.

### 📚 The Lesson:
**Context Quality Determines Solution Quality**
- Vague prompt → Generic, unhelpful advice
- Specific location → Targeted but incomplete solution
- Complete context → Production-ready fix
- Business context → Understanding of urgency and impact

**Cursor's Automatic Context Magic:**
- Open files = AI knowledge
- Terminal output = Problem evidence
- Multiple functions = Relationship understanding
- Error messages = Debugging hints

### Cache Invalidation Patterns:
```python
# PATTERN 1: Delete specific key
cache_key = f"dataset_stats_{dataset_id}"
cache.delete(cache_key)

# PATTERN 2: Use cache tags (Django-cachalot)
cache.delete_many(cache.make_key(f"dataset_{dataset_id}_*"))

# PATTERN 3: Version-based invalidation
cache_key = f"dataset_stats_{dataset_id}_v{version}"
```

### Famous Quote:
> "There are only two hard things in Computer Science: cache invalidation and naming things." - Phil Karlton

## Time Management

**Total Time: ~10-12 minutes**
- Step 1: Investigate problem (2 min)
- Step 2: Examine code (2 min)
- Step 3: Progressive prompting (4 min)
- Step 4: Test fix (2 min)
- Step 5: Reference solution if needed (1 min)
- Discussion: Business impact (1 min)

> **📝 Instructor Tip:**
> - **If running fast**: Discuss additional invalidation points
> - **If running slow**: Skip reference solution, focus on their fix
> - **Key point**: Ensure everyone gets their fix working