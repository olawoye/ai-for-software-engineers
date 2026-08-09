"""
Lesson 6.3: Tool Use & Function Calling — TODO Scaffold

Teach agents to discover, select, and invoke tools from external toolkits to
extend their capabilities and take real-world actions.

BUSINESS SCENARIO:
Agents need to access external systems (databases, APIs, MCP servers) to complete
complex tasks. This lesson teaches systematic tool discovery and function calling
patterns that enable agents to execute real workflows.

Run: python lesson-03-tool-use-function-calling.py
Requires: export OPENROUTER_API_KEY='your-key-here'
"""

import sys
import json
from pathlib import Path
from typing import List, Dict, Optional, Any, Callable
from enum import Enum


# ============================================================================
# STAGE 1: Tool Registry & Discovery
# ============================================================================
# Build a registry system for discovering and describing available tools.
# Available utilities: tool metadata schemas, type hints, documentation
# TODO: Add your Stage 1 implementation here


# ============================================================================
# STAGE 2: Function Calling & Tool Selection
# ============================================================================
# Implement agent reasoning for tool selection based on task requirements.
# Available utilities: tool matching logic, LLM-based selection, validation
# TODO: Add your Stage 2 implementation here


# ============================================================================
# STAGE 3: Tool Execution & Result Integration
# ============================================================================
# Execute selected tools and integrate results back into agent reasoning.
# Available utilities: error handling, result formatting, state updates
# TODO: Add your Stage 3 implementation here


# ============================================================================
# STAGE 4: Demonstrations
# ============================================================================
# Show agents discovering, selecting, and executing tools in realistic scenarios.
# Available utilities: sample tool kits, task examples, execution traces
# TODO: Add your Stage 4 implementation here
