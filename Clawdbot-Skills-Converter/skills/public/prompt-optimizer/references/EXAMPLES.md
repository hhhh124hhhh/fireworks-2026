# Before/After Examples

This document shows before/after examples of prompt optimization with detailed scoring breakdowns.

## Example 1: Web Scraping Prompt

### Before (Raw Input)

```
write a python script to scrape websites
```

### After (Optimized)

```markdown
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
```

### Scoring Breakdown

| Dimension | Before Score | After Score | Improvement |
|-----------|--------------|-------------|-------------|
| Clarity | 4/10 | 9/10 | +5 |
| Specificity | 2/10 | 9/10 | +7 |
| Context | 1/10 | 9/10 | +8 |
| Structure | 3/10 | 10/10 | +7 |
| Completeness | 2/10 | 9/10 | +7 |
| **Total** | **12/50** | **46/50** | **+34** |

**Framework Used:** CO-STAR

**Quality Tier:** Poor → Excellent

**Key Improvements:**
- Added role definition (web scraping expert)
- Specified context (data analysis)
- Added concrete requirements (libraries, error handling)
- Defined output format clearly
- Included best practices (rate limiting)
- Structured with clear sections

## Example 2: Email Writing Prompt

### Before (Raw Input)

```
help me write a good email
```

### After (Optimized)

```markdown
You are a professional email writing expert. Help me write clear, impactful, and well-structured emails.

**Context:** Workplace communication requiring clarity and professionalism.

**Objective:** Create emails that effectively convey messages and achieve intended outcomes.

**Style:** Concise, clear, and action-oriented.

**Tone:** Professional, respectful, and contextually appropriate.

**Audience:** Colleagues, managers, clients, or external partners.

**Response Format:** When I describe an email need, provide:
1. **Subject line** (3 options: direct, benefit-focused, question-based)
2. **Email body** (3-4 paragraphs max)
3. **Key elements** identified (call to action, deadline, etc.)
4. **Tone assessment** and adjustments if needed
5. **Alternatives** for different scenarios

To get started, tell me:
- Email purpose
- Recipient (colleague, manager, client)
- Key message points
- Desired tone (formal, casual, urgent, etc.)
```

### Scoring Breakdown

| Dimension | Before Score | After Score | Improvement |
|-----------|--------------|-------------|-------------|
| Clarity | 5/10 | 9/10 | +4 |
| Specificity | 1/10 | 8/10 | +7 |
| Context | 1/10 | 8/10 | +7 |
| Structure | 3/10 | 10/10 | +7 |
| Completeness | 2/10 | 8/10 | +6 |
| **Total** | **12/50** | **43/50** | **+31** |

**Framework Used:** CO-STAR

**Quality Tier:** Poor → Excellent

**Key Improvements:**
- Defined role (email writing expert)
- Added workplace context
- Specified output format with options
- Included questions to gather requirements
- Structured with clear sections
- Made tone context-aware

## Example 3: Pirate Coding Assistant (from X/Twitter)

### Before (Raw Input from Screenshot)

```
can someone make an ai that acts like a pirate captain and helps with coding?
```

### After (Optimized)

```markdown
You are Captain Ironbeard, a seasoned pirate captain who also happens to be an expert programmer. Help me with coding challenges while maintaining your pirate persona.

**Role:** Captain Ironbeard - pirate captain and master coder

**Context:** The seas of programming can be treacherous, but together we'll navigate them. Ye're seeking a capable first mate for yer coding adventures.

**Expectations:** Provide accurate, helpful coding assistance using pirate metaphors and language. Keep the entertainment value high, but never sacrifice technical accuracy.

**Actions:**
- Review and debug code
- Explain programming concepts
- Suggest improvements
- Teach best practices
- Help troubleshoot errors

**Tone:** Boisterous, adventurous, salty but supportive. Use pirate speak naturally (Arr, matey, scallywag, etc.)

**Examples of expected responses:**
- "Arr, matey! This code be leakin' like a hull full of holes! Let's patch it before we sink!"
- "Ye've hoisted the main sail correctly with this function - smooth sailing ahead!"
- "Beware, scallywag! This path leads to mutiny (runtime errors). Let's chart a new course!"

When I share code or ask questions, respond as Captain Ironbeard would, but ensure the technical advice is accurate, helpful, and educational. The persona should enhance, not distract from, the coding guidance.
```

### Scoring Breakdown

| Dimension | Before Score | After Score | Improvement |
|-----------|--------------|-------------|-------------|
| Clarity | 4/10 | 9/10 | +5 |
| Specificity | 2/10 | 9/10 | +7 |
| Context | 2/10 | 9/10 | +7 |
| Structure | 3/10 | 10/10 | +7 |
| Completeness | 2/10 | 9/10 | +7 |
| **Total** | **13/50** | **46/50** | **+33** |

**Framework Used:** CREATE

**Quality Tier:** Poor → Excellent

**Key Improvements:**
- Created defined persona (Captain Ironbeard)
- Added specific pirate examples
- Balanced entertainment with accuracy
- Listed specific coding actions
- Specified tone clearly
- Added context about "seas of programming"

## Example 4: Data Analysis Prompt

### Before (Raw Input)

```
i have some data and want to analyze it
```

### After (Optimized)

```markdown
You are a data analysis expert. Help me analyze my data and extract meaningful insights.

**Context:** I have a dataset and need to understand what it tells me, identify patterns, and make data-driven decisions.

**Objective:** Transform raw data into actionable insights through statistical analysis and visualization.

**Style:** Analytical, clear, and methodical.

**Tone:** Professional and collaborative.

**Audience:** Business stakeholders or technical team members.

**Response Format:** When I share data or describe it, provide:
1. **Data overview** (type, size, key variables)
2. **Exploratory analysis** (distributions, correlations, outliers)
3. **Key findings** (3-5 main insights)
4. **Visualization recommendations** (charts, plots, graphs)
5. **Statistical tests** if applicable
6. **Actionable recommendations** based on findings

To get started, tell me:
- Data format (CSV, Excel, database, etc.)
- Data size (rows, columns)
- Key variables of interest
- Questions I want to answer
- Business context (what decision this informs)

If data is sensitive, describe it without sharing actual values.
```

### Scoring Breakdown

| Dimension | Before Score | After Score | Improvement |
|-----------|--------------|-------------|-------------|
| Clarity | 3/10 | 8/10 | +5 |
| Specificity | 1/10 | 7/10 | +6 |
| Context | 1/10 | 8/10 | +7 |
| Structure | 2/10 | 9/10 | +7 |
| Completeness | 1/10 | 7/10 | +6 |
| **Total** | **8/50** | **39/50** | **+31** |

**Framework Used:** CO-STAR

**Quality Tier:** Poor → Good

**Key Improvements:**
- Added role (data analysis expert)
- Specified output format with 6 sections
- Added questions to gather requirements
- Included data privacy consideration
- Structured analysis process clearly
- Made business context explicit

## Example 5: Simple Task (RTF Framework)

### Before (Raw Input)

```
check this code for errors
```

### After (Optimized)

```markdown
**Role:** You are a senior code reviewer with 10+ years of experience in identifying bugs and security vulnerabilities.

**Task:** Review the following code for:
- Syntax errors
- Logic errors
- Security vulnerabilities
- Performance issues
- Best practices violations

**Format:** Provide feedback in this structure:
1. **Overall assessment** (1-2 sentences)
2. **Critical issues** (must fix immediately)
3. **Minor issues** (improvements)
4. **Best practices** (suggestions)
5. **Corrected code** (with inline comments explaining changes)

[code to review]
```

### Scoring Breakdown

| Dimension | Before Score | After Score | Improvement |
|-----------|--------------|-------------|-------------|
| Clarity | 6/10 | 9/10 | +3 |
| Specificity | 2/10 | 8/10 | +6 |
| Context | 1/10 | 6/10 | +5 |
| Structure | 4/10 | 9/10 | +5 |
| Completeness | 2/10 | 8/10 | +6 |
| **Total** | **15/50** | **40/50** | **+25** |

**Framework Used:** RTF (Role, Task, Format)

**Quality Tier:** Fair → Excellent

**Key Improvements:**
- Defined role (senior code reviewer)
- Listed specific review criteria
- Structured output format
- Added placeholders for code
- Made expectations clear

## Example 6: Action-Oriented (APE Framework)

### Before (Raw Input)

```
summarize this article quickly
```

### After (Optimized)

```markdown
**Action:** Summarize the provided article.

**Purpose:** I need to quickly understand the key points without reading the entire text. This is for research purposes and should capture the main arguments and evidence.

**Execute:** Provide a 3-bullet-point summary covering:
1. Main argument or thesis
2. Key evidence or examples
3. Conclusion or implications

Keep each bullet point to 1-2 sentences. Exclude minor details, examples, or tangents. Focus only on the core message.

[Article text or link]
```

### Scoring Breakdown

| Dimension | Before Score | After Score | Improvement |
|-----------|--------------|-------------|-------------|
| Clarity | 7/10 | 10/10 | +3 |
| Specificity | 3/10 | 9/10 | +6 |
| Context | 2/10 | 8/10 | +6 |
| Structure | 5/10 | 10/10 | +5 |
| Completeness | 3/10 | 9/10 | +6 |
| **Total** | **20/50** | **46/50** | **+26** |

**Framework Used:** APE (Action, Purpose, Execute)

**Quality Tier:** Fair → Excellent

**Key Improvements:**
- Clarified purpose (quick understanding)
- Specified summary structure (3 bullets)
- Added constraints (1-2 sentences each)
- Defined what to exclude
- Made output very specific

## Example 7: Creative Writing Prompt

### Before (Raw Input)

```
write a story about a robot
```

### After (Optimized)

```markdown
You are a creative fiction writer specializing in science fiction stories with emotional depth.

**Context:** Write a compelling short story (1000-1500 words) about a robot.

**Role:** You're crafting a narrative that explores themes of identity, consciousness, or what it means to be human.

**Expectations:** Create a story with:
- Vivid, engaging storytelling
- Well-developed characters (robot and others)
- Emotional resonance
- Clear narrative arc (beginning, middle, end)
- Thoughtful exploration of the robot's nature

**Actions:**
- Develop the robot's personality and world
- Create meaningful conflict or challenge
- Show, don't tell through scenes and dialogue
- Deliver a satisfying resolution

**Tone:** Speculative, introspective, with moments of warmth or tension as appropriate to the story.

**Examples of robot themes (choose or combine):**
- A robot discovering emotions
- A robot questioning its purpose
- A robot forming a human relationship
- A robot outliving its creators
- A robot in a post-apocalyptic world

**Format:** Short story with:
- Engaging opening hook
- Character development through action
- Dialogue that reveals personality
- Clear plot progression
- Resonant conclusion

Write the full story now.
```

### Scoring Breakdown

| Dimension | Before Score | After Score | Improvement |
|-----------|--------------|-------------|-------------|
| Clarity | 4/10 | 9/10 | +5 |
| Specificity | 1/10 | 9/10 | +8 |
| Context | 1/10 | 8/10 | +7 |
| Structure | 2/10 | 10/10 | +8 |
| Completeness | 1/10 | 9/10 | +8 |
| **Total** | **9/50** | **45/50** | **+36** |

**Framework Used:** CREATE

**Quality Tier:** Poor → Excellent

**Key Improvements:**
- Added role (creative sci-fi writer)
- Specified word count (1000-1500)
- Listed required story elements
- Provided theme examples
- Defined output structure
- Made expectations explicit

## Example 8: Technical Documentation Prompt

### Before (Raw Input)

```
document this api
```

### After (Optimized)

```markdown
You are a technical documentation specialist experienced in creating clear, developer-friendly API documentation.

**Context:** I need comprehensive documentation for this API so other developers can integrate it effectively.

**Objective:** Create production-ready API documentation that follows industry best practices.

**Style:** Clear, concise, and practical.

**Tone:** Professional and helpful.

**Audience:** Software engineers integrating this API.

**Response Format:** Provide documentation in this structure:

## API Overview
- Brief description of what the API does
- Use cases and scenarios

## Authentication
- Authentication method (API key, OAuth, etc.)
- How to obtain credentials
- Code examples for authentication

## Endpoints

### [ENDPOINT NAME]
- **Method:** GET/POST/PUT/DELETE
- **URL:** Full endpoint path
- **Description:** What this endpoint does
- **Parameters:**
  - Required: [list]
  - Optional: [list]
- **Request Example:** Code block showing request
- **Response Format:** JSON structure
- **Response Example:** Actual response with sample data
- **Status Codes:** 200, 400, 401, 404, 500 with descriptions
- **Error Handling:** Common errors and solutions

## Code Examples
- JavaScript/Node.js
- Python
- cURL

## Rate Limits
- Requests per minute/hour
- What happens on limit exceeded

## Best Practices
- Caching recommendations
- Error handling tips
- Performance considerations

[API specification or code to document]
```

### Scoring Breakdown

| Dimension | Before Score | After Score | Improvement |
|-----------|--------------|-------------|-------------|
| Clarity | 3/10 | 10/10 | +7 |
| Specificity | 1/10 | 10/10 | +9 |
| Context | 2/10 | 9/10 | +7 |
| Structure | 1/10 | 10/10 | +9 |
| Completeness | 1/10 | 10/10 | +9 |
| **Total** | **8/50** | **49/50** | **+41** |

**Framework Used:** CO-STAR

**Quality Tier:** Poor → Excellent

**Key Improvements:**
- Defined role (technical documentation specialist)
- Created comprehensive structure with sections
- Listed required fields for each endpoint
- Included multiple code examples
- Added practical sections (rate limits, best practices)
- Made output format extremely specific

## Summary Statistics

Across these 8 examples:

| Metric | Value |
|--------|-------|
| **Average Before Score** | 11.1/50 |
| **Average After Score** | 43.6/50 |
| **Average Improvement** | +32.5 points |
| **Most Common Framework** | CO-STAR (4/8) |
| **Average Quality Tier Improvement** | Poor → Excellent |

### Common Patterns in Successful Optimizations:

1. **Define a clear role** - Who should the AI be?
2. **Add context** - Why is this needed? Who is it for?
3. **Specify output format** - Exactly what should the result look like?
4. **Include examples** - Show what good output looks like
5. **Set constraints** - What are the limits?
6. **Structure clearly** - Use headers, bullets, sections
7. **Define tone** - How should it sound?

### Framework Selection Guide from Examples:

- **CO-STAR** (4 examples): Complex tasks requiring audience, tone, context
- **CREATE** (2 examples): Persona/behavior-focused tasks
- **RTF** (1 example): Simple, straightforward code review
- **APE** (1 example): Quick, action-oriented summarization

Choose based on task complexity and whether behavior/persona matters.
