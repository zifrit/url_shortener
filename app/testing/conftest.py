from os import getenv

import pytest

if getenv("TESTING") != "1":
    pytest.exit("Environmental is not ready to start test")
