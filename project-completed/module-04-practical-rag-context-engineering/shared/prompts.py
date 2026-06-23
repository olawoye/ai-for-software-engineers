"""
RAG-specific prompt templates for context augmentation.
Handles document retrieval formatting and answer generation.
"""

# Document retrieval prompt
CONTEXT_PROMPT = """
Use the following documents to answer the question. If the answer is not in the documents, say so.

Documents:
{documents}

Question: {question}

Answer:
"""

# RAG generation with citations
CITED_ANSWER_PROMPT = """
Based on the following documents, provide an answer with citations.

Documents:
{documents}

Question: {question}

Provide your answer with citations like [Doc 1], [Doc 2], etc.

Answer:
"""

# Summarization of retrieved documents
SUMMARY_PROMPT = """
Summarize the key points from these documents:

{documents}

Focus on information relevant to: {query}

Summary:
"""

# Quality check for RAG answers
QUALITY_CHECK_PROMPT = """
Does this answer address the question and rely on the provided documents?

Question: {question}
Documents: {documents}
Answer: {answer}

Rate: Good/Partial/Poor
Explanation:
"""


def format_context(documents: list, question: str) -> str:
    """Format retrieved documents as context."""
    doc_text = "\n---\n".join(
        [f"[Doc {i+1}]\n{doc}" for i, doc in enumerate(documents)]
    )
    return CONTEXT_PROMPT.format(documents=doc_text, question=question)


def format_citations(documents: list, question: str) -> str:
    """Format documents with citation markers."""
    doc_text = "\n---\n".join(
        [f"[Doc {i+1}]\n{doc}" for i, doc in enumerate(documents)]
    )
    return CITED_ANSWER_PROMPT.format(documents=doc_text, question=question)


def format_summary(documents: list, query: str) -> str:
    """Format documents for summarization."""
    doc_text = "\n---\n".join(documents)
    return SUMMARY_PROMPT.format(documents=doc_text, query=query)
