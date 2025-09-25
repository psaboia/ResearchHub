# Complete Step-by-Step Security Vulnerability Demonstration

## Prerequisites
Run the setup command before starting:
```bash
docker compose exec web python manage.py setup_test_data
```
This creates the "Confidential Drug Trial Results" dataset and test users.

## Note on Scripts
Instead of copying code into the Django shell, we'll use pre-made scripts for cleaner execution.
All scripts are in the `workshop_scripts/` directory.

## The Scenario

**Data Breach Risk**
A security audit reveals that any logged-in user can download private research datasets, including confidential drug trials and patient data. A researcher from a competing institution could access your proprietary research worth millions just by creating an account. This violates HIPAA compliance and exposes the institution to legal liability.

**Your Task:** Fix the authorization vulnerability so only authorized users can download datasets.

## Step 1: Present the Security Problem

```bash
# Let's demonstrate how unauthorized users can access private data
docker compose exec web python workshop_scripts/security_demonstrate_breach.py
```

This demonstration script will:
- Show a user from a competing institution accessing private drug trial data
- Verify they have no legitimate access rights
- Demonstrate the successful unauthorized download
- Calculate the compliance and financial impact

**Expected Output:**
```
🔒 DEMONSTRATION: Authorization Vulnerability

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

💰 POTENTIAL DAMAGE:
  • Competitor accessed proprietary research
  • $10M+ research value compromised
  • HIPAA violation - patient data exposed
```

> **📝 Instructor Note:**
> 1. **Emphasize the distinction** - Authentication (login) vs Authorization (permissions)
> 2. **Point out the real risk** - Competitors, data thieves, insider threats
> 3. **Ask participants** - "What would happen if this was patient medical records?"
> 4. **Connect to news** - Reference recent data breaches and their costs

## Step 2: Context Quality Demonstration

> **📝 INSTRUCTOR DEMONSTRATION:**
> Before participants set up their context, demonstrate why security-specific prompts work better!
> They just saw the security breach - perfect moment to show how generic security advice won't help.

### Instructor Demo - Generic Security Context (2 minutes)

**Setup for Instructor:**
1. **Close all files** in your Cursor/IDE
2. **Clear terminal** so breach details aren't visible
3. **Start fresh AI conversation**

**Live Demo:**
- **Ask AI:** "Add security to this function"
- **Point out to participants:** Watch how the AI gives generic security advice
- **Expected AI Response:** Generic suggestions about input validation, rate limiting, HTTPS
- **Say to participants:** "See? The AI doesn't know about our specific authorization problem or dataset permissions!"

**Key Teaching Point:**
> **"Generic security advice won't fix our specific authorization vulnerability. We need AI to understand our permission model!"**

---

**Transition to Good Context:**
> **"Now let's give the AI the specific context about our dataset permissions so it can implement proper authorization!"**

## Step 3: Prepare Your Cursor Context

> **💡 CURSOR CONTEXT MANAGEMENT:**
> Cursor automatically includes all open files and terminal output in the AI's context.
> Setting this up properly will dramatically improve the AI's ability to help you!

### Set Up Your IDE for Optimal AI Assistance:

**1. Open Multiple Relevant Files:**
- Open `research/views.py` → Navigate to `download_dataset` (lines 53-70)
- Open `research/models.py` → So AI understands the model relationships (Dataset, ResearchProject, DataAccessRequest)
- Keep terminal visible with the breach demonstration output

**2. Arrange Your Cursor Windows:**
```
┌─────────────────┬──────────────────┐
│   views.py      │    models.py     │
│ (download_      │  (Dataset,       │
│  dataset)       │   DataAccessRequest)│
├─────────────────┴──────────────────┤
│         Terminal Output             │
│    (CRITICAL SECURITY BREACH)      │
└─────────────────────────────────────┘
```

> **📝 Instructor Note:**
> 1. **Demo Cursor's context display** - Show participants where Cursor shows included context
> 2. **Explain automatic inclusion** - "Everything you see open, the AI sees too"
> 3. **Point out relationships in models.py** - ForeignKey and ManyToMany matter for authorization
> 4. **Terminal context is crucial** - The breach evidence guides the AI

### Why This Context Setup Matters:
- **views.py alone**: AI might suggest generic security improvements
- **+ models.py**: AI understands the relationships for authorization
- **+ terminal output**: AI sees the exact breach (unauthorized access)
- **= Perfect solution**: AI can now suggest all four authorization paths

## Step 4: Examine the Vulnerable Code

### The Vulnerable Code (for instructor reference):
```python
@api_view(['POST'])
@login_required  # Only checks if user is logged in!
def download_dataset(request, dataset_id):
    dataset = Dataset.objects.get(id=dataset_id)
    # BUG: No check if user has permission to download this dataset

    # Proceeds directly to download without authorization!
    file_path = dataset.file_path
    # ... sends file ...
```

**Analyzing the Vulnerability:**
- **Line 53**: `@login_required` only verifies user is logged in
- **Line 55**: Gets the dataset without checking permissions
- **Missing**: Authorization checks for ownership, collaboration, access requests
- **Impact**: Any authenticated user can download any dataset

> **📝 Instructor Note:**
> 1. **Walk through the code** - Point out @login_required only checks authentication
> 2. **Ask the key question** - "What's missing between lines 55 and 59?"
> 3. **Highlight the comment** - Even says "BUG" right there!
> 4. **Connect to models.py** - Show the relationships that define permissions

## Step 5: Use AI to Generate the Fix (Workshop Exercise)

### Leveraging Cursor's Context for Progressive Improvement

> **🎯 PRE-PROMPT CHECKLIST:**
> □ views.py open at download_dataset function
> □ models.py open showing Dataset and ResearchProject models
> □ Terminal visible with "CRITICAL SECURITY BREACH" output
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
"Add security to the download function"
```
*AI sees: Just the download_dataset function*
*Expected: Generic suggestions about passwords, encryption, or tokens*

**Level 2 - Single File Context:**
*Setup: views.py open at download_dataset function*
```
"The download_dataset function lets any logged-in user download private datasets.
Add permission checks to prevent unauthorized access."
```
*AI sees: The function with @login_required decorator*
*Expected: AI adds some checks but might miss edge cases or correct models*

**Level 3 - Multi-File Context:**
*Setup: Open models.py alongside views.py*
```
"Fix the authorization vulnerability. The terminal shows unauthorized access.
Check if the user is the owner, collaborator, or has approved access.
Use PermissionDenied for unauthorized access."
```
*AI sees: Function + model definitions + relationships*
*Expected: Better understanding of which fields to check*

**Level 4 - Full Context:**
*Setup: views.py + models.py + terminal with breach output visible*
```
"Fix the authorization vulnerability in download_dataset.
The terminal shows alice accessed bob's private dataset without permission.
Add checks for: dataset.uploaded_by, project.collaborators, DataAccessRequest(approved),
and dataset.privacy_level=='public'. Use any([...]) to check permissions.
Import PermissionDenied and show the complete fixed function."
```
*AI sees: Complete context - code, models, and breach evidence*
*Expected: Perfect solution with all four authorization paths correctly implemented*

> **📝 What to do with AI's solution:**
> - **Review** the code from each prompt level
> - **Choose** the best solution (probably Level 4)
> - **Check** all four access paths are covered
> - **Apply** the changes to your `research/views.py` file
> - **Test** your AI-generated fix with Step 5 below

### The Power of Cursor's Automatic Context:
- **No copy/paste needed** - Cursor includes all open files
- **Terminal matters** - Security breach evidence guides the AI
- **Models are crucial** - Relationships determine authorization paths
- **Fresh conversations** - Start new when context gets cluttered

## Step 6: Test YOUR AI-Generated Solution

```bash
# Test if your AI's solution actually fixed the security vulnerability
docker compose exec web python workshop_scripts/security_test_your_fix.py
```

> **📝 Success Criteria:**
> - Should show "4/4 tests passed"
> - Unauthorized users blocked, authorized users allowed
> - If tests fail, review your authorization logic

**Expected Output for Working Fix:**
```
🧪 TESTING YOUR SECURITY FIX

📝 TEST 1: Unauthorized User Should Be Blocked
✅ PASS! Access correctly denied

📝 TEST 2: Owner Should Have Access
✅ PASS! Owner can download their own dataset

📝 TEST 3: Public Datasets Should Be Accessible
✅ PASS! Public dataset is accessible

📝 TEST 4: Approved Access Requests Should Work
✅ PASS! Approved requester can download

🎉 ALL TESTS PASSED!
```

> **📝 Instructor Note:**
> - **Common mistake** - Checking only ownership, forgetting other access paths
> - **Debugging tip** - Print the four boolean checks to see which is failing
> - **Reminder** - Must import PermissionDenied from django.core.exceptions
> - **Note** - The @api_view decorator catches PermissionDenied and returns a 403 Response

## Step 7: Compare with Reference Solution (If Needed)

```bash
# If your solution didn't work, see the reference implementation
docker compose exec web python workshop_scripts/security_fixed_version.py
```

> **📝 Purpose of this step:**
> - **Shows working solution** if participant's fix has issues
> - **Teaching moment** - Compare authorization logic
> - **Best practices** - Including audit logging
> - **Not a failure** - Learning from reference is valuable

The reference will show:
- All four authorization paths
- Proper use of PermissionDenied
- Audit logging for security monitoring
- Performance optimization with select_related

## Step 8: Verify the Vulnerability is Fixed

After applying the fix, verify unauthorized access is now blocked:

```bash
# Run the demonstration again to confirm the fix works
docker compose exec web python workshop_scripts/security_demonstrate_breach.py
```

> **📝 Final Verification:**
> - Should now show "ACCESS DENIED" instead of breach
> - Unauthorized attempts are logged
> - Compliance requirements now met

## Key Takeaways for Participants

### 🎯 The Problem:
- **Authentication ≠ Authorization**: Login doesn't mean permission
- **Critical Impact**: Data breach, compliance violation, legal liability
- **Root Cause**: Missing permission checks after authentication

### 🔧 The Solution:
- **Check multiple paths**: Owner, collaborator, approved request, public
- **Use any([...])**: User needs just ONE valid permission
- **Raise PermissionDenied**: Django's standard way to deny access
- **Log attempts**: Security monitoring and compliance

### 📚 The Lesson:
**Context Quality Determines Solution Quality**
- Vague prompt → Generic security suggestions
- Specific vulnerability → Targeted fix
- Complete requirements → Production-ready solution
- Business context → Comprehensive authorization

**Cursor's Automatic Context Magic:**
- Open files = AI knowledge
- Terminal output = Security breach evidence
- Model relationships = Authorization paths
- Error messages = Debugging hints

### Security Quick Reference:
```python
# Authentication: Who are you?
@login_required  # Only checks if logged in

# Authorization: What can you do?
if not user_has_permission:
    raise PermissionDenied("Access denied")

# Common permission checks:
is_owner = obj.owner == request.user
is_member = obj.members.filter(id=user.id).exists()
is_public = obj.privacy == 'public'
has_role = user.groups.filter(name='editors').exists()
```

### Key Security Principle:
> **Default Deny**: Block access unless explicitly permitted. Never assume permission.

## Time Management

**Total Time: ~10-12 minutes**
- Step 1: Present vulnerability (2 min)
- Step 2: Examine code (2 min)
- Step 3: Progressive prompting (4 min)
- Step 4: Test fix (2 min)
- Step 5: Reference solution if needed (1 min)
- Discussion: Authentication vs Authorization (1 min)

> **📝 Instructor Tip:**
> - **If running fast**: Discuss GDPR/HIPAA implications
> - **If running slow**: Skip reference solution, focus on their fix
> - **Key point**: Everyone understands authentication vs authorization