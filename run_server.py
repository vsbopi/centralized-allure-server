#!/usr/bin/env python3
"""
Simple script to run the Allure Reports Server
Similar to 'python -m http.server 8080' but for our Flask app
"""

import sys
import os
from app import app, logger

def main():
    """Main entry point for running the server"""
    try:
        port = int(os.getenv('PORT', 8080))
        debug = os.getenv('DEBUG', 'False').lower() == 'true'
        
        logger.info(f"Starting Centralized Allure Reports Server...")
        logger.info(f"Server will run on http://localhost:{port}")
        logger.info(f"Debug mode: {debug}")
        
        if debug:
            app.run(host='0.0.0.0', port=port, debug=True)
        else:
            # Use waitress for production
            from waitress import serve
            logger.info("Using Waitress WSGI server for production")
            serve(app, host='0.0.0.0', port=port)
            
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
