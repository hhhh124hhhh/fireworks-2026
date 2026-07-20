# Prompt Optimization Guide

Techniques and best practices for improving existing prompts to meet WeChat cover specifications and quality standards.

## Overview

This guide covers:
- WeChat-specific optimizations
- Dimension and aspect ratio adjustments
- Text space enhancement
- Color scheme refinement
- Technical parameter tuning
- Common issues and fixes

---

## WeChat-Specific Optimizations

### 1. Aspect Ratio Correction

**WeChat Cover Dimensions:**
- Standard: 900×383 pixels
- Aspect ratio: 2.35:1 (cinematic wide)
- Must include: `--ar 2.35:1` or `900x383 aspect ratio`

**Common Issues and Fixes:**

**Problem:** Wrong aspect ratio (16:9, 4:3, 1:1)
```
Before: A corporate cover --ar 16:9
After: A corporate cover for WeChat official account, 900x383 aspect ratio --ar 2.35:1
```

**Problem:** No aspect ratio specified
```
Before: A business cover with blue background
After: A business cover for WeChat official account, blue background, 
        900x383 aspect ratio, --ar 2.35:1
```

**Problem:** Inconsistent aspect ratio formats
```
Before: A cover, aspect ratio 2.35:1
After: A professional cover, 900x383 aspect ratio --ar 2.35:1
```

### 2. Text Space Specification

**Why Text Space Matters:**
- WeChat covers always need headlines (10-30 characters)
- Text must be legible over the image
- Clean areas needed for overlay

**Text Space Placement Options:**
- Left side: "clean headline space on left"
- Right side: "clean headline space on right"
- Center: "clean headline space at center"
- Bottom: "clean text area at bottom"

**Common Issues and Fixes:**

**Problem:** No text space specified
```
Before: A fintech cover with blockchain elements
After: A fintech cover for WeChat official account, blockchain network 
        visualization with clean headline space on left side, 
        deep blue and emerald green gradients, 900x383 aspect ratio --ar 2.35:1
```

**Problem:** Busy background makes text illegible
```
Before: A cover with many overlapping elements
After: A clean minimalist cover with plenty of white space for text overlay, 
        organized elements, high contrast background, 900x383 aspect ratio --ar 2.35:1
```

### 3. WeChat Ecosystem Keywords

**Keywords to Add:**
- "WeChat official account"
- "Chinese social media aesthetic"
- "WeChat cover style"
- "Mobile-optimized"
- "Social media banner"

**Example:**
```
Before: A professional business cover
After: A professional business cover for WeChat official account, 
        Chinese social media aesthetic, mobile-optimized layout, 
        900x383 aspect ratio --ar 2.35:1
```

### 4. Chinese Market Considerations

**Color Preferences:**
- **Red:** Fortune, celebration (use sparingly)
- **Gold:** Wealth, premium, luxury
- **Blue:** Trust, professionalism, technology
- **Green:** Growth, health, finance
- **White:** Clean, purity, professional

**Avoid:**
- Overly dark or somber colors
- Inappropriate cultural symbols
- Political or sensitive imagery
- Western-centric themes without localization

**Example:**
```
Before: A luxury cover in black and silver
After: A premium luxury cover for WeChat official account, gold and navy 
        blue color scheme, elegant aesthetic, trustworthy and sophisticated, 
        900x383 aspect ratio --ar 2.35:1
```

---

## Dimension and Aspect Ratio Adjustments

### Understanding Aspect Ratios

**Common Ratios:**
- 2.35:1 - WeChat cover (cinematic wide)
- 16:9 - Standard widescreen
- 4:3 - Traditional TV
- 1:1 - Square

**Why 2.35:1 for WeChat:**
- Optimized for mobile viewing
- Allows horizontal text placement
- Fits WeChat's header display
- Balances subject and text

### Conversion Examples

**16:9 to 2.35:1:**
```
Before: A cover, 1920x1080, --ar 16:9
After: A cover optimized for WeChat, 900x383 pixels, cinematic composition, 
        wider horizontal layout, --ar 2.35:1
```

**Square to 2.35:1:**
```
Before: A circular logo in center, --ar 1:1
After: A horizontal cover layout with logo on left, wide composition, 
        cinematic aspect ratio, 900x383 aspect ratio --ar 2.35:1
```

### Composition Adjustments

**Wide Layout Techniques:**
- Horizontal elements (lines, shapes)
- Left-right flow
- Asymmetric balance
- Negative space on sides

**Example:**
```
Before: A centered composition with subject in middle
After: A horizontal composition with subject slightly off-center, 
        negative space on left for text, wide cinematic layout, 
        900x383 aspect ratio --ar 2.35:1
```

---

## Text Space Enhancement

### Creating Text-Friendly Backgrounds

**Technique 1: Gradient Backgrounds**
```
Professional corporate cover for WeChat official account, subtle 
gradient background from dark blue to lighter blue, clean ample 
space for headline text overlay, minimal elements, 900x383 
aspect ratio --ar 2.35:1
```

**Technique 2: Clean Solid Colors**
```
Minimalist cover for WeChat official account, clean white or light 
gray background with small accent elements on right, large text 
area on left, professional and simple, 900x383 aspect ratio --ar 2.35:1
```

**Technique 3: Blurred Backgrounds**
```
Corporate cover with blurred office background, sharp foreground 
elements, clean text area on left with solid overlay, professional 
aesthetic, 900x383 aspect ratio --ar 2.35:1
```

**Technique 4: Compositional Spacing**
```
Modern tech cover with geometric shapes arranged on right side, 
clean open space on left for headline, balanced composition, 
minimalist design, 900x383 aspect ratio --ar 2.35:1
```

### Contrast Enhancement

**Ensure Text Readability:**
- High contrast between text area and background
- Avoid busy patterns under text
- Use solid or gradient overlays if needed
- Test different color combinations

**Example:**
```
Before: A cover with colorful patterned background
After: A cover with subtle patterned background and light overlay 
        for high contrast text area, clean headline space, 
        900x383 aspect ratio --ar 2.35:1
```

---

## Color Scheme Refinement

### Professional Color Palettes

**Business/Finance:**
```
Professional business cover for WeChat official account, navy blue 
and gold color scheme with white accents, corporate aesthetic, 
clean text area, 900x383 aspect ratio --ar 2.35:1
```

**Technology:**
```
Modern tech cover for WeChat official account, deep blue and cyan 
with white accents, futuristic aesthetic, clean design, 
900x383 aspect ratio --ar 2.35:1
```

**Lifestyle:**
```
Lifestyle cover for WeChat official account, warm natural colors, 
soft pastel palette, inviting and friendly, clean text space, 
900x383 aspect ratio --ar 2.35:1
```

### Color Psychology for WeChat

**Blue:** Trust, professionalism (most popular)
**Green:** Growth, health, finance
**Gold/Premium Colors:** Luxury, high-end
**White/Gray:** Clean, minimal, professional
**Red:** Energy, attention (use sparingly)

### Color Harmony Techniques

**Monochromatic:**
```
Monochromatic blue cover for WeChat official account, various 
shades of blue from dark to light, professional and cohesive, 
clean text space, 900x383 aspect ratio --ar 2.35:1
```

**Complementary:**
```
Complementary color scheme cover for WeChat official account, 
blue and orange with white accents, vibrant yet professional, 
clean headline space, 900x383 aspect ratio --ar 2.35:1
```

**Analogous:**
```
Analogous color palette cover for WeChat official account, 
shades of blue and green with white accents, harmonious and 
professional, clean text area, 900x383 aspect ratio --ar 2.35:1
```

---

## Technical Parameter Tuning

### Quality and Resolution

**High-Quality Keywords:**
- "4K quality"
- "8K resolution"
- "ultra high definition"
- "professional photography"
- "magazine-quality"

**Example:**
```
Before: A corporate cover
After: A professional corporate cover for WeChat official account, 
        4K quality, high resolution, magazine-quality photography, 
        900x383 aspect ratio --ar 2.35:1
```

### Lighting and Atmosphere

**Lighting Types:**
- "soft natural lighting"
- "golden hour"
- "studio lighting"
- "professional lighting"
- "dramatic lighting"
- "soft ambient lighting"

**Example:**
```
Professional cover for WeChat official account, clean minimalist 
design, soft studio lighting, professional atmosphere, high 
contrast, 4K quality, 900x383 aspect ratio --ar 2.35:1
```

### Style and Medium

**Style Options:**
- "photorealistic"
- "minimalist"
- "modern"
- "corporate"
- "editorial"
- "abstract"

**Medium Options:**
- "photography"
- "3D render"
- "digital art"
- "vector illustration"
- "mixed media"

**Example:**
```
Modern fintech cover for WeChat official account, 3D render of 
abstract geometric shapes, minimalist design, photorealistic 
quality, professional aesthetic, 4K render, 900x383 aspect ratio --ar 2.35:1
```

### Camera and Composition

**Camera Settings:**
- "wide angle"
- "telephoto"
- "shallow depth of field"
- "sharp focus"
- "professional photography"

**Composition:**
- "balanced composition"
- "asymmetric balance"
- "rule of thirds"
- "minimalist layout"
- "clean arrangement"

**Example:**
```
Professional photography cover for WeChat official account, 
wide angle shot with balanced composition, shallow depth of field, 
clean background, sharp subject, 4K quality, 900x383 aspect ratio --ar 2.35:1
```

---

## Common Issues and Fixes

### Issue 1: Generated Images Don't Match Specs

**Symptoms:**
- Wrong dimensions
- Incorrect aspect ratio
- Poor quality

**Fixes:**
```
Add/verify:
- 900x383 aspect ratio
- --ar 2.35:1
- 4K quality or high resolution
- Specific style/medium
```

### Issue 2: Text Overlap Problems

**Symptoms:**
- Text covers important image elements
- Text illegible due to background
- No space for headline

**Fixes:**
```
Add/verify:
- "clean headline space on [location]"
- "high contrast background for text"
- "solid or gradient text area"
- "minimal background elements under text"
```

### Issue 3: Aesthetic Doesn't Fit WeChat

**Symptoms:**
- Too artistic/abstract
- Inappropriate for professional use
- Doesn't match WeChat style

**Fixes:**
```
Add/verify:
- "WeChat official account style"
- "Chinese social media aesthetic"
- "professional and trustworthy"
- "corporate or business-appropriate"
- Appropriate color scheme
```

### Issue 4: Images Look Generic

**Symptoms:**
- Overused patterns
- Lacks uniqueness
- Not differentiated

**Fixes:**
```
Add:
- Unique creative elements
- Industry-specific details
- Distinctive color combinations
- Novel composition approaches
- Personal or brand touches
```

### Issue 5: Poor Image Quality

**Symptoms:**
- Blurry or pixelated
- AI artifacts (distortion, extra elements)
- Low detail

**Fixes:**
```
Add/verify:
- "4K quality" or "8K resolution"
- "high detail"
- "professional quality"
- "photorealistic" or specific medium
- Quality boosters (--v 6.0, --style raw, etc.)
```

---

## Optimization Workflow

### Step-by-Step Process

**Step 1: Evaluate Current Prompt**
- Identify missing elements
- Check WeChat compatibility
- Assess quality issues

**Step 2: Add Required Elements**
- Aspect ratio: 900x383px, --ar 2.35:1
- Text space specification
- WeChat context keywords
- Resolution/quality specs

**Step 3: Improve Quality**
- Add technical parameters
- Enhance color scheme
- Improve composition
- Add lighting details

**Step 4: Refine and Polish**
- Ensure smooth flow
- Remove contradictions
- Check for clarity
- Verify all specs

**Step 5: Test and Iterate**
- Generate test image
- Evaluate against requirements
- Make adjustments if needed
- Document successful patterns

### Before/After Examples

**Example 1: Fintech Cover**

**Before:**
```
A blockchain cover with some cool effects
```

**After:**
```
Modern fintech cover for WeChat official account, blockchain network 
visualization with interconnected glowing nodes and digital chains, 
deep blue and emerald green gradient background, clean headline space 
at top left, professional corporate aesthetic, high contrast, 4K render, 
900x383 aspect ratio --ar 2.35:1
```

**Improvements:**
- Added WeChat context
- Specified aspect ratio
- Added text space
- Enhanced technical specs
- Improved color scheme

---

**Example 2: Lifestyle Cover**

**Before:**
```
Food photo --ar 16:9
```

**After:**
```
Vibrant food photography cover for WeChat official account, close-up 
shot of steaming Asian cuisine, warm natural lighting, shallow depth 
of field, appetizing presentation, clean text space on left side, 
magazine-quality, bright and inviting colors, professional food styling, 
900x383 aspect ratio --ar 2.35:1
```

**Improvements:**
- Corrected aspect ratio
- Added WeChat optimization
- Enhanced technical details
- Specified text space
- Improved photography specs

---

## Quick Reference Checklist

Use this checklist when optimizing prompts:

### Essential (Must Have)
- [ ] 900x383 aspect ratio or --ar 2.35:1
- [ ] "WeChat official account" or similar
- [ ] Text space specification
- [ ] Resolution/quality (4K, high quality)
- [ ] High contrast for text

### Important (Should Have)
- [ ] Specific industry/category
- [ ] Clear style/medium
- [ ] Color scheme
- [ ] Composition details
- [ ] Professional aesthetic

### Nice to Have
- [ ] Unique creative elements
- [ ] Industry-specific details
- [ ] Lighting specifications
- [ ] Camera settings
- [ ] Quality boosters (--v 6.0, etc.)

---

## Continuous Improvement

**Track What Works:**
- Note which optimizations improve results
- Document successful patterns
- Monitor user feedback
- Analyze generated image quality

**Regular Updates:**
- Update prompts as AI tools evolve
- Adapt to changing WeChat guidelines
- Incorporate new best practices
- Learn from extraction from X

**Testing Framework:**
- Generate test images regularly
- Evaluate against quality criteria
- Score prompts before/after optimization
- Track improvement metrics
