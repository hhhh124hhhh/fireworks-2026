# Prompt to Skill Conversion Template

Standardized template for transforming AI prompts into Clawdbot Skills.

## Template Structure

```markdown
---
name: [skill-name]
description: [What the skill does + when to use it + specific trigger scenarios]
---

# [Skill Title - Human Readable]

## Overview

[Brief explanation of what this skill enables in 1-2 sentences]

## [Choose Structure: Workflow / Tasks / Guidelines / Capabilities]

### [Section 1: Core Concepts / First Steps]

[Explain key concepts or initial setup needed]

### [Section 2: Main Workflow / Task Categories]

[Step-by-step instructions or organized task list]

#### [Subsection if needed]

[Detailed steps with examples]

### [Section 3: Examples / Use Cases]

[Concrete examples of how users would interact with this skill]

**Example 1: [Title]**
> User: [Example user request]
>
> Claude: [Expected response demonstrating skill usage]

### [Section 4: Tips & Best Practices]

[Guidelines for getting the most out of this skill]

## Quick Start

[How to use this skill immediately - get started in 30 seconds]

## Resources (optional - delete if not needed)

### scripts/
[List any scripts and their purposes]

### references/
[List any reference documentation to load as needed]

### assets/
[List any templates or output files]
```

## Field-by-Field Guide

### Frontmatter: `name`

**Rules:**
- Kebab-case: lowercase with hyphens
- 2-5 words maximum
- Descriptive but concise
- Domain-specific terms encouraged
- Avoid generic words like "ai", "helper", "tool"

**Examples:**
✅ `email-drafter`
✅ `code-reviewer`
✅ `twitter-scanner`
✅ `prompt-optimizer`

❌ `AI-helper`
❌ `the-best-email-writer`
❌ `CodeReviewTool`
❌ `skill123`

### Frontmatter: `description`

**Purpose:** This is Claude's primary trigger mechanism. It must clearly indicate:
1. What the skill does
2. When to use it
3. Specific scenarios that should trigger it

**Formula:**
```
[Action verb phrase] for [domain/use case]. Use when [trigger scenarios].
```

**Examples:**

Good description:
```yaml
description: Generate professional email drafts for various scenarios including job applications, follow-ups, and business correspondence. Use when users need help writing emails, crafting professional messages, or improving email tone and clarity.
```

Components:
- Action: "Generate professional email drafts"
- Domain: "various scenarios including job applications, follow-ups, and business correspondence"
- Triggers: "users need help writing emails, crafting professional messages, or improving email tone and clarity"

Another good example:
```yaml
description: Optimize and refine prompts for better LLM performance using advanced techniques like chain-of-thought, few-shot learning, and role-playing. Use when improving existing prompts, crafting new prompts for specific tasks, or troubleshooting poor LLM outputs.
```

### Body: Overview

**Goal:** 1-2 sentences explaining the skill's purpose.

**Examples:**
```
Comprehensive email drafting assistance for professional and personal scenarios.

Optimization techniques to improve prompt quality and LLM performance.
```

### Body: Structure Selection

Choose based on the prompt type:

#### 1. Workflow-Based (Multi-step Processes)

Use when the prompt is a sequential procedure with clear steps.

**Structure:**
```markdown
## Workflow

### Step 1: [First Step]
[Instructions]

### Step 2: [Second Step]
[Instructions]

### Step 3: [Third Step]
[Instructions]
```

**Best for:**
- Tutorial-style prompts
- Step-by-step guides
- Processes with dependencies

#### 2. Task-Based (Multiple Operations)

Use when the prompt provides different, independent capabilities.

**Structure:**
```markdown
## Capabilities

### Task 1: [Task Name]
[Instructions]

### Task 2: [Task Name]
[Instructions]

### Task 3: [Task Name]
[Instructions]
```

**Best for:**
- Prompt libraries with options
- Multi-purpose tools
- Different ways to use the skill

#### 3. Reference/Guidelines

Use when the prompt is about standards, templates, or best practices.

**Structure:**
```markdown
## Guidelines

### [Guideline Category 1]
[Rules and recommendations]

### [Guideline Category 2]
[Rules and recommendations]
```

**Best for:**
- Style guides
- Design patterns
- Best practices
- Standards

#### 4. Capabilities-Based (Integrated Features)

Use when the skill provides multiple interrelated features.

**Structure:**
```markdown
## Core Capabilities

### 1. [Feature Name]
[Brief description + how it works]

### 2. [Feature Name]
[Brief description + how it works]

### 3. [Feature Name]
[Brief description + how it works]
```

**Best for:**
- Complex systems
- Multi-feature tools
- Integrated workflows

### Body: Examples

Include 2-3 concrete examples showing real usage.

**Format:**
```markdown
**Example 1: [Descriptive Title]**
> User: [What the user might say]
>
> Claude: [Expected response showing skill in action]
```

**Tips:**
- Examples should cover different use cases
- Show the skill's full capabilities
- Include edge cases if relevant
- Use realistic user requests

### Body: Quick Start

Enable users to get started immediately without reading everything.

**Format:**
```markdown
## Quick Start

For immediate use, just ask: "[example request]"

Claude will automatically:
- [Step 1]
- [Step 2]
- [Step 3]

For more control, see the full workflow above.
```

### Body: Resources

Only include sections that actually exist. Delete empty sections.

**Scripts:**
```markdown
### scripts/
- `script_name.py`: [What it does]
- `another_script.sh`: [When to use it]
```

**References:**
```markdown
### references/
- `topic.md`: Load when [specific situation]
- `guide.md`: Reference for [specific tasks]
```

**Assets:**
```markdown
### assets/
- `template.docx`: Template for [output]
- `example.json`: Example configuration
```

## Conversion Process

### Step 1: Analyze the Original Prompt

Read the tweet/prompt and identify:
- **Core task**: What is the main objective?
- **Inputs**: What does the user provide?
- **Outputs**: What is produced?
- **Methodology**: How does it work?
- **Prerequisites**: What is needed first?

### Step 2: Choose Skill Structure

Based on the analysis, pick the best structure:
- Sequential process? → Workflow-based
- Multiple options? → Task-based
- Rules/standards? → Reference-based
- Integrated features? → Capabilities-based

### Step 3: Draft Frontmatter

Write `name` and `description`:
- Name: Kebab-case, descriptive
- Description: Action + domain + triggers

### Step 4: Write the Body

Using the template:
- Overview (1-2 sentences)
- Main section (workflow/tasks/guidelines)
- Examples (2-3 concrete cases)
- Quick Start (immediate use)

### Step 5: Add Resources

Create only what's needed:
- `scripts/`: For automation
- `references/`: For detailed docs
- `assets/`: For templates

### Step 6: Review and Refine

Check for:
- Clarity and completeness
- Proper structure
- Good examples
- No redundant sections
- Concise, focused content

## Example: Conversion

**Original Prompt (Tweet):**
"Here's a prompt to write professional declining emails for job offers. Be polite, express gratitude, keep door open, suggest future collaboration. Key phrases: 'thank you for the offer', 'difficult decision', 'appreciate your time', 'hope our paths cross'"

**Converted Skill:**

```markdown
---
name: job-offer-decliner
description: Generate polite, professional job offer decline emails that maintain good relationships and keep future opportunities open. Use when declining job offers, crafting rejection messages for employment, or writing professional turn-down responses.
---

# Job Offer Decliner

## Overview

Professional email templates and guidance for declining job offers gracefully while maintaining positive relationships with employers.

## Workflow

### Step 1: Express Gratitude
- Thank the employer for the offer
- Acknowledge their time and consideration
- Show appreciation for the opportunity

### Step 2: Explain the Decision
- State the decision to decline clearly
- Keep the explanation brief and honest
- Avoid negative details about the position/company

### Step 3: Keep the Door Open
- Express interest in future opportunities
- Suggest potential collaboration
- Offer to stay connected (LinkedIn, etc.)

### Step 4: Professional Closing
- Reiterate thanks
- Wish the company well
- Close professionally

## Key Phrases

Use these phrases as building blocks:
- "Thank you for the offer"
- "This was a difficult decision"
- "I appreciate your time"
- "I hope our paths cross again"

## Examples

**Example 1: Standard Decline**
> User: Decline a job offer from Acme Corp, was offered as frontend developer.
>
> Claude: Here's a professional decline email:
>
> Dear [Hiring Manager],
>
> Thank you so much for offering me the Frontend Developer position at Acme Corp. I genuinely appreciate the time you and your team took to interview me and get to know me.
>
> After careful consideration, I've decided to decline the offer. This was a difficult decision as I was very impressed with your team and the company culture.
>
> I hope our paths cross again in the future. I'd love to stay connected on LinkedIn and would be open to potential collaborations down the road.
>
> Thank you again for the opportunity. I wish you and Acme Corp all the best.
>
> Sincerely,
> [Your Name]

## Quick Start

Simply say: "Decline the job offer from [Company Name] for [Position]"

Claude will automatically generate a polite, professional response using gratitude, clear communication, and relationship-maintaining language.
```

## Quality Checklist

Before finalizing, verify:
- [ ] Frontmatter has valid YAML format
- [ ] Name is kebab-case and descriptive
- [ ] Description includes triggers
- [ ] Overview is 1-2 sentences
- [ ] Structure matches content type
- [ ] Examples are concrete and varied
- [ ] Quick Start enables immediate use
- [ ] Only necessary resource sections included
- [ ] Content is concise and focused
- [ ] No redundant or generic sections

## Common Pitfalls to Avoid

### 1. Over-Explaining
❌ "This skill helps you write emails because emails are important for business communication and..."
✅ "Professional email drafting for business and personal scenarios."

### 2. Missing Triggers
❌ "Generates emails for various purposes."
✅ "Generates emails for job applications, follow-ups, and business correspondence. Use when writing emails or crafting professional messages."

### 3. Too Generic
❌ name: `email-helper`
❌ description: "Helps with email writing"
✅ name: `email-drafter`
✅ description: "Generate professional email drafts for various scenarios. Use when users need help writing emails..."

### 4. Wrong Structure
❌ Workflow structure for a prompt library (use Task-based)
❌ Task structure for a sequential guide (use Workflow-based)

### 5. Empty Sections
❌ Leaving `scripts/`, `references/`, `assets/` in SKILL.md when not needed
✅ Delete sections that don't have content
