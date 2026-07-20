# Intel Output Format

When reporting intelligence to the user, prefer this fixed structure:

1. 今日资讯重点
2. 深度判断
3. 公众号转化
4. 选题建议
5. 建议动作

Rules:

- Put the conclusion first.
- Keep each section short and readable.
- Default to Top 3 items only.
- If there are more than 3 items, rank them and suppress the rest into logs or memory.
- Do not dump raw collection logs unless the user explicitly asks.
- If there are no strong signals, say that plainly and lower the confidence.
- In `公众号转化`, explicitly judge fit for: AI 实战 / 踩坑 / 教程 / 测评 / 心法 / skills / OpenClaw.
- End each item with one action stance: `建议写` / `建议观察` / `建议忽略`.
- Midday and afternoon runs are background material only, not user-facing briefs.
- If midday output is substantially the same as the morning brief, record `no meaningful delta` in memory and do not push.
