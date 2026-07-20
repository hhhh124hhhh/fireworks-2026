# Skills Auto-Publishing Report

**Generated**: 2026-01-30 14:XX GMT+8
**Status**: Ready to publish (requires authentication)

---

## 📦 Skills in dist/ Directory

| # | Skill Name | Size | Published | Notes |
|---|------------|------|-----------|-------|
| 1 | ad-creative-generator | 31K | ❌ | Not found on ClawdHub |
| 2 | ai-music-prompts | 66K | ❌ | Not found on ClawdHub |
| 3 | creative-illustration | 7.8K | ❌ | Not found on ClawdHub |
| 4 | game-character-gen | 8.2K | ❌ | Not found on ClawdHub |
| 5 | interview-coach | 9.3K | ❌ | Not found on ClawdHub |
| 6 | openai-image-gen | 4.4K | ❌ | Different skill exists (Openai Image Gen v1.0.1) |
| 7 | prompt-craft | 12K | ⚠️ | Similar skill exists (prompt-craft v1.0.1 "Prompt Crafter") |
| 8 | sql-assistant | 12K | ❌ | Different skill exists (ai-sql v1.0.2) |
| 9 | style-transfer | 7.1K | ❌ | Not found on ClawdHub |
| 10 | tiktok-ai-model-generator | 13K | ✅ | Already published |

**Summary**:
- ✅ Published: 1 (tiktok-ai-model-generator)
- ❌ Not published: 9
- ⚠️ Potential conflicts: 2 (prompt-craft, openai-image-gen)

---

## 🔐 Authentication Issue

**Current Status**: ❌ Unauthorized

```
Error: Unauthorized
```

**Configuration**:
- Registry: https://www.clawhub.ai/api
- Token: clh_QLBQfQAjDlECG4xfm-ccmcZdJ3Dg4s-CRza9GcOiMDA
- Status: Token expired or invalid

**Required Action**:
Please obtain a new API token from ClawdHub and login:

```bash
clawdhub login --token <NEW_TOKEN> --no-browser
```

To get a new token:
1. Visit https://www.clawhub.ai
2. Go to your account settings
3. Generate a new API token
4. Share the token with me

---

## 🚀 Auto-Publish Script

**Location**: `/root/clawd/scripts/auto-publish-skills.sh`

**Features**:
- ✅ Checks authentication before publishing
- ✅ Verifies if skill is already published
- ✅ Extracts skill metadata from SKILL.md
- ✅ Publishes all unpublished skills
- ✅ Generates detailed logs
- ✅ Shows summary report

**Usage**:
```bash
# Run the script (after authentication)
/root/clawd/scripts/auto-publish-skills.sh
```

**Script Behavior**:
1. Checks ClawdHub authentication
2. Lists all .skill files in dist/
3. For each skill:
   - Extracts to temp directory
   - Reads SKILL.md for metadata
   - Checks if already published
   - Publishes if not published
4. Generates summary report

---

## 📊 Detailed Skill Information

### 1. ad-creative-generator
**Size**: 31K
**Description**: Generate diverse, engaging ad prompts for any product or brand across 20+ creative styles and 10 categories.
**Status**: Not published
**Recommendation**: Publish as-is

### 2. ai-music-prompts
**Size**: 66K
**Description**: AI music prompt templates and best practices for generating music with Suno, Udio, Mureka, and others.
**Status**: Not published
**Recommendation**: Publish as-is

### 3. creative-illustration
**Size**: 7.8K
**Description**: Generate diverse creative illustrations via OpenAI Images API.
**Status**: Not published
**Recommendation**: Publish as-is

### 4. game-character-gen
**Size**: 8.2K
**Description**: Generate professional game character designs via OpenAI Images API.
**Status**: Not published
**Recommendation**: Publish as-is

### 5. interview-coach
**Size**: 9.3K
**Description**: Professional interview preparation and practice coach.
**Status**: Not published
**Recommendation**: Publish as-is

### 6. openai-image-gen
**Size**: 4.4K
**Description**: Batch-generate images via OpenAI Images API.
**Status**: Potential conflict
**Existing**: "Openai Image Gen v1.0.1" (likely different)
**Recommendation**: Publish with version 1.0.0 (will be distinguished by author)

### 7. prompt-craft
**Size**: 12K
**Description**: Transform basic prompts into elite structured prompts using Anthropic's 10-step framework.
**Status**: Potential conflict
**Existing**: "prompt-craft v1.0.1 Prompt Crafter"
**Recommendation**: Verify if this is the same skill before publishing

### 8. sql-assistant
**Size**: 12K
**Description**: Comprehensive SQL query assistant for database operations.
**Status**: Not published
**Existing**: "ai-sql v1.0.2 SQL Query Generator" (different)
**Recommendation**: Publish as-is (different functionality)

### 9. style-transfer
**Size**: 7.1K
**Description**: Professional artistic style transfer via OpenAI Images API.
**Status**: Not published
**Recommendation**: Publish as-is

### 10. tiktok-ai-model-generator
**Size**: 13K
**Status**: ✅ Published on 2026-01-30 14:02 GMT+8
**Version**: v1.0.0

---

## ⚠️ Potential Conflicts

### prompt-craft
- **Your skill**: "Transform basic prompts into elite structured prompts using Anthropic's 10-step framework"
- **Existing**: "prompt-craft v1.0.1 Prompt Crafter"
- **Action**: Verify if this is the same skill or a different implementation

**Recommendation**: Extract and compare SKILL.md files:
```bash
# Extract your skill
cd /tmp && unzip -q /root/clawd/dist/prompt-craft.skill
cat SKILL.md

# Search and view existing skill
clawdhub search prompt-craft
clawdhub info prompt-craft
```

### openai-image-gen
- **Your skill**: "Batch-generate images via OpenAI Images API. Random prompt sampler + index.html gallery."
- **Existing**: "Openai Image Gen v1.0.1"
- **Action**: Verify if this is the same skill or a different implementation

**Recommendation**: Similar to above, compare SKILL.md files.

---

## 🎯 Next Steps

### Option 1: Provide New API Token
1. Get new token from https://www.clawhub.ai
2. Share the token with me
3. I will login and run the auto-publish script

### Option 2: Login Manually
1. Run: `clawdhub login --token <NEW_TOKEN> --no-browser`
2. Run: `/root/clawd/scripts/auto-publish-skills.sh`

### Option 3: Selective Publishing
If you want to publish specific skills only, let me know which ones and I can create individual publish commands.

---

## 📋 Verification Checklist

After publishing, verify each skill:

- [ ] Skill appears in `clawdhub search <skill-name>`
- [ ] SKILL.md is properly rendered
- [ ] All files are included
- [ ] Version is correct (1.0.0)
- [ ] Description is accurate
- [ ] Installation works: `clawdhub install <skill-name>`

---

## 📝 Notes

- All skills will be published with version **1.0.0**
- Default changelog will be: "Initial release: <description from SKILL.md>"
- Logs will be saved to `/root/clawd/auto-publish-YYYYMMDD-HHMMSS.log`
- Conflicts with existing skills can be resolved by renaming before publishing

---

**Report Generated**: 2026-01-30 14:XX GMT+8
**Action Required**: Provide new ClawdHub API token
**Estimated Time**: 5-10 minutes (after authentication)
