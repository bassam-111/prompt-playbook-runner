# Prompt Playbook Runner

A local prompt-engineering tool for operations work: pick a reusable prompt
template, fill in the client/task details, and get a ready-to-paste prompt
plus a transparent checklist score.

**Important, stated plainly:** this tool does not call any LLM API and
needs no API key. It is a template library and checklist scorer, not an
AI service. You paste the finished prompt into ChatGPT, Claude, or any
other tool yourself.

Built with **Python, Flask, HTML/CSS** — skills on the resume, nothing extra claimed.

## Templates included

- `follow-up` — polite follow-up email for an overdue task
- `status-update` — short client status update as a bullet list
- `triage-summary` — triage a new request into category, priority, owner, next action
- `meeting-recap` — recap with decisions, owners, and due dates

## How to run

```bash
pip install -r requirements.txt

# List templates
python playbook.py list

# Fill one template
python playbook.py follow-up client="Acme Media" task="edited property photos" due_date="2026-10-27"

# Web UI
python app.py
# then open http://127.0.0.1:5000
```

## Sample output

```
You are an operations coordinator. Write a short, polite follow-up email to Acme Media about edited property photos. Mention it was due on 2026-10-27, ask for an updated timeline, and offer help if anything is blocked. Reply as a short email with a subject line.

{'score': '4/4', 'checks': {'role': True, 'task': True, 'context': True, 'output_format': True}, 'tips': []}
```

## Files

- `playbook.py` — template filling and checklist scoring (no framework dependency)
- `prompts.json` — the 4 prompt templates
- `app.py` — Flask UI using the same logic
- `requirements.txt` — Flask

## Try your own template

Add an entry to `prompts.json` with an `id`, a `purpose`, and a `body`
using `{placeholders}`. Then run it with `python playbook.py <id> name=value ...`.
