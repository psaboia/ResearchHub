# Week 3: Context-Aware Prompt Engineering Workshop - Purpose & Overview

## Workshop Thesis

**ResearchHub is a hands-on teaching platform designed to teach developers how to effectively communicate with AI coding assistants.** The workshop is not about building production software—it's about mastering a critical skill: **providing better context to AI produces dramatically better solutions**.

## The Core Insight

The fundamental lesson of this workshop can be visualized as:

```
No Context → Some Context → Good Context → Excellent Context
    ↓            ↓              ↓               ↓
 Useless      Generic         Helpful        Perfect
```

Participants will experience this progression firsthand through multiple real-world examples, understanding that **context quality determines solution quality**.

## Why This Matters

As AI coding assistants become essential tools for developers, the ability to communicate effectively with them is a differentiator skill. Many developers ask AI vague questions and receive generic answers. This workshop teaches participants to:

1. **Recognize what context AI needs** to solve problems effectively
2. **Set up their workspace strategically** so the AI has visibility into what matters
3. **Iterate on prompts** progressively from vague to comprehensive
4. **Verify solutions work** before deploying them

## Workshop Duration & Structure

**Total Time: 60 minutes**

### Part 1: Documentation Generation (20 minutes)
**Objective:** Learn how context improves AI-generated documentation quality

- **Starting Point:** Two complex, undocumented functions (`calculate_data_quality_metrics` and `process_research_workflow`)
- **Poor Context Demo:** Vague prompt "Document this" → Generic, unhelpful output
- **Progressive Context Building:** Add business context, parameter details, examples → Each step improves quality
- **Key Teaching:** Business understanding and domain context transform generic documentation into production-ready guides

### Part 2: Bug Fixing Exercises (25-30 minutes)
**Objective:** Fix real bugs using AI with strategic context setup

Participants choose **ONE** of three bug scenarios:

#### 🔍 Option 1: N+1 Query Problem (Performance)
- **Location:** `research/views.py`, lines 31-48 (`get_project_dashboard`)
- **Problem:** Dashboard makes 32 queries for 10 datasets → timeouts at scale
- **Performance Impact:** 10 datasets = 32 queries; 1000 datasets = 3002 queries (5+ second timeout)
- **Learning:** Django ORM optimization with `select_related()` and `prefetch_related()`
- **Context Progression:**
  - Level 1 (vague): "Fix the performance issue" → generic suggestions
  - Level 2 (specific): "Fix N+1 in views.py" → mentions optimization
  - Level 3 (contextual): Open models.py + terminal showing 32 queries → AI suggests specific optimizations
  - Level 4 (excellent): Full context → production-ready solution

#### 💾 Option 2: Cache Invalidation Bug
- **Location:** `research/views.py`, lines 53-70 and 126-149
- **Problem:** Statistics cached for 1 hour, never invalidated → CEO's dashboard shows wrong metrics in board meeting
- **Business Impact:** 35 downloads in database, 15 shown in cache = 57% data hidden
- **Learning:** Cache invalidation strategies and the famous quote: *"There are only two hard things in Computer Science: cache invalidation and naming things"*
- **Key Fix:** Add `cache.delete()` after data changes, with correct key format

#### 🔒 Option 3: Security Vulnerability (Authorization)
- **Location:** `research/views.py`, lines 53-70
- **Problem:** Any logged-in user can download private datasets → unauthorized access to confidential drug trial data
- **Compliance Risk:** HIPAA/GDPR violations, $10M+ research exposure
- **Learning:** Critical distinction between **Authentication** (who are you?) vs **Authorization** (what can you do?)
- **Security Principle:** Default Deny—block access unless explicitly permitted

### Part 3: Wrap-up & Discussion (10-15 minutes)
**Objective:** Consolidate learnings and plan application to participants' own work

- **Review the Context Pyramid** showing progression of context quality
- **Discuss key teaching points** about workspace setup and prompt strategy
- **Guided questions** about what surprised participants and how they'll apply these lessons
- **Best practices checklist** for future AI-assisted development

## The "Just-In-Time" Teaching Moment

The most powerful aspect of this workshop is the **embedded context demonstration** at each bug exercise:

1. **Participants investigate** the problem (slow dashboard, stale cache, security breach)
2. **Instructor demonstrates bad context** with a vague prompt → participants see generic AI response
3. **Instructor explains good context** setup (open files + terminal visible)
4. **Participants use AI with good context** → they experience the dramatic improvement firsthand
5. **They test their AI-generated fix** → confirmation that context-driven solutions work

This just-in-time demonstration is far more impactful than a separate "how to prompt AI" lecture.

## Cursor's Automatic Context Magic

A key theme throughout is explaining **how Cursor automatically includes context**:

```
┌─────────────────────────────────┐
│   Open files                    │
│   + Terminal output             │ = Everything AI sees
│   + Error messages              │
│   + Visible relationships       │
└─────────────────────────────────┘
```

Participants learn that everything they have open and visible in their IDE becomes the AI's knowledge base—no copy/paste needed.

## Success Metrics

By the end of the workshop, participants should be able to:

- ✅ **Identify** what context AI needs to solve problems effectively
- ✅ **Set up** their workspace strategically for AI assistance
- ✅ **Generate** meaningful documentation using context-aware prompts
- ✅ **Fix** at least one bug using context-driven AI assistance
- ✅ **Explain** the difference between vague and contextual prompts
- ✅ **Iterate** on prompts progressively from basic to comprehensive
- ✅ **Apply** these strategies to their own codebases

## Key Takeaways

### Context Components That Matter
- **Location:** File names, line numbers, function names
- **Relationships:** Models, dependencies, imports between files
- **Business:** Purpose, requirements, constraints from domain context
- **Technical:** Framework conventions, design patterns, architectural decisions
- **Examples:** Input/output specimens, edge cases, error scenarios
- **Evidence:** Terminal output, error messages, performance metrics

### The Prompt Quality Ladder
```
Level 1: "Fix bug"
Level 2: "Fix performance issue"
Level 3: "Fix N+1 query in dashboard view"
Level 4: "Fix N+1 in lines 31-49 using select_related/prefetch_related"
Level 5: [Full context: models visible, terminal showing 32 queries, business impact clear]
```

### Cursor Context Setup Checklist
- □ Open relevant files (views.py, models.py, etc.)
- □ Show terminal output (errors, logs, test results, performance metrics)
- □ Arrange windows to show relationships between code sections
- □ Start fresh conversation if context becomes cluttered
- □ Check context limit indicator before prompting
- □ Reference visible output in prompts ("The terminal shows...")

## Magic Phrases That Improve AI Responses
- "Show the complete fixed code"
- "Include all necessary imports"
- "The terminal shows..." (reference visible output)
- "Using the models shown in models.py..."
- "Consider edge cases like..."
- "Use [specific framework] best practices"

## Post-Workshop Application

Participants should leave with a clear plan to:

1. **In their own projects:** Set up workspace before asking AI for help
2. **Build a prompt library:** Save good prompts for recurring tasks
3. **Experiment with context:** Try adding/removing files to see impact
4. **Join communities:** Connect with other AI-assisted developers
5. **Practice iteratively:** Start simple, add detail based on AI's responses

## The Bottom Line

This workshop teaches a **meta-skill**: how to get better results from AI tools by understanding what information the AI needs to be helpful. In the era of AI-assisted development, this is a **foundational skill** that multiplies the effectiveness of every other technical skill a developer has.

The ResearchHub platform with its intentional bugs serves as the **teaching vehicle**—but the real value is the lesson about **communication, context, and collaboration with AI**.
