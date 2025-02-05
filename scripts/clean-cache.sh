# clean all python cache files

find . -name "__pycache__" -exec rm -rf {} \;

# clean all pytest cache files

find . -name ".pytest_cache" -exec rm -rf {} \;

# clean all ruff cache files

find . -name ".ruff_cache" -exec rm -rf {} \;

# clean all mypy cache files

find . -name ".mypy_cache" -exec rm -rf {} \;