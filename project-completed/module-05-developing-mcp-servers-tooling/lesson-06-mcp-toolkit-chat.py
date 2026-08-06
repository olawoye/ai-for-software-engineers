"""
Lesson 5.6 Bonus: MCP Toolkit Chat Interface (Streamlit UI)

Real-world 2-step scenario demonstrating how MCP clients use the toolkit:
  (a) FIND: Analyze customer emails to identify most urgent issue
  (b) SOLVE: Search internal knowledge base to find solution

This UI showcases:
  - Email analysis & prioritization (Lesson 5.4 tools: parse, analyze, categorize)
  - Knowledge search & retrieval (Lesson 5.3 tools: search, get_document)
  - Cross-tool workflows in action
  - Real LLM processing for intelligent decision-making
  - JSON-RPC protocol visibility (Debug mode)

Run:
    streamlit run lesson-06-mcp-toolkit-chat.py

Requires: OPENROUTER_API_KEY environment variable (optional, falls back to mock)
"""

import streamlit as st
import json
import uuid
import importlib.util
import os
import re
from pathlib import Path
from typing import List, Dict, Optional, Any
from datetime import datetime
import requests

# Import MCP toolkit
try:
    lesson_06_path = Path(__file__).parent / "lesson-06-mcp-toolkit-server.py"
    spec = importlib.util.spec_from_file_location("lesson_06_toolkit", lesson_06_path)
    lesson_06 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(lesson_06)
    create_mcp_toolkit = lesson_06.create_mcp_toolkit
except (ImportError, AttributeError) as e:
    st.error(f"Could not import lesson-06: {e}")
    st.stop()

# ============================================================================
# CONFIGURATION & DATA SETUP
# ============================================================================

# Tool Manifest - simulates MCP server's available tools
# When new tools are added to your MCP server, add them here to enable chat routing
TOOL_MANIFEST = {
    "email_search": {
        "description": "Analyze and search customer emails to find urgent issues, support tickets, or specific customer communications. Use this when user asks about emails, urgent customer problems, incoming messages, or support tickets."
    },
    "knowledge_search": {
        "description": "Search internal knowledge base for documentation, guides, solutions, troubleshooting steps, and how-to materials. Use this when user asks for documentation, guides, solutions, or how to resolve issues."
    },
    "general_chat": {
        "description": "General conversation and answering questions on any topic not related to email or knowledge search. Use this for general knowledge questions, trivia, explanations, or any non-tool-specific queries."
    }
}

st.set_page_config(
    page_title="MCP Toolkit AI Assistant",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sample customer emails (simulated email system)
SAMPLE_EMAILS = [
    {
        "id": "email-001",
        "from": "customer1@acme.com",
        "subject": "Website is down - losing revenue",
        "body": "Our website hasn't been accessible since 2pm. This is impacting our business. Please help immediately!",
        "timestamp": "2026-08-06 14:30:00"
    },
    {
        "id": "email-002",
        "from": "customer2@techcorp.com",
        "subject": "Question about RAG implementation",
        "body": "Hi, I'm looking to implement RAG in our system. Can you point me to some resources?",
        "timestamp": "2026-08-06 13:15:00"
    },
    {
        "id": "email-003",
        "from": "customer3@startup.io",
        "subject": "URGENT: Database connection pooling issue in production",
        "body": "Critical: Our production database keeps dropping connections. We're losing transactions. This needs immediate attention!",
        "timestamp": "2026-08-06 14:45:00"
    },
]

# Sample internal knowledge base docs (pre-created)
SAMPLE_DOCS = {
    "db-troubleshooting.md": """# Database Connection Troubleshooting Guide

## Connection Pool Issues
When database connections drop, follow these steps:

1. Check connection pool configuration (max_connections, timeout)
2. Review database logs for timeout patterns
3. Restart database service if needed
4. Monitor connection metrics

## Common Solutions
- Increase max_connections in database config
- Adjust connection timeout values
- Implement connection retry logic
- Use connection pooling middleware

## Prevention
- Set up monitoring alerts for connection drops
- Implement automatic failover
- Use load balancing for database connections
""",
    "rag-guide.md": """# Retrieval-Augmented Generation (RAG) Pattern

## Overview
RAG combines retrieval and generation for better AI responses.

## Implementation Steps
1. Prepare knowledge base (documents, chunks)
2. Create embeddings for each chunk
3. Implement retrieval mechanism
4. Integrate with LLM for generation

## Architecture
- Document ingestion → Embedding → Storage → Retrieval → Generation
""",
    "system-architecture.md": """# System Architecture Guide

## Components
- API Layer: REST/GraphQL endpoints
- Middleware: Authentication, rate limiting
- Database: Connection pooling, replication
- Cache: Redis for performance
- Queue: Message processing

## Best Practices
- Use connection pooling for databases
- Implement circuit breakers
- Monitor all service layers
"""
}

# ============================================================================
# LLM API INTEGRATION (OPENROUTER)
# ============================================================================

def call_llm_api(prompt: str, system_prompt: str = "", temperature: float = 0.7) -> Optional[str]:
    """
    Call OpenRouter API for LLM inference.
    Returns: LLM response text, or None if API unavailable.
    
    This demonstrates real LLM-powered processing instead of rule-based logic.
    Requires: OPENROUTER_API_KEY environment variable
    """
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return None
    
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "HTTP-Referer": "http://localhost:8501",
            "X-Title": "MCP Toolkit Chat",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": system_prompt} if system_prompt else None,
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature,
            "max_tokens": 1000
        }
        
        # Remove None values
        data["messages"] = [m for m in data["messages"] if m]
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            print(f"LLM API Error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"LLM API Exception: {e}")
        return None


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def initialize_toolkit():
    """Initialize MCP Toolkit on first load."""
    if st.session_state.toolkit is None:
        with st.spinner("🔄 Initializing MCP Toolkit..."):
            st.session_state.toolkit = create_mcp_toolkit(
                permission_strategy="power_user",
                enable_audit_logging=True
            )
        st.success("✅ Toolkit initialized!")
    return st.session_state.toolkit


def log_jsonrpc_call(tool_name: str, arguments: Dict[str, Any], result: Any):
    """Log JSON-RPC request/response for debugging."""
    request_id = str(uuid.uuid4())[:8]
    
    jsonrpc_request = {
        "jsonrpc": "2.0",
        "id": request_id,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments
        }
    }
    
    jsonrpc_response = {
        "jsonrpc": "2.0",
        "id": request_id,
        "result": result if isinstance(result, dict) else {"output": str(result)[:300]}
    }
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "tool": tool_name,
        "request": jsonrpc_request,
        "response": jsonrpc_response
    }
    
    st.session_state.json_rpc_logs.append(log_entry)


def classify_message_intent(query: str) -> str:
    """
    Classify user's message intent by matching against available tools.
    
    Uses LLM to intelligently match user query to tool descriptions from TOOL_MANIFEST.
    This simulates how real MCP clients determine which tool to invoke based on 
    available tool registry.
    
    Returns: Tool name from TOOL_MANIFEST, or "general_chat" if no tool matches
    """
    # Build tool options for LLM classification
    tools_description = "\n".join([
        f"- {tool_name}: {tool_info['description']}"
        for tool_name, tool_info in TOOL_MANIFEST.items()
    ])
    
    classification_prompt = f"""Given the user's query below, determine which tool they are trying to use.

Available tools:
{tools_description}

User query: "{query}"

Which tool should handle this query? Respond with ONLY the tool name (email_search, knowledge_search, or general_chat), nothing else."""
    
    # Try LLM-based classification
    llm_available = os.getenv("OPENROUTER_API_KEY") is not None
    
    if llm_available:
        response = call_llm_api(classification_prompt, temperature=0.3)
        if response:
            response_clean = response.strip().lower()
            # Check if response contains a valid tool name
            for tool_name in TOOL_MANIFEST.keys():
                if tool_name in response_clean:
                    return tool_name
    
    # Fallback: use simple keyword matching for critical paths
    query_lower = query.lower()
    
    # Strong email indicators
    if any(keyword in query_lower for keyword in ["email", "urgent", "critical", "customer", "ticket", "support"]):
        return "email_search"
    
    # Strong knowledge indicators
    if any(keyword in query_lower for keyword in ["document", "documentation", "guide", "rag", "solution", "troubleshoot"]):
        return "knowledge_search"
    
    # Default to general chat
    return "general_chat"


def analyze_emails_for_urgency(query: str = "") -> Dict[str, Any]:
    """
    STEP (a): Analyze customer emails to find most urgent issue.
    Uses email tools: parse_email → analyze_sentiment → categorize
    
    With LLM API: Uses Claude to intelligently rank emails by urgency.
    Without LLM API: Falls back to rule-based keyword matching.
    
    Args:
        query: User's query to help prioritize emails
    """
    results = []
    
    # First try LLM-based analysis
    llm_available = os.getenv("OPENROUTER_API_KEY") is not None
    
    if llm_available:
        # LLM-powered email analysis
        emails_text = "\n\n".join([
            f"Email {i+1}:\nFrom: {e['from']}\nSubject: {e['subject']}\nBody: {e['body']}"
            for i, e in enumerate(SAMPLE_EMAILS)
        ])
        
        analysis_prompt = f"""Analyze these customer emails and identify the most urgent one.
For each email, rate urgency as HIGH, MEDIUM, or LOW based on business impact.

Emails:
{emails_text}

Output ONLY valid JSON. Example: {{"analysis": [{{"email_index": 0, "urgency": "HIGH", "reasoning": "text"}}], "most_urgent_index": 0}}"""
        
        llm_response = call_llm_api(analysis_prompt)
        
        if llm_response:
            try:
                # Extract JSON from LLM response
                json_start = llm_response.find("{")
                json_end = llm_response.rfind("}") + 1
                if json_start >= 0 and json_end > json_start:
                    analysis_data = json.loads(llm_response[json_start:json_end])
                    
                    # Process each email with LLM analysis
                    for idx, email in enumerate(SAMPLE_EMAILS):
                        # Tool 1: Parse email
                        parse_result = {
                            "id": email["id"],
                            "from": email["from"],
                            "subject": email["subject"],
                            "body": email["body"][:100] + "...",
                            "timestamp": email["timestamp"]
                        }
                        log_jsonrpc_call("parse_email", {"email_id": email["id"]}, parse_result)
                        
                        # Get LLM analysis for this email
                        email_analysis = next(
                            (a for a in analysis_data.get("analysis", []) if a.get("email_index") == idx),
                            {"urgency": "MEDIUM", "category": "inquiry"}
                        )
                        
                        # Tool 2: Analyze sentiment (LLM-based)
                        sentiment_result = {
                            "email_id": email["id"],
                            "sentiment": email_analysis.get("urgency", "MEDIUM").lower(),
                            "reasoning": email_analysis.get("reasoning", ""),
                            "urgency_score": {"HIGH": 3, "MEDIUM": 2, "LOW": 1}.get(
                                email_analysis.get("urgency", "MEDIUM"), 2
                            )
                        }
                        log_jsonrpc_call("analyze_sentiment", {"email_id": email["id"]}, sentiment_result)
                        
                        # Tool 3: Categorize
                        category = email_analysis.get("category", "inquiry")
                        categorize_result = {
                            "email_id": email["id"],
                            "category": category,
                            "priority": email_analysis.get("urgency", "MEDIUM")
                        }
                        log_jsonrpc_call("categorize_email", {"email_id": email["id"]}, categorize_result)
                        
                        results.append({
                            "email": email,
                            "sentiment": email_analysis.get("urgency", "MEDIUM").lower(),
                            "category": category,
                            "priority": email_analysis.get("urgency", "MEDIUM"),
                            "reasoning": email_analysis.get("reasoning", "")
                        })
                    
                    # Find most urgent
                    most_urgent_idx = analysis_data.get("most_urgent_index", 0)
                    if 0 <= most_urgent_idx < len(results):
                        most_urgent = results[most_urgent_idx]
                    else:
                        most_urgent = max(results, key=lambda x: (
                            x["priority"] == "HIGH",
                            x["priority"] == "MEDIUM"
                        ))
                    
                    return {
                        "all_emails": results,
                        "most_urgent": most_urgent["email"],
                        "urgency_level": most_urgent["priority"],
                        "reasoning": most_urgent.get("reasoning", ""),
                        "mode": "llm"
                    }
            except (json.JSONDecodeError, KeyError, IndexError):
                pass  # Fall through to rule-based analysis
    
    # Fallback: Rule-based analysis (query-aware)
    query_lower = query.lower() if query else ""
    
    for email in SAMPLE_EMAILS:
        # Tool 1: Parse email
        parse_result = {
            "id": email["id"],
            "from": email["from"],
            "subject": email["subject"],
            "body": email["body"][:100] + "...",
            "timestamp": email["timestamp"]
        }
        log_jsonrpc_call("parse_email", {"email_id": email["id"]}, parse_result)
        
        # Tool 2: Analyze sentiment (keyword-based + query-aware)
        email_text = (email["subject"] + " " + email["body"]).lower()
        sentiment = "low"
        
        # If query mentions specific topics, match those
        if query_lower:
            if "rag" in query_lower and "rag" in email_text:
                sentiment = "medium"
            elif "website" in query_lower and "website" in email_text:
                sentiment = "high"
            elif "database" in query_lower and ("database" in email_text or "connection" in email_text):
                sentiment = "high"
            elif "document" in query_lower:
                # For document queries, prioritize feature request (RAG email)
                if "rag" in email_text:
                    sentiment = "high"
                elif any(word in email_text for word in ["urgent", "critical", "immediate", "down"]):
                    sentiment = "high"
        
        # Default behavior when no specific query
        if sentiment == "low":
            if any(word in email_text for word in ["urgent", "critical", "immediate", "down"]):
                sentiment = "high"
            elif any(word in email_text for word in ["question", "help", "resource", "rag"]):
                sentiment = "medium"
        
        sentiment_result = {
            "email_id": email["id"],
            "sentiment": sentiment,
            "urgency_keywords": ["urgent", "critical", "immediate"] if sentiment == "high" else []
        }
        log_jsonrpc_call("analyze_sentiment", {"email_id": email["id"]}, sentiment_result)
        
        # Tool 3: Categorize
        category = "technical_issue" if sentiment == "high" else "inquiry"
        categorize_result = {
            "email_id": email["id"],
            "category": category,
            "priority": "HIGH" if sentiment == "high" else "MEDIUM" if sentiment == "medium" else "LOW"
        }
        log_jsonrpc_call("categorize_email", {"email_id": email["id"]}, categorize_result)
        
        results.append({
            "email": email,
            "sentiment": sentiment,
            "category": category,
            "priority": categorize_result["priority"]
        })
    
    # Find most urgent (query-aware selection)
    if query_lower and "document" in query_lower:
        # If asking for documents, prefer RAG email since it has doc guidance
        most_urgent = next(
            (r for r in results if "rag" in r["email"]["body"].lower()),
            max(results, key=lambda x: (x["priority"] == "HIGH", x["sentiment"] == "high"))
        )
    elif query_lower and "website" in query_lower:
        # If asking about website, select website email
        most_urgent = next(
            (r for r in results if "website" in r["email"]["body"].lower()),
            max(results, key=lambda x: (x["priority"] == "HIGH", x["sentiment"] == "high"))
        )
    else:
        # Default: select HIGH priority or highest urgency
        most_urgent = max(results, key=lambda x: (x["priority"] == "HIGH", x["sentiment"] == "high"))
    
    return {
        "all_emails": results,
        "most_urgent": most_urgent["email"],
        "urgency_level": most_urgent["priority"],
        "mode": "keyword_fallback"
    }


def search_solution_docs(urgent_email: Dict[str, str], query: str = "") -> Dict[str, Any]:
    """
    STEP (b): Search internal knowledge base for solution.
    Uses knowledge tools: extract_keywords → search_knowledge → get_document
    
    With LLM API: Uses Claude to semantically match email to best docs.
    Without LLM API: Falls back to keyword matching.
    """
    llm_available = os.getenv("OPENROUTER_API_KEY") is not None
    keywords = []
    
    if llm_available:
        # LLM-powered keyword extraction
        extract_prompt = f"""Extract 3-5 key technical terms from this email for knowledge base search.
Email Subject: {urgent_email['subject']}
Email Body: {urgent_email['body']}

Output ONLY valid JSON: {{"keywords": ["term1", "term2"], "topics": ["topic1", "topic2"]}}"""
        
        llm_response = call_llm_api(extract_prompt)
        if llm_response:
            try:
                json_start = llm_response.find("{")
                json_end = llm_response.rfind("}") + 1
                if json_start >= 0 and json_end > json_start:
                    extracted = json.loads(llm_response[json_start:json_end])
                    keywords = extracted.get("keywords", []) + extracted.get("topics", [])
            except (json.JSONDecodeError, KeyError):
                pass  # Fall back to keyword matching below
    
    # If LLM didn't extract keywords, use rule-based extraction
    if not keywords:
        body_lower = urgent_email["body"].lower()
        if "database" in body_lower or "connection" in body_lower:
            keywords = ["database", "connection", "troubleshooting"]
        elif "website" in body_lower or "down" in body_lower:
            keywords = ["website", "deployment", "infrastructure"]
        elif "rag" in body_lower:
            keywords = ["rag", "retrieval", "generation"]
        else:
            keywords = ["system", "architecture", "guide"]
    
    # Tool 1: Extract keywords
    extract_result = {
        "email_subject": urgent_email["subject"],
        "extracted_keywords": keywords,
        "method": "llm" if llm_available and keywords else "keyword_matching"
    }
    log_jsonrpc_call("extract_keywords", {"email": urgent_email["subject"]}, extract_result)
    
    # Tool 2: Search knowledge base (LLM-assisted if available)
    search_query = " ".join(keywords)
    matching_docs = []
    
    if llm_available:
        # LLM-powered document relevance scoring
        docs_text = "\n\n".join([
            f"Document: {name}\nContent preview:\n{content[:200]}..."
            for name, content in SAMPLE_DOCS.items()
        ])
        
        ranking_prompt = f"""Given this customer email issue, rank which documents would be most helpful.
Email Issue: {urgent_email['subject']}
Email Description: {urgent_email['body']}

Available Documents:
{docs_text}

Output ONLY valid JSON: {{"ranked_documents": ["doc1.md", "doc2.md"], "reasoning": "explanation"}}"""
        
        llm_response = call_llm_api(ranking_prompt)
        if llm_response:
            try:
                json_start = llm_response.find("{")
                json_end = llm_response.rfind("}") + 1
                if json_start >= 0 and json_end > json_start:
                    ranking = json.loads(llm_response[json_start:json_end])
                    matching_docs = [d for d in ranking.get("ranked_documents", []) if d in SAMPLE_DOCS]
            except (json.JSONDecodeError, KeyError):
                pass  # Fall back to keyword matching
    
    # Fallback: keyword-based matching
    if not matching_docs:
        for doc_name, doc_content in SAMPLE_DOCS.items():
            if any(keyword.lower() in doc_content.lower() for keyword in keywords):
                matching_docs.append(doc_name)
    
    search_result = {
        "query": search_query,
        "matches_found": len(matching_docs),
        "matching_documents": matching_docs,
        "method": "llm_ranking" if llm_available else "keyword_matching"
    }
    log_jsonrpc_call("search_knowledge", {"query": search_query}, search_result)
    
    # Tool 3: Get most relevant document
    if matching_docs:
        doc_name = matching_docs[0]
        doc_content = SAMPLE_DOCS.get(doc_name, "")
        get_result = {
            "document": doc_name,
            "content_preview": doc_content[:300] + "..."
        }
        log_jsonrpc_call("get_document", {"filename": doc_name}, get_result)
        
        return {
            "relevant_doc": doc_name,
            "content": doc_content,
            "keywords_used": keywords,
            "method": "llm_ranking" if llm_available else "keyword_matching"
        }
    
    return {"relevant_doc": None, "content": "", "keywords_used": keywords, "method": "not_found"}


def process_urgent_issue_request(query: str) -> tuple:
    """
    Main workflow: 2-step issue resolution.
    Returns: (email_response, docs_response) as separate formatted strings
    Uses query parameter to filter and select relevant emails dynamically.
    """
    # STEP (a): Email Analysis
    email_analysis = analyze_emails_for_urgency(query)
    urgent_email = email_analysis["most_urgent"]
    
    email_response = f"""**Most Urgent Issue Found:**

📧 **From:** {urgent_email['from']}
📋 **Subject:** {urgent_email['subject']}
⏰ **Priority:** {email_analysis['urgency_level']}
📝 **Message:** {urgent_email['body']}"""
    
    # STEP (b): Knowledge Search
    solution = search_solution_docs(urgent_email, query)
    
    if solution["relevant_doc"]:
        docs_response = f"""**Relevant Documentation Found:**

📄 **Document:** `{solution['relevant_doc']}`
🔑 **Keywords Matched:** {', '.join(solution['keywords_used'])}

**Recommended Solution:**
```
{solution['content'][:500]}
```"""
    else:
        docs_response = f"""**Documentation Status:**

ℹ️ No specific documentation found for this issue.
🔑 **Keywords Searched:** {', '.join(solution['keywords_used'])}

**Recommendation:** Consider adding documentation to your knowledge base for:
- Issue: {urgent_email['subject']}
- Keywords: {', '.join(solution['keywords_used'])}"""
    
    return (email_response, docs_response)


# ============================================================================
# STATE MANAGEMENT
# ============================================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "toolkit" not in st.session_state:
    st.session_state.toolkit = None

if "json_rpc_logs" not in st.session_state:
    st.session_state.json_rpc_logs = []

if "last_submitted" not in st.session_state:
    st.session_state.last_submitted = None

# ============================================================================
# MAIN UI LAYOUT
# ============================================================================

st.title("🔧 MCP Toolkit - Urgent Issue Resolution")
st.markdown("""
**Real-World Scenario:** Find and resolve urgent customer issues
  
1. **Step (a):** System analyzes multiple customer emails using email tools (parse, analyze_sentiment, categorize)
2. **Step (b):** Based on the urgent issue, system searches internal knowledge base using knowledge tools (extract_keywords, search_knowledge, get_document)

Try asking: *"What's our most urgent customer issue?"*
""")

# Accordion for scenario architecture
with st.expander("📚 Scenario Architecture & Tools", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Email Tools Used:**")
        st.markdown("""
- `parse_email()` - Structure email data
- `analyze_sentiment()` - Detect urgency
- `categorize_email()` - Classify issue type
""")
    with col2:
        st.markdown("**Knowledge Tools Used:**")
        st.markdown("""
- `extract_keywords()` - Identify solution topics
- `search_knowledge()` - Find relevant docs
- `get_document()` - Retrieve full content
""")
    st.markdown("**Workflow Pattern:** Parse → Analyze → Categorize → Extract → Search → Retrieve")
    
    st.markdown("---")
    st.markdown("**Test with Your Own Documents:**")
    st.markdown(f"""
To test with custom knowledge documents:
1. Add `.md` files to: `{Path(__file__).parent}/knowledge/`
2. Add sample emails to `SAMPLE_EMAILS` in this script
3. Re-run the app to load new documents

Example document: `database-troubleshooting.md`
```markdown
# Database Connection Issues

## Quick Fix
1. Check connection pool settings
2. Review error logs
3. Restart service if needed
```
""")
    
    st.markdown("**LLM Processing Status:**")
    llm_key = os.getenv("OPENROUTER_API_KEY")
    if llm_key:
        st.success("✅ LLM API enabled (OPENROUTER_API_KEY found)")
        st.markdown("""Real LLM-powered processing active:
- Email urgency analysis using OpenRouter (GPT-3.5-turbo)
- Intelligent document ranking and matching
- Semantic understanding instead of keyword matching
- Multi-turn conversation support with reasoning
""")
    else:
        st.warning("⚠️ LLM API not configured (OPENROUTER_API_KEY not found)")
        st.markdown("Falling back to rule-based keyword matching. To enable LLM processing:")
        st.code("export OPENROUTER_API_KEY='your-key-here'\nstreamlit run lesson-06-mcp-toolkit-chat.py", language="bash")
        st.markdown("""
Benefits of LLM mode:
- Understand urgency beyond keywords
- Match emails to docs by meaning, not just keywords
- Provide reasoning for decisions
- Support follow-up questions naturally
""")
    
    st.markdown("---")
    st.markdown("**Get OpenRouter API Key:**")
    st.markdown("Visit https://openrouter.ai/ and create an account to get your API key")

# Initialize toolkit
toolkit = initialize_toolkit()

# Main chat area (full width)
st.subheader("💬 Issue Resolution Chat")

# Display chat history with proper Streamlit chat interface
st.subheader("💬 Chat")

chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        if message["type"] == "status":
            st.info(message["content"])
        else:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

# Chat Input
st.divider()
user_input = st.chat_input("What's our most urgent email issue? Or search for documents...", key="chat_input")

if user_input and user_input != st.session_state.last_submitted:
    # Add user message to history
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "type": "user"
    })
    
    # Classify the intent
    intent = classify_message_intent(user_input)
    
    if intent == "email_search":
        # INTENT: User asking about emails, urgent issues
        # Use email analysis tool ONLY (not automatic document search)
        
        # Show analyzing status
        with st.chat_message("assistant"):
            st.info("🤖 Analyzing customer emails...")
        
        # Get email analysis only
        email_analysis = analyze_emails_for_urgency(user_input)
        urgent_email = email_analysis["most_urgent"]
        
        email_response = f"""**Email Found:**

📧 **From:** {urgent_email['from']}
📋 **Subject:** {urgent_email['subject']}
⏰ **Priority:** {email_analysis['urgency_level']}
📝 **Message:** {urgent_email['body']}"""
        
        # Add email analysis result
        st.session_state.messages.append({
            "role": "assistant",
            "content": email_response,
            "type": "assistant"
        })
    
    elif intent == "knowledge_search":
        # INTENT: User asking for documentation or solutions
        # Use document search tool only (standalone, not dependent on email)
        
        with st.chat_message("assistant"):
            st.info("🤖 Searching knowledge base...")
        
        # Search documents based on the user's query
        # Create a minimal email object just for search context
        query_email = {
            "id": "user_query",
            "subject": "User Query",
            "body": user_input
        }
        
        solution = search_solution_docs(query_email, user_input)
        
        if solution["relevant_doc"]:
            docs_response = f"""**Relevant Documentation Found:**

📄 **Document:** `{solution['relevant_doc']}`
🔑 **Keywords Matched:** {', '.join(solution['keywords_used'])}

**Content:**
```
{solution['content'][:500]}
```"""
        else:
            docs_response = f"""**Documentation Status:**

ℹ️ No documentation found matching your query.
🔑 **Keywords Searched:** {', '.join(solution['keywords_used'])}

**Tip:** Try asking about specific topics like "database", "website", or "RAG" to find relevant documentation."""
        
        st.session_state.messages.append({
            "role": "assistant",
            "content": docs_response,
            "type": "assistant"
        })
    
    else:
        # INTENT: General chat - use LLM for normal response
        
        with st.chat_message("assistant"):
            st.info("🤖 Thinking...")
        
        # Build chat context from history
        chat_messages = []
        for msg in st.session_state.messages:
            if msg["type"] != "status":
                chat_messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
        
        # Prepare system prompt
        system_prompt = """You are a helpful AI assistant. Answer questions directly and concisely.
You have access to customer email analysis and document search tools, but only use them when the user explicitly asks about urgent issues or wants documentation.
For general questions, just provide a helpful answer."""
        
        # Call LLM for general chat
        user_prompt = f"User query: {user_input}\n\nProvide a helpful, concise answer."
        llm_response = call_llm_api(user_prompt, system_prompt)
        
        if llm_response:
            response = llm_response
        else:
            response = f"I'd be happy to help! However, I need an API key to provide a full response. For now, I can tell you that '{user_input}' is a great question. Feel free to ask about urgent issues or search for documentation using the tools available."
        
        st.session_state.messages.append({
            "role": "assistant",
            "content": response,
            "type": "assistant"
        })
    
    st.session_state.last_submitted = user_input
    st.rerun()

# JSON-RPC Logs at bottom (full width, tabbed)
if len(st.session_state.json_rpc_logs) > 0:
    st.markdown("---")
    st.subheader("🔍 JSON-RPC Protocol Logs")
    
    # Group logs by tool
    tools_dict = {}
    for log_entry in st.session_state.json_rpc_logs:
        tool = log_entry['tool']
        if tool not in tools_dict:
            tools_dict[tool] = []
        tools_dict[tool].append(log_entry)
    
    # Create tabs
    tab_names = [f"📤 {tool} ({len(logs)})" for tool, logs in tools_dict.items()] + ["📥 Export", "🗑️ Clear"]
    tabs = st.tabs(tab_names)
    
    # Display logs in tabs
    for idx, (tool, logs) in enumerate(tools_dict.items()):
        with tabs[idx]:
            for log_entry in logs:
                with st.expander(f"{tool} - {log_entry['timestamp']}", expanded=False):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**Request:**")
                        st.json(log_entry['request'])
                    with col2:
                        st.markdown("**Response:**")
                        st.json(log_entry['response'])
    
    # Export tab
    with tabs[-2]:
        logs_json = json.dumps(st.session_state.json_rpc_logs, indent=2)
        st.download_button(
            label="Download All Logs (JSON)",
            data=logs_json,
            file_name="jsonrpc_logs.json",
            mime="application/json"
        )
    
    # Clear tab
    with tabs[-1]:
        if st.button("Clear All Logs", use_container_width=True, type="secondary"):
            st.session_state.json_rpc_logs = []
            st.rerun()
else:
    st.markdown("---")
    st.info("💡 JSON-RPC logs will appear here as you interact with the toolkit")

st.markdown("---")
st.caption("""
**Learning Flow:** CLI Demo 1 (Toolkit Base) > CLI Demo 2 (Workflows & Security) > This Streamlit UI (Real-Time Interaction)

Inspect JSON-RPC messages to understand how MCP clients communicate with servers!
""")
