# Flower Bouquet Templates

Curated examples from Nano Banana Pro case studies (Case IDs: 11, 15, 16, 18, 26, 27)

## Template 1: Romantic Brand Bouquet (Case ID: 11)

**Original Prompt:**
```
A luxurious bouquet of red roses featuring Chanel No. 5 perfume bottle. The perfume bottle is resting among the blooms. Gold and black accent colors. Warm, elegant lighting. Centered composition.
```

**Customizable Parameters:**
- Brand Name: Chanel No. 5
- Product: perfume bottle
- Flower Type: red roses
- Accent Colors: Gold and black
- Lighting: Warm, elegant
- Composition: Centered

**Variation Ideas:**
- Substitute red roses with peonies, lilies, or tulips
- Change to pastel flowers for softer look
- Use silver instead of gold for modern feel

---

## Template 2: Brand Gift Bouquet (Case ID: 15)

**Original Prompt:**
```
An elegant bouquet of white lilies and pink roses featuring Tiffany & Co. jewelry box. The jewelry box is floating slightly above the blooms. Tiffany blue and white color scheme. Soft, romantic lighting. Wide shot showing full bouquet.
```

**Customizable Parameters:**
- Brand Name: Tiffany & Co.
- Product: jewelry box
- Flower Types: White lilies and pink roses
- Color Scheme: Tiffany blue and white
- Lighting: Soft, romantic
- Shot: Wide, full bouquet

**Variation Ideas:**
- Change to cosmetics, perfume, or watch boxes
- Use brand's signature color instead of blue
- Add ribbon or packaging elements

---

## Template 3: Minimalist Brand Flowers (Case ID: 16)

**Original Prompt:**
```
A minimalist arrangement of white orchids with Apple iPhone 15 Pro. The phone is nestled among the orchid stems. Apple silver and white color palette. Clean studio lighting. Top-down flat lay composition.
```

**Customizable Parameters:**
- Brand Name: Apple
- Product: iPhone 15 Pro
- Flower Type: White orchids
- Color Palette: Apple silver and white
- Lighting: Clean studio
- Composition: Top-down flat lay

**Variation Ideas:**
- Use succulents or single-stem flowers
- Add brand logo subtly in background
- Include accessories like headphones or cases

---

## Template 4: Luxury Wrapped Product (Case ID: 18)

**Original Prompt:**
```
A bouquet of yellow sunflowers wrapped in branded paper featuring L'Occitane hand cream. The hand cream tube is tied to the bouquet with ribbon. Lavender and yellow color scheme. Bright, cheerful lighting. Close-up on product.
```

**Customizable Parameters:**
- Brand Name: L'Occitane
- Product: hand cream tube
- Flower Type: Yellow sunflowers
- Color Scheme: Lavender and yellow
- Lighting: Bright, cheerful
- Shot: Close-up on product

**Variation Ideas:**
- Use gift wrap with brand pattern
- Add multiple products (mini gift set)
- Change to winter flowers for seasonal campaigns

---

## Template 5: Brand Color Theme Bouquet (Case ID: 26)

**Original Prompt:**
```
A vibrant bouquet of multicolor flowers representing Spotify's brand colors (green, black, white). The Spotify logo is subtly integrated as a charm on the bouquet ribbon. Dynamic lighting. Heroic composition.
```

**Customizable Parameters:**
- Brand Name: Spotify
- Brand Colors: Green, black, white
- Logo Placement: Charm on ribbon
- Lighting: Dynamic
- Composition: Heroic

**Variation Ideas:**
- Use 2-3 brand colors for elegance
- Add brand mascot or icon instead of logo
- Create gradient effect with flowers

---

## Template 6: Premium Product Showcase (Case ID: 27)

**Original Prompt:**
```
An exquisite arrangement of black calla lilies featuring Dior Sauvage cologne bottle. The bottle is prominently displayed among the sleek black blooms. Dior silver and black theme. Dramatic chiaroscuro lighting. Low angle shot.
```

**Customizable Parameters:**
- Brand Name: Dior
- Product: Sauvage cologne bottle
- Flower Type: Black calla lilies
- Theme: Dior silver and black
- Lighting: Dramatic chiaroscuro
- Shot: Low angle

**Variation Ideas:**
- Use dark red or purple flowers for drama
- Include multiple bottles (product line)
- Add luxury packaging elements

---

## Prompt Engineering Tips

### Product Placement Strategies

1. **Floating Above**: Creates magical, dreamy effect
   - Works best for: Perfume, jewelry, cosmetics
   - Lighting: Soft, ethereal

2. **Nestled Among**: Natural, organic integration
   - Works best for: Tech products, accessories, small items
   - Lighting: Natural, soft shadows

3. **Wrapped/Bound**: Gift-like presentation
   - Works best for: Gift sets, limited editions
   - Lighting: Bright, warm

4. **Prominently Displayed**: Hero shot focus
   - Works best for: Luxury items, flagship products
   - Lighting: Dramatic, high contrast

### Color Theory for Brand Flowers

**Luxury Brands:**
- Black, gold, silver, deep red
- Flowers: Black roses, white lilies, orchids
- Mood: Sophisticated, exclusive

**Tech Brands:**
- Silver, white, blue, minimal colors
- Flowers: White orchids, green succulents
- Mood: Modern, sleek

**Beauty/Fashion:**
- Pastels, pinks, warm neutrals
- Flowers: Roses, peonies, tulips
- Mood: Romantic, elegant

**Lifestyle/Casual:**
- Bright colors, yellows, oranges
- Flowers: Sunflowers, daisies, wildflowers
- Mood: Cheerful, approachable

### Flower-Brand Pairing Guide

| Flower Type | Best For | Mood |
|-------------|----------|------|
| Red Roses | Luxury, romance | Passionate, elegant |
| White Lilies | Beauty, purity | Soft, refined |
| Orchids | Tech, premium | Modern, sophisticated |
| Sunflowers | Lifestyle, casual | Cheerful, vibrant |
| Peonies | Fashion, beauty | Romantic, dreamy |
| Calla Lilies | Luxury, minimal | Sleek, dramatic |
| Succulents | Tech, eco-friendly | Modern, fresh |
| Wildflowers | Casual, organic | Natural, free-spirited |

### Lighting Techniques

**Warm Soft Lighting:**
- Time: Golden hour
- Effect: Romantic, inviting
- Best for: Beauty, romance themes

**Clean Studio Lighting:**
- Type: Diffused, even
- Effect: Professional, product-focused
- Best for: Tech, e-commerce

**Dramatic Chiaroscuro:**
- Type: High contrast, deep shadows
- Effect: Luxury, mystery
- Best for: Premium products, fashion

**Bright Natural Light:**
- Type: Sun-drenched, daylight
- Effect: Fresh, energetic
- Best for: Lifestyle, casual brands

## Batch Generation Prompts

### Test Multiple Flower Types
```
Generate 4 variations:
1. [Brand Name] product with red roses
2. [Brand Name] product with white lilies
3. [Brand Name] product with orchids
4. [Brand Name] product with sunflowers
```

### Test Different Lighting
```
Generate 3 variations of same setup:
1. Soft, romantic lighting
2. Clean, studio lighting
3. Dramatic, high-contrast lighting
```

### Test Product Placements
```
Generate 3 variations:
1. Product floating above flowers
2. Product nestled among flowers
3. Product prominently displayed
```

## API Integration Notes

For Nano Banana Pro API, structure parameters:

```json
{
  "prompt": "A luxurious bouquet of [flowers] featuring [brand_name] [product]",
  "parameters": {
    "style": "photorealistic",
    "resolution": "4K",
    "quality": "ultra"
  },
  "negative_prompt": "blurry, low quality, distorted"
}
```

See [api-integration.md](api-integration.md) for full API details.
