# PowerPoint Automation Script
param(
    [string]$Title,
    [string]$OutputFile = "presentation.pptx"
)

# Create PowerPoint application
$powerpoint = New-Object -ComObject PowerPoint.Application
$powerpoint.Visible = $false
$presentation = $powerpoint.Presentations.Add()

# Add title slide
$titleSlide = $presentation.Slides.Add(1, 1)  # 1 = ppLayoutTitle
$titleSlide.Shapes.Title.TextFrame.TextRange.Text = $Title

# Save and close
$presentation.SaveAs($OutputFile)
$powerpoint.Quit()

Write-Host "Presentation created: $OutputFile"
