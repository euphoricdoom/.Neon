from neon.cli import build_parser
from neon.commands.core import cmd_doctor


class Dummy:
    pass


def test_doctor_command_exists_in_parser():
    parser = build_parser()
    args = parser.parse_args(["doctor"])
    assert args.func == cmd_doctor


def test_doctor_runs_after_init(capsys, tmp_path, monkeypatch):
    monkeypatch.setenv("NEON_VAULT", str(tmp_path / "vault"))

    from neon.commands.core import cmd_init

    cmd_init(Dummy())
    cmd_doctor(Dummy())

    out = capsys.readouterr().out

    assert "✓ vault" in out
    assert "✓ database" in out
    assert "doctor ok" in out
