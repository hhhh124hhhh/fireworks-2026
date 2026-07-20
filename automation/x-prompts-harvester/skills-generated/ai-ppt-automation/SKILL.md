---
name: ai-ppt-automation
description: Generate PowerPoint presentations using AI automation with PowerShell and Claude Sonnet. Perfect for creating slides with desktop automation, content generation, and design optimization.
tags: [powerpoint, ppt, automation, claude, ai, presentation, slides]
version: 1.0.0
author: Generated from X/Twitter discovery
---

# AI PowerPoint Automation

Generate professional PowerPoint presentations using AI-powered automation.

## Overview

This skill implements the AI-driven PowerPoint automation workflow discovered on X/Twitter by @hirokiaramaki. It combines PowerShell desktop automation with Claude Sonnet code generation to create complete presentations automatically.

## Use Cases

- Business presentations and reports
- Training materials and courseware
- Sales pitches and proposals
- Academic presentations
- Team meeting slides

## Workflow

### Step 1: Define Your Topic

Provide a topic and key points for your presentation:

```
Topic: Q4 Sales Performance Review
Key points:
- Revenue growth: 23%
- New client acquisition: 45 customers
- Team expansion: 12 new hires
- Product launch success
```

### Step 2: Generate Content with Claude

Ask Claude to generate the slide content:

```
Create a 10-slide PowerPoint presentation about Q4 Sales Performance Review. Include:
1. Title slide
2. Executive summary
3. Revenue breakdown
4. Client acquisition metrics
5. Team growth
6. Product launch highlights
7. Challenges addressed
8. Q4 achievements
9. Q1 goals
10. Thank you slide

For each slide, provide:
- Slide title
- 3-5 bullet points
- Suggested slide layout (title slide, content, comparison, chart, etc.)
- Speaker notes (2-3 sentences)
```

### Step 3: Automate with PowerShell

Use PowerShell to create the PowerPoint file:

```powershell
# Create PowerPoint presentation
$powerpoint = New-Object -ComObject PowerPoint.Application
$presentation = $powerpoint.Presentations.Add()

# Add slides based on Claude-generated content
$slides = @(
    @{Title="Q4 Sales Performance"; Content=@("Revenue Growth", "New Clients", "Team Expansion")},
    @{Title="Executive Summary"; Content=@("23% revenue increase", "45 new customers acquired")},
    # ... more slides
)

foreach ($slideData in $slides) {
    $slide = $presentation.Slides.Add($presentation.Slides.Count + 1)
    $slide.Shapes.Title.TextFrame.TextRange.Text = $slideData.Title
    
    $content = $slide.Shapes.AddTextbox(1, 100, 100, 600, 400)
    $content.TextFrame.TextRange.Text = $slideData.Content -join "`n"
}

# Save presentation
$presentation.SaveAs("Q4_Sales_Review.pptx")
$powerpoint.Quit()
```

### Step 4: Optimize and Polish

Review the generated slides and:
- Adjust formatting and design
- Add charts and visuals
- Refine speaker notes
- Apply company branding

## Advanced Features

### Automatic Design Enhancement

Ask Claude to suggest design improvements:

```
Review these PowerPoint slides and suggest:
1. Better color schemes for a sales presentation
2. Chart types for each data slide
3. Visual hierarchy improvements
4. Professional transitions between slides
5. Consistent slide master template
```

### Batch Presentation Generation

Generate multiple presentations from templates:

```python
import json
from pathlib import Path

# Load presentation templates
templates = Path("presentation_templates/").glob("*.json")

for template in templates:
    with open(template) as f:
        data = json.load(f)
    
    # Generate content with Claude
    content = generate_slides_content(data)
    
    # Create PowerPoint with PowerShell
    create_pptx(content, f"{data['title']}.pptx")
```

## Integration with Other Tools

### Databricks Integration

For advanced use cases, integrate with Databricks and Claude Sonnet:

1. Store presentation templates in Databricks
2. Use Claude Sonnet API for content generation
3. Execute PowerShell scripts on remote machines
4. Automate slide creation on a schedule

### Google Slides Export

Convert PowerPoint to Google Slides format:

```python
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

# Upload to Google Drive
drive_service = build('drive', 'v3', credentials=creds)
slides_service = build('slides', 'v1', credentials=creds)

# Convert PPTX to Google Slides
file_metadata = {'name': 'Q4 Sales Review', 'mimeType': 'application/vnd.google-apps.presentation'}
media = MediaFileUpload('Q4_Sales_Review.pptx', mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation')
file = drive_service.files().create(body=file_metadata, media_body=media).execute()
```

## Tips and Best Practices

### Content Structure
- Keep slide text concise (max 6 bullets per slide)
- Use clear, actionable titles
- Include data visualization where possible
- Add speaker notes for reference

### Design Guidelines
- Use consistent color schemes
- Apply professional fonts (e.g., Arial, Calibri)
- Maintain adequate white space
- Limit transitions and animations

### Automation Tips
- Test PowerShell scripts on sample data first
- Handle errors gracefully in automation
- Add logging for debugging
- Schedule regular backups of generated presentations

## Troubleshooting

### PowerPoint Not Responding
```powershell
# Force close PowerPoint
Get-Process POWERPNT | Stop-Process -Force

# Restart automation
$powerpoint = New-Object -ComObject PowerPoint.Application
```

### Claude Content Issues
- Refine prompts for better output
- Specify format requirements clearly
- Request multiple options to choose from
- Iterate and improve based on results

### Formatting Problems
- Use PowerPoint templates for consistency
- Apply slide masters globally
- Check text boxes for overflow
- Verify chart data ranges

## Examples

### Example 1: Sales Presentation
```bash
# Generate content
claude generate-slides --topic "Q3 Sales" --output slides.json

# Create PowerPoint
powershell -File create-pptx.ps1 -Input slides.json -Output Q3_Sales.pptx
```

### Example 2: Training Materials
```bash
# Create training deck
claude generate-slides --topic "Onboarding Training" --slides 20

# Generate interactive elements
powershell -File add-quizzes.ps1 -Presentation Training.pptx
```

### Example 3: Weekly Reports
```bash
# Schedule automated reports
# Add to crontab: 0 17 * * 5 /root/scripts/weekly-report.sh
```

## Resources

- Original discovery: https://x.com/hirokiaramaki/status/2017010656114069740
- Claude API: https://docs.anthropic.com
- PowerPoint Automation: https://docs.microsoft.com/en-us/office/vba/api/overview/powerpoint
- Databricks: https://docs.databricks.com

## Changelog

### Version 1.0.0 (2026-01-30)
- Initial release based on X/Twitter discovery
- Complete workflow for AI-powered PowerPoint automation
- PowerShell integration examples
- Claude prompt templates included
