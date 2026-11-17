import re
def stage1_draft(sign, date):  # swap in DeepSeek call
    return f"{sign} on {date}: focus on one priority today. Trust your instincts about money and health."
def stage2_review(text):  # swap in Claude Sonnet call: tone, safety, format
    issues = []
    if re.search(r"\b(diagnos|cure|guaranteed|invest in)\w*", text, re.I): issues.append("unsafe claim")
    if len(text) > 400: issues.append("too long")
    return {"text": text, "issues": issues, "needs_human": bool(issues)}
def reading(sign, date):
    return stage2_review(stage1_draft(sign, date))
if __name__ == "__main__": print(reading("Leo", "2026-11-17"))
