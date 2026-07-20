---
name: brand-creative-suite
description: Generate professional brand visual content using AI image generation. Includes brand-themed flower bouquets, brand planets, style transfer (water/flow, paper-glass), and creative brand scenes (treehouse, parachute packaging). Use when creating brand marketing materials, social media visuals, product ads, or any brand-focused creative content that requires professional AI-generated imagery.
---

# Brand Creative Suite

## Overview

Generate professional, brand-focused visual content using Nano Banana Pro's advanced AI image generation capabilities. This skill provides template-based workflows for creating brand-themed creative assets including flower arrangements, planetary worlds, style transfers, and imaginative scenes.

## Quick Start

**Basic usage pattern:**
1. Identify the brand name and key visual elements (logo, colors, tagline)
2. Choose the creative template type
3. Configure parameters (style, mood, composition)
4. Generate and iterate

**Example prompt:**
```
Create a brand-themed flower bouquet for [Brand Name] with [Brand Colors]. The flowers should be arranged as a romantic gift, with the brand's signature [Product] as the centerpiece. Warm, elegant lighting.
```

## Creative Templates

### 1. Brand Flower Bouquet Generator

**Purpose:** Generate romantic, elegant flower arrangements featuring brand products or logos.

**Template parameters:**
- `brand_name`: Company or product name
- `brand_colors`: Brand's signature colors (hex codes or descriptions)
- `product_type`: Featured product (perfume, jewelry, cosmetics, etc.)
- `flower_types`: Specific flowers or "assorted"
- `arrangement_style`: "romantic", "modern", "elegant", "luxury"
- `centerpiece_type`: Product placement (floating, resting, wrapped)

**Base prompt structure:**
```
A luxurious bouquet of [flowers] featuring [brand_name]'s [product_type]. 
The [centerpiece_type] among the blooms. [brand_colors] accent colors. 
[lighting] lighting. [composition] composition.
```

**Reference:** See [references/flower-templates.md](references/flower-templates.md) for 10+ curated examples from Nano Banana Pro case studies.

### 2. Brand Planet World Creator

**Purpose:** Create imaginative planetary worlds themed around a brand.

**Template parameters:**
- `brand_name`: Brand to feature
- `planet_type`: "realistic", "stylized", "whimsical", "sci-fi"
- `surface_elements`: Logo shapes, product icons, brand symbols
- `atmosphere`: Dreamy, dramatic, peaceful, energetic
- `lighting_time`: Day, sunset, night, twilight
- `camera_angle`: Wide shot, orbit view, surface close-up

**Base prompt structure:**
```
A [planet_type] planet themed around [brand_name]. 
[brand_colors] landscape featuring [surface_elements]. 
[lighting_time] with [atmosphere] atmosphere. 
[camera_angle]. 4K resolution.
```

**Reference:** See [references/planet-templates.md](references/planet-templates.md) for creative examples.

### 3. Brand Style Transfer

**Purpose:** Transform brand products into artistic styles (water flow, paper-glass, ceramic, etc.).

**Template parameters:**
- `brand_product`: Product to transform
- `style_type`: "water-flow-sculpture", "paper-glass", "ceramic", "gold-abstract"
- `background_type`: Clean, gradient, natural, abstract
- `lighting_style`: Dramatic, soft, studio, natural
- `detail_level`: Minimal, moderate, intricate

**Base prompt structure:**
```
[brand_product] rendered in [style_type] style. 
[background_type] background. [lighting_style] lighting. 
[detail_level] details. Professional product photography.
```

**Reference:** See [references/style-transfer-templates.md](references/style-transfer-templates.md) for style variations.

### 4. Brand Scene Generator

**Purpose:** Create imaginative brand-themed scenes and settings.

**Template parameters:**
- `scene_type`: "luxury-treehouse", "parachute-delivery", "underwater-world", "floating-island"
- `brand_elements`: Logo, products, brand colors
- `mood`: "serene", "dynamic", "magical", "adventurous"
- `time_of_day`: Golden hour, night, dawn, bright day
- `detail_inclusion`: Include/exclude specific elements

**Base prompt structure:**
```
A [mood] [scene_type] featuring [brand_elements]. 
[time_of_day] lighting. Cinematic composition. 
Hyper-realistic with [detail_level] detail. 4K.
```

**Reference:** See [references/scene-templates.md](references/scene-templates.md) for scene variations.

## Parameter Optimization Guide

### Color Integration

**Effective approaches:**
- Use brand colors as accents (20-30% of palette)
- Pair brand colors with complementary neutrals
- For multi-color brands, focus on primary brand color + secondary
- Consider color psychology (warm = inviting, cool = premium)

**Example:**
```
Brand: Nike (Black/White/Orange)
Palette: Dominant white/gray, black accents, orange highlights
```

### Composition Best Practices

**Product placement strategies:**
- **Center stage**: Hero product in center, brand colors framing
- **Rule of thirds**: Product at intersection, brand elements at corners
- **Natural flow**: Products integrated into environment, logo subtle
- **Logo prominence**: Large logo for awareness campaigns, subtle for brand reinforcement

### Style Selection Guide

| Use Case | Recommended Template | Style |
|----------|---------------------|-------|
| Luxury brands | Flower Bouquet, Planet | Elegant, sophisticated |
| Tech products | Style Transfer, Scene | Modern, sleek |
| Fashion/Beauty | Flower Bouquet | Romantic, dreamy |
| Consumer goods | Scene Generator | Approachable, relatable |
| Food & Beverage | Scene Generator | Appetizing, vibrant |

## Advanced Techniques

### Multi-Image Compositions

For complex campaigns requiring multiple related visuals:

1. **Consistent color palette**: Define brand colors upfront
2. **Cohesive lighting**: Use same lighting style across images
3. **Narrative sequence**: Plan visual story arc (reveal → showcase → action)
4. **Brand consistency**: Keep logo placement similar but not identical

**Example sequence:**
1. Planet world (brand setting introduction)
2. Flower bouquet (product presentation)
3. Scene generator (product in use)

### A/B Testing Workflow

Generate variations to test different creative approaches:

```
Base product: [brand_name] [product_type]

Variation A: Minimalist style, clean background, soft lighting
Variation B: Dynamic style, gradient background, dramatic lighting
Variation C: Artistic style, textured background, natural lighting
```

Run `scripts/generate_variations.py [base_prompt]` to automate batch generation.

### Custom Brand Elements

For unique brand elements not in standard templates:

1. Describe the element in detail
2. Provide reference examples if available
3. Specify how it should integrate with existing templates
4. Test with minimal parameters first, then refine

**Example:**
```
Custom element: "My brand has a mascot - a golden lion"
Integration: Add "featuring a golden lion character" to scene templates
```

## Resources

### scripts/

- `generate_variations.py` - Batch generate prompt variations for A/B testing
- `validate_prompt.py` - Check if prompts follow template structure
- `color_palette_extractor.py` - Extract brand colors from images

### references/

- `flower-templates.md` - 10+ curated flower bouquet examples from Nano Banana Pro
- `planet-templates.md` - Creative brand planet world examples
- `style-transfer-templates.md` - Style transfer technique variations
- `scene-templates.md` - Imaginative scene generator templates
- `api-integration.md` - Nano Banana Pro API integration guide
- `case-studies.md` - Real-world brand campaign examples

## Troubleshooting

### Common Issues

**Issue:** Generated images don't reflect brand identity
- **Solution:** Increase brand color presence, add specific product descriptions, include logo positioning

**Issue:** Results look generic
- **Solution:** Add unique parameters, specify lighting and composition details, use more descriptive adjectives

**Issue:** Inconsistent style across multiple generations
- **Solution:** Use consistent template parameters, batch generate with same base prompt, save successful prompts for reuse

**Issue:** API rate limiting or cost concerns
- **Solution:** Use local validation first, batch prompts efficiently, prioritize high-value templates

## Quality Checklist

Before finalizing brand visuals:

- [ ] Brand colors are prominent but not overwhelming
- [ ] Product is clearly visible and recognizable
- [ ] Lighting and composition are professional quality
- [ ] Image matches intended mood/atmosphere
- [ ] Resolution meets platform requirements (4K for print/web)
- [ ] Style aligns with brand guidelines
- [ ] Multiple variations generated for selection

## Integration with ClawdHub

This skill is designed for distribution on ClawdHub. Ensure:

- All reference files are well-documented
- Scripts include error handling
- Templates are easily customizable
- Pricing aligns with skill value ($12-15/month suggested)

For ClawdHub publishing guidelines, see [references/clawdhub-publishing.md](references/clawdhub-publishing.md).
