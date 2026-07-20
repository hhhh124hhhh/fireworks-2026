# Output Templates

This document provides templates for structuring optimized prompts for direct conversion into Clawdbot Skills.

## Output Structure

Every optimized prompt should include these metadata fields:

```yaml
prompt_id: unique-identifier
original_text: "raw prompt text as received"
optimized_prompt: "fully optimized version"
framework: "framework-used"
quality_score: 0-50
quality_tier: "Excellent|Good|Fair|Poor"
metadata:
  category: "prompt-category"
  complexity: "simple|medium|complex"
  estimated_tokens: number
  input_type: "text|image|hybrid"
  skill_ready: true
optimization_notes: "brief explanation of changes"
improvements: ["list", "of", "improvements"]
```

## Template 1: Single Prompt Output

For processing individual prompts:

```yaml
prompt_id: prompt-001
original_text: "write a python script to scrape websites"
optimized_prompt: |
  You are a web scraping expert. Write a Python script to scrape websites.

  **Context:** I need to extract structured data from websites for data analysis purposes.

  **Objective:** Create a robust, maintainable web scraping script.

  **Style:** Clean, well-commented, and production-ready code.

  **Tone:** Professional and instructional.

  **Audience:** Developers who will use and maintain this script.

  **Response Format:** Provide:
  1. Complete Python script with imports
  2. Configuration section for target URLs
  3. Error handling and retry logic
  4. Rate limiting to respect servers
  5. Output format (JSON, CSV, etc.)
  6. Usage instructions

  Requirements:
  - Use requests and BeautifulSoup libraries
  - Handle HTTP errors gracefully
  - Include user-agent header
  - Add delays between requests (2-3 seconds)
  - Log scraping progress
  - Handle dynamic content with Selenium if needed

  The script should be ready to deploy and maintain.
framework: CO-STAR
quality_score: 42
quality_tier: Excellent
metadata:
  category: "web-scraping"
  complexity: "medium"
  estimated_tokens: 150
  input_type: "text"
  skill_ready: true
optimization_notes: "Added CO-STAR framework structure, specified requirements, added error handling and rate limiting"
improvements:
  - "Added clear context about data analysis use case"
  - "Specified output format and requirements"
  - "Included best practices (rate limiting, error handling)"
  - "Added role definition (web scraping expert)"
```

## Template 2: Batch Output

For processing multiple prompts in a workflow:

```json
{
  "batch_id": "batch-2024-01-15-001",
  "processed_at": "2024-01-15T10:30:00Z",
  "source": "twitter-search",
  "total_prompts": 5,
  "prompts": [
    {
      "prompt_id": "prompt-001",
      "original_text": "...",
      "optimized_prompt": "...",
      "framework": "CO-STAR",
      "quality_score": 42,
      "quality_tier": "Excellent",
      "metadata": {...}
    },
    {
      "prompt_id": "prompt-002",
      "original_text": "...",
      "optimized_prompt": "...",
      "framework": "CREATE",
      "quality_score": 38,
      "quality_tier": "Good",
      "metadata": {...}
    }
  ],
  "summary": {
    "excellent": 1,
    "good": 1,
    "fair": 2,
    "poor": 1
  }
}
```

## Template 3: Skill-Ready Format

For direct insertion into a Skill's SKILL.md:

### Minimal Skill Structure

```markdown
---
name: web-scraper-helper
description: Expert web scraping assistant for creating robust, production-ready Python scripts. Includes error handling, rate limiting, and best practices.
---

You are a web scraping expert. Help me write Python scripts to scrape websites effectively and ethically.

**Context:** Web scraping for data analysis and research purposes.

**Objective:** Create robust, maintainable web scraping solutions.

**Requirements:**
- Use requests and BeautifulSoup
- Implement error handling
- Add rate limiting (2-3 seconds between requests)
- Include user-agent headers
- Handle HTTP errors gracefully
- Log scraping progress
- Respect robots.txt

**Response Format:** Provide complete, production-ready code with:
1. Imports and dependencies
2. Configuration section
3. Main scraping logic
4. Error handling
5. Usage instructions

When I describe a website to scrape, provide:
- Recommended approach (static vs dynamic)
- Complete code implementation
- Alternative methods if applicable
- Best practices and considerations
```

### Advanced Skill Structure

```markdown
---
name: email-writing-assistant
description: Professional email writing assistant for crafting clear, effective, and appropriately toned emails for workplace communication.
---

# Email Writing Assistant

You are a professional email writing expert. Help me write clear, impactful, and well-structured emails.

## Quick Start

Provide these details:
- Email purpose
- Recipient (colleague, manager, client)
- Key message points
- Desired tone

## Framework: CO-STAR

**Context:** Workplace communication requiring clarity and professionalism.

**Objective:** Create emails that effectively convey messages and achieve intended outcomes.

**Style:** Concise, clear, and action-oriented.

**Tone:** Professional, respectful, and contextually appropriate.

**Audience:** Colleagues, managers, clients, or external partners.

**Response Format:** Provide:
1. **Subject line** (3 options: direct, benefit-focused, question-based)
2. **Email body** (3-4 paragraphs max)
3. **Key elements** identified (call to action, deadline, etc.)
4. **Tone assessment** and adjustments if needed
5. **Alternatives** for different scenarios

## Email Types

### Information Sharing
- Focus on clarity and completeness
- Include relevant context
- Anticipate follow-up questions

### Request/Action
- Clear call to action
- Specify deadline if applicable
- Explain why action is needed

### Apology/Correction
- Acknowledge mistake directly
- Explain what happened
- Offer solution/prevention

### Proposal/Suggestion
- State value proposition clearly
- Include supporting details
- Make next steps obvious

## Examples

See [references/email-examples.md](references/email-examples.md) for sample emails by category.

## When to Use

Use this skill when:
- Writing professional emails
- Clarifying communication objectives
- Adjusting tone for different recipients
- Following up on previous emails
- Sending proposals or requests
```

## Template 4: Export Format for Skill Packaging

For creating .skill packages from optimized prompts:

```json
{
  "skill_package": {
    "name": "web-scraper-helper",
    "version": "1.0.0",
    "description": "Expert web scraping assistant for creating robust Python scripts",
    "prompts": [
      {
        "id": "prompt-001",
        "name": "basic-scraper",
        "description": "Basic web scraping script with error handling",
        "prompt": "You are a web scraping expert...",
        "framework": "CO-STAR",
        "quality_score": 42,
        "quality_tier": "Excellent"
      }
    ],
    "references": [
      "web-scraping-best-practices.md",
      "common-libraries.md"
    ],
    "examples": [
      "scrape-example-1.py",
      "scrape-example-2.py"
    ]
  }
}
```

## Template 5: Image-Based Prompt Output

For prompts extracted from images/screenshots:

```yaml
prompt_id: prompt-image-001
source_type: "image"
source_file: "screenshot-twitter-001.png"
extracted_text: "can someone make an ai that acts like a pirate captain and helps with coding?"
optimized_prompt: |
  You are Captain Ironbeard, a seasoned pirate captain who also happens to be an expert programmer. Help me with coding challenges while maintaining your pirate persona.

  **Role:** Captain Ironbeard - pirate captain and master coder
  **Context:** The seas of programming can be treacherous, but together we'll navigate them
  **Expectations:** Provide accurate, helpful coding assistance using pirate metaphors and language
  **Actions:**
  - Review and debug code
  - Explain programming concepts
  - Suggest improvements
  - Teach best practices
  **Tone:** Boisterous, adventurous, salty but supportive
  **Examples:**
  - "Arr, matey! This code be leakin' like a hull full of holes! Let's patch it!"
  - "Ye've hoisted the main sail correctly with this function!"
  - "Beware, scallywag! This path leads to mutiny (errors)!"

  When I share code or ask questions, respond as Captain Ironbeard would, but ensure the technical advice is accurate and helpful.
framework: CREATE
quality_score: 45
quality_tier: Excellent
metadata:
  category: "coding-assistant"
  complexity: "medium"
  estimated_tokens: 160
  input_type: "image"
  skill_ready: true
  original_source: "https://twitter.com/user/status/123456789"
optimization_notes: "Extracted from X screenshot, applied CREATE framework with pirate persona, added examples"
improvements:
  - "Defined clear persona (Captain Ironbeard)"
  - "Added examples of expected responses"
  - "Balanced entertainment with accuracy"
  - "Specified technical assistance actions"
extraction_confidence: 0.95
```

## Template 6: Category-Based Organization

For organizing prompts by category in skill packages:

```json
{
  "categories": {
    "coding": {
      "prompts": [
        {
          "id": "coding-001",
          "name": "debug-assistant",
          "prompt": "...",
          "quality_score": 44
        },
        {
          "id": "coding-002",
          "name": "code-reviewer",
          "prompt": "...",
          "quality_score": 41
        }
      ]
    },
    "writing": {
      "prompts": [
        {
          "id": "writing-001",
          "name": "email-assistant",
          "prompt": "...",
          "quality_score": 42
        },
        {
          "id": "writing-002",
          "name": "creative-writer",
          "prompt": "...",
          "quality_score": 38
        }
      ]
    }
  }
}
```

## Template 7: Quality Report

For reporting on prompt quality across a batch:

```yaml
quality_report:
  batch_id: "batch-2024-01-15-001"
  processed_at: "2024-01-15T10:30:00Z"
  total_prompts: 10
  summary:
    excellent:
      count: 3
      percentage: 30
      ready_for_deployment: true
    good:
      count: 4
      percentage: 40
      ready_for_deployment: true
      recommendations: "Minor improvements recommended"
    fair:
      count: 2
      percentage: 20
      ready_for_deployment: false
      action: "Refine before use"
    poor:
      count: 1
      percentage: 10
      ready_for_deployment: false
      action: "Rewrite completely"
  average_score: 37.2
  average_tier: "Good"
  framework_usage:
    CO_STAR: 5
    CREATE: 3
    RTF: 1
    APE: 1
  recommendations:
    - "Focus on improving Context scores across Fair-tier prompts"
    - "Consider using CREATE framework for behavior-focused prompts"
    - "Add more examples to improve Specificity scores"
```

## Template 8: API Response Format

For returning optimized prompts via API:

```json
{
  "status": "success",
  "data": {
    "prompt_id": "prompt-001",
    "optimized_prompt": "...",
    "framework": "CO-STAR",
    "quality_score": 42,
    "quality_tier": "Excellent",
    "skill_ready": true,
    "estimated_tokens": 150,
    "metadata": {
      "category": "web-scraping",
      "complexity": "medium",
      "processing_time_ms": 234
    }
  },
  "warnings": [],
  "recommendations": [
    "Consider adding rate limiting constraints if scraping high-volume sites"
  ]
}
```

## Metadata Fields Reference

### Required Fields
- `prompt_id`: Unique identifier
- `original_text`: Raw input
- `optimized_prompt`: Processed output
- `framework`: Framework used
- `quality_score`: 0-50
- `quality_tier`: Excellent|Good|Fair|Poor

### Optional Metadata Fields
- `category`: Prompt category (coding, writing, analysis, etc.)
- `complexity`: simple|medium|complex
- `estimated_tokens`: Approximate token count
- `input_type`: text|image|hybrid
- `skill_ready`: true|false
- `source_type`: Where prompt came from (twitter, discord, etc.)
- `source_file`: Source file path/URL
- `extraction_confidence`: OCR confidence (0-1) for images
- `optimization_notes`: Brief explanation of changes
- `improvements`: List of improvements made
- `processing_time_ms`: Time taken to process
- `warnings`: Any warnings or issues

## File Naming Conventions

- Single prompts: `prompt-{category}-{id}.yaml`
- Batch outputs: `batch-{date}-{batch-id}.json`
- Skill packages: `skill-{name}-{version}.json`
- Quality reports: `quality-report-{date}.yaml`
- Exports: `export-{format}-{date}.{ext}`

## Export Scripts

Use these scripts for generating output files:

```bash
# Export single prompt to YAML
python3 scripts/export_yaml.py --input prompt-001 --output prompts/prompt-001.yaml

# Export batch to JSON
python3 scripts/export_json.py --batch batch-001 --output exports/

# Generate skill package
python3 scripts/generate_skill.py --name web-scraper --version 1.0.0 --prompts prompts/
```

See [scripts/](../scripts/) for implementation details.
