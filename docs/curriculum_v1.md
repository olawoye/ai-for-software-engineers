# AI For Software Engineers - Curriculum (Draft v1)

## Module 1: AI Shift for Engineers

**Module Slug:** `module-01-ai-shift-for-engineers`

### Module Objective

This module establishes the strategic foundation for the entire course by helping experienced software engineers understand why AI represents a platform shift comparable to the emergence of the internet, cloud computing, and mobile platforms. Rather than focusing on tools, students will learn how the role of the engineer is evolving and what skills remain valuable in an AI-first world.

By the end of this module, students will understand the major AI patterns used in modern software systems, the realities of AI engineering work, and how to create a practical roadmap for transitioning from traditional software development into AI-native engineering roles.

---

### Lesson 1.1: Why This Course Matters Now

**Type:** Talking Head

**Code File:** N/A

#### Lesson Objective

This lesson establishes the urgency behind AI adoption within software engineering. Students will examine how leading technology companies, researchers, and AI labs are reshaping engineering workflows through AI-assisted development and increasingly autonomous systems.

By the end of this lesson, students will understand why AI literacy is becoming a core engineering competency and why adapting early creates significant career advantages over waiting for industry-wide disruption.

#### Keywords

* AI transformation
* Future of software engineering
* AI-assisted development
* Industry disruption
* Career relevance
* Market shifts

---

### Lesson 1.2: AI at Work Today

**Type:** Talking Head

**Code File:** N/A

#### Lesson Objective

This lesson explores how AI is already being integrated into real-world software products and engineering workflows. Students will review modern AI application patterns including chat interfaces, retrieval systems, copilots, and autonomous agents.

By the end of this lesson, students will recognize that AI is no longer merely a development tool but increasingly acts as a software consumer and decision-making participant within modern applications.

#### Keywords

* Chat interfaces
* RAG systems
* Agents
* AI-native applications
* Voice interfaces
* AI as a client

---

### Lesson 1.3: Core AI Patterns

**Type:** Talking Head

**Code File:** N/A

#### Lesson Objective

This lesson introduces the most important architectural patterns that underpin modern AI systems. Students will learn how retrieval systems, chat interfaces, copilots, workflows, and agentic systems differ, where they are used, and what trade-offs exist between them.

By the end of this lesson, students will be able to identify common AI architectures in the wild and reason about when each pattern is appropriate for a particular business problem.

#### Keywords

* RAG
* Agents
* Copilots
* Human-in-the-loop
* Agentic loops
* Fine-tuning
* Context injection
* AI failure modes

---

### Lesson 1.4: AI Engineers at Work

**Type:** Talking Head

**Code File:** N/A

#### Lesson Objective

This lesson examines what AI engineers actually do on a day-to-day basis and how the role differs from traditional software engineering. Students will compare corporate AI teams, startups, SaaS builders, consultants, and freelance practitioners to understand the opportunities available in the AI economy.

By the end of this lesson, students will understand the practical workflows, tools, responsibilities, and product decisions that define modern AI engineering roles.

#### Keywords

* AI engineer workflow
* Corporate AI
* Freelance AI
* SaaS development
* Product-first mindset
* Cost vs latency vs quality

---

### Lesson 1.5: Mindset & Skills

**Type:** Talking Head

**Code File:** N/A

#### Lesson Objective

This lesson focuses on the mindset shifts required to thrive in an AI-assisted engineering environment. Students will learn why verification, systems thinking, experimentation, and orchestration are becoming more valuable than memorizing syntax or framework details.

By the end of this lesson, students will understand which technical and non-technical skills will remain durable and how to position themselves as high-leverage engineers in an AI-native future.

#### Keywords

* Systems thinking
* Verification mindset
* T-shaped skills
* Prompt engineering
* AI literacy
* Engineering leverage

---

### Lesson 1.6: Your AI Transition Plan

**Type:** Talking Head + Worksheet

**Code File:** N/A

#### Lesson Objective

This lesson helps students convert the concepts from the module into a personalized action plan. Students will assess their current skills, identify gaps, select a target outcome, and create a practical roadmap for achieving their desired AI-related career objective.

By the end of this lesson, students will leave with a documented transition strategy and a clear understanding of how the remaining modules support their long-term goals.

#### Keywords

* Self-assessment
* Career planning
* Learning roadmap
* Goal setting
* AI transition
* Skills audit

#### Deliverables

* Skills Assessment Worksheet
* AI Career Roadmap Template
* 90-Day Learning Plan
* Personal North Star Goal Definition




## Module 2: AI Fundamentals

**Module Slug:** `module-02-ai-fundamentals`

### Module Objective

This module establishes the technical foundation required for every subsequent module in the course. Students will develop a practical understanding of how modern Large Language Models work, how they process information, how context influences behavior, and how retrieval and embeddings enable AI systems to reason over proprietary knowledge.

By the end of this module, students will understand the core concepts that underpin RAG systems, agents, MCP tooling, fine-tuning, and production AI applications. Rather than treating AI as a black box, they will understand the major components and tradeoffs involved in modern AI systems.

---

### Lesson 2.1: LLMs Under the Hood

**Type:** Talking Head

**Repository Folder:** N/A

**Code File:** N/A

**Business Scenario:**
A company is evaluating AI solutions and needs engineers who can explain why models sometimes hallucinate, produce inconsistent outputs, or respond differently to similar prompts.

#### Lesson Objective

This lesson introduces Large Language Models from a software engineer's perspective. Students will learn what an LLM is, how it is trained at a high level, and how it generates outputs through pattern prediction rather than true reasoning.

By the end of this lesson, students will be able to explain common LLM behaviors and limitations without relying on oversimplified marketing explanations.

#### Keywords

- Large Language Models
- Training
- Inference
- Pattern prediction
- Hallucinations
- Attention
- Foundation models

---

### Lesson 2.2: Tokens, Context & Completion

**Type:** Code Screencast

**Repository Folder:** `module-02-ai-fundamentals`

**Code File:** `lesson-02-tokens-context-completion.py`

**Business Scenario:**
An AI application suddenly becomes expensive and starts producing poor answers because prompts exceed context limits and token consumption was never monitored.

#### Lesson Objective

This lesson explores how LLMs process text through tokens and how context windows constrain model behavior. Students will learn how prompts become completions and why token management is critical for cost, performance, and reliability.

By the end of this lesson, students will be able to estimate token usage, diagnose context-related failures, and design prompts that operate effectively within model limits.

#### Keywords

- Tokens
- Context windows
- Prompt completion
- Tokenization
- Token budgeting
- Cost management

---

### Lesson 2.3: Transformer Architecture

**Type:** Talking Head

**Repository Folder:** N/A

**Code File:** N/A

**Business Scenario:**
An engineering team must choose between traditional machine learning approaches and transformer-based systems for a document understanding platform.

#### Lesson Objective

This lesson provides a visual, intuitive explanation of transformer architecture and the self-attention mechanism. Students will learn why transformers revolutionized natural language processing and why nearly all modern AI systems are built upon them.

By the end of this lesson, students will understand how attention enables models to capture context and relationships across large bodies of text.

#### Keywords

- Transformers
- Self-attention
- Context awareness
- Neural networks
- Sequence modeling

---

### Lesson 2.4: Prompting, Retrieval & Fine-Tuning

**Type:** Code Screencast

**Repository Folder:** `module-02-ai-fundamentals`

**Code File:** `lesson-04-prompting-retrieval-finetuning.py`

**Business Scenario:**
A company wants an AI assistant to answer internal policy questions and must decide whether prompt engineering, RAG, or fine-tuning is the most cost-effective solution.

#### Lesson Objective

This lesson compares the three primary methods used to improve AI outputs: prompt engineering, retrieval-augmented generation, and fine-tuning. Students will learn where each approach excels and how to evaluate tradeoffs between complexity, cost, maintainability, and performance.

By the end of this lesson, students will be able to select the appropriate strategy for a given business problem rather than defaulting to a single solution.

#### Keywords

- Prompt engineering
- RAG
- Fine-tuning
- Tradeoffs
- Cost optimization
- Knowledge injection

---

### Lesson 2.5: Embeddings & Semantic Search

**Type:** Code Screencast

**Repository Folder:** `module-02-ai-fundamentals`

**Code File:** `lesson-05-embeddings-semantic-search.py`

**Business Scenario:**
A legal firm wants users to search thousands of contracts using natural language rather than exact keyword matches.

#### Lesson Objective

This lesson introduces embeddings and explains how semantic similarity enables AI systems to retrieve information based on meaning rather than exact wording. Students will generate embeddings, compare vectors, and explore how modern search systems work.

By the end of this lesson, students will understand how embeddings power search, recommendations, retrieval systems, and knowledge assistants.

#### Keywords

- Embeddings
- Vector representations
- Similarity search
- Semantic search
- Retrieval
- Vector databases

---

### Lesson 2.6: Build a Mini Search Demo

**Type:** Code Screencast

**Repository Folder:** `module-02-ai-fundamentals`

**Code File:** `lesson-06-mini-search-demo.py`

**Business Scenario:**
A consulting client needs a searchable knowledge repository that allows staff to quickly find information across company documents.

#### Lesson Objective

This lesson brings together tokens, embeddings, vector storage, and retrieval into a single working application. Students will build a semantic search tool capable of retrieving relevant information from a small document collection.

By the end of this lesson, students will have built their first complete AI-powered retrieval application and established the foundation for the RAG systems developed in Module 4.

#### Keywords

- Semantic search
- Embeddings
- Retrieval
- Vector storage
- Knowledge discovery
- Search systems

#### Deliverables

- Working semantic search application
- Python source code
- Search dataset
- Example queries




## Module 3: AI Developer Toolkit

**Module Slug:** `module-03-ai-developer-toolkit`

### Module Objective

This module bridges the gap between understanding AI and actually building AI-powered software. Students will learn how to integrate LLM APIs into applications, rapidly prototype solutions, build user-facing interfaces, and deploy production-ready services using modern developer tooling.

By the end of this module, students will be able to transform an AI idea into a functioning application, deploy it to the cloud, and establish the development patterns that will be reused throughout the remainder of the course.

---

### Lesson 3.1: From API Call to Product

**Type:** Talking Head

**Repository Folder:** N/A

**Code File:** N/A

**Business Scenario:**
A company wants to add AI-powered summarization, content generation, or support capabilities to an existing application. The engineering team must understand how to transform a simple API call into a product feature that delivers business value.

#### Lesson Objective

This lesson introduces the journey from raw LLM API calls to production software. Students will learn the core components required to transform a prompt-response interaction into a usable application feature, including user input, prompt orchestration, output handling, and application integration.

By the end of this lesson, students will understand the architectural building blocks behind AI-powered applications and be prepared to begin coding practical integrations.

#### Keywords

- LLM APIs
- Product development
- AI application architecture
- Prompt-response workflows
- User interactions
- AI features

---

### Lesson 3.2: Calling LLM APIs (Python)

**Type:** Code Screencast

**Repository Folder:** `module-03-ai-developer-toolkit`

**Code File:** `lesson-02-calling-llm-apis.py`

**Business Scenario:**
A software team must integrate multiple AI providers into a business application while maintaining flexibility, reliability, and portability.

#### Lesson Objective

This lesson teaches practical API integration patterns using Python and OpenRouter. Students will learn how to invoke modern LLMs, manage API credentials, handle responses, and compare synchronous versus asynchronous execution patterns.

By the end of this lesson, students will possess reusable implementation patterns that can be applied to almost any AI API integration project.

#### Keywords

- OpenRouter
- API integrations
- Async programming
- Request handling
- Response handling
- AI providers

#### Future Production Topics (Patched)

- Structured Outputs
- JSON Mode
- Schema Validation
- Pydantic Models
- Typed Responses

---

### Lesson 3.3: Rapid Prototyping Tools

**Type:** Code Screencast

**Repository Folder:** `module-03-ai-developer-toolkit`

**Code File:** `lesson-03-rapid-prototyping.py`

**Business Scenario:**
A client requests a proof-of-concept AI solution and expects a working demonstration within days rather than weeks.

#### Lesson Objective

This lesson demonstrates how modern tools such as Streamlit dramatically reduce the effort required to build AI applications. Students will rapidly connect user inputs, AI services, and outputs into a functioning prototype suitable for demonstrations and validation.

By the end of this lesson, students will understand how to move from idea to demo quickly while maintaining a foundation that can later evolve into a production application.

#### Keywords

- Streamlit
- Rapid prototyping
- MVP development
- Proof of concept
- AI applications
- Product validation

---

### Lesson 3.4: Building Chat Interfaces

**Type:** Code Screencast

**Repository Folder:** `module-03-ai-developer-toolkit`

**Code File:** `lesson-04-building-chat-interface.py`

**Business Scenario:**
A business wants a customer-facing AI assistant embedded into a web application to provide support, recommendations, or knowledge retrieval.

#### Lesson Objective

This lesson focuses on building a user-facing chat interface capable of sending prompts to an AI backend and displaying responses dynamically. Students will implement a simple frontend and understand how frontend and backend layers collaborate within AI-powered systems.

By the end of this lesson, students will be able to build conversational interfaces that form the foundation of many AI products.

#### Keywords

- Chat UI
- Frontend integration
- HTML
- JavaScript
- CSS
- Conversational interfaces

---

### Lesson 3.5: DevOps for AI Apps

**Type:** Talking Head + Code Screencast

**Repository Folder:** `module-03-ai-developer-toolkit`

**Code File:** `lesson-05-devops-for-ai-apps.py`

**Business Scenario:**
An internal AI tool has proven valuable and now needs to be deployed so employees or customers can access it reliably.

#### Lesson Objective

This lesson introduces deployment workflows and operational considerations for AI applications. Students will learn how to configure environments, manage secrets, package applications, and deploy services to modern cloud platforms.

By the end of this lesson, students will understand the complete journey from local development to publicly accessible AI applications.

#### Keywords

- Deployment
- Vercel
- Railway
- Fly.io
- Environment variables
- Docker
- Hosting

---

### Lesson 3.6: Deploy a Mini AI Service

**Type:** Code Screencast

**Repository Folder:** `module-03-ai-developer-toolkit`

**Code File:** `lesson-06-ai-summarizer-service.py`

**Business Scenario:**
A business needs an AI-powered service capable of processing and summarizing large amounts of information through a simple API endpoint.

#### Lesson Objective

This capstone project combines everything learned throughout the module into a complete AI application. Students will build, package, deploy, and validate a production-ready AI summarization service while applying API integration, backend development, and deployment principles.

By the end of this lesson, students will have independently delivered an end-to-end AI product and gained practical experience with full-stack AI application development.

#### Keywords

- AI services
- Summarization
- API development
- Deployment
- Backend engineering
- Product delivery

#### Deliverables

- GitHub Repository
- Live Deployment
- AI Summarization Service
- Deployment Configuration
- Environment Setup Documentation

#### Repository Assets

- `README.md`
- `.env.example`
- `requirements.txt`
- `Dockerfile`
- Deployment configuration

---

### Module 3 Repository Structure

```text
module-03-ai-developer-toolkit/
│
├── lesson-02-calling-llm-apis.py
├── lesson-03-rapid-prototyping.py
├── lesson-04-building-chat-interface.py
├── lesson-05-devops-for-ai-apps.py
├── lesson-06-ai-summarizer-service.py
│
├── shared/
│   ├── llm_client.py
│   ├── config.py
│   └── prompts.py
│
├── datasets/
│
└── assets/
```



## Module 4: Practical RAG & Context Engineering

**Module Slug:** `module-04-practical-rag-context-engineering`

### Module Objective

This module teaches engineers how to build Retrieval-Augmented Generation (RAG) systems that allow AI models to reason over proprietary knowledge. Students will progress from understanding RAG architecture through implementing embeddings, vector search, retrieval pipelines, optimization strategies, and ultimately a deployable knowledge assistant.

By the end of this module, students will be capable of designing, building, debugging, and optimizing production-grade RAG systems that deliver accurate, grounded responses using custom business data.

---

### Lesson 4.1: The RAG Blueprint

**Type:** Talking Head

**Repository Folder:** N/A

**Code File:** N/A

**Business Scenario:**
A company wants to build an internal AI assistant that can answer questions using company policies, documentation, contracts, and operational procedures rather than relying solely on the model's training data.

#### Lesson Objective

This lesson introduces Retrieval-Augmented Generation from a systems architecture perspective. Students will learn how user queries move through ingestion, retrieval, augmentation, and generation stages while understanding how chunking, embeddings, vector search, and prompt assembly work together.

By the end of this lesson, students will be able to sketch and reason about a complete RAG architecture before writing code and identify common failure points that affect retrieval quality.

#### Keywords

- RAG
- Retrieval-Augmented Generation
- Retrieval pipeline
- Chunking
- Embeddings
- Vector search
- Prompt assembly
- Context augmentation

---

### Lesson 4.2: Embedding Your Data

**Type:** Code Screencast

**Repository Folder:** `module-04-practical-rag-context-engineering`

**Code File:** `lesson-02-embedding-your-data.py`

**Business Scenario:**
A consulting client wants thousands of PDF documents transformed into searchable knowledge that can be used by an AI assistant.

#### Lesson Objective

This lesson focuses on building the ingestion layer of a RAG system. Students will learn how to prepare raw documents, chunk content appropriately, generate embeddings, and create a retrieval-ready knowledge base using Python.

By the end of this lesson, students will have implemented a practical ingestion pipeline capable of transforming proprietary information into searchable vector representations.

#### Keywords

- Data ingestion
- Text chunking
- Embeddings
- Document processing
- Knowledge preparation
- Semantic indexing

---

### Lesson 4.3: The Vector Store Lab

**Type:** Code Screencast

**Repository Folder:** `module-04-practical-rag-context-engineering`

**Code File:** `lesson-03-vector-store-lab.py`

**Business Scenario:**
An organization needs to search millions of records efficiently and retrieve the most relevant information based on meaning rather than keywords.

#### Lesson Objective

This lesson introduces vector databases and semantic retrieval. Students will store embeddings, build indexes, execute similarity searches, and compare retrieval results using tools such as FAISS or ChromaDB.

By the end of this lesson, students will understand how vector stores enable fast and scalable retrieval for modern AI applications.

#### Keywords

- Vector databases
- ChromaDB
- FAISS
- Similarity search
- Semantic retrieval
- Indexing
- Metadata filtering

---

### Lesson 4.4: Building the Pipeline

**Type:** Code Screencast

**Repository Folder:** `module-04-practical-rag-context-engineering`

**Code File:** `lesson-04-building-rag-pipeline.py`

**Business Scenario:**
A company wants employees to ask natural-language questions against internal documentation and receive grounded, source-backed answers.

#### Lesson Objective

This lesson assembles the complete RAG workflow. Students will connect retrieval, prompt construction, context augmentation, and LLM generation into a single end-to-end application using a custom PDF knowledge source.

By the end of this lesson, students will have a fully functional RAG system capable of answering questions using proprietary data.

#### Keywords

- RAG pipeline
- Retrieval
- Prompt construction
- LLM integration
- Context injection
- Knowledge assistants

---

### Lesson 4.5: RAG Optimization

**Type:** Code Screencast

**Repository Folder:** `module-04-practical-rag-context-engineering`

**Code File:** `lesson-05-rag-optimization.py`

**Business Scenario:**
A deployed knowledge assistant produces inconsistent answers because retrieval quality varies significantly across different queries and document types.

#### Lesson Objective

This lesson focuses on improving retrieval quality and overall system performance. Students will learn how to diagnose poor retrieval results and implement optimization techniques such as hybrid search, metadata filtering, query transformation, and reranking.

By the end of this lesson, students will be able to systematically improve accuracy and relevance in production RAG systems.

#### Keywords

- Hybrid search
- Metadata filtering
- Reranking
- Query expansion
- Retrieval quality
- Search optimization

#### Future Production Topics (Patched)

- Evaluation datasets
- Retrieval metrics
- Precision and Recall
- RAG regression testing
- Golden datasets
- Automated evaluation

---

### Lesson 4.6: Mini-App – Corporate Knowledge Bot

**Type:** Code Screencast

**Repository Folder:** `module-04-practical-rag-context-engineering`

**Code File:** `lesson-06-corporate-knowledge-bot.py`

**Business Scenario:**
An organization wants a deployable AI knowledge assistant capable of searching policies, procedures, documentation, and internal knowledge repositories.

#### Lesson Objective

This capstone project combines ingestion, embeddings, retrieval, storage, prompt assembly, and user interaction into a complete business application. Students will create a searchable knowledge assistant that demonstrates the practical value of RAG systems in real organizations.

By the end of this lesson, students will have built a deployable AI-powered knowledge bot suitable for extension into enterprise environments.

#### Keywords

- Knowledge assistant
- RAG application
- Enterprise search
- Internal knowledge systems
- Semantic retrieval
- AI copilots

#### Deliverables

- Corporate Knowledge Bot
- Source Code Repository
- Sample Knowledge Base
- Search Interface
- Retrieval Evaluation Examples

---

### Module 4 Repository Structure

```text
module-04-practical-rag-context-engineering/
│
├── lesson-02-embedding-your-data.py
├── lesson-03-vector-store-lab.py
├── lesson-04-building-rag-pipeline.py
├── lesson-05-rag-optimization.py
├── lesson-06-corporate-knowledge-bot.py
│
├── shared/
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── retriever.py
│   ├── prompts.py
│   └── rag_pipeline.py
│
├── datasets/
│   ├── company-handbook.pdf
│   ├── policies/
│   └── sample-documents/
│
├── evaluations/
│   ├── test_queries.json
│   └── expected_answers.json
│
└── assets/
```

### Module Progression

```text
RAG Architecture
        ↓
Document Ingestion
        ↓
Embeddings
        ↓
Vector Storage
        ↓
Retrieval
        ↓
Prompt Augmentation
        ↓
Generation
        ↓
Optimization
        ↓
Corporate Knowledge Assistant
```




## Module 5: Developing MCP Servers & Tooling
5.1 Introduction to MCP
5.2 JSON-RPC & Environments
5.3 Your First MCP Server
5.4 Connecting Real-World Tools
5.5 Debugging & Security
5.6 MCP Toolkit




## Module 6: AI Agents & Autonomy
6.1 Introduction to Agents & Architectures
6.2 Agent Memory Systems
6.3 Tool Use & Function Calling
6.4 Chaining, CoT & Pipelines
6.5 Building Autonomous Workflows
6.6 Multi-Agent Collaboration




## Module 7: Designing AI-Native Systems
7.1 Architectural Thinking & Application Patterns
7.2 Context Engineering
7.3 Design Patterns
7.4 Human-in-the-Loop Systems
7.5 Evaluation & Performance




## Module 8: Production AI Systems
8.1 Deployment Strategies
8.2 Security & Reliability
8.3 Observability, Monitoring & Logging
8.4 Scaling
8.5 Cost Optimization
8.6 Performance Evaluation




## Module 9: Advanced Capabilities & Specializations
9.1 Multimodal AI Systems
9.2 Fine-Tuning Models
9.3 Reinforcement Learning & RLHF
9.4 Mechanistic Interpretability
9.5 Ethical AI & Bias




## Module 10: Career Transition & Monetization
10.1 Career Paths
10.2 Building Your AI Portfolio
10.3 Building an AI SaaS App
10.4 Consulting & Freelancing
10.5 Research & Continuous Learning
