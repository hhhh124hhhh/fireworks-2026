# Prompt Scoring Criteria

Comprehensive evaluation framework for WeChat cover prompt quality assessment.

## Scoring Overview

Each prompt is evaluated across four dimensions:
- **Technical Quality** (0-10): Technical specifications and parameters
- **Commercial Value** (0-10): Business potential and marketability
- **WeChat Compatibility** (0-10): Platform-specific optimization
- **Uniqueness** (0-10): Originality and differentiation

**Overall Score**: Average of all four dimensions (0-10)

**Quality Benchmarks:**
- 9.0-10.0: Excellent - Ready for commercial use
- 7.0-8.9: Good - Minor improvements recommended
- 5.0-6.9: Fair - Needs optimization
- 0.0-4.9: Poor - Significant rework required

---

## Dimension 1: Technical Quality (0-10)

### Scoring Rubric

**10 Points (Excellent)**
- Includes all technical specifications: aspect ratio, resolution, style
- Precise dimensions specified (900×383px or 2.35:1 aspect ratio)
- Advanced parameters included (lighting, render quality, camera settings)
- Clear, concise technical language
- No contradictory or conflicting specifications

**8-9 Points (Good)**
- Includes most technical specifications
- Aspect ratio present but may lack precision
- Good use of style and quality keywords
- Minor technical omissions

**5-7 Points (Fair)**
- Basic technical information present
- Aspect ratio may be missing or incorrect
- Some quality keywords included
- Technical language could be improved

**0-4 Points (Poor)**
- Missing critical technical specifications
- No aspect ratio or incorrect dimensions
- Vague or conflicting technical details
- Lacks quality indicators

### Technical Checklist

- [ ] Aspect ratio specified (2.35:1 or 900×383px)
- [ ] Resolution/quality mentioned (4K, high quality, detailed)
- [ ] Style/medium defined (photography, illustration, 3D render)
- [ ] Lighting specifications
- [ ] Color scheme mentioned
- [ ] Text placeholder area specified
- [ ] No technical contradictions

### Example Scoring

**Excellent (10/10):**
```
A professional magazine cover for a business WeChat official account, minimalist design, 
featuring abstract geometric shapes in blue and gold gradients, modern typography with 
headline space, clean layout, 900x383 aspect ratio, 4K quality, professional lighting 
--ar 2.35:1
```

**Poor (3/10):**
```
A business cover with some shapes and colors
```

---

## Dimension 2: Commercial Value (0-10)

### Scoring Rubric

**10 Points (Excellent)**
- Clearly targets high-demand market segment
- Professional, brand-ready aesthetic
- Scalable template applicable to multiple topics
- Strong differentiation from generic prompts
- High perceived value for content creators
- Ready for commercial productization

**8-9 Points (Good)**
- Targets recognizable market segment
- Professional aesthetic
- Good scalability
- Some differentiation
- Commercial potential exists

**5-7 Points (Fair)**
- Market segment identifiable
- Decent aesthetic quality
- Moderate scalability
- Generic but usable
- Basic commercial potential

**0-4 Points (Poor)**
- Unclear market positioning
- Unprofessional or inconsistent aesthetic
- Limited scalability
- Too generic or niche
- Low commercial viability

### Commercial Value Indicators

**High Value (+2 points):**
- Industry-specific (fintech, SaaS, healthcare, etc.)
- Professional corporate aesthetic
- Brand-safe and trustworthy
- Applicable to multiple content types
- solves clear pain point (design costs, time)

**Medium Value (+1 point):**
- Lifestyle category (food, travel, fashion)
- Good but not exceptional aesthetic
- Moderate scalability
- Clear use case

**Low Value (0 points):**
- Very niche or unclear audience
- Inconsistent or amateur aesthetic
- Limited applicability
- Generic or overused patterns

### Market Demand Assessment

**High Demand:**
- Business/Finance (fintech, corporate, investment)
- Technology (AI, SaaS, software)
- E-commerce (retail, marketplace)
- Education (courses, certifications)

**Medium Demand:**
- Lifestyle (food, travel, fashion)
- Health & Wellness
- Media & Entertainment

**Lower Demand:**
- Very specialized industries
- Unclear positioning

---

## Dimension 3: WeChat Compatibility (0-10)

### Scoring Rubric

**10 Points (Excellent)**
- Perfect dimensions (900×383px or 2.35:1)
- Explicit text placeholder for headlines
- WeChat ecosystem aesthetic
- Optimized for mobile viewing
- Color scheme fits WeChat UI
- Professional for Chinese audience

**8-9 Points (Good)**
- Correct aspect ratio
- Text space mentioned
- Good aesthetic fit
- Mobile-friendly
- Appropriate colors

**5-7 Points (Fair)**
- Aspect ratio present but could be more precise
- Text space implied but not explicit
- Decent aesthetic
- Minor WeChat optimization issues

**0-4 Points (Poor)**
- Missing or incorrect dimensions
- No text space for headlines
- Aesthetic doesn't fit WeChat
- Not optimized for platform
- Inappropriate for Chinese market

### WeChat Optimization Checklist

- [ ] Exact dimensions: 900×383px or 2.35:1 aspect ratio
- [ ] Text placeholder area specified
- [ ] Clean background for text readability
- [ ] High contrast for text overlay
- [ ] Mobile-friendly composition
- [ ] WeChat ecosystem keywords included
- [ ] Appropriate for Chinese audience (colors, symbols, style)

### WeChat-Specific Considerations

**Must-Have:**
- Aspect ratio: 2.35:1 (900×383px)
- Text space for headlines (left, right, or center)
- High contrast for text readability
- Professional, brand-safe aesthetic

**Should-Have:**
- WeChat official account style references
- Chinese social media aesthetic
- Mobile-optimized layout
- Clean, uncluttered design

**Nice-to-Have:**
- WeChat color palette integration
- Mobile thumbnail optimization
- WeChat UI element references

### Common Issues

**Missing Text Space** (-2 points):
- Prompt doesn't specify where headline goes
- No clean background area for text overlay

**Incorrect Dimensions** (-3 points):
- Wrong aspect ratio (e.g., 16:9 instead of 2.35:1)
- Missing dimension specifications

**Poor Contrast** (-1 point):
- Background too busy for text overlay
- Colors that don't provide good text readability

---

## Dimension 4: Uniqueness (0-10)

### Scoring Rubric

**10 Points (Excellent)**
- Highly original concept
- Creative combination of elements
- Novel interpretation of category
- Distinctive visual language
- Not derivative of existing templates
- Creative innovation apparent

**8-9 Points (Good)**
- Good originality
- Creative elements present
- Unique perspective
- Some differentiation from common patterns
- Interesting combinations

**5-7 Points (Fair)**
- Some unique elements
- Moderate creativity
- Minor differentiation
- Follows common patterns with small twists
- Adequately unique

**0-4 Points (Poor)**
- Very generic or cliché
- Overused patterns
- No creative elements
- Derivative of existing templates
- Lacks originality

### Uniqueness Indicators

**High Uniqueness (+2 points):**
- Novel concept or approach
- Creative color combinations
- Innovative visual elements
- Fresh interpretation of category
- Unexpected but effective combinations

**Medium Uniqueness (+1 point):**
- Some creative elements
- Interesting variations
- Good but not groundbreaking

**Low Uniqueness (0 points):**
- Generic, common patterns
- Standard category conventions
- Overused templates

### Creativity Assessment

**Creative Innovation:**
- Unexpected subject matter treatment
- Unique composition techniques
- Innovative use of style/medium
- Creative color palettes
- Fresh visual metaphors

**Derivative Warning Signs:**
- Follows exact same structure as common templates
- Uses overused color schemes without variation
- Generic visual language
- Lacks personal or brand touch

---

## Scoring Examples

### Example 1: High-Scoring Prompt (9.5/10)

```
Modern fintech cover for WeChat official account, blockchain network visualization with 
interconnected glowing nodes and digital chains, deep blue and emerald green gradient 
background, abstract data visualization elements, clean headline space at top left, 
professional corporate aesthetic, high contrast, 4K render, 900x383 aspect ratio --ar 2.35:1
```

**Scoring:**
- Technical Quality: 10/10 (all specs present, precise, professional)
- Commercial Value: 9/10 (fintech is high-demand, professional, scalable)
- WeChat Compatibility: 10/10 (perfect dimensions, text space, optimized)
- Uniqueness: 9/10 (creative blockchain visualization, distinctive)

**Overall: 9.5/10 - Excellent**

---

### Example 2: Medium-Scoring Prompt (7.0/10)

```
A business cover with some blue and green colors, clean design, 900x383 aspect ratio
```

**Scoring:**
- Technical Quality: 7/10 (has dimensions, but lacks quality specs)
- Commercial Value: 6/10 (business category OK but vague)
- WeChat Compatibility: 8/10 (correct dimensions, but no text space)
- Uniqueness: 7/10 (generic but not terrible)

**Overall: 7.0/10 - Fair to Good**

---

### Example 3: Low-Scoring Prompt (4.0/10)

```
Make a cover for my article
```

**Scoring:**
- Technical Quality: 1/10 (no technical specs)
- Commercial Value: 3/10 (unclear market positioning)
- WeChat Compatibility: 2/10 (no dimensions or optimization)
- Uniqueness: 0/10 (completely generic)

**Overall: 4.0/10 - Poor**

---

## Improvement Recommendations

### For Low Scores (0-4):
1. Add technical specifications (aspect ratio, resolution, quality)
2. Define industry/category and target audience
3. Specify text space and WeChat optimization
4. Add style and visual elements
5. Include color scheme and composition details

### For Medium Scores (5-7):
1. Refine technical specifications
2. Be more specific about industry use case
3. Add unique creative elements
4. Enhance WeChat optimization details
5. Improve clarity and conciseness

### For High Scores (8-9):
1. Polish wording and flow
2. Add innovative creative touches
3. Enhance differentiation from templates
4. Verify all specifications are optimal
5. Consider scalability for multiple uses

---

## Automated Scoring Script

Use `scripts/score_prompt.py` for automated evaluation based on these criteria.

**Usage:**
```bash
python3 /root/clawd/skills/wechat-cover-generator/scripts/score_prompt.py "<prompt>"
```

The script will output scores for each dimension with explanations and improvement suggestions.
