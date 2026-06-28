"""
Lesson 4.6: Corporate Knowledge Bot (Capstone - TODO)

In this final lesson, you'll build a complete, deployable RAG knowledge assistant
that combines all prior lessons (4.2-4.5) into production-ready code.

Business Scenario:
  A company needs a knowledge assistant that employees can query about policies,
  tech stack, offices, benefits, and culture. The system must handle:
  • Document ingestion and embedding
  • Real-time retrieval and answer generation
  • Query history and analytics
  • Production deployment patterns
  • Error handling and monitoring

LEARNING OBJECTIVES:
  • Orchestrate complete RAG pipeline into single deployable method
  • Implement document ingestion at scale
  • Handle interactive user queries
  • Track metrics and performance indicators
  • Design for scalability and monitoring
  • Deploy RAG systems to production

REFERENCE:
  • See lesson-06-corporate-knowledge-bot.py (completed version)
  • Review lesson-04-building-rag-pipeline.py for orchestration
  • Review lesson-05-rag-optimization.py for quality improvement
  • Review shared/embeddings.py for embedding API

Run: python lesson-06-corporate-knowledge-bot.py
     python lesson-06-corporate-knowledge-bot.py --demo 1-4
     python lesson-06-corporate-knowledge-bot.py --interactive
"""

import os
import sys
import time
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

# Add project paths
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent / "shared"))

# TODO (PHASE 1): Import necessary modules
# You'll need:
#   - Optional embedding and vector store modules (for real implementation)
#   - time for measuring performance
#   - datetime for timestamps
#   - json for saving/loading bot state


# ============================================================================
# PHASE 1: IMPLEMENT THE CORE TEMPLATE METHOD
# ============================================================================
# Your main task: implement deploy_knowledge_assistant()


def deploy_knowledge_assistant(
    documents: List[str],
    queries: Optional[List[str]] = None,
    embedding_provider: str = "openrouter",
    chunk_size: int = 512,
    top_k: int = 5,
    interactive_mode: bool = False,
) -> Dict:
    """
    TODO: Deploy a complete RAG knowledge assistant.

    This method orchestrates the full RAG stack combining all prior lessons
    into a production-ready bot. It should support both batch and interactive modes.

    Implementation should:
    1. Initialize embedding engine and vector store
    2. Log initialization details (timestamps, config)
    3. Process and ingest all documents
       - Chunk documents if needed
       - Generate embeddings for each chunk
       - Store in vector store
    4. If interactive_mode:
       - Loop: accept user query → retrieve → answer → store history
    5. Else (batch mode):
       - Process all queries in sequence
    6. For each query:
       - Embed query
       - Retrieve top-K documents
       - Generate answer (or use stub)
       - Track metrics: retrieval time, token count
    7. Compute aggregate bot statistics:
       - total_documents, total_queries, avg_retrieval_time, etc.
    8. Return comprehensive results with answers, history, stats

    Args:
        documents: List of knowledge documents to ingest
        queries: Optional list of queries to process (batch mode)
        embedding_provider: "openrouter", "cohere", or "tfidf"
        chunk_size: Characters per chunk for document splitting
        top_k: Number of documents to retrieve per query
        interactive_mode: If True, accept stdin queries; else use queries list

    Returns:
        Dict with REQUIRED keys:
            - answers: List[Dict] with {query, answer, sources, retrieval_time}
            - bot_stats: {total_documents, total_queries, avg_retrieval_time, total_retrieval_time}
            - query_history: List of {query, timestamp, retrieval_time}
            - deployment_metadata: {timestamp, embedding_provider, chunk_size, top_k, total_documents}
            - errors: List of any errors encountered

    HINTS:
      • Use try/except to catch initialization errors
      • For each query: embed it, search vector store, retrieve top-K
      • Create answer from context (template or LLM)
      • Track retrieval_time for each query
      • Store query_history for analytics
      • Handle empty queries or document list gracefully
      • Return results dict even on partial failure
    """

    # TODO (PHASE 1): Implement all steps above
    raise NotImplementedError("Implement deploy_knowledge_assistant() - see docstring")


# ============================================================================
# PHASE 2: IMPLEMENT HELPER METHODS
# ============================================================================


def _get_interactive_queries() -> List[str]:
    """
    TODO: Accept queries from user interactively.

    Implementation should:
    1. Print prompt: "Enter queries (empty line to finish):"
    2. Loop: read from stdin with input("Query> ")
    3. Break if input is empty
    4. Return list of queries

    Returns:
        List[str]: User-entered queries
    """

    # TODO (PHASE 2): Implement interactive input
    raise NotImplementedError("Implement _get_interactive_queries()")


def _generate_answer(query: str, context: str) -> str:
    """
    TODO: Generate answer from retrieved context.

    This is a simplified stub. In production, call LLM (OpenRouter).

    Implementation should:
    1. Take top results from context
    2. Create answer stub or call LLM
    3. Return answer string

    Args:
        query: Original user query
        context: Retrieved document context

    Returns:
        str: Generated answer
    """

    # TODO (PHASE 2): Generate answer from context
    # For now, return a simple template
    raise NotImplementedError("Implement _generate_answer()")


# ============================================================================
# PHASE 3: IMPLEMENT DEMONSTRATIONS
# ============================================================================


def demo_basic_bot():
    """
    TODO: Demonstrate basic bot deployment with sample documents.

    This demo should:
    1. Create sample HR/company knowledge documents (5-8 docs)
    2. Create list of sample queries to process
    3. Call deploy_knowledge_assistant() with these documents
    4. Print bot statistics and sample answers

    REQUIREMENTS:
      • Use realistic company documents
      • Test 3-5 diverse queries
      • Show bot_stats output
      • Display retrieval times
    """

    print("\n" + "=" * 70)
    print("DEMO 1: BASIC BOT DEPLOYMENT")
    print("=" * 70)

    # TODO (PHASE 3): Create documents, call deploy_knowledge_assistant(), print results
    raise NotImplementedError("Implement demo_basic_bot()")


def demo_scalability():
    """
    TODO: Demonstrate and explain scalability considerations.

    This demo should print text explanations (no code execution needed) of:
    1. Document size scaling (small <1K, medium 1K-100K, large >100K)
    2. Latency requirements and architecture implications
    3. Update frequency (static, daily, real-time)
    4. Cost optimization techniques
    5. Monitoring and alerting

    REQUIREMENTS:
      • Print clear sections for each scalability dimension
      • Explain tradeoffs
      • Recommend solutions for different scenarios
    """

    print("\n" + "=" * 70)
    print("DEMO 2: SCALABILITY CONSIDERATIONS")
    print("=" * 70)

    # TODO (PHASE 3): Print scalability information
    raise NotImplementedError("Implement demo_scalability()")


def demo_deployment_options():
    """
    TODO: Explain different deployment patterns for RAG bots.

    This demo should print text explanations of:
    1. CLI Tool (batch processing, internal use)
    2. REST API (web integration, mobile)
    3. Streamlit UI (quick demos)
    4. Slack Bot (employee self-service)
    5. Web Chat Widget (customer support)
    6. Desktop App (offline access)

    For each, explain: use cases, pros, cons

    REQUIREMENTS:
      • Print clear deployment options
      • Explain when to use each
      • Note tradeoffs
    """

    print("\n" + "=" * 70)
    print("DEMO 3: DEPLOYMENT OPTIONS")
    print("=" * 70)

    # TODO (PHASE 3): Print deployment options
    raise NotImplementedError("Implement demo_deployment_options()")


def demo_monitoring():
    """
    TODO: Explain monitoring and observability for production bots.

    This demo should print text explanations of metrics to track:
    1. Retrieval Quality (Precision, Recall, MRR, NDCG)
    2. Performance (Query latency, cache hit rate)
    3. User Satisfaction (Query volume, ratings, repeat queries)
    4. Cost (API calls, storage, compute)
    5. Reliability (Uptime, error rate, recovery time)

    REQUIREMENTS:
      • Print clear metric categories
      • Explain what each metric means
      • Show how to use metrics for optimization
    """

    print("\n" + "=" * 70)
    print("DEMO 4: MONITORING & OBSERVABILITY")
    print("=" * 70)

    # TODO (PHASE 3): Print monitoring information
    raise NotImplementedError("Implement demo_monitoring()")


def main():
    """Run demonstrations or deploy bot."""
    import argparse
    parser = argparse.ArgumentParser(description="Corporate Knowledge Bot")
    parser.add_argument("--interactive", action="store_true", help="Interactive mode")
    parser.add_argument("--demo", type=int, default=0, help="Demo number (1-4)")
    args = parser.parse_args()

    print("\n" + "🚀 LESSON 4.6: CORPORATE KNOWLEDGE BOT".center(70, "="))
    print("Core Template Method: deploy_knowledge_assistant()")
    print("Business Scenario: Employee Knowledge Assistant")

    try:
        if args.demo == 1:
            demo_basic_bot()
        elif args.demo == 2:
            demo_scalability()
        elif args.demo == 3:
            demo_deployment_options()
        elif args.demo == 4:
            demo_monitoring()
        elif args.interactive:
            # Interactive mode
            documents = [
                "Our company values innovation, collaboration, and continuous learning.",
                "We support remote work with flexible hours and $500/month home office stipend.",
                "Our tech stack includes Python, Go, TypeScript, and PostgreSQL.",
                "We have offices in San Francisco, London, and Singapore.",
                "All employees receive comprehensive health insurance and unlimited PTO.",
            ]
            result = deploy_knowledge_assistant(
                documents=documents,
                interactive_mode=True,
            )
        else:
            # Run all demos
            demo_basic_bot()
            demo_scalability()
            demo_deployment_options()
            demo_monitoring()

        print("\n" + "=" * 70)
        print("✅ Knowledge bot demonstrations complete!")
        print("=" * 70)
        print("\nKey Takeaways:")
        print("  • deploy_knowledge_assistant() is your capstone template")
        print("  • Combines lessons 4.2 → 4.3 → 4.4 → 4.5 → 4.6")
        print("  • Choose deployment pattern for your domain")
        print("  • Plan monitoring from day one")
        print("  • Design for scale, implement minimum viable product")

    except NotImplementedError as e:
        print(f"\n⚠️  {e}")
        print("\nImplementation steps:")
        print("  PHASE 1: Implement deploy_knowledge_assistant() core method")
        print("  PHASE 2: Implement helper methods")
        print("  PHASE 3: Implement all 4 demo functions")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
