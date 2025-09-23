# Week 3: Context-Aware Prompt Engineering Workshop - ResearchHub

## Overview

ResearchHub is a Scientific Research Data Management Platform that contains intentional bugs and undocumented functions designed for practicing context-aware prompt engineering with AI tools like Cursor IDE.

The workshop follows a logical progression:
1. **First**: Generate documentation to understand the codebase
2. **Then**: Use that understanding to identify and fix bugs

This approach mirrors real-world scenarios where engineers must understand existing code before making changes.

## Learning Objectives

1. Understand how AI uses context to provide accurate responses
2. Learn to structure prompts with clear constraints and examples  
3. Practice iterative prompt refinement for better results
4. Master providing the right context for debugging and documentation

## Workshop Activities

### Part 1: Documentation Generation (30 minutes)

Start by understanding the codebase through generating documentation for complex functions. This will help you learn the system's architecture and business logic before debugging.

#### Functions to Document:

1. **calculate_data_quality_metrics** (`research/views.py:184-261`)
   - Complex data validation logic
   - Multiple parameter types
   - Statistical calculations
   
   Practice prompts:
   - "Generate comprehensive documentation for calculate_data_quality_metrics including parameter descriptions and return value structure"
   - "Explain the data quality scoring algorithm in calculate_data_quality_metrics"
   - "What are the dependencies and models this function uses?"

2. **process_research_workflow** (`research/views.py:265-375`)
   - Multi-step workflow orchestration
   - Dynamic configuration handling
   - Error aggregation
   
   Practice prompts:
   - "Document the process_research_workflow function explaining each workflow step type"
   - "Create usage examples for process_research_workflow with different workflow configurations"
   - "How does this function interact with other parts of the system?"

3. **get_project_dashboard** (`research/views.py:31-49`)
   - API endpoint for project overview
   - Aggregates dataset information
   
   Practice prompts:
   - "Document this API endpoint including expected response format"
   - "What database models does this function access?"

### Part 2: Bug Identification & Fixing (30 minutes)

Now that you understand the codebase through documentation, identify and fix bugs using the context you've gained.

#### Bug Categories:

1. **Performance Bug (N+1 Query)**
   - Location: `research/views.py:31-49` (get_project_dashboard)
   - Context needed: Django ORM relationships, database query optimization
   - Practice prompt: "Based on the documentation we generated, identify performance issues in get_project_dashboard considering Django ORM best practices"

2. **Security Bug (Missing Permission Check)**
   - Location: `research/views.py:52-70`
   - Context needed: Authentication system, data access policies
   - Practice prompt: "Review the download_dataset endpoint for security vulnerabilities. Consider the multi-institutional context from the models"

3. **Race Condition Bug**
   - Location: `research/views.py:73-99`
   - Context needed: Concurrent file uploads, filesystem operations
   - Practice prompt: "Identify concurrency issues in process_uploaded_file considering multiple users uploading simultaneously"

4. **Memory Management Bug**
   - Location: `research/views.py:102-119`
   - Context needed: Large file processing, pandas memory usage
   - Practice prompt: "Analyze process_dataset_task for memory issues when processing files larger than 2GB"

5. **API Integration Bug**
   - Location: `research/views.py:122-133`
   - Context needed: External API rate limits, error handling
   - Practice prompt: "Review sync_external_research_data for API integration issues including rate limiting"

6. **Cache Invalidation Bug**
   - Location: `research/views.py:137-162`
   - Context needed: Caching strategy, data freshness requirements
   - Practice prompt: "Identify cache invalidation issues in get_dataset_statistics"

7. **SQL Injection Vulnerability**
   - Location: `research/views.py:166-180`
   - Context needed: SQL security, Django ORM
   - Practice prompt: "Find and fix the SQL injection vulnerability in search_datasets"

## Prompt Engineering Techniques

### 1. Providing Context

**Poor prompt:**
"Fix the bug in this function"

**Good prompt:**
"This Django view function handles dataset downloads in a multi-institutional research platform. Users from different institutions have different access rights. Identify and fix security vulnerabilities considering the authentication context and data privacy requirements."

### 2. Specifying Constraints

**Poor prompt:**
"Optimize this code"

**Good prompt:**
"Optimize this Django view for handling 1000+ datasets per project. Consider using select_related and prefetch_related to reduce database queries. The view should complete in under 200ms."

### 3. Requesting Specific Output Format

**Poor prompt:**
"Document this function"

**Good prompt:**
"Generate Python docstring for this function including:
- One-line summary
- Detailed description
- Args section with types and descriptions
- Returns section with type and structure
- Raises section for exceptions
- Example usage"

### 4. Iterative Refinement

Start broad, then narrow:
1. "Identify issues in this code"
2. "Focus on database query performance issues"
3. "Show me how to fix the N+1 query problem using Django's prefetch_related"

## Tips for Success

1. **Read surrounding code**: Always examine imports, models, and related functions
2. **Understand the domain**: This is a research data platform - consider scientific workflows
3. **Check configuration**: Look at settings.py for context about the system setup
4. **Consider dependencies**: Check models.py for relationships between entities
5. **Think about scale**: Consider performance with large datasets and many users

## Evaluation Criteria

Your prompts will be evaluated on:
- Clarity and specificity
- Appropriate context inclusion
- Iterative improvement
- Understanding of the codebase structure
- Ability to guide AI to accurate solutions

## Challenge Questions

1. How would you prompt the AI to understand the relationship between ResearchProject and Dataset models?
2. What context would you provide to help the AI fix the SQL injection vulnerability?
3. How would you structure a prompt to generate API documentation that includes authentication requirements?
4. What information would you include to help the AI understand the caching strategy?

## Resources

- Django documentation: https://docs.djangoproject.com/
- Django REST Framework: https://www.django-rest-framework.org/
- Celery documentation: https://docs.celeryproject.org/