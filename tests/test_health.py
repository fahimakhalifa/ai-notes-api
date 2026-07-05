from pathlib import Path


def test_main_app_file_exists():
    assert Path("app/main.py").exists()


def test_env_example_exists():
    assert Path(".env.example").exists()


def test_requirements_file_exists():
    assert Path("requirements.txt").exists()
