import os
import sys
import pytest
from pathlib import Path

# Get the project root directory
project_root = str(Path(__file__).parent.parent)

# Add the project root to Python path
sys.path.append(project_root)

@pytest.fixture
def test_app():
    from app.main import app
    return app