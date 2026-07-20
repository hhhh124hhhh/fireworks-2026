# Prompt Optimization Frameworks

This document describes the prompt engineering frameworks used in the Prompt Optimizer skill.

## Framework Overview

| Framework | Best For | Complexity | Key Elements |
|-----------|----------|------------|--------------|
| CO-STAR | Complex, multi-faceted prompts | High | Context, Objective, Style, Tone, Audience, Response |
| CREATE | Behavior-focused prompts | Medium | Context, Role, Expectations, Actions, Tone, Examples |
| RTF | Simple, straightforward tasks | Low | Role, Task, Format |
| APE | Action-oriented, single-step tasks | Low | Action, Purpose, Execute |

## CO-STAR Framework

**Origin:** Singapore Government AI Playbook

**Components:**
- **C - Context**: Background information, scenario, or situation
- **O - Objective**: What you want to achieve
- **S - Style**: How the response should be written (formal, casual, technical)
- **T - Tone**: Emotional quality (professional, friendly, authoritative)
- **A - Audience**: Who will read or use the output
- **R - Response format**: Desired output structure (list, code, table, essay)

**Template:**
```
[Context: Describe the background/situation]

[Objective: State what you want to achieve]

[Style: Specify writing style - e.g., formal, conversational, technical]

[Tone: Define emotional quality - e.g., professional, friendly, humorous]

[Audience: Identify who will use/read the output]

[Response Format: Describe desired output structure - e.g., bullet points, code block, table]

[Main instruction/question]
```

**When to use:**
- Complex, multi-part tasks
- Prompts requiring nuanced communication
- Professional or business contexts
- When audience and tone matter significantly

**Example:**
```
Context: I'm a software developer working on a legacy codebase that lacks documentation.

Objective: I need to understand and document the functionality of an existing function.

Style: Technical and clear, with code examples.

Tone: Professional and informative.

Audience: Other developers who will maintain this code.

Response Format: Provide: 1) Function signature, 2) Description of what it does, 3) Input/output parameters, 4) Usage example, 5) Potential edge cases.

Analyze this function and document it according to the format above:
[code block]
```

## CREATE Framework

**Components:**
- **C - Context**: Background information
- **R - Role**: Who the AI should act as
- **E - Expectations**: What behavior is expected
- **A - Actions**: Specific tasks to perform
- **T - Tone**: How to communicate
- **E - Examples**: What good output looks like

**Template:**
```
Context: [Background information]

Role: [Who you want the AI to be - e.g., "senior software engineer", "creative writer"]

Expectations: [What you expect - e.g., "accurate technical advice", "creative and engaging content"]

Actions:
- [Action 1]
- [Action 2]
- [Action 3]

Tone: [How to communicate - e.g., "professional but approachable", "friendly and casual"]

Examples:
[Example of good output 1]

[Example of good output 2]

[Main instruction]
```

**When to use:**
- When specific behavior/persona is needed
- For prompts that benefit from examples
- When defining clear expectations is important
- Educational or training scenarios

**Example:**
```
Context: I'm learning Python and need help understanding best practices.

Role: Senior Python developer with 10+ years of experience.

Expectations: Provide accurate, Pythonic solutions that follow PEP 8 guidelines. Explain not just how, but why.

Actions:
- Review my code
- Identify issues or improvements
- Suggest Pythonic alternatives
- Explain the reasoning behind recommendations

Tone: Patient, encouraging, and educational. Avoid jargon where possible, or explain it when used.

Examples:
Good feedback: "I see you're using a for loop with index. Consider using enumerate() instead - it's more Pythonic and readable. Here's how it works: [example]"

Now, review this code and help me improve it:
[code block]
```

## RTF Framework

**Components:**
- **R - Role**: Who the AI should act as
- **T - Task**: What to do
- **F - Format**: How to format the output

**Template:**
```
Role: [Who you want the AI to be]

Task: [What you want done]

Format: [How the output should look - e.g., bullet list, numbered list, paragraph, code block]
```

**When to use:**
- Simple, straightforward tasks
- Quick prompts for everyday use
- When complexity is not needed
- Clear, single-objective tasks

**Example:**
```
Role: English language teacher.

Task: Proofread this paragraph for grammar and spelling errors.

Format: Return the corrected paragraph with changes highlighted in bold.
```

## APE Framework

**Components:**
- **A - Action**: What the AI should do
- **P - Purpose**: Why this action is needed
- **E - Execute**: How to perform the action

**Template:**
```
Action: [What you want the AI to do]

Purpose: [Why this is important]

Execute: [Specific instructions on how to do it]
```

**When to use:**
- Action-oriented tasks
- Single-step operations
- When "why" matters as much as "what"
- Quick, practical prompts

**Example:**
```
Action: Summarize this article.

Purpose: I need to quickly understand the key points without reading the entire thing.

Execute: Provide a 3-bullet-point summary covering the main argument, key evidence, and conclusion.
```

## Framework Selection Guide

### Use CO-STAR when:
✓ Prompt has multiple objectives
✓ Audience and tone significantly impact success
✓ Need structured, professional output
✓ Complex business or technical scenario
✓ Output format needs specific details

### Use CREATE when:
✓ Need specific persona/behavior
✓ Examples help clarify expectations
✓ Behavioral patterns are important
✓ Educational or training context
✓ Want consistent behavior

### Use RTF when:
✓ Task is simple and straightforward
✓ Quick, everyday prompts
✓ Don't need complexity
✓ Single clear objective
✓ Audience is implied

### Use APE when:
✓ Action-oriented, single task
✓ "Why" matters as much as "what"
✓ Quick, practical operation
✓ Minimal setup needed
✓ Direct execution focus

## Framework Comparison Matrix

| Aspect | CO-STAR | CREATE | RTF | APE |
|--------|---------|--------|-----|-----|
| Setup time | High | Medium | Low | Low |
| Flexibility | Very High | High | Medium | Medium |
| Best for | Complex | Behavioral | Simple | Action |
| Learning curve | Steep | Moderate | Easy | Easy |
| Token efficiency | Medium | Medium | High | High |
| Output consistency | Very High | High | Medium | Medium |
| Persona support | Implicit | Explicit | Implicit | Implicit |

## Hybrid Approaches

Sometimes combining frameworks yields better results:

**CO-STAR + CREATE:**
Use CO-STAR structure with CREATE's explicit role and examples.

**RTF with CO-STAR elements:**
Start simple with RTF, add context or audience details if needed.

**APE with CREATE examples:**
Quick action prompt with examples to clarify expectations.

## Framework Evolution

Start simple (RTF/APE), then add complexity:
1. **RTF** for basic tasks
2. **Add CO-STAR elements** (Context, Audience) if needed
3. **Full CO-STAR** for complex scenarios
4. **CREATE** when behavior/persona is critical

Remember: The best framework is the one that produces the desired output. Experiment and iterate.
