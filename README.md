# Centralized Allure Reports Server

[![CI/CD Pipeline](https://github.com/vsbopi/centralized-allure-server/actions/workflows/ci.yml/badge.svg)](https://github.com/vsbopi/centralized-allure-server/actions/workflows/ci.yml)
[![Docker Build](https://github.com/vsbopi/centralized-allure-server/actions/workflows/docker.yml/badge.svg)](https://github.com/vsbopi/centralized-allure-server/actions/workflows/docker.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)](https://hub.docker.com/)
[![AWS S3](https://img.shields.io/badge/AWS-S3-orange.svg?style=flat&logo=amazon-aws)](https://aws.amazon.com/s3/)

A Python web server that serves Allure test reports from an S3 bucket with a beautiful web interface. This project allows you to centralize all your Allure reports from multiple repositories in one place.

> **⭐ Star this repository if you find it useful!**

## Table of Contents

- [Features](#features)
- [Demo](#demo)
- [Directory Structure](#directory-structure)
- [Quick Start](#quick-start)
- [GitHub Actions Integration](#github-actions-integration)
- [Environment Variables](#environment-variables)
- [AWS Setup](#aws-setup)
- [Production Deployment](#production-deployment)
- [API Endpoints](#api-endpoints)
- [Development](#development)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Features

- 🏗️ **Multi-Repository Support**: Organize reports by repository
- 📊 **Allure Report Viewer**: Interactive HTML reports
- 📋 **Result Files Browser**: Browse raw test result files
- ☁️ **S3 Integration**: Fetch reports directly from S3
- 🎨 **Modern UI**: Beautiful, responsive web interface
- 🚀 **Easy Deployment**: Simple Python server that can run anywhere

## Demo

### Screenshots

| Main Dashboard | Repository View | Branch Reports |
|:---:|:---:|:---:|
| <img width="340" height="187" alt="Dashboard" src="https://github.com/user-attachments/assets/c6178a78-b3e4-47ed-a16b-d0e9b12a8eb7" /> | <img width="340" height="187" alt="Repository" src="https://github.com/user-attachments/assets/f251fccd-753c-4ecf-bac3-1b6c5ec1d559" /> | <img width="340" height="187" alt="Reports" src="https://github.com/user-attachments/assets/0881619f-ac03-4521-a1ef-edd80627d784" /> |


## Directory Structure

The server expects your S3 bucket to be organized as follows:

```
your-s3-bucket/
├── repo1/
│   ├── main/
│   │   ├── allure-report/
│   │   │   ├── index.html
│   │   │   ├── app.js
│   │   │   └── ...
│   │   └── allure-results/
│   │       ├── test-result-1.json
│   │       ├── test-result-2.json
│   │       └── ...
│   ├── develop/
│   │   ├── allure-report/
│   │   └── allure-results/
│   └── feature-branch/
│       ├── allure-report/
│       └── allure-results/
├── repo2/
│   ├── main/
│   │   ├── allure-report/
│   │   └── allure-results/
│   └── develop/
│       ├── allure-report/
│       └── allure-results/
└── repo3/
    └── main/
        ├── allure-report/
        └── allure-results/
```

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Copy the example environment file and edit it:

```bash
cp env.example .env
```

Edit `.env` with your AWS credentials and S3 bucket information:

```env
S3_BUCKET_NAME=your-allure-reports-bucket
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_REGION=us-east-1
PORT=8080
DEBUG=False
```

### 3. Run the Server

```bash
python app.py
```

Or use the built-in HTTP server approach:

```bash
python -m app
```

The server will start on `http://localhost:8080`

## GitHub Actions Integration

To upload your Allure reports to S3 from GitHub Actions, add this step to your workflow:

```yaml
name: Upload Allure Reports
on:
  push:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run tests and generate Allure report
        run: |
          # Your test commands here
          # This should generate allure-results/ directory
          
      - name: Generate Allure Report
        uses: simple-elf/allure-report-action@master
        if: always()
        with:
          allure_results: allure-results
          allure_report: allure-report
          
      - name: Upload to S3
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          AWS_REGION: us-east-1
          S3_BUCKET: ${{ secrets.S3_BUCKET_NAME }}
        run: |
          # Get branch name (remove refs/heads/ prefix)
          BRANCH_NAME=${GITHUB_REF#refs/heads/}
          
          # Upload allure-report
          aws s3 sync allure-report s3://$S3_BUCKET/${{ github.event.repository.name }}/$BRANCH_NAME/allure-report/ --delete
          
          # Upload allure-results
          aws s3 sync allure-results s3://$S3_BUCKET/${{ github.event.repository.name }}/$BRANCH_NAME/allure-results/ --delete
```

## Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `S3_BUCKET_NAME` | Name of your S3 bucket | Yes | - |
| `AWS_ACCESS_KEY_ID` | AWS Access Key ID | Yes* | - |
| `AWS_SECRET_ACCESS_KEY` | AWS Secret Access Key | Yes* | - |
| `AWS_REGION` | AWS Region | No | us-east-1 |
| `PORT` | Server port | No | 8080 |
| `DEBUG` | Enable debug mode | No | False |

*Required unless using IAM roles or other AWS credential methods

## AWS Setup

### 1. Create S3 Bucket

```bash
aws s3 mb s3://your-allure-reports-bucket
```

### 2. Create IAM Policy

Create an IAM policy with the following permissions:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::your-allure-reports-bucket",
                "arn:aws:s3:::your-allure-reports-bucket/*"
            ]
        }
    ]
}
```

### 3. Create IAM User

Create an IAM user and attach the policy, then create access keys for the server.

## Production Deployment

### Using Docker

#### Quick Start with Docker

1. **Build the image**:
   ```bash
   # Linux/Mac
   ./docker-build.sh
   
   # Windows
   docker-build.bat
   
   # Or manually
   docker build -t allure-reports-server .
   ```

2. **Run the container**:
   ```bash
   # Linux/Mac
   ./docker-run.sh
   
   # Windows
   docker-run.bat
   
   # Or manually
   docker run -p 8080:8080 --env-file .env allure-reports-server
   ```

#### Using Docker Compose (Recommended)

1. **Production deployment**:
   ```bash
   docker-compose up -d
   ```

2. **Development with live reload**:
   ```bash
   docker-compose -f docker-compose.dev.yml up
   ```

#### Production Dockerfile

For optimized production builds, use the multi-stage Dockerfile:

```bash
docker build -f Dockerfile.production -t allure-reports-server:prod .
```

#### Docker Environment Variables

The container accepts these environment variables:
- `S3_BUCKET_NAME` (required)
- `AWS_ACCESS_KEY_ID` (required)
- `AWS_SECRET_ACCESS_KEY` (required)
- `AWS_REGION` (default: us-east-1)
- `PORT` (default: 8080)
- `DEBUG` (default: False)
- `HOST` (default: 0.0.0.0)

### Using systemd (Linux)

Create `/etc/systemd/system/allure-reports.service`:

```ini
[Unit]
Description=Allure Reports Server
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/centralized-allure-server
Environment=PATH=/path/to/your/venv/bin
ExecStart=/path/to/your/venv/bin/python app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable allure-reports
sudo systemctl start allure-reports
```

## API Endpoints

- `GET /` - Main page listing all repositories
- `GET /repo/<repo_name>` - Repository detail page showing branches
- `GET /repo/<repo_name>/<branch_name>` - Branch detail page showing report types
- `GET /repo/<repo_name>/<branch_name>/<report_type>` - View specific report type
- `GET /files/<path:path>` - Serve individual files from S3
- `GET /health` - Health check endpoint

## Development

### Local Development

1. Set `DEBUG=True` in your `.env` file
2. The server will automatically reload on code changes
3. Use the Flask development server for debugging

### Testing

To test the server without AWS:

1. Create a mock S3 bucket structure locally
2. Modify the S3 client to use local filesystem
3. Or use LocalStack for local AWS services

## Troubleshooting

### Common Issues

1. **S3 Connection Error**: Check your AWS credentials and bucket permissions
2. **Files Not Loading**: Ensure your S3 bucket has the correct directory structure
3. **CORS Issues**: Make sure your S3 bucket allows cross-origin requests if needed

### Logging

The application uses Python's logging module. Set `DEBUG=True` for verbose logging.

## Contributing

We welcome contributions from everyone! Here's how you can help:

### 🐛 Found a Bug?
- Check if it's already reported in [Issues](../../issues)
- If not, [create a new issue](../../issues/new/choose) with the bug report template

### 💡 Have a Feature Idea?
- [Create a feature request](../../issues/new/choose) using our template
- Join the discussion in [Discussions](../../discussions)

### 🔧 Want to Contribute Code?
1. Read our [Contributing Guide](CONTRIBUTING.md)
2. Fork the repository
3. Create a feature branch: `git checkout -b feature/amazing-feature`
4. Make your changes and add tests
5. Submit a pull request

### 📖 Improve Documentation?
- Fix typos, improve examples, or add missing information
- Documentation improvements are always welcome!

Please read our [Code of Conduct](CODE_OF_CONDUCT.md) before contributing.

## Community & Support

- 💬 **Discussions**: [GitHub Discussions](../../discussions) - Ask questions, share ideas
- 🐛 **Issues**: [GitHub Issues](../../issues) - Report bugs, request features  
- 📧 **Security**: See [SECURITY.md](SECURITY.md) for reporting security issues
- ⭐ **Show Support**: Star the repository if you find it useful!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to all [contributors](../../graphs/contributors) who have helped improve this project
- Built with [Flask](https://flask.palletsprojects.com/) and [Allure Framework](https://docs.qameta.io/allure/)
- Inspired by the need for centralized test reporting across multiple repositories
