# Contributing to Centralized Allure Reports

Thank you for your interest in contributing to this project! We welcome contributions from everyone.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Docker (optional, for containerized development)
- AWS account with S3 access (for testing with real data)
- Git

### Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/your-username/centralized-allure-reports.git
   cd centralized-allure-reports
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install pytest pytest-cov flake8  # Development dependencies
   ```

4. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

5. **Run tests to verify setup**
   ```bash
   python test_server.py
   ```

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](../../issues)
2. If not, create a new issue using the bug report template
3. Provide as much detail as possible, including:
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details
   - Log output

### Suggesting Features

1. Check if the feature has already been requested in [Issues](../../issues)
2. Create a new issue using the feature request template
3. Describe the use case and expected behavior
4. Consider implementation details if you have ideas

### Contributing Code

1. **Find an issue to work on**
   - Look for issues labeled `good first issue` for beginners
   - Comment on the issue to let others know you're working on it

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/issue-number
   ```

3. **Make your changes**
   - Follow the coding standards below
   - Add tests for new functionality
   - Update documentation as needed

4. **Test your changes**
   ```bash
   python test_server.py
   flake8 .
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add new feature" # Use conventional commits
   ```

6. **Push and create a pull request**
   ```bash
   git push origin feature/your-feature-name
   ```

## Pull Request Process

1. **Before submitting**
   - Ensure all tests pass
   - Update documentation if needed
   - Follow the coding standards
   - Rebase your branch on the latest main

2. **Pull Request Requirements**
   - Fill out the PR template completely
   - Link to related issues
   - Include screenshots for UI changes
   - Ensure CI checks pass

3. **Review Process**
   - Maintainers will review your PR
   - Address any feedback promptly
   - Be patient - reviews take time

4. **After Approval**
   - Your PR will be merged by a maintainer
   - You can delete your feature branch

## Coding Standards

### Python Style

- Follow [PEP 8](https://pep8.org/) style guide
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Maximum line length: 127 characters

### Code Organization

- Keep functions small and focused
- Use type hints where appropriate
- Handle exceptions gracefully
- Log important events and errors

### Example Code Style

```python
def list_repositories(self) -> List[str]:
    """List all repository directories in the S3 bucket.
    
    Returns:
        List[str]: Sorted list of repository names
        
    Raises:
        ClientError: If S3 operation fails
    """
    try:
        response = self.s3_client.list_objects_v2(
            Bucket=self.bucket_name,
            Prefix='',
            Delimiter='/'
        )
        
        repos = []
        if 'CommonPrefixes' in response:
            for prefix in response['CommonPrefixes']:
                repo_name = prefix['Prefix'].rstrip('/')
                if repo_name:  # Skip empty prefixes
                    repos.append(repo_name)
        
        return sorted(repos)
    except ClientError as e:
        logger.error(f"Error listing repositories: {e}")
        raise
```

## Testing

### Running Tests

```bash
# Run all tests
python test_server.py

# Run with coverage
pytest --cov=app test_server.py

# Lint code
flake8 .
```

### Writing Tests

- Add tests for new functionality
- Use descriptive test names
- Mock external dependencies (S3, etc.)
- Test both success and failure cases

### Test Structure

```python
def test_feature_name():
    """Test description of what is being tested."""
    # Arrange
    setup_test_data()
    
    # Act
    result = function_under_test()
    
    # Assert
    assert result == expected_value
```

## Documentation

### Code Documentation

- Add docstrings to all public functions and classes
- Use Google-style docstrings
- Include parameter types and return types
- Document exceptions that may be raised

### README Updates

- Update README.md if you add new features
- Include examples of new functionality
- Update configuration documentation

### API Documentation

- Document new endpoints
- Include request/response examples
- Update the API section in README

## Development Tips

### Local Development

1. **Use debug mode**
   ```bash
   export DEBUG=True
   python app.py
   ```

2. **Test with mock data**
   - Create local test files
   - Use mocked S3 responses
   - Consider using LocalStack for AWS services

3. **Docker development**
   ```bash
   docker-compose -f docker-compose.dev.yml up
   ```

### Debugging

- Use Python debugger (`pdb`) for complex issues
- Check logs in the `logs/` directory
- Use browser developer tools for frontend issues

### Performance Considerations

- Profile code for performance bottlenecks
- Consider caching for frequently accessed data
- Optimize S3 API calls (use pagination, filters)

## Release Process

Releases are handled by maintainers:

1. Version bumping follows [Semantic Versioning](https://semver.org/)
2. Changelog is updated with new features and fixes
3. Docker images are built and pushed automatically
4. GitHub releases are created with release notes

## Getting Help

- **Questions**: Open a [Discussion](../../discussions)
- **Bugs**: Create an [Issue](../../issues)
- **Security**: Follow our [Security Policy](SECURITY.md)

## Recognition

Contributors will be recognized in:
- GitHub contributors list
- Release notes for significant contributions
- Special mentions for first-time contributors

Thank you for contributing to make this project better! 🎉
