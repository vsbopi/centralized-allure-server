#!/usr/bin/env python3
"""
Centralized Allure Reports Web Server
Serves allure reports from S3 bucket with directory-based organization
"""

import os
import logging
from flask import Flask, render_template, send_file, abort, request, redirect, url_for
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from dotenv import load_dotenv
import tempfile
from urllib.parse import unquote
import mimetypes

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class S3ReportsServer:
    def __init__(self):
        self.bucket_name = os.getenv('S3_BUCKET_NAME')
        self.aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
        self.aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        self.aws_region = os.getenv('AWS_REGION', 'us-east-1')
        
        if not self.bucket_name:
            raise ValueError("S3_BUCKET_NAME environment variable is required")
        
        try:
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=self.aws_access_key,
                aws_secret_access_key=self.aws_secret_key,
                region_name=self.aws_region
            )
            # Test connection
            self.s3_client.head_bucket(Bucket=self.bucket_name)
            logger.info(f"Successfully connected to S3 bucket: {self.bucket_name}")
        except NoCredentialsError:
            logger.error("AWS credentials not found")
            raise
        except ClientError as e:
            logger.error(f"Error connecting to S3: {e}")
            raise

    def list_repositories(self):
        """List all repository directories in the S3 bucket"""
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
            return []

    def list_branches_for_repo(self, repo_name):
        """List all branches for a repository"""
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=f"{repo_name}/",
                Delimiter='/'
            )
            
            branches = []
            if 'CommonPrefixes' in response:
                for prefix in response['CommonPrefixes']:
                    branch_path = prefix['Prefix'].rstrip('/')
                    branch_name = branch_path.split('/')[-1]
                    if branch_name:  # Skip empty prefixes
                        branches.append(branch_name)
            
            return sorted(branches)
        except ClientError as e:
            logger.error(f"Error listing branches for {repo_name}: {e}")
            return []

    def list_reports_for_branch(self, repo_name, branch_name):
        """List available report types for a specific branch"""
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=f"{repo_name}/{branch_name}/",
                Delimiter='/'
            )
            
            reports = []
            if 'CommonPrefixes' in response:
                for prefix in response['CommonPrefixes']:
                    report_path = prefix['Prefix'].rstrip('/')
                    report_type = report_path.split('/')[-1]
                    if report_type in ['allure-report', 'allure-results']:
                        reports.append(report_type)
            
            return sorted(reports)
        except ClientError as e:
            logger.error(f"Error listing reports for {repo_name}/{branch_name}: {e}")
            return []

    def get_file_from_s3(self, s3_key):
        """Download a file from S3 and return it as a temporary file"""
        try:
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=s3_key)
            
            # Create a temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False)
            temp_file.write(response['Body'].read())
            temp_file.close()
            
            return temp_file.name
        except ClientError as e:
            logger.error(f"Error downloading file {s3_key}: {e}")
            return None

    def list_files_in_path(self, s3_prefix):
        """List all files in a given S3 path"""
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=s3_prefix
            )
            
            files = []
            if 'Contents' in response:
                for obj in response['Contents']:
                    if not obj['Key'].endswith('/'):  # Skip directories
                        files.append(obj['Key'])
            
            return files
        except ClientError as e:
            logger.error(f"Error listing files in {s3_prefix}: {e}")
            return []

# Initialize the S3 server
try:
    s3_server = S3ReportsServer()
except Exception as e:
    logger.error(f"Failed to initialize S3 server: {e}")
    s3_server = None

@app.route('/')
def index():
    """Main page showing all repositories"""
    if not s3_server:
        return render_template('error.html', error="S3 connection not available"), 500
    
    repos = s3_server.list_repositories()
    return render_template('index.html', repositories=repos)

@app.route('/repo/<repo_name>')
def repo_detail(repo_name):
    """Show available branches for a repository"""
    if not s3_server:
        return render_template('error.html', error="S3 connection not available"), 500
    
    branches = s3_server.list_branches_for_repo(repo_name)
    return render_template('repo_detail.html', repo_name=repo_name, branches=branches)

@app.route('/repo/<repo_name>/<branch_name>')
def branch_detail(repo_name, branch_name):
    """Show available reports for a specific branch"""
    if not s3_server:
        return render_template('error.html', error="S3 connection not available"), 500
    
    reports = s3_server.list_reports_for_branch(repo_name, branch_name)
    return render_template('branch_detail.html', repo_name=repo_name, branch_name=branch_name, reports=reports)

@app.route('/repo/<repo_name>/<branch_name>/<report_type>')
def view_report(repo_name, branch_name, report_type):
    """Redirect to the main report file (index.html for allure-report)"""
    if report_type == 'allure-report':
        return redirect(url_for('serve_file', path=f"{repo_name}/{branch_name}/{report_type}/index.html"))
    elif report_type == 'allure-results':
        # For allure-results, show a file listing
        return render_template('file_listing.html', 
                             repo_name=repo_name,
                             branch_name=branch_name, 
                             report_type=report_type,
                             files=s3_server.list_files_in_path(f"{repo_name}/{branch_name}/{report_type}/"))
    else:
        abort(404)

@app.route('/files/<path:path>')
def serve_file(path):
    """Serve individual files from S3"""
    if not s3_server:
        abort(500)
    
    # Decode URL-encoded path
    path = unquote(path)
    
    # Download file from S3
    temp_file_path = s3_server.get_file_from_s3(path)
    if not temp_file_path:
        abort(404)
    
    # Determine MIME type
    mime_type, _ = mimetypes.guess_type(path)
    if mime_type is None:
        mime_type = 'application/octet-stream'
    
    # Serve the file and clean up temp file after sending
    try:
        return send_file(temp_file_path, mimetype=mime_type, as_attachment=False)
    finally:
        # Clean up temp file
        try:
            os.unlink(temp_file_path)
        except OSError:
            pass

@app.route('/health')
def health_check():
    """Health check endpoint"""
    if s3_server:
        return {"status": "healthy", "bucket": s3_server.bucket_name}
    else:
        return {"status": "unhealthy", "error": "S3 not connected"}, 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    if debug:
        app.run(host='0.0.0.0', port=port, debug=True)
    else:
        # Use waitress for production
        from waitress import serve
        logger.info(f"Starting server on port {port}")
        serve(app, host='0.0.0.0', port=port)
