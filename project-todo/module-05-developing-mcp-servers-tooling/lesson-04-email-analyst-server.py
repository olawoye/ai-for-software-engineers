"""
Lesson 5.4: Email Analyst Server — TODO Scaffold

Build an MCP server that processes and analyzes email data, demonstrating
real-world use cases with multiple sophisticated tools.

BUSINESS SCENARIO:
Customer support teams need to analyze email conversations at scale. This server
provides tools for sentiment analysis, spam detection, intent classification, and
key phrase extraction from email datasets.

Run: python lesson-04-email-analyst-server.py
Requires: export OPENROUTER_API_KEY='your-key-here'
"""

import os
import sys
import json
from pathlib import Path
from typing import List, Dict, Optional

# Import from shared module
sys.path.insert(0, str(Path(__file__).parent))
from shared.mcp_server import MCPServer, Resource, Tool


# ============================================================================
# STAGE 1: Tool Implementations (5 Analysis Tools)
# ============================================================================
# Implement sentiment analysis, spam detection, intent classification, and
# key phrase extraction tools for email processing.
# Available utilities: text processing, sentiment analysis, classification helpers
# TODO: Add your Stage 1 implementation here


# ============================================================================
# STAGE 2: Core Server Setup
# ============================================================================
# Initialize MCP server and register all email analysis tools.
# Available utilities: MCPServer, Tool registration, schema definitions
# TODO: Add your Stage 2 implementation here


# ============================================================================
# STAGE 3: Email Dataset & Demo Scenarios
# ============================================================================
# Create sample email data and demonstrate each tool's capabilities.
# Available utilities: sample emails, email parsing, result formatting
# TODO: Add your Stage 3 implementation here


# ============================================================================
# STAGE 4: Analytics & Batch Processing
# ============================================================================
# Implement bulk email analysis and results aggregation.
# Available utilities: batch processing, metrics aggregation, JSON export
# TODO: Add your Stage 4 implementation here
