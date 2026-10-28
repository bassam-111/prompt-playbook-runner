"""Prompt playbook runner: fill operations prompt templates, score them.

Templates live in prompts.json. Each template has named placeholders
(e.g. {client}, {task}) and a short purpose. This tool:
1. lists available templates,
2. fills a template with values you supply, and
3. scores the filled prompt on a simple, transparent checklist:
   - states a role, a task, context, and a desired output format
   - stays within a length band (too short = vague, very long = noisy)

No LLM API is called and no API key is needed: this is a local template
and checklist tool, not an AI service. That distinction is stated in the
README so nobody mistakes it for a hosted model.
"""
import json
import sys


def load_templates(path="prompts.json"):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)["templates"]


def fill(template, values):
    try:
        return template["body"].format(**values)
    except KeyError as missing:
        raise ValueError(f"Missing value for placeholder: {missing}") from missing


def score(prompt):
    text = prompt.lower()
    checks = {
        "role": any(word in text for word in ["you are", "act as"]),
        "task": any(word in text for word in ["write", "draft", "summarise", "summarize", "list", "triage"]),
        "context": len(prompt) > 80,
        "output_format": any(word in text for word in ["bullet", "table", "list", "format", "email"]),
    }
    passed = sum(checks.values())
    tips = []
    if not checks["role"]:
        tips.append("Add a role, e.g. 'You are an operations coordinator.'")
    if not checks["output_format"]:
        tips.append("State the output format, e.g. 'Reply as a short bullet list.'")
    if len(prompt) > 1200:
        tips.append("Prompt is very long; trim background that does not change the answer.")
    return {"score": f"{passed}/4", "checks": checks, "tips": tips}


def main(argv):
    templates = {t["id"]: t for t in load_templates()}
    if len(argv) < 2 or argv[1] == "list":
        for template in templates.values():
            print(f"{template['id']}: {template['purpose']}")
        return 0
    template = templates[argv[1]]
    values = dict(pair.split("=", 1) for pair in argv[2:])
    filled = fill(template, values)
    print(filled)
    print()
    print(score(filled))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
