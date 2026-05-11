from neon.cli import cmd_symbolic_status


class Dummy:
    pass


def test_symbolic_status_runs_without_error(capsys):
    cmd_symbolic_status(Dummy())
    out = capsys.readouterr().out
    assert "λ.cas" in out
    assert "λ.lineage" in out
