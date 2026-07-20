# Prompt Evaluation Criteria

Detailed rubric for scoring AI prompts from Twitter for conversion to Clawdbot Skills.

## Scoring Guide

### Clarity & Completeness (10 points)

Evaluates how well the prompt is written and how complete the instructions are.

| Score | Description |
|-------|-------------|
| 10 | Crystal clear, complete, no ambiguity. Ready to use as-is. |
| 8-9 | Minor ambiguities, mostly complete. Small adjustments needed. |
| 5-7 | Some missing steps, moderately clear. Requires interpretation. |
| 3-4 | Vague, incomplete. Significant gaps in instructions. |
| 1-2 | Confusing, unusable. Cannot determine intent or process. |

**What to look for:**
- Clear objective statement
- Step-by-step instructions
- Defined inputs and outputs
- No conflicting or contradictory directions
- Complete workflow

### Uniqueness (10 points)

Assesses how novel and differentiated the prompt is from existing skills.

| Score | Description |
|-------|-------------|
| 10 | Novel, unlike any existing skill. Breakthrough approach. |
| 8-9 | Unique approach to common problem. Fresh perspective. |
| 5-7 | Good but not groundbreaking. Some differentiation. |
| 3-4 | Similar to existing skills. Minor variations only. |
| 1-2 | Duplicate or generic. No unique value proposition. |

**What to check:**
- Search ClawdHub for similar skills
- Evaluate if it solves a new problem
- Assess if it improves on existing solutions
- Consider if it's a new application of known techniques

### Market Potential (10 points)

Measures commercial viability based on engagement and demand indicators.

| Score | Description |
|-------|-------------|
| 10 | High demand, viral engagement. Clear market need. |
| 8-9 | Clear niche audience, strong interest. Sustainable demand. |
| 5-7 | Moderate interest, growing but not proven. |
| 3-4 | Small audience, limited appeal. |
| 1-2 | Little/no demand. No engagement metrics. |

**Engagement Metrics (Twitter):**
- Likes: 50+ (high), 20-49 (medium), <20 (low)
- Retweets: 10+ (high), 5-9 (medium), <5 (low)
- Replies: 10+ (high), 5-9 (medium), <5 (low)
- Combined: High + High = 10 points
- Combined: High + Medium or Medium + High = 8-9 points
- Combined: Medium + Medium = 5-7 points
- Combined: All low = 1-4 points

**Other indicators:**
- Number of saves/bookmarks (if available)
- Comments indicating "useful" or "saved"
- Frequency of reposts
- Influencer shares

### Technical Feasibility (10 points)

Evaluates how easily the prompt can be converted into an automated Clawdbot Skill.

| Score | Description |
|-------|-------------|
| 10 | Easily automatable, fits Clawdbot perfectly. No blockers. |
| 8-9 | Requires some tools, feasible. Minor dependencies. |
| 5-7 | Complex but possible. Significant effort needed. |
| 3-4 | Very difficult, may not work. Major technical challenges. |
| 1-2 | Impossible or requires external services. Cannot automate. |

**Feasibility Factors:**
- Can Claude execute the workflow?
- Does it require paid APIs or services?
- Are there external dependencies (beyond Clawdbot)?
- Is the workflow deterministic or ambiguous?
- Does it require human judgment/creativity?

**Clawdbot Capabilities:**
- Text processing and generation
- Web search and scraping
- File operations (read/write/edit)
- Code generation and execution
- API calls via exec/curl
- Browser automation via browser tool
- Messaging and notifications
- Calendar and scheduling
- Task scheduling via cron

**Red Flags (reduces score):**
- Requires specialized AI models not available
- Needs proprietary software or databases
- Complex image/video processing
- Real-time data feeds
- User authentication for external services
- Interactive GUI requirements

## Total Score Calculation

```
Total Score = Clarity + Uniqueness + Market + Feasibility
Maximum: 40 points
Recommended Threshold: 30 points (75%)
```

## Scoring Example

**Prompt:** "Write a professional email that politely declines a job offer while maintaining good relationship"

**Evaluation:**
- Clarity: 9/10 (Clear objective, complete instructions)
- Uniqueness: 6/10 (Common use case, but good template)
- Market: 7/10 (Professional emails always in demand)
- Feasibility: 10/10 (Pure text generation, Claude excels at this)

**Total:** 32/40 ✅ **Convert to skill**

**Prompt:** "Create a video from scratch using AI"

**Evaluation:**
- Clarity: 3/10 (Vague, what kind of video? what tools?)
- Uniqueness: 5/10 (AI video generation is popular)
- Market: 8/10 (High demand)
- Feasibility: 2/10 (Requires specialized video AI tools)

**Total:** 18/40 ❌ **Do not convert**

## Decision Thresholds

| Score Range | Action |
|-------------|--------|
| 35-40 | Immediate conversion, high priority |
| 30-34 | Convert soon, good potential |
| 25-29 | Consider conversion if unique aspect exists |
| 20-24 | Low priority, requires significant work |
| <20 | Do not convert |

## Quality Control

### Manual Review Required

Even for high-scoring prompts, manual review should assess:

1. **Ethical Considerations**
   - Does it promote harm?
   - Is it misleading or deceptive?
   - Does it violate policies?

2. **Legal Considerations**
   - Does it infringe on intellectual property?
   - Does it encourage illegal activities?
   - Are there privacy concerns?

3. **Practicality**
   - Is the workflow realistic?
   - Are the expectations reasonable?
   - Can it be tested and validated?

### Reject Regardless of Score

Reject prompts that:
- Generate harmful content (violence, hate speech, etc.)
- Engage in fraud or deception
- Violate platform policies
- Require breaking terms of service
- Promote unethical behavior
- Contain NSFW content
- Require illegal activities

## Continuous Improvement

Update evaluation criteria based on:
- Published skill performance (downloads, ratings)
- User feedback on converted skills
- Market trends and demand shifts
- Technical capabilities of Clawdbot
- Success/failure patterns

Regularly review the threshold and scoring weights to optimize for skill quality and market fit.
