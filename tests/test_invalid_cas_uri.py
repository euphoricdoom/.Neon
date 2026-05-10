import pytest

from neon.cli import main


def test_invalid_cas_uri_fails():
    with pytest.raises(SystemExit):
        main(["fetch", "invalid://uri"])
