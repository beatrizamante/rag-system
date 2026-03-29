#!/usr/bin/env python
"""
Main entry point for Hermes RAG API Server.

Usage:
    python main.py                    # Run with default settings
    python main.py --port 8080        # Run on custom port
    python main.py --reload           # Run with auto-reload (development)
"""
import argparse
import logging
import sys
import os
import uvicorn
from interface.api import create_app

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def setup_logging(debug: bool = False):
    """Configure logging."""
    level = logging.DEBUG if debug else logging.INFO

    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)


def main():
    """Run the API server."""
    parser = argparse.ArgumentParser(description="Hermes RAG API Server")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")

    args = parser.parse_args()

    setup_logging(args.debug)
    logger = logging.getLogger(__name__)

    logger.info("Starting Hermes RAG API Server")
    logger.info("Host: %s, Port: %s", args.host, args.port)

    try:


        app = create_app()

        uvicorn.run(
            app,
            host=args.host,
            port=args.port,
            reload=args.reload,
            log_level="debug" if args.debug else "info"
        )

    except ImportError as e:
        logger.error("Missing dependency: %s", e)
        logger.error("Install dependencies with: pip install -r requirements.txt")
        sys.exit(1)
    except (OSError, ValueError) as e:
        logger.error("Failed to start server: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
