from scripts.check_vertical_alignment import main


def test_vertical_alignment_passes():
    assert main() == 0
