# Module 3: AI Developer Toolkit

This module bridges the gap between understanding AI and building AI-powered software. Learn how to integrate LLM APIs into applications, rapidly prototype solutions, build user-facing interfaces, and deploy production-ready services using modern developer tooling.

By the end of this module, students will be able to transform an AI idea into a functioning application, deploy it to the cloud, and establish development patterns that will be reused throughout the course.

## Module Overview

**Learning Path:**
1. **Lesson 3.1** (Talking Head): Conceptual foundation for moving from API calls to product
2. **Lesson 3.2** (Code): Direct API integration patterns with multiple providers
3. **Lesson 3.3** (Code): Rapid prototyping using Streamlit
4. **Lesson 3.4** (Code): Building conversational interfaces
5. **Lesson 3.5** (Code): DevOps, deployment, and operational concerns
6. **Lesson 3.6** (Code): Capstone — Deploy a complete summarization service

## Lessons

### Lesson 3.1: From API Call to Product
**Type:** Talking Head (No Code)

Conceptual introduction to the journey from raw LLM API calls to production software.

---

### Lesson 3.2: Calling LLM APIs (Python)
**Type:** Code Screencast  
**Status:** ✅ Complete

**Interactive learning:** Menu-driven script with 5 real API patterns. Students choose patterns, see live API responses, understand token costs, then copy patterns into their projects.

#### Run Instructions
```bash
# Ensure virtual environment is active
source .venv/bin/activate

# Set your API key (OpenRouter is free-friendly)
export OPENROUTER_API_KEY='your-key-here'

# Run the interactive menu
python lesson-02-calling-llm-apis.py
```

**What You'll Learn (5 Patterns):**

1. **Basic Synchronous Call** — Simple completion, response parsing, timing
   - How to initialize LLMClient
   - Making a completion request
   - Measuring latency and token usage

2. **Provider Switching** — Same code, different models (GPT-3.5, GPT-4, Claude)
   - Testing multiple models with identical code
   - Understanding trade-offs (speed, cost, quality)
   - Choosing the right model for your use case

3. **Temperature Effect** — Precise vs Creative responses
   - Temperature 0.3 (deterministic)
   - Temperature 0.7 (balanced)
   - Temperature 0.9 (creative/random)
   - When to use each setting

4. **Real-World Use Case** — Text classification
   - Structuring classification prompts
   - Processing multiple items
   - Production pattern for categorization

5. **Error Handling** — What can go wrong
   - API key validation
   - Graceful error messages
   - Try/except patterns
   - User-friendly error recovery

**Learning Approach:**
- ✅ Interactive menu - students choose what to explore
- ✅ Real API calls - see actual responses from OpenRouter
- ✅ Code displayed with line numbers - easy to copy patterns
- ✅ Metrics shown - latency, tokens, estimated cost
- ✅ Customization guidance - "edit line X to change..."
- ✅ Return to menu - experiment with different patterns

**Key Files:**
- `lesson-02-calling-llm-apis.py` — Interactive menu-driven script
- `shared/llm_client.py` — Reusable LLM client (OpenRouter wrapper)
- `shared/config.py` — Model definitions and temperature constants
- `shared/prompts.py` — Reusable prompt templates

**Code Marker Format Used:**
```python
# >>> CUSTOMIZE: What to change and why
variable = "default_value"

# >>> CONFIGURE: Setup/environment section
config_key = os.getenv("SETTING")

# >>> REFERENCE: Just showing how it's used (don't change)
result = function(variable)
```

**Expected Output Example:**
```
══════════════════════════════════════════════════
PATTERN 2: Provider Switching - Same Code, Different Models
══════════════════════════════════════════════════

📝 Code:
  1 | from shared.llm_client import LLMClient
  2 |
  3 | # >>> CUSTOMIZE: Model choices
  4 | models = ["gpt-3.5-turbo", "claude-3-sonnet"]
  ...

🔄 Running with multiple models...

✓ gpt-3.5-turbo (0.89s):
  "Retrieval-Augmented Generation combines retrieval..."
  
✓ claude-3-sonnet (1.23s):
  "RAG is a technique that augments LLMs with..."

✅ Pattern complete. Return to menu.
```

**Student Workflow:**
1. Run script with valid API key
2. See interactive menu with 5 patterns
3. Choose a pattern to learn
4. View code with line numbers
5. Press ENTER to run real API call
6. See actual response and metrics
7. Read guidance: "To customize, edit line X"
8. Return to menu to try another pattern

---

### Lesson 3.3: Rapid Prototyping with Streamlit
**Type:** Code Screencast  
**Status:** ✅ Complete

Learn how Streamlit dramatically reduces the effort required to build AI applications. Connect user inputs, AI services, and outputs into functioning prototypes in minutes instead of weeks.

#### Run Instructions
```bash
source .venv/bin/activate
export OPENROUTER_API_KEY='your-key-here'
streamlit run lesson-03-rapid-prototyping.py
```

**What You'll Learn (3 Interactive Modes):**

1. **Text Classification** — Categorize any text into predefined categories
   - Example: sentiment analysis, support ticket routing, intent detection
   - Pre-filled examples for quick testing
   - Customizable category selection
   - Live API call with response metrics

2. **Text Summarization** — Reduce long documents to key points
   - Example: news articles, meeting notes, customer feedback
   - Example buttons for instant testing
   - 2-3 bullet point summaries
   - Response timing and token metrics

3. **Question & Answer** — Ask questions about documents
   - Example: company policy, FAQ, research papers
   - Two-column layout (document + question)
   - Context-aware responses
   - Example buttons (Policy, FAQ)

**Key Features:**
- **Sidebar configuration:** Model selector, temperature slider (0.0-1.0), max tokens slider (50-500)
- **Session state management:** Persist settings and user inputs across interactions
- **Code comparison:** Shows "Traditional Python (50+ lines)" vs "Streamlit (10 lines)" for each mode
- **Real API calls:** Live responses from OpenRouter, not mock data
- **Metrics display:** Response time and settings for each call
- **Pre-filled examples:** Buttons to quickly test with sample data

**Architecture:**
- `st.session_state` persists model/temperature/max_tokens across app reruns
- Three independent modes via `st.radio()` for easy switching
- `st.expander()` sections for learning explanations and code comparisons
- `st.spinner()` for user feedback during API calls
- Real-time metrics displayed with `st.metric()` and `st.columns()`

**Key Files:**
- `lesson-03-rapid-prototyping.py` — Full Streamlit web application
- `shared/llm_client.py` — LLM client for API calls
- `shared/config.py` — Model definitions and temperature constants

**Code Marker Format (for reference):**
```python
# >>> CUSTOMIZE: Things you should change (prompts, examples, parameters)
categories = ["Positive", "Negative", "Neutral"]

# >>> REFERENCE: How the code is used (don't change)
response = client.complete(prompt, temperature=0.7)
```

**Expected Workflow:**
1. Run script with valid API key
2. Streamlit app loads in browser at http://localhost:8501
3. Sidebar shows configuration options
4. Select a mode (Classification/Summarization/Q&A)
5. Click example button OR paste your own text
6. Adjust model, temperature, max_tokens in sidebar as needed
7. Click action button (Classify/Summarize/Get Answer)
8. See response and metrics
9. Expand code comparison to understand efficiency vs traditional approaches

**Deployment:**
Deploy to Streamlit Cloud in 3 clicks:
```bash
# 1. Commit to GitHub
git add .
git commit -m "Add Streamlit rapid prototyping app"
git push

# 2. Visit streamlit.io/cloud
# 3. Connect GitHub repo → Select branch → Deploy
```

---

### Lesson 3.6: AI Operations Assistant with Tool Calling
**Type:** Code Screencast (Capstone)  
**Status:** ✅ Complete

Learn how LLMs orchestrate actions through tool calling. This capstone introduces the paradigm shift from text generation to action orchestration—the foundation for agents, MCP, and autonomous systems.

#### Run Instructions
```bash
source .venv/bin/activate
export OPENROUTER_API_KEY='your-key-here'
streamlit run lesson-06-ai-operations-assistant.py
```

**The Core Concept:**

```
User Input
    ↓
LLM Decides What Tool to Use
    ↓
Tool Selection & Execution
    ↓
Result Processing
    ↓
Intelligent Response
```

**What You'll Learn:**

1. **Function Calling** — How LLMs decide which tools to use
2. **Tool Orchestration** — Safely executing tools based on LLM decisions
3. **Structured Outputs** — Parsing tool calls from LLM responses
4. **Tool Execution Engine** — Running tools and handling results
5. **Result Integration** — Using tool results to generate final responses
6. **The Paradigm Shift** — "LLMs don't just generate text—they orchestrate actions"

**5 Functional Tool Implementations:**

| Tool | Purpose | Pattern | 
|------|---------|---------|
| **Weather** | Get city weather | External API integration |
| **Ticket** | Look up support tickets | Database query pattern |
| **Policy** | Search company policies | Semantic search pattern |
| **SQL** | Execute read-only queries | Data analysis pattern |
| **Calculator** | Perform calculations | Expression evaluation |

**Key Architecture:**

- **Tool Registry:** Centralized TOOLS dict with definitions
- **Tool Context:** System prompt describing available tools
- **Tool Call Detection:** Regex parsing of `<tool_call>...</tool_call>` format
- **Safe Execution:** Error handling, validation, dangerous command blocking
- **Result Injection:** Feed tool results back to LLM for context-aware responses
- **Analytics Dashboard:** Track tool usage, success rates, execution times

**Real-World Workflow:**

1. **User:** "Look up ticket TKT-001"
2. **LLM:** "I'll call the ticket tool to help you"
3. **Response:** `<tool_call>ticket(ticket_id=TKT-001)</tool_call>`
4. **System:** Executes tool, gets `{status: "open", priority: "high"}`
5. **LLM Again:** "Ticket TKT-001 is open with high priority..."
6. **User:** Sees tool call, result, and intelligent response

**Why This Matters (Strategic Context):**

This lesson is the **bridge between application building and agent systems**:

- **Modules 3.1-3.5:** Build AI applications (UI, chat, deployment)
- **Lesson 3.6:** Demonstrate LLM orchestration (tool calling)
- **Module 5:** Standardize tool access (MCP servers)
- **Module 6:** Autonomous decision-making (agents)
- **Modules 7-8:** System design and operations at scale

Students completing Lesson 3.6 understand that modern AI isn't just about generating text—it's about orchestrating complex workflows where LLMs make decisions and take actions.

**Key Files:**

- `lesson-06-ai-operations-assistant.py` — Full Streamlit assistant with tool calling
- `shared/llm_client.py` — LLM client for API calls
- `shared/config.py` — Model definitions and temperature constants

**Code Markers (for reference):**

```python
# >>> REFERENCE: Why this matters (educational)
# This tells the LLM what tools it can use and how to call them.

# >>> REFERENCE: Implementation details
# Don't change, but understand why this pattern is used.
```

**Expected Interaction:**

```
User: "What's the weather in San Francisco?"
LLM: [thinks] "I need weather information"
Response: <tool_call>weather(city=San Francisco)</tool_call>
System: Executes tool → {temp: 65, condition: "sunny"}
LLM: [responds using result]
Output: "The weather in San Francisco is sunny, 65°F"
```

**Learning Outcomes:**

After this lesson, students will understand:
- ✅ How function calling works
- ✅ How LLMs make tool selection decisions
- ✅ How to safely execute external tools
- ✅ How to use tool results in responses
- ✅ Why tool orchestration is the foundation for agents
- ✅ The paradigm: "LLMs orchestrate actions"

**Production Considerations (Demonstrated):**

- Parameter validation
- Error handling and graceful failures
- Dangerous command blocking (SQL safety)
- Tool execution tracking
- Result integrity checking
- Safety guardrails

**Deployment:**

Fully deployable using Lesson 3.5 patterns:
- Docker-ready
- Environment variable configuration
- Cloud platform compatible
- Production error handling

**Next Steps After This Lesson:**

Students are now ready for:
- **Module 4:** RAG systems (using tools to access knowledge bases)
- **Module 5:** MCP servers (standardizing tool protocols)
- **Module 6:** AI agents (autonomous tool selection)
- **Modules 7-8:** Production AI systems

---
**Type:** Code Screencast  
**Status:** ✅ Complete

Learn how to build multi-turn conversational AI interfaces with context management. Master state persistence, conversation history, and context window constraints—all with a clean, real-world UI.

#### Run Instructions
```bash
source .venv/bin/activate
export OPENROUTER_API_KEY='your-key-here'
streamlit run lesson-04-building-chat-interface.py
```

**What You'll Learn:**

1. **State Management** — How `st.session_state` persists conversation history across Streamlit reruns
2. **Multi-turn Context** — Building conversation memory within token limits without context overflow
3. **Message Formatting** — Proper role-based message structure (system/user/assistant)
4. **Token Budget Management** — Dropping oldest messages when context window gets full
5. **System Prompts** — Controlling assistant behavior and personality through code
6. **Real-world UX** — Clean interface focusing on message display + input (NOT developer knobs)

**Key Architecture:**

- **Session State:** `st.session_state.messages` stores `[{"role": "user/assistant", "content": "..."}]`
- **Context Window:** Respects model limits (GPT-3.5: 4k, GPT-4: 8k/128k, Claude: 100k+)
- **Conversation Memory:** Keeps recent messages, drops old ones to stay under token budget
- **System Prompt:** Editable in code (line 30) to customize assistant personality
- **Error Handling:** Graceful failures—removes user message if API call fails

**Real-world UI Components Only:**
- ✅ Message display container
- ✅ Text input field + send button
- ✅ Clear conversation button
- ✅ Clean, focused interface

**Developer Settings (Code Comments):**
- `CHAT_MODEL` (line 21) — Switch models for cost/quality tradeoffs
- `SYSTEM_PROMPT` (line 25) — Define assistant behavior
- `MAX_CONTEXT_TOKENS` (line 35) — Token limit before dropping old messages
- `TEMPERATURE` (line 41) — Precision (0.3) vs creativity (0.9)
- Helper functions with detailed comments explaining token management

**Key Files:**
- `lesson-04-building-chat-interface.py` — Full Streamlit chat application
- `shared/llm_client.py` — LLM client for API calls
- `shared/config.py` — Model definitions and temperature constants

**Code Marker Format (for reference):**
```python
# >>> CUSTOMIZE: Things you can change (model, system prompt, token limits)
CHAT_MODEL = "gpt-3.5-turbo"

# >>> REFERENCE: Implementation details (don't change, but understand why)
context_messages = build_context_for_api(st.session_state.messages)
```

**Expected Workflow:**
1. Run script with valid API key
2. Streamlit app loads with clean message interface
3. Type message and click Send
4. App adds to history, calls API, displays response
5. Conversation persists across reruns (this is `st.session_state` at work)
6. Clear button resets conversation
7. Expand dev panels to understand token management and system prompts

**Production Considerations (documented but out of scope):**
- User authentication (who owns this conversation?)
- Database persistence (save conversations across sessions)
- Rate limiting (prevent abuse)
- Cost tracking (monitor API spending)
- Moderation (block harmful content)

---

### Lesson 3.5: DevOps for AI Apps
**Type:** Code Screencast (Interactive CLI)  
**Status:** ✅ Complete

Learn deployment strategies, environment management, and operational concerns. Move from "it works on my machine" to "it works in production."

#### Run Instructions
```bash
source .venv/bin/activate
export OPENROUTER_API_KEY='your-key-here'
python lesson-05-devops-for-ai-apps.py
```

**What You'll Learn (6 Topics):**

1. **Pre-Deployment Checklist** — Validate setup before deploying
   - API keys configured
   - Dependencies installed
   - Network connectivity verified

2. **Environment Variables** — Manage secrets safely
   - Never commit secrets to git
   - Use .env files locally
   - Expose environment variables in production
   - Platform-specific guidance (Streamlit Cloud, Railway, GCP, etc.)

3. **Docker Containerization** — Ensure apps run identically everywhere
   - Multi-stage Docker build (optimized image size)
   - Dockerfile best practices
   - docker-compose.yml for local testing
   - Health checks for production

4. **Platform Comparison** — Choose the right deployment option
   - **Streamlit Cloud** ($0 free) — 1-click GitHub deploy, best for learning
   - **Railway.app** ($5/month) — Simple PaaS, Docker support, recommended
   - **Digital Ocean App Platform** ($12+/month) — Predictable costs, reliable
   - **Digital Ocean Droplets** ($4-6/month) — Budget option, full control
   - **GCP Cloud Run** ($0-5/month) — Scales to 0, pay-per-request
   - **AWS Lambda/EC2** ($0-50+/month) — Most powerful, complex
   - **Vercel** ($0-20/month) — NOT recommended for Streamlit

5. **Deployment Instructions** — Step-by-step for each platform
   - Platform-specific workflows
   - Time estimates
   - Cost breakdown
   - Configuration examples

6. **Production Patterns** — Avoid common failure modes
   - Error handling (try/except, retries, graceful messages)
   - Monitoring (health checks, error rates, metrics)
   - Security (no secrets in git, input validation, rate limiting)
   - Performance (caching, timeouts, load testing)
   - Logging (structured, persistent, alerting)

**Key Features:**
- Interactive CLI flow (ENTER to advance through each section)
- Pre-deployment validation (API keys, dependencies, network)
- Environment template generation (.env.example)
- Docker templates (Dockerfile + docker-compose)
- Platform comparison with pros/cons
- Platform-specific deployment instructions
- Production best practices guide

**Architecture:**

- **PHASE 1:** Validation (checklist functions)
- **PHASE 2:** Configuration management (.env templates, Docker)
- **PHASE 3:** Deployment guidance (platform comparison, instructions, patterns)

**Key Files:**
- `lesson-05-devops-for-ai-apps.py` — Interactive DevOps walkthrough
- Generated outputs: `.env.example`, `Dockerfile`, `docker-compose.yml`

**Deployment Options Summary:**

| Platform | Cost | Ease | Best For |
|----------|------|------|----------|
| Streamlit Cloud | $0 | ⭐⭐⭐⭐⭐ | Learning |
| Railway.app | $5+/mo | ⭐⭐⭐⭐ | Production (recommended) |
| Digital Ocean App | $12+/mo | ⭐⭐⭐⭐ | Reliability |
| Digital Ocean Droplets | $4-6/mo | ⭐⭐ | Budget |
| GCP Cloud Run | $0-5/mo | ⭐⭐⭐ | Scalable |
| AWS | $0-50+/mo | ⭐ | Enterprise |

**Expected Workflow:**
1. Run script with valid API key
2. Pass pre-deployment checks (or fix issues)
3. Review environment variable template
4. See Docker templates (copy to your project)
5. Compare platform options
6. Select platform and view deployment instructions
7. Review production patterns
8. Execute deployment steps on chosen platform

**After This Lesson:**
- ✅ Understand pre-deployment validation
- ✅ Can manage secrets safely
- ✅ Know how to containerize Python apps
- ✅ Can choose appropriate deployment platform
- ✅ Ready to deploy AI apps to production
- ✅ Understand operational best practices

---

### Lesson 3.6: Deploy a Mini AI Service (Capstone)
**Type:** Code Screencast  
**Status:** ✅ Complete

Build, package, deploy, and validate a production-ready AI summarization service.

#### Run Instructions
```bash
source .venv/bin/activate
export OPENROUTER_API_KEY='your-key-here'
streamlit run lesson-06-ai-summarizer-service.py
```

**What You'll Learn:**
- Combine all Module 3 concepts into one application
- Implement business logic (SummarizationService class)
- Add request tracking and analytics
- Handle errors and edge cases
- Deploy complete AI service

**Features:**
- Document summarization in multiple languages
- Service statistics and request history
- Error tracking and logging
- Model selection and parameter tuning
- Production-ready architecture

**Output:** Deployable summarization service

---

## Shared Resources

All lessons leverage utilities in `shared/`:

- **`llm_client.py`** — Unified LLM client supporting OpenRouter, Anthropic, OpenAI, etc.
- **`config.py`** — Model definitions, temperature constants, context limits
- **`prompts.py`** — Reusable prompt templates for classification, summarization, chat

## Setup & Dependencies

### First-Time Setup (Required Once)
```bash
# Create clean virtual environment
rm -rf .venv
./setup.sh
source .venv/bin/activate

# Install Module 3 dependencies (lightweight, ~20MB base)
pip install -r requirements-module-03.txt
```

**First run:** Lessons are instant (cloud-based APIs, no downloads needed).

### API Key Setup
```bash
# Sign up at openrouter.io (free, supports 100+ models)
export OPENROUTER_API_KEY='your-key-here'

# Verify setup
python lesson-02-calling-llm-apis.py
```

### Available Models (via OpenRouter)
- GPT-3.5 Turbo
- GPT-4
- Claude 3 Sonnet
- Claude 3 Opus

---

## Module Progression

```
API Integration
      ↓
Rapid Prototyping
      ↓
Chat Interfaces
      ↓
DevOps & Deployment
      ↓
Complete Service
```

---

## Recommended Project Timeline

| Lesson | Time | Focus |
|--------|------|-------|
| 3.2 | 45 min | API calls, provider switching |
| 3.3 | 45 min | Streamlit rapid prototyping |
| 3.4 | 45 min | Chat interface patterns |
| 3.5 | 45 min | Deployment and DevOps |
| 3.6 | 90 min | Capstone: Build, test, deploy |

**Total:** ~4-5 hours of hands-on development

---

## Next Steps

After completing Module 3:
- ✅ You can build AI applications quickly
- ✅ You understand API integration patterns
- ✅ You can deploy to production
- ✅ You're ready for Module 4: **Practical RAG & Context Engineering**

In Module 4, you'll learn how to build RAG systems that let your AI applications reason over proprietary knowledge using the deployment patterns established here.

---

## Reference

- Full curriculum: `docs/curriculum_v1.md`
- Agent instructions: `agents.md`
- Architecture guide: `docs/architecture.md`
