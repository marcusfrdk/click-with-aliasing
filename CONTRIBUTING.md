# Contributing to Click With Aliasing

Thank you for your interest in contributing to Click With Aliasing! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Submitting Changes](#submitting-changes)
- [Release Process](#release-process)

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone. Please:

- Be respectful and considerate in your communication
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

### Prerequisites

- Python 3.10 or newer
- Git
- A GitHub account

### Finding an Issue

1. Check the [issue tracker](https://github.com/marcusfrdk/click-with-aliasing/issues) for existing issues
2. Look for issues tagged with `good first issue` or `help wanted`
3. If you want to work on something not listed, create a new issue first to discuss it

## Development Setup

### 1. Fork and Clone

Fork the repository on GitHub, then clone your fork:

```bash
git clone https://github.com/YOUR-USERNAME/click-with-aliasing.git
cd click-with-aliasing
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Development Dependencies

```bash
pip install -e ".[dev]"
```

This installs the package in editable mode along with all development dependencies:

- `pytest` - Testing framework
- `mypy` - Type checking
- `black` - Code formatting
- `isort` - Import sorting
- `pylint` - Code linting
- `pre-commit` - Git hooks for code quality

### 4. Set Up Pre-commit Hooks

```bash
pre-commit install
```

This automatically runs quality checks before each commit:

- **pytest** - Runs all tests
- **mypy** - Type checking (strict mode)
- **pylint** - Code linting (minimum score: 9.0/10)
- **black** - Code formatting check
- **isort** - Import sorting check

## Development Workflow

### 1. Create a Branch

Create a descriptive branch name:

```bash
git checkout -b feature/add-new-validation
git checkout -b fix/issue-123
git checkout -b docs/update-readme
```

Branch naming conventions:

- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation changes
- `refactor/` - Code refactoring
- `test/` - Test additions or changes

### 2. Make Your Changes

Follow the [coding standards](#coding-standards) when making changes.

### 3. Run Quality Checks

Before committing, ensure all checks pass:

```bash
# Run tests
pytest

# Type checking
mypy click_with_aliasing

# Code linting
pylint . --fail-under=9

# Format code
black .
isort .
```

### 4. Commit Your Changes

Write clear, descriptive commit messages:

```bash
git add .
git commit -m "feat: add support for conditional validation rules"
```

Commit message format:

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `test:` - Test changes
- `refactor:` - Code refactoring
- `style:` - Code style changes
- `chore:` - Maintenance tasks

### 5. Push and Create Pull Request

```bash
git push origin your-branch-name
```

Then create a pull request on GitHub with:

- Clear description of changes
- Reference to related issues (e.g., "Fixes #123")
- Any breaking changes highlighted
- Screenshots or examples if applicable

## Coding Standards

### Python Style

We follow strict coding standards enforced by automated tools:

#### Type Hints

All functions must have complete type hints using Python 3.10+ syntax:

```python
def option(
    *param_decls: str,
    mutually_exclusive: list[str] | None = None,
    requires: list[str] | None = None,
    **kwargs: Any,
) -> Callable[[F], F]:
    """Add an option with validation."""
    pass
```

Note: Use `list[str]` instead of `List[str]` and `str | None` instead of `Optional[str]`.

#### Docstrings

Use clear, descriptive docstrings in this format:

```python
def rule(
    params: List[str],
    *,
    mode: str = "all_or_none",
    count: int = 0,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Apply validation rules to command parameters.

    Parameters:
        params (list[str]):
            List of parameter names to validate.
        mode (str):
            Validation mode (all_or_none, at_least, at_most, exactly).
        count (int):
            Number used with at_least, at_most, or exactly modes.

    Returns:
        Callable:
            Decorator function that adds validation rules.
    """
    pass
```

#### Code Formatting

- **Line length**: 80 characters (enforced by Black)
- **Import sorting**: Organized by isort
- **Quotes**: Double quotes for strings
- **Indentation**: 4 spaces

### Quality Requirements

Your code must meet these requirements:

- **Pylint score**: ≥ 9.0/10
- **Test coverage**: All new features must have tests
- **Type checking**: Pass mypy strict mode
- **All tests passing**: 100% test pass rate

## Testing

### Writing Tests

Tests are located in the `tests/` directory. Follow existing patterns:

```python
import pytest
from click.testing import CliRunner
from click_with_aliasing import command, option, rule

def test_mutually_exclusive_options():
    """Test that mutually exclusive options raise an error."""
    @command(name="test")
    @option("--a", mutually_exclusive=["b"])
    @option("--b", mutually_exclusive=["a"])
    def cmd(a, b):
        pass

    runner = CliRunner()
    result = runner.invoke(cmd, ["--a", "1", "--b", "2"])
    assert result.exit_code != 0
    assert "mutually exclusive" in result.output.lower()
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_option.py

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=click_with_aliasing
```

### Test Requirements

- Test all new features and bug fixes
- Include both positive and negative test cases
- Test edge cases and error conditions
- Use descriptive test names
- Add docstrings to complex tests

## Documentation

### Code Documentation

- Add docstrings to all public functions and classes
- Include type hints for all parameters and return values
- Document exceptions that can be raised

### User Documentation

When adding new features, update:

1. **Relevant docs/ file** - Add examples and API documentation
2. **README.md** - Update if it's a major feature
3. **Docstrings** - Keep inline documentation current

### Documentation Style

- Use simple, clear language
- Provide many practical examples
- Include both basic and advanced usage
- Show expected input and output
- Use Google style for docstrings and comments

Example documentation structure:

```markdown
## Feature Name

Brief description of what it does.

### Basic Usage

[Simple example with explanation]

### Advanced Usage

[Complex example showing edge cases]

### API Reference

[Parameter descriptions and return values]
```

## Submitting Changes

### Pull Request Checklist

Before submitting a pull request, ensure:

- [ ] Code follows the style guidelines
- [ ] All tests pass (`pytest`)
- [ ] Type checking passes (`mypy click_with_aliasing`)
- [ ] Code linting passes (`pylint . --fail-under=9`)
- [ ] Code is formatted (`black .` and `isort .`)
- [ ] New features have tests
- [ ] Documentation is updated
- [ ] Commit messages are clear and descriptive
- [ ] Branch is up to date with main

### Pull Request Process

1. **Create PR** with clear title and description
2. **Link related issues** using "Fixes #123" or "Relates to #456"
3. **Respond to feedback** from reviewers promptly
4. **Update your PR** based on review comments
5. **Ensure CI passes** - All automated checks must pass

### Review Process

- Maintainers will review your PR within a few days
- Address all review comments
- Keep the discussion focused and professional
- Be patient - quality takes time!

## Release Process

Releases are automatically published when a new tag in the semver format "X.Y.Z" is pushed to the main branch.

### Version Numbering

We follow [Semantic Versioning](https://semver.org/):

- **Major** (X.0.0): Breaking changes
- **Minor** (0.X.0): New features, backwards compatible
- **Patch** (0.0.X): Bug fixes, backwards compatible

### Creating a Release

1. Update version in `pyproject.toml`
2. Update CHANGELOG.md with changes
3. Create and push a git tag
4. Build and publish to PyPI

```bash
# Update version
vim pyproject.toml

# Build package
python -m build

# Upload to PyPI
python -m twine upload dist/*
```

## Questions?

If you have questions:

1. Check existing [documentation](docs/)
2. Search [existing issues](https://github.com/marcusfrdk/click-with-aliasing/issues)
3. Create a new issue with the `question` label

## Thank You

Your contributions make this project better for everyone. Thank you for taking the time to contribute!
