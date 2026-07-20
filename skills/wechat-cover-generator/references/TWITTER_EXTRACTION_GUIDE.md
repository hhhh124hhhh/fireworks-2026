# X (Twitter) Prompt Extraction Guide

Comprehensive guide for mining X (Twitter) for high-quality AI image generation prompts and adapting them for WeChat covers.

## Overview

This guide teaches you how to:
- Search X effectively for AI art prompts
- Identify high-quality prompts from search results
- Extract and filter prompts based on engagement metrics
- Adapt extracted prompts for WeChat cover specifications
- Integrate new prompts into the template library

---

## Search Strategies

### Primary Search Queries

Use these query patterns to find AI image generation prompts on X:

**General AI Art Prompts:**
```
AI art prompt
Midjourney prompt
Stable Diffusion prompt
"prompt engineering" image
DALL-E prompt
AI image generation
```

**WeChat-Specific:**
```
WeChat cover AI
"公众号封面" AI
Chinese AI art prompt
social media cover AI
2.35:1 aspect ratio prompt
```

**High-Quality Indicators:**
```
"best AI prompt" image
"amazing prompt" AI art
"prompt template" Midjourney
"pro prompt" Stable Diffusion
```

### Advanced Search Operators

Use X's search operators for better results:

**Quotes for exact phrases:**
```
"Midjourney prompt template"
"AI art style guide"
"prompt engineering tutorial"
```

**Exclude unwanted results:**
```
AI prompt -spam -bot -ad
Midjourney prompt -crypto -NFT
```

**Hashtag combinations:**
```
#AIart #prompt
#Midjourney #tutorial
#StableDiffusion #prompt
```

**Date filtering:**
```
AI prompt since:2026-01-01
Midjourney prompt from:2026-01-01 until:2026-01-28
```

**Language filtering:**
```
AI prompt lang:en
AI 提示词 lang:zh
```

### Account Types to Follow

**Prompt Engineers & AI Artists:**
- Look for accounts that consistently share high-quality prompts
- Check follower count and engagement ratios
- Prioritize accounts with expertise in AI art

**AI Tool Creators:**
- Official accounts of Midjourney, Stable Diffusion, DALL-E
- Prompt engineering influencers
- AI art communities

**Design & Content Creation:**
- UI/UX designers sharing AI workflows
- Content marketers using AI tools
- Graphic design professionals

---

## Quality Assessment Framework

### Engagement Metrics as Quality Indicators

**High Quality (Consider for extraction):**
- Likes: 500+
- Retweets: 100+
- Replies: 50+
- Ratio: High engagement relative to follower count

**Medium Quality (Review case-by-case):**
- Likes: 100-500
- Retweets: 20-100
- Replies: 10-50

**Low Quality (Skip):**
- Likes: <100
- Retweets: <20
- Replies: <10

**Exceptions:**
- New accounts with high quality but low engagement
- Niche topics with smaller audiences
- Recent posts that haven't had time to accumulate engagement

### Visual Quality Indicators

**Look for prompts that generate:**
- Clear, sharp images
- Good composition and balance
- Appropriate use of negative space
- Professional aesthetic
- High detail and resolution

**Red flags:**
- Blurry or distorted images
- Cluttered, chaotic compositions
- Poor color choices
- Amateur or unprofessional appearance
- AI artifacts (distortion, extra limbs, weird textures)

### Prompt Structure Quality

**High-Quality Prompt Structure:**
```
[Subject + action/context] + [style/medium] + [composition/layout] + 
[technical specs] + [quality parameters] + [aspect ratio]
```

**Example of Good Structure:**
```
A serene mountain landscape at golden hour, dramatic sunset colors, 
photorealistic oil painting style, wide angle shot, majestic composition, 
soft atmospheric lighting, high detail, 8K resolution, --ar 16:9
```

**Poor Structure Examples:**
```
mountain sunset
make it pretty
good image
```

---

## Extraction Process

### Step 1: Identify Candidate Prompts

1. Run searches using the strategies above
2. Scan results for high engagement
3. Check attached images for visual quality
4. Read the full prompt text

### Step 2: Evaluate Prompt Quality

Use the quality assessment framework:

**Technical Quality Check:**
- [ ] Clear subject and context
- [ ] Style/medium specified
- [ ] Composition/layout described
- [ ] Technical parameters included
- [ ] Aspect ratio specified

**Visual Quality Check:**
- [ ] Generated image is sharp and clear
- [ ] Good composition and balance
- [ ] Professional aesthetic
- [ ] High detail level

**Engagement Check:**
- [ ] Likes > 500 (or > 100 for niche topics)
- [ ] Retweets > 100 (or > 20 for niche)
- [ ] Positive comments and replies

### Step 3: Extract the Prompt

1. Copy the full prompt text
2. Note any variations or versions shared
3. Check if the author provided additional context or tips
4. Document the source (account, date, URL)

**Extraction Template:**
```json
{
  "prompt": "Full prompt text here",
  "source": "@account_name",
  "date": "2026-01-28",
  "url": "https://twitter.com/...",
  "likes": 1234,
  "retweets": 234,
  "category": "Technology",
  "visual_quality": "High",
  "technical_quality": "High",
  "notes": "Additional context or observations"
}
```

### Step 4: Filter and Prioritize

**Prioritize extraction of:**
- Prompts with high engagement (>1000 likes)
- Prompts from reputable accounts
- Prompts in target categories (business, tech, lifestyle, etc.)
- Prompts with clear structure
- Prompts adaptable to WeChat covers

**Skip:**
- Spam or low-effort prompts
- Overly generic prompts
- Prompts in irrelevant categories
- Prompts with poor structure
- Prompts from low-quality sources

---

## WeChat Adaptation Process

### Step 1: Identify Adaptation Potential

**Prompts Good for Adaptation:**
- Clean, minimal designs
- Professional or corporate aesthetic
- Clear subject and composition
- Good use of negative space
- Appropriate for business/marketing

**Challenging to Adapt:**
- Portrait-oriented compositions
- Very complex or busy designs
- Highly stylized or artistic interpretations
- Prompts relying on specific characters or IP
- Inappropriate for professional contexts

### Step 2: WeChat-Specific Modifications

**Required Modifications:**
1. **Add Aspect Ratio:** Include `--ar 2.35:1` or `900x383 aspect ratio`
2. **Add Text Space:** Specify "clean headline space at [location]"
3. **Add WeChat Context:** Include "WeChat official account style" or "Chinese social media aesthetic"
4. **Add Resolution:** Include "4K quality" or "high resolution"
5. **Add Contrast:** Include "high contrast" or "clean background"

**Example Adaptation:**

**Original Prompt (from X):**
```
A modern office building with glass facade, sunset lighting, 
photorealistic, 8K, professional photography --ar 16:9
```

**Adapted for WeChat:**
```
Modern corporate building photography for WeChat official account, 
glass facade with sunset lighting, photorealistic style, clean 
headline space on left side, high contrast background, professional 
corporate aesthetic, 4K quality, 900x383 aspect ratio --ar 2.35:1
```

### Step 3: Quality Verification

After adaptation, verify:
- [ ] Aspect ratio is 2.35:1 or 900×383px
- [ ] Text space is clearly specified
- [ ] WeChat context keywords included
- [ ] Resolution/quality specified
- [ ] Contrast mentioned for text readability
- [ ] Overall prompt still flows naturally

### Step 4: Test and Iterate

**Testing:**
- Generate a test image with the adapted prompt
- Evaluate if it meets WeChat cover requirements
- Check if text overlay is possible
- Assess visual quality

**Iteration:**
- If issues found, refine the prompt
- Test again until quality is satisfactory
- Document successful patterns for future adaptations

---

## Integration into Template Library

### Categorization

Before adding to PROMPT_TEMPLATES.md:

1. **Identify Industry Category:**
   - Business & Finance (fintech, corporate, investment)
   - Technology (AI, SaaS, hardware)
   - Lifestyle (food, travel, fashion)
   - Education (courses, tutorials)
   - Healthcare (medical, wellness)
   - Media & Entertainment (gaming, streaming)
   - E-commerce (retail, marketplace)
   - Professional Services (marketing, design)

2. **Create Sub-category or Variation:**
   - If similar to existing template, add as variation
   - If new direction, create new sub-category
   - If completely novel, create new category section

3. **Document the Source:**
   - Note the original X account
   - Include date of extraction
   - Reference the URL

### Format for Integration

**Add to PROMPT_TEMPLATES.md:**
```markdown
### [Industry/Sub-category]
```
Original Prompt extracted from @account_name (2026-01-28)
```
[Adapted prompt text with WeChat optimizations]
```

**Variations:**
- [Variation 1 description]
- [Variation 2 description]

**Color Palette:**
- Primary: [colors]
- Secondary: [colors]
- Accent: [colors]
```

### Quality Score

Before adding to library, score the prompt using SCORING_CRITERIA.md:
- If score ≥ 8.0: Add directly
- If score 7.0-7.9: Add with improvements
- If score < 7.0: Improve before adding or skip

---

## Automated Scanning

### Scan Script Configuration

The automated scanner (`scripts/scan_twitter_prompts.py`) uses these parameters:

**Search Configuration:**
```python
{
  "queries": [
    "AI art prompt",
    "Midjourney prompt",
    "Stable Diffusion prompt",
    "WeChat cover AI"
  ],
  "min_likes": 100,
  "min_retweets": 20,
  "max_results": 50,
  "categories": [
    "business", "technology", "lifestyle", "education"
  ]
}
```

**Output Format:**
- Extracted prompts saved to `scripts/extracted_prompts.json`
- Each entry includes prompt, source, engagement metrics
- JSON format for easy parsing and integration

**Schedule:**
- Runs every 6 hours via cron
- Timestamped logs for tracking
- Automatic deduplication

### Manual Scan

For manual scanning:

1. Use the search strategies above
2. Evaluate quality using the framework
3. Extract promising prompts
4. Adapt for WeChat
5. Score and add to library if high quality

---

## Best Practices

### Do's
- Follow reputable AI artists and prompt engineers
- Check engagement metrics for quality signals
- Adapt prompts specifically for WeChat requirements
- Test adapted prompts before adding to library
- Document sources and dates for attribution
- Regularly scan for new prompt patterns

### Don'ts
- Extract spam or low-quality content
- Skip engagement quality checks
- Adapt without proper WeChat optimization
- Add low-scoring prompts to library
- Overlook attribution and documentation
- Rely on a single source or account

### Continuous Improvement

1. **Track Performance:**
   - Monitor which templates get most use
   - Track user feedback and requests
   - Identify gaps in template library

2. **Regular Scans:**
   - Scheduled scans every 6 hours
   - Manual scans for emerging trends
   - Focus on high-demand categories

3. **Quality Control:**
   - Score all new prompts before adding
   - Remove low-performing templates
   - Update templates based on feedback

4. **Market Trends:**
   - Monitor new AI tools and techniques
   - Adapt to changing WeChat guidelines
   - Update color palettes and aesthetics

---

## Example Workflow

### Full Extraction and Integration Workflow

**1. Search X:**
```
Query: "Midjourney prompt" business cover
Filter: likes > 500, since:2026-01-01
```

**2. Identify Candidate:**
- Found prompt with 1,234 likes from reputable AI artist
- Visual quality: High
- Technical quality: Excellent structure

**3. Extract:**
```json
{
  "prompt": "A professional corporate cover with geometric shapes, 
             blue and gold gradients, minimalist design, --ar 16:9",
  "source": "@AI_Prompt_Master",
  "date": "2026-01-25",
  "url": "https://twitter.com/...",
  "likes": 1234,
  "retweets": 234
}
```

**4. Adapt for WeChat:**
```
Professional corporate cover for WeChat official account, geometric 
shapes in blue and gold gradients, minimalist design with clean 
headline space at top left, 900x383 aspect ratio, 4K quality, 
high contrast --ar 2.35:1
```

**5. Score:**
- Technical Quality: 10/10
- Commercial Value: 9/10
- WeChat Compatibility: 10/10
- Uniqueness: 8/10
- **Overall: 9.25/10**

**6. Add to Library:**
Add to PROMPT_TEMPLATES.md under "Business & Finance > Corporate & Professional Services"

---

## Troubleshooting

### Problem: Low-Quality Results

**Solutions:**
- Refine search queries with more specific terms
- Increase minimum engagement thresholds
- Focus on specific categories
- Follow better accounts

### Problem: Adapting Doesn't Work

**Solutions:**
- Check if original prompt is suitable for adaptation
- Ensure all WeChat-specific modifications are applied
- Test and iterate on adaptation
- Consider if a different adaptation approach is needed

### Problem: Too Many Results

**Solutions:**
- Narrow search with more specific terms
- Increase minimum engagement thresholds
- Focus on specific accounts or hashtags
- Use date filters for recent content

### Problem: Duplicate Prompts

**Solutions:**
- Use deduplication in automated scanner
- Check existing library before adding
- Document sources to track variations
- Only keep highest-quality version
