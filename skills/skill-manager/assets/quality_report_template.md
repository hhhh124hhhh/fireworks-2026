# Skill Quality Report

**Skill Name**: {{skill_name}}
**Date**: {{date}}
**Overall Score**: {{total_score}}/{{max_score}} ({{percentage}}%)
**Grade**: {{grade}}

---

## Executive Summary

{{summary}}

---

## Detailed Breakdown

### Documentation ({{doc_score}}/{{doc_max}})

#### Name: {{name_score}}/10
{{name_feedback}}

#### Description: {{desc_score}}/10
{{desc_feedback}}

#### Description Quality: {{desc_quality_score}}/15
{{desc_quality_feedback}}

#### Instructions: {{instructions_score}}/15
{{instructions_feedback}}

#### Instruction Quality: {{inst_quality_score}}/10
{{inst_quality_feedback}}

### Structure ({{structure_score}}/{{structure_max}})

{{structure_feedback}}

### Code Quality ({{code_quality_score}}/{{code_quality_max}})

{{code_quality_feedback}}

---

## Issues Found

{{#if has_issues}}
### Critical Issues
{{#each critical_issues}}
- [ ] {{this}}
{{/each}}

### Warnings
{{#each warnings}}
- [ ] {{this}}
{{/each}}

### Suggestions
{{#each suggestions}}
- [ ] {{this}}
{{/each}}
{{else}}
No issues found! ✨
{{/if}}

---

## Recommendations

{{recommendations}}

---

## Next Steps

{{next_steps}}
