"""Minimal Flask UI: pick a template, fill it, see the prompt and its score."""
from flask import Flask, render_template_string, request

from playbook import fill, load_templates, score

app = Flask(__name__)
TEMPLATES = {t["id"]: t for t in load_templates()}

PAGE = """
<!doctype html><html><head><meta charset="utf-8"><title>Prompt Playbook Runner</title>
<style>body{font-family:system-ui,sans-serif;max-width:720px;margin:2em auto;padding:0 1em}
textarea,input,select{width:100%;margin:6px 0;padding:8px}pre{white-space:pre-wrap;background:#f4f4f4;padding:1em}</style>
</head><body><h1>Prompt Playbook Runner</h1>
<form method="post">
<select name="template">{% for t in templates.values() %}
<option value="{{ t.id }}">{{ t.id }} — {{ t.purpose }}</option>{% endfor %}</select>
<input name="client" placeholder="client (e.g. Acme Media)">
<input name="task" placeholder="task">
<input name="due_date" placeholder="due date (for follow-up)">
<button>Build prompt</button></form>
{% if prompt %}<h2>Prompt</h2><pre>{{ prompt }}</pre><h2>Checklist score: {{ result.score }}</h2>
<ul>{% for tip in result.tips %}<li>{{ tip }}</li>{% endfor %}</ul>{% endif %}
</body></html>
"""


@app.route("/", methods=["GET", "POST"])
def index():
    prompt = result = None
    if request.method == "POST":
        template = TEMPLATES[request.form["template"]]
        values = {k: v for k, v in request.form.items() if k != "template" and v}
        prompt = fill(template, values)
        result = score(prompt)
    return render_template_string(PAGE, templates=TEMPLATES, prompt=prompt, result=result)


if __name__ == "__main__":
    app.run(debug=True)
