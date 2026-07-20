---
name: prompt-optimizer
description: Transform raw prompts into optimized, skill-ready outputs using established prompt engineering frameworks. Accepts text or image-based prompts, applies quality optimization, scores result quality, and outputs structured formats ready for direct conversion into Clawdbot Skills. Use when: (1) User provides a raw or unstructured prompt that needs professional refinement, (2) Converting X/Twitter prompts into Clawdbot Skills, (3) Evaluating and improving prompt quality before deployment, (4) Creating structured prompt templates for commercial skill packages, (5) Building prompt evaluation and optimization pipelines.
---

# Prompt Optimizer

This skill transforms raw, unstructured prompts into high-quality, skill-ready outputs using established prompt engineering frameworks. It provides a complete pipeline: **Input → Optimization → Quality Scoring → Structured Output**.

## Quick Start

For a raw prompt, run this three-step process:

1. **Optimize** - Apply frameworks (see [OPTIMIZATION-FRAMEWORKS.md](references/OPTIMIZATION-FRAMEWORKS.md))
2. **Score** - Evaluate quality (see [SCORING-CRITERIA.md](references/SCORING-CRITERIA.md))
3. **Structure** - Format for Skill conversion (see [OUTPUT-TEMPLATES.md](references/OUTPUT-TEMPLATES.md))

## Workflow

### Step 1: Analyze Input

**Determine input type:**
- **Text prompt**: Copy-pasted text from X, web, or user input
- **Image prompt**: Screenshot or image containing prompt text

**Extract content:**
- For text: Direct processing
- For images: Use OCR to extract text, then process

**Identify intent:**
- What is the user trying to accomplish?
- What AI capabilities are required?
- What output format does the user expect?

### Step 2: Apply Optimization Framework

Select the most appropriate framework from [OPTIMIZATION-FRAMEWORKS.md](references/OPTIMIZATION-FRAMEWORKS.md):

- **CO-STAR**: Context, Objective, Style, Tone, Audience, Response format
- **CREATE**: Context, Role, Expectations, Actions, Tone, Examples
- **RTF**: Role, Task, Format
- **APE**: Action, Purpose, Execute

**Framework selection guide:**
- Use **CO-STAR** for complex, multi-faceted prompts
- Use **CREATE** when examples or specific behaviors are needed
- Use **RTF** for simple, straightforward tasks
- Use **APE** for action-oriented, single-step tasks

### Step 3: Score Quality

Evaluate the optimized prompt using [SCORING-CRITERIA.md](references/SCORING-CRITERIA.md):

**Scoring dimensions (0-10 each):**
1. **Clarity**: Is the intent unambiguous?
2. **Specificity**: Does it have concrete details and constraints?
3. **Context**: Is background information provided?
4. **Structure**: Is it well-organized?
5. **Completeness**: Are all necessary elements present?

**Quality tiers:**
- **Excellent (40-50)**: Ready for commercial deployment
- **Good (30-39)**: Usable with minor improvements
- **Fair (20-29)**: Needs refinement
- **Poor (0-19)**: Requires complete rewrite

### Step 4: Generate Structured Output

Format the optimized prompt for direct Skill conversion using templates in [OUTPUT-TEMPLATES.md](references/OUTPUT-TEMPLATES.md):

**Output structure:**
```yaml
prompt_id: unique-id
original_text: "raw prompt text"
optimized_prompt: "optimized version"
framework: "CO-STAR"
quality_score: 42
quality_tier: "Excellent"
metadata:
  category: "text-processing"
  complexity: "medium"
  estimated_tokens: 150
skill_ready: true
```

### Step 5: Batch Processing (Optional)

For processing multiple prompts from X/Twitter:

1. Use `scripts/extract_prompts.py` to scrape and extract prompts
2. Run `scripts/optimize_batch.py` for batch optimization
3. Use `scripts/score_prompts.py` for automated quality scoring
4. Generate skill packages with `scripts/package_skills.py`

## Input Formats

### Text Input

Direct text string processing:

```
Raw: "write a python script to scrape websites"
```

### Image Input

For screenshots or images containing prompt text:

1. Save image to temporary location
2. Extract text using OCR (Tesseract or similar)
3. Process as text input
4. Include `source: "image"` in metadata

## Quality Scoring

### Automated Scoring

Run the scoring script:

```bash
python3 scripts/score_prompt.py --prompt "your prompt here"
```

Output:
```
Clarity: 8/10
Specificity: 6/10
Context: 4/10
Structure: 9/10
Completeness: 7/10
---
Total Score: 34/50
Quality Tier: Good
Recommendations:
- Add specific website constraints
- Include output format requirements
- Provide context about scraping purpose
```

### Manual Scoring

Use the checklist in [SCORING-CRITERIA.md](references/SCORING-CRITERIA.md) for manual evaluation.

## Output for Skill Conversion

### Skill-Ready Format

The optimized prompt should be ready for direct insertion into a Skill's SKILL.md:

```markdown
---
name: your-skill-name
description: [extracted from optimized prompt context]
---

[optimized prompt content]
```

### Batch Export

Export multiple optimized prompts for skill package generation:

```bash
python3 scripts/export_skills.py --input optimized_prompts.json --output dist/
```

## Optimization Examples

### Example 1: Raw Text Input

**Input:**
```
"help me write better emails"
```

**Framework Applied:** CO-STAR

**Optimized:**
```
You are a professional email writing assistant. Help me write more effective and impactful emails.

**Context:** I need to communicate clearly and professionally in workplace settings
**Objective:** Create emails that are concise, actionable, and appropriate for the recipient
**Style:** Professional, clear, and direct
**Tone:** Confident but approachable
**Audience:** Colleagues, managers, or external partners
**Response Format:** Provide 2-3 email options with explanations for when to use each

When I describe an email scenario, provide:
1. Subject line options
2. Email body draft
3. Key tips for effectiveness
4. Alternative approaches if needed
```

**Quality Score:** 42/50 (Excellent)

### Example 2: X/Twitter Prompt

**Input (from screenshot):**
```
"can someone make an ai that acts like a pirate captain and helps with coding?"
```

**Framework Applied:** CREATE

**Optimized:**
```
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
```

**Quality Score:** 45/50 (Excellent)

## Common Improvements

When optimizing, focus on these areas:

1. **Add context**: What's the background or purpose?
2. **Define role**: Who should the AI act as?
3. **Specify output**: What should the result look like?
4. **Provide constraints**: What shouldn't be included?
5. **Include examples**: Show what good output looks like
6. **Set tone**: Formal, casual, professional, etc.

## Troubleshooting

**Prompt still unclear after optimization:**
- Add more specific constraints
- Include negative examples (what NOT to do)
- Break into multiple, focused prompts

**Quality score below 30:**
- Review [OPTIMIZATION-FRAMEWORKS.md](references/OPTIMIZATION-FRAMEWORKS.md) for alternative frameworks
- Check if the original prompt's intent is clear
- Consider if multiple prompts would work better than one

**Batch processing errors:**
- Check input JSON format
- Verify prompts are UTF-8 encoded
- Review script logs for specific error messages

## When to Use This Skill

Use this skill when:
- User provides raw/unstructured prompts needing refinement
- Converting social media prompts into professional skills
- Evaluating prompt quality before deployment
- Building prompt optimization pipelines
- Creating commercial prompt packages
- Standardizing prompts across multiple skills

## References

- [OPTIMIZATION-FRAMEWORKS.md](references/OPTIMIZATION-FRAMEWORKS.md) - Detailed framework descriptions
- [SCORING-CRITERIA.md](references/SCORING-CRITERIA.md) - Quality scoring rubric
- [OUTPUT-TEMPLATES.md](references/OUTPUT-TEMPLATES.md) - Output format templates
- [EXAMPLES.md](references/EXAMPLES.md) - Before/after optimization examples
- [BEST-PRACTICES.md](references/BEST-PRACTICES.md) - Prompt engineering guidelines
