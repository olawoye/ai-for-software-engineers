"""
Lesson 6.6: Multi-Agent Collaboration (Capstone) - Streamlit Dashboard

This lesson demonstrates how multiple specialized agents coordinate on complex
business processes through a shared toolkit and real-time Streamlit dashboard.

Business Scenario:
  Marketing campaign orchestration with 4 specialized agents:
  - Campaign Manager: Overall strategy
  - Content Agent: Material creation
  - Analytics Agent: Metrics and analysis
  - Customer Service Agent: Customer interaction

Run: streamlit run lesson-06-multi-agent-collaboration.py
Requires: export OPENROUTER_API_KEY='your-key-here'
"""

import os
import sys
import json
from pathlib import Path
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent))
from shared.agent import Agent


# ============================================================================
# STREAMLIT PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="Multi-Agent Collaboration",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🤖 Multi-Agent Collaboration: Marketing Campaign Orchestration")

st.markdown("""
This lesson demonstrates how specialized agents coordinate on complex business processes.
Each agent has distinct capabilities, but they share tools, coordinate actions, and learn from collective experience.

**Scenario:** Marketing Campaign Orchestration
- 4 specialized agents working together
- Shared toolkit and memory
- Real-time dashboard showing agent state
""")


# ============================================================================
# AGENT SETUP
# ============================================================================

class AgentRole(Enum):
    """Agent roles in the system."""
    MANAGER = "Campaign Manager"
    CONTENT = "Content Agent"
    ANALYTICS = "Analytics Agent"
    SERVICE = "Customer Service Agent"


def get_agents():
    """Get or create agent instances."""
    # Don't use cache to avoid issues with partial initialization
    agents = {}
    
    agent_specs = [
        (AgentRole.MANAGER, "CampaignManager"),
        (AgentRole.CONTENT, "ContentAgent"),
        (AgentRole.ANALYTICS, "AnalyticsAgent"),
        (AgentRole.SERVICE, "CustomerServiceAgent"),
    ]
    
    for role, name in agent_specs:
        try:
            agent = Agent(name=name, use_memory=True)
            agents[role] = agent
        except Exception as e:
            st.error(f"Failed to initialize {name}: {str(e)}")
            raise
    
    return agents


# ============================================================================
# SYSTEM CONTROL (MAIN AREA)
# ============================================================================

# Check API key
if not os.getenv("OPENROUTER_API_KEY"):
    st.error("❌ OPENROUTER_API_KEY not set. Export it before running: export OPENROUTER_API_KEY='your-key'")
    st.stop()

st.success("✅ API key configured")

# Controls layout
col1, col2, col3 = st.columns(3)

with col1:
    scenario = st.selectbox(
        "📋 Select Scenario:",
        ["Campaign Strategy Review", "Content Creation", "Analytics Report", "Customer Feedback", "Full Workflow"]
    )

with col2:
    if st.button("🔄 Clear Memory"):
        st.session_state.clear()
        st.rerun()

with col3:
    st.write("")
    st.write("")
    if st.button("ℹ️ How to Use"):
        st.info("""\n**How to Use:**\n1. Select a scenario from the dropdown\n2. Click 'Execute' button in Tab 2\n3. Watch agents reason and respond""")

st.divider()


# ============================================================================
# TAB 1: MULTI-AGENT SYSTEM STATE
# ============================================================================

tab1, tab2, tab3, tab4 = st.tabs(
    ["System State", "Agent Reasoning", "Execution History", "Documentation"]
)

with tab1:
    st.header("Multi-Agent System State")
    
    agents = get_agents()
    
    # Agent status grid
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Campaign Manager")
        st.info("""
        **Role:** Overall strategy and coordination
        **Status:** Idle → Planning → Executing → Complete
        **Tools:** Task assignment, decision-making
        """)
    
    with col2:
        st.subheader("Content Agent")
        st.info("""
        **Role:** Marketing material creation
        **Status:** Idle → Analyzing Brief → Creating → Complete
        **Tools:** Template generation, content synthesis
        """)
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("Analytics Agent")
        st.info("""
        **Role:** Metrics and insight analysis
        **Status:** Idle → Querying → Analyzing → Complete
        **Tools:** Metric calculation, trend detection
        """)
    
    with col4:
        st.subheader("Customer Service Agent")
        st.info("""
        **Role:** Customer interaction and feedback
        **Status:** Idle → Reading Feedback → Responding → Complete
        **Tools:** Sentiment analysis, categorization
        """)
    
    # Execution timeline
    st.subheader("Execution Timeline")
    st.write("""
    Campaign workflow execution order:
    1. **Manager** → Reviews strategy and creates task list
    2. **Content** → Creates marketing materials (parallel with Analytics)
    3. **Analytics** → Analyzes campaign metrics (parallel with Content)
    4. **Service** → Handles customer feedback and responds
    5. **Manager** → Synthesizes results and next steps
    """)


# ============================================================================
# TAB 2: AGENT REASONING
# ============================================================================

with tab2:
    st.header("Agent Reasoning & LLM Integration")
    
    try:
        agents = get_agents()
        
        # Debug: Show agent initialization status
        with st.expander("🔍 Agent Status", expanded=False):
            st.write(f"Total agents initialized: {len(agents)}")
            for role, agent in agents.items():
                st.write(f"✅ {role.value}: {agent.name}")
        
        if st.button(f"🚀 Execute: {scenario}", key="execute_scenario"):
            st.session_state.current_scenario = scenario
            st.session_state.execution_time = datetime.now()
            st.rerun()
        
        if "current_scenario" in st.session_state:
            scenario_name = st.session_state.current_scenario
            st.subheader(f"Executing: {scenario_name}")
            st.divider()
            
            if scenario_name == "Campaign Strategy Review":
                with st.spinner("Campaign Manager reviewing strategy..."):
                    manager = agents.get(AgentRole.MANAGER)
                    if not manager:
                        available = [r.value for r in agents.keys()] if agents else "none"
                        st.error(f"❌ Manager agent not found. Available: {available}")
                        st.stop()
                    
                    manager.learn_fact("campaign_budget", "$50,000")
                    manager.learn_fact("campaign_duration", "Q4 2024")
                    manager.learn_relationship("campaign", "targets", "enterprise_customers")
                    
                    query = "Review the Q4 campaign strategy and create an action plan. Budget: $50k, Target: Enterprise customers."
                    response = manager.reason_with_memory(
                        query,
                        system_prompt="You are a strategic campaign manager. Provide a structured plan.",
                        include_context=True,
                        temperature=0.7
                    )
                    
                    st.success("✅ Campaign Manager Response:")
                    st.write(response)
                    
                    manager.memory.episodic.record_episode(
                        manager.name,
                        "strategy_review",
                        {"description": "Q4 campaign strategy review", "outcome": "plan_created"}
                    )
            
            elif scenario_name == "Content Creation":
                with st.spinner("Content Agent creating materials..."):
                    content = agents.get(AgentRole.CONTENT)
                    if not content:
                        available = [r.value for r in agents.keys()] if agents else "none"
                        st.error(f"❌ Content agent not found. Available: {available}")
                        st.stop()
                    
                    content.learn_fact("brand_voice", "professional and approachable")
                    content.learn_fact("target_audience", "Enterprise IT decision makers")
                    
                    query = "Create marketing copy for enterprise customers. Brand voice: professional and approachable. Include value proposition."
                    response = content.reason_with_memory(
                        query,
                        system_prompt="You are a creative marketing copywriter. Generate compelling content.",
                        include_context=True,
                        temperature=0.8
                    )
                    
                    st.success("✅ Content Agent Response:")
                    st.write(response)
                    
                    content.memory.episodic.record_episode(
                        content.name,
                        "content_creation",
                        {"description": "Marketing copy creation", "outcome": "draft_created"}
                    )
            
            elif scenario_name == "Analytics Report":
                with st.spinner("Analytics Agent analyzing metrics..."):
                    analytics = agents.get(AgentRole.ANALYTICS)
                    if not analytics:
                        available = [r.value for r in agents.keys()] if agents else "none"
                        st.error(f"❌ Analytics agent not found. Available: {available}")
                        st.stop()
                    
                    analytics.learn_fact("prior_conversion_rate", "3.2%")
                    analytics.learn_fact("campaign_reach", "50,000 impressions")
                    
                    query = "Analyze campaign performance. Prior conversion: 3.2%, Reach: 50k impressions. Provide insights and recommendations."
                    response = analytics.reason_with_memory(
                        query,
                        system_prompt="You are a data analyst. Provide actionable insights from metrics.",
                        include_context=True,
                        temperature=0.6
                    )
                    
                    st.success("✅ Analytics Agent Response:")
                    st.write(response)
                    
                    analytics.memory.episodic.record_episode(
                        analytics.name,
                        "analysis",
                        {"description": "Campaign performance analysis", "outcome": "insights_generated"}
                    )
            
            elif scenario_name == "Customer Feedback":
                with st.spinner("Customer Service Agent processing feedback..."):
                    service = agents.get(AgentRole.SERVICE)
                    if not service:
                        available = [r.value for r in agents.keys()] if agents else "none"
                        st.error(f"❌ Service agent not found. Available: {available}")
                        st.stop()
                    
                    service.learn_fact("avg_response_time", "2 hours")
                    
                    sample_feedback = "Great product! But setup was confusing. Would recommend with better docs."
                    query = f"Customer feedback: '{sample_feedback}'. Analyze sentiment and generate response."
                    response = service.reason_with_memory(
                        query,
                        system_prompt="You are a customer service specialist. Acknowledge feedback and provide helpful response.",
                        include_context=True,
                        temperature=0.7
                    )
                    
                    st.success("✅ Customer Service Agent Response:")
                    st.write(response)
                    
                    service.memory.episodic.record_episode(
                        service.name,
                        "feedback_handling",
                        {"description": "Customer feedback response", "outcome": "resolved"}
                    )
            
            elif scenario_name == "Full Workflow":
                st.info("Running full multi-agent workflow...")
                
                progress = st.progress(0)
                
                agents_to_run = [
                    (AgentRole.MANAGER, "Campaign Manager", "Review strategy and plan execution"),
                    (AgentRole.CONTENT, "Content Agent", "Create marketing materials"),
                    (AgentRole.ANALYTICS, "Analytics Agent", "Analyze performance"),
                    (AgentRole.SERVICE, "Customer Service Agent", "Handle customer feedback"),
                ]
                
                results = {}
                for i, (role, name, task) in enumerate(agents_to_run):
                    agent = agents.get(role)
                    if not agent:
                        st.error(f"Agent {name} ({role}) not found")
                        st.stop()
                    
                    with st.spinner(f"{name}: {task}..."):
                        response = agent.reason_with_memory(
                            f"Task: {task}. Provide update.",
                            system_prompt=f"You are a {name}.",
                            include_context=True,
                            temperature=0.7
                        )
                        results[name] = response
                        progress.progress((i + 1) / len(agents_to_run))
                
                st.success("✅ Full Workflow Complete!")
                
                for name, response in results.items():
                    st.subheader(name)
                    st.write(response[:300] + "...")
    
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        import traceback
        with st.expander("Debug Info"):
            st.code(traceback.format_exc())


# ============================================================================
# TAB 3: EXECUTION HISTORY
# ============================================================================

with tab3:
    st.header("Execution History & Learning")
    
    try:
        agents = get_agents()
        
        # Agent selection
        selected_agent_name = st.selectbox(
            "Select Agent:",
            ["Campaign Manager", "Content Agent", "Analytics Agent", "Customer Service Agent"]
        )
        
        # Map to agent role
        agent_role_map = {
            "Campaign Manager": AgentRole.MANAGER,
            "Content Agent": AgentRole.CONTENT,
            "Analytics Agent": AgentRole.ANALYTICS,
            "Customer Service Agent": AgentRole.SERVICE,
        }
        
        role = agent_role_map[selected_agent_name]
        
        if role not in agents:
            st.error(f"Agent {selected_agent_name} not found in agents dictionary. Available: {list(agents.keys())}")
            st.stop()
        
        agent = agents[role]
        
        # Memory summary
        st.subheader(f"Memory for {selected_agent_name}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Long-Term Facts:**")
            facts = agent.memory.semantic.get_all_facts(agent.name)
            if facts:
                for k, v in list(facts.items())[:5]:
                    st.write(f"- {k}: {v}")
            else:
                st.write("(No facts recorded)")
        
        with col2:
            st.write("**Episodes:**")
            episodes = agent.memory.episodic.get_episodes(agent.name, limit=5)
            if episodes:
                for ep in episodes:
                    st.write(f"- {ep['type']}: {ep['content'].get('description', 'N/A')[:50]}...")
            else:
                st.write("(No episodes recorded)")
    
    except Exception as e:
        st.error(f"Error in Execution History tab: {e}")
        st.info("Please ensure OPENROUTER_API_KEY is set and try again.")


# ============================================================================
# TAB 4: DOCUMENTATION
# ============================================================================

with tab4:
    st.header("Lesson Documentation")
    
    st.subheader("Learning Goals")
    st.write("""
    1. ✅ Design multi-agent architectures with specialization
    2. ✅ Implement coordination strategies (hierarchy, voting, market-based)
    3. ✅ Manage shared resource access across agents
    4. ✅ Handle agent communication and task assignment
    5. ✅ Learn from shared episodic memory
    6. ✅ Scale from single-agent to multi-agent systems
    """)
    
    st.subheader("Key Concepts")
    st.write("""
    - **Agent Specialization:** Each agent focuses on specific domain/role
    - **Shared Memory:** Agents learn from collective experience
    - **Tool Access Management:** Controlled access to shared resources
    - **Coordination:** Making decisions when agents have different preferences
    - **Communication:** Async message passing between agents
    - **Learning:** Storing coordination history for future improvement
    """)
    
    st.subheader("Architecture")
    st.write("""
    ```
    User Input (Campaign Task)
           ↓
    Campaign Manager (Orchestrator)
           ↓
    ┌──────┼──────┬──────────┐
    ↓      ↓      ↓          ↓
    Content  Analytics  Service  (Specialist Agents)
    ↓      ↓      ↓          ↓
    └──────┼──────┴──────────┘
           ↓
    Shared Memory (SQLite + JSONL)
           ↓
    Results & Learning
    ```
    """)
    
    st.subheader("Run Instructions")
    st.code("""
export OPENROUTER_API_KEY='your-key-here'
streamlit run lesson-06-multi-agent-collaboration.py
    """, language="bash")
