# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial release of Centralized Allure Reports Server
- Multi-repository support for organizing Allure reports
- S3 integration for storing and serving reports
- Web interface for browsing reports and results
- Docker support with multi-stage builds
- GitHub Actions CI/CD pipeline
- Comprehensive documentation and contributing guidelines

### Features
- 🏗️ Multi-Repository Support: Organize reports by repository
- 📊 Allure Report Viewer: Interactive HTML reports
- 📋 Result Files Browser: Browse raw test result files
- ☁️ S3 Integration: Fetch reports directly from S3
- 🎨 Modern UI: Beautiful, responsive web interface
- 🚀 Easy Deployment: Simple Python server that can run anywhere

### Technical Details
- Python 3.8+ support
- Flask web framework
- AWS S3 integration with boto3
- Waitress WSGI server for production
- Docker containerization
- GitHub Actions workflows
- Comprehensive test coverage

## [1.0.0] - TBD

### Added
- Initial stable release

---

## Release Notes Template

When creating a new release, use this template:

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- New features

### Changed
- Changes in existing functionality

### Deprecated
- Soon-to-be removed features

### Removed
- Removed features

### Fixed
- Bug fixes

### Security
- Security improvements
```
