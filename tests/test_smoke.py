"""Smoke tests for the Phase 0 scaffold (replaced by real tests in later phases)."""

from web3_threat_monitor import __version__


def test_version_is_a_nonempty_string() -> None:
    assert isinstance(__version__, str)
    assert __version__
