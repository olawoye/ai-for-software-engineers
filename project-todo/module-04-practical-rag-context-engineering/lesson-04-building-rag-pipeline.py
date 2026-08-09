"""
Lesson 4.4: Building the RAG Pipeline — TODO Scaffold

Assemble a complete end-to-end RAG workflow combining retrieval and LLM generation.

BUSINESS SCENARIO:
An HR assistant answers employee questions using internal knowledge base documents.
Must retrieve relevant docs and generate accurate answers with proper citations.

Run: python lesson-04-building-rag-pipeline.py
Requires: export OPENROUTER_API_KEY='your-key-here'
"""

import os
import sys
import time
from pathlib import Path
from typing import List, Dict, Optional
import numpy as np

# Add project paths
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent / "shared"))


# ============================================================================
# STAGE 1: Helper Functions (Smart Chunking & LLM Integration)
# ============================================================================
# Implement text chunking and LLM API integration utilities.
# Available utilities: EmbeddingEngine, VectorStore, requests, time module
# TODO: Add your Stage 1 implementation here


# ============================================================================
# STAGE 2: Core Template Method (build_rag_pipeline)
# ============================================================================
# Orchestrate complete end-to-end RAG workflow with retrieval and generation.
# Available utilities: EmbeddingEngine, VectorStore, LLM API, performance metrics
# TODO: Add your Stage 2 implementation here


# ============================================================================
# STAGE 3: Demonstrations
# ============================================================================
# Implement demo functions showing the RAG pipeline in action.
# Available utilities: sample documents, queries, timing/metrics tracking
# TODO: Add your Stage 3 implementation here


# ============================================================================
# STAGE 4: Main Entry Point
# ============================================================================
# Orchestrate demo execution with CLI support.
# Available utilities: conditional demo selection, argument parsing
# TODO: Add your Stage 4 implementation here
