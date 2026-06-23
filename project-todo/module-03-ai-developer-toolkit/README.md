# Module 3: AI Developer Toolkit — TODO Scaffold

This is the student workbook version with phase-based scaffolding. Each lesson is marked with PHASE comments showing what to implement at each stage.

## Working Through the Lessons

### Lesson 3.2: Calling LLM APIs

**PHASE 1:** Implement basic synchronous API calls
- Create LLMClient and make simple requests
- Print responses with timing

**PHASE 2:** Provider switching and use cases
- Test multiple models
- Implement text classification example

**PHASE 3:** Advanced patterns
- Implement temperature comparison
- Add async pattern demonstration

### Lesson 3.3: Rapid Prototyping

**PHASE 1:** Basic Streamlit structure
- Set up page layout
- Add configuration sidebar

**PHASE 2:** Multiple application modes
- Implement text classification mode
- Implement summarization mode
- Implement Q&A mode

**PHASE 3:** Polish and error handling
- Add state management
- Add error messages
- Display key takeaways

### Lesson 3.4: Chat Interfaces

**PHASE 1:** Display and session state
- Set up Streamlit page
- Initialize message history
- Display previous messages

**PHASE 2:** User input handling
- Add chat input box
- Handle user submissions
- Store messages in session state

**PHASE 3:** Context management
- Build message context properly
- Call API with conversation history
- Add system prompt customization

### Lesson 3.5: DevOps for AI Apps

**PHASE 1:** Environment validation
- Check API keys are set
- Validate configuration

**PHASE 2:** Pre-deployment checklist
- Verify dependencies installed
- Test network connectivity
- Run all checks

**PHASE 3:** Deployment guides
- Show Docker templates
- Display deployment platform instructions

### Lesson 3.6: Capstone - Summarization Service

**PHASE 1:** Business logic
- Implement SummarizationService class
- Implement summarize() method
- Add history tracking

**PHASE 2:** User interface
- Build Streamlit layout
- Add configuration sidebar
- Add input/output areas
- Add action button

**PHASE 3:** Analytics and deployment
- Implement statistics calculation
- Add request history display
- Add deployment instructions

## Shared Modules to Complete

### shared/llm_client.py
- Implement __init__ (PHASE 1)
- Implement complete() (PHASE 2)
- Implement call() (PHASE 3)

### shared/config.py
- Define MODELS dict (PHASE 1)
- Add temperature constants (PHASE 2)
- Add get_api_key() function (PHASE 3)

### shared/prompts.py
- Define prompt templates (PHASE 1-2)
- Implement build_chat_context() (PHASE 3)

## Implementation Tips

1. **Start Simple**: Get PHASE 1 working before moving to later phases
2. **Test Each Phase**: Run your code after each phase
3. **Use the Completed Version**: Reference `project-completed/` if stuck
4. **API Key**: Always set `export OPENROUTER_API_KEY='your-key-here'`
5. **Error Messages**: Read them carefully—they usually point to the issue

## Running Your Code

### Prerequisites
```bash
source .venv/bin/activate
pip install -r requirements-module-03.txt
export OPENROUTER_API_KEY='your-key-here'
```

### Script Lessons
```bash
python lesson-02-calling-llm-apis.py
python lesson-05-devops-for-ai-apps.py
```

### Streamlit Lessons
```bash
streamlit run lesson-03-rapid-prototyping.py
streamlit run lesson-04-building-chat-interface.py
streamlit run lesson-06-ai-summarizer-service.py
```

## Common Issues

| Issue | Solution |
|-------|----------|
| `OPENROUTER_API_KEY not found` | Set API key: `export OPENROUTER_API_KEY='...'` |
| `ModuleNotFoundError: No module named 'streamlit'` | Install deps: `pip install -r requirements-module-03.txt` |
| `API request failed` | Check internet connection and API key validity |
| `syntax error on line X` | Check TODO comments—your implementation is incomplete |

## Learning Resources

- **Streamlit Docs**: streamlit.io/docs
- **OpenRouter**: openrouter.io/docs
- **Python async**: docs.python.org/3/library/asyncio.html
- **Complete Versions**: `project-completed/module-03-ai-developer-toolkit/`

## Next Steps

After completing Module 3, you'll understand how to:
- ✅ Call LLM APIs from Python
- ✅ Build interactive UIs with Streamlit
- ✅ Implement chat interfaces
- ✅ Deploy AI applications
- ✅ Create complete AI services

Ready for **Module 4: Practical RAG & Context Engineering**
