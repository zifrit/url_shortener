from app.services.dependencies.other import UNSAFE_METHODS


def test_unsave_methods_doesnt_contain_safe_methods() -> None:
    safe_methods = {
        "GET",
        "HEAD",
        "OPTIONS",
    }
    assert not UNSAFE_METHODS & safe_methods
