import pytest

from playbook import fill, load_templates, main


def _templates_by_id():
    return {template["id"]: template for template in load_templates()}


def test_list_templates_outputs_expected_template_ids(capsys):
    exit_code = main(["playbook.py", "list"])
    assert exit_code == 0

    output = capsys.readouterr().out
    assert "follow-up:" in output
    assert "status-update:" in output
    assert "triage-summary:" in output
    assert "meeting-recap:" in output


def test_fill_template_replaces_placeholders():
    follow_up = _templates_by_id()["follow-up"]

    rendered = fill(
        follow_up,
        {
            "client": "Acme Media",
            "task": "edited property photos",
            "due_date": "2026-10-27",
        },
    )

    assert "Acme Media" in rendered
    assert "edited property photos" in rendered
    assert "2026-10-27" in rendered


def test_unknown_template_raises_key_error():
    with pytest.raises(KeyError):
        main(["playbook.py", "unknown-template"])


def test_missing_template_value_raises_value_error():
    with pytest.raises(ValueError, match="Missing value for placeholder"):
        main(
            [
                "playbook.py",
                "follow-up",
                "client=Acme Media",
                "task=edited property photos",
            ]
        )
