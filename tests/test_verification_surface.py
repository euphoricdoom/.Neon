from neon.verification import (
    proof_packet_manifest,
    verify_artifact_file,
    verify_proof_packet,
)


def test_verification_surface_exports():
    assert callable(proof_packet_manifest)
    assert callable(verify_artifact_file)
    assert callable(verify_proof_packet)
