# Prompt Quality Scoring Criteria

This document defines the quality scoring rubric used to evaluate optimized prompts.

## Scoring Overview

Each prompt is evaluated across **5 dimensions** (0-10 points each):
- **Clarity**: How unambiguous is the intent?
- **Specificity**: How concrete are the details and constraints?
- **Context**: Is sufficient background information provided?
- **Structure**: How well-organized is the prompt?
- **Completeness**: Are all necessary elements present?

**Total Score**: 0-50 points
**Quality Tiers**: Poor (0-19), Fair (20-29), Good (30-39), Excellent (40-50)

## Scoring Dimensions

### 1. Clarity (0-10 points)

**Definition:** How unambiguous and easy to understand the prompt is.

| Score | Description | Indicators |
|-------|-------------|------------|
| 10 | Crystal clear | Intent is obvious, no ambiguity, anyone would interpret the same way |
| 8-9 | Very clear | Minor ambiguity that doesn't affect core intent |
| 6-7 | Mostly clear | Some ambiguity, but likely to produce correct output |
| 4-5 | Somewhat unclear | Multiple interpretations possible, may need clarification |
| 2-3 | Unclear | Intent is vague or confusing, likely to misunderstand |
| 0-1 | Very unclear | No clear intent, essentially impossible to execute |

**Checklist:**
- [ ] Is the main request stated explicitly?
- [ ] Are there confusing or contradictory instructions?
- [ ] Would different people interpret it differently?
- [ ] Is there unnecessary complexity or jargon?

**Examples:**
- **10/10**: "Write a Python function that takes a list of integers and returns the sum of even numbers."
- **6/10**: "Help me with a function for lists." (Too vague)
- **2/10**: "Do the code thing." (Completely unclear)

### 2. Specificity (0-10 points)

**Definition:** How concrete and detailed the requirements are.

| Score | Description | Indicators |
|-------|-------------|------------|
| 10 | Highly specific | All requirements are detailed, constraints are clear, no room for guessing |
| 8-9 | Very specific | Most requirements detailed, minor gaps that don't affect quality |
| 6-7 | Somewhat specific | Key requirements specified, but some details missing |
| 4-5 | Moderately specific | General direction given, but significant ambiguity remains |
| 2-3 | Vague | High-level only, requires many assumptions |
| 0-1 | No specifics | No concrete requirements at all |

**Checklist:**
- [ ] Are input/output formats specified?
- [ ] Are constraints defined (length, format, style)?
- [ ] Are edge cases or limitations mentioned?
- [ ] Are success criteria clear?

**Examples:**
- **10/10**: "Write a Python function `sum_even(numbers: List[int]) -> int` that returns the sum of even numbers. Handle empty lists by returning 0. If any element is not an integer, raise TypeError."
- **6/10**: "Write a function that adds even numbers." (Missing types, error handling)
- **2/10**: "Make a math function." (No specifics)

### 3. Context (0-10 points)

**Definition:** How much background information is provided.

| Score | Description | Indicators |
|-------|-------------|------------|
| 10 | Full context | Complete background, scenario, purpose, and constraints provided |
| 8-9 | Good context | Most relevant background information included |
| 6-7 | Adequate context | Sufficient background for understanding the task |
| 4-5 | Limited context | Basic background, but key missing information |
| 2-3 | Minimal context | Very little background information |
| 0-1 | No context | Zero background information provided |

**Checklist:**
- [ ] Is the purpose of the task clear?
- [ ] Is the target audience or use case mentioned?
- [ ] Are constraints or limitations described?
- [ ] Is relevant background information included?

**Examples:**
- **10/10**: "I'm building a data processing pipeline for a fintech company. The function will process transaction records. Security is critical - no sensitive data should be logged. Write a function that..."
- **6/10**: "I need a function for data processing."
- **2/10**: "Write a function."

### 4. Structure (0-10 points)

**Definition:** How well-organized and easy to navigate the prompt is.

| Score | Description | Indicators |
|-------|-------------|------------|
| 10 | Excellent structure | Logical flow, clear sections, easy to scan, uses formatting effectively |
| 8-9 | Very good structure | Well-organized with minor organizational issues |
| 6-7 | Good structure | Generally organized, but could be clearer |
| 4-5 | Fair structure | Some organization present, but could be improved |
| 2-3 | Poor structure | Disorganized, hard to follow |
| 0-1 | No structure | Wall of text, no organization |

**Checklist:**
- [ ] Is information logically ordered?
- [ ] Are sections clearly delineated (headers, bullets)?
- [ ] Is visual formatting used effectively?
- [ ] Is it easy to find specific information?

**Examples:**
- **10/10**: Structured with clear headers, bullet points, and logical grouping
- **6/10**: Some paragraphs, but no clear sections
- **2/10**: Single unbroken paragraph

### 5. Completeness (0-10 points)

**Definition:** Whether all necessary elements are present for successful execution.

| Score | Description | Indicators |
|-------|-------------|------------|
| 10 | Complete | All necessary elements present, ready to execute without clarification |
| 8-9 | Nearly complete | Minor missing details that don't prevent execution |
| 6-7 | Mostly complete | Main elements present, some gaps that may need clarification |
| 4-5 | Partially complete | Key elements missing, requires significant clarification |
| 2-3 | Incomplete | Major elements missing, hard to execute |
| 0-1 | Very incomplete | Lacks most necessary elements |

**Checklist:**
- [ ] Is the main task clearly stated?
- [ ] Are requirements specified?
- [ ] Is the desired output format clear?
- [ ] Are constraints or boundaries defined?
- [ ] Are examples provided if helpful?

**Examples:**
- **10/10**: Clear task, requirements, output format, constraints, examples
- **6/10**: Clear task and requirements, missing output format
- **2/10**: Vague task only

## Quality Tiers

### Excellent (40-50 points)

**Characteristics:**
- Ready for commercial deployment
- Produces consistent, high-quality outputs
- Minimal ambiguity or missing information
- Professional, well-structured
- Can be used as-is in production

**Action:** Deploy directly, no changes needed.

**Example Score Breakdown:**
```
Clarity:     9/10
Specificity: 8/10
Context:     9/10
Structure:   10/10
Completeness:8/10
Total:       44/50
```

### Good (30-39 points)

**Characteristics:**
- Usable but could be improved
- Generally clear with some gaps
- Produces acceptable results
- Minor improvements recommended

**Action:** Use with confidence, consider minor refinements for better consistency.

**Example Score Breakdown:**
```
Clarity:     7/10
Specificity: 6/10
Context:     7/10
Structure:   8/10
Completeness:6/10
Total:       34/50
```

### Fair (20-29 points)

**Characteristics:**
- Needs refinement before deployment
- Multiple ambiguities or gaps
- Results may be inconsistent
- Significant improvements needed

**Action:** Rewrite or refine before use. Add missing context, clarify requirements.

**Example Score Breakdown:**
```
Clarity:     5/10
Specificity: 4/10
Context:     4/10
Structure:   5/10
Completeness:4/10
Total:       22/50
```

### Poor (0-19 points)

**Characteristics:**
- Requires complete rewrite
- Intent unclear or contradictory
- Missing critical information
- Unlikely to produce useful output

**Action:** Discard and start from scratch. Use a framework to rebuild.

**Example Score Breakdown:**
```
Clarity:     2/10
Specificity: 1/10
Context:     2/10
Structure:   3/10
Completeness:1/10
Total:        9/50
```

## Scoring Process

### Automated Scoring

The `scripts/score_prompt.py` script implements these criteria with natural language analysis:

```bash
python3 scripts/score_prompt.py --prompt "your prompt here"
```

**Automated analysis includes:**
- Clarity: Analyzes for ambiguous language, contradictions
- Specificity: Checks for concrete details, constraints
- Context: Identifies background information
- Structure: Evaluates formatting and organization
- Completeness: Checks for required elements

### Manual Scoring

Use the checklist in each dimension to evaluate prompts manually.

### Combined Approach

For best results:
1. Run automated scoring for objective metrics
2. Manual review for nuanced aspects
3. Final score is the average or consensus

## Common Issues and Point Deductions

### Common Clarity Issues
- Contradictory instructions: -3 to -5 points
- Unclear pronouns (it, that, they): -2 points
- Ambiguous terminology: -2 to -4 points

### Common Specificity Issues
- Vague verbs (help, make, do): -2 points
- Missing constraints: -2 to -4 points
- Undefined output format: -3 points

### Common Context Issues
- Missing purpose/use case: -3 points
- No target audience: -2 points
- Missing constraints/limitations: -2 points

### Common Structure Issues
- Wall of text: -4 points
- No sections/headers: -3 points
- Poor visual hierarchy: -2 points

### Common Completeness Issues
- Missing task definition: -5 points
- No output format: -3 points
- Missing requirements: -2 to -4 points

## Improvement Recommendations

Based on scores, provide specific recommendations:

**Low Clarity (0-5):**
- Rewrite with explicit intent
- Remove contradictions
- Define ambiguous terms

**Low Specificity (0-5):**
- Add concrete requirements
- Define output format
- Specify constraints

**Low Context (0-5):**
- Add background information
- Explain purpose/use case
- Identify target audience

**Low Structure (0-5):**
- Add headers and sections
- Use bullet points
- Improve visual formatting

**Low Completeness (0-5):**
- State the main task clearly
- Define requirements
- Provide examples

## Quality Tracking

Track prompt quality over time to identify patterns:

```json
{
  "prompt_id": "unique-id",
  "date": "2024-01-15",
  "scores": {
    "clarity": 8,
    "specificity": 7,
    "context": 9,
    "structure": 10,
    "completeness": 8
  },
  "total": 42,
  "tier": "Excellent",
  "framework": "CO-STAR",
  "improvements_needed": []
}
```

## Reference Scoring Examples

See [EXAMPLES.md](EXAMPLES.md) for complete before/after examples with detailed scoring breakdowns.
