"""
Memory Management System for AI Agents using SQLite + JSONL

Provides persistent memory layers for agents:
- Semantic Memory: Facts, relationships, knowledge (SQLite for queries)
- Episodic Memory: Past interactions and events (JSONL for append-only history)
- Tool Call History: LLM tool invocations and results (JSONL log)

Students learn: structured memory (SQL) vs temporal logs (JSONL)
"""

import sqlite3
import json
from pathlib import Path
from typing import List, Dict, Optional, Any
from datetime import datetime
import threading


class SemanticMemory:
    """Structured facts and relationships stored in SQLite.
    
    Schema:
        - facts: agent_name, key, value, timestamp
        - relationships: agent_name, subject, predicate, object, timestamp
    """
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.lock = threading.Lock()
        self._init_db()
    
    def _init_db(self):
        """Initialize SQLite tables if they don't exist."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS facts (
                    id INTEGER PRIMARY KEY,
                    agent_name TEXT,
                    key TEXT,
                    value TEXT,
                    timestamp TEXT,
                    UNIQUE(agent_name, key)
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS relationships (
                    id INTEGER PRIMARY KEY,
                    agent_name TEXT,
                    subject TEXT,
                    predicate TEXT,
                    object TEXT,
                    timestamp TEXT
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS short_term (
                    id INTEGER PRIMARY KEY,
                    agent_name TEXT,
                    content TEXT,
                    timestamp TEXT
                )
            """)
            conn.commit()
    
    def add_fact(self, agent_name: str, key: str, value: str):
        """Store a fact (overwrites if exists)."""
        with self.lock:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    "INSERT OR REPLACE INTO facts (agent_name, key, value, timestamp) VALUES (?, ?, ?, ?)",
                    (agent_name, key, value, datetime.now().isoformat())
                )
                conn.commit()
    
    def get_fact(self, agent_name: str, key: str) -> Optional[str]:
        """Retrieve a fact by key."""
        with self.lock:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    "SELECT value FROM facts WHERE agent_name = ? AND key = ?",
                    (agent_name, key)
                )
                row = cursor.fetchone()
                return row[0] if row else None
    
    def get_all_facts(self, agent_name: str) -> Dict[str, str]:
        """Get all facts for an agent."""
        with self.lock:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    "SELECT key, value FROM facts WHERE agent_name = ? ORDER BY timestamp DESC",
                    (agent_name,)
                )
                return {row[0]: row[1] for row in cursor.fetchall()}
    
    def add_relationship(self, agent_name: str, subject: str, predicate: str, obj: str):
        """Store a relationship (subject -[predicate]-> object)."""
        with self.lock:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    "INSERT INTO relationships (agent_name, subject, predicate, object, timestamp) VALUES (?, ?, ?, ?, ?)",
                    (agent_name, subject, predicate, obj, datetime.now().isoformat())
                )
                conn.commit()
    
    def get_relationships(self, agent_name: str, subject: str = None) -> List[Dict]:
        """Get relationships, optionally filtered by subject."""
        with self.lock:
            with sqlite3.connect(self.db_path) as conn:
                if subject:
                    cursor = conn.execute(
                        "SELECT subject, predicate, object, timestamp FROM relationships WHERE agent_name = ? AND subject = ? ORDER BY timestamp DESC",
                        (agent_name, subject)
                    )
                else:
                    cursor = conn.execute(
                        "SELECT subject, predicate, object, timestamp FROM relationships WHERE agent_name = ? ORDER BY timestamp DESC",
                        (agent_name,)
                    )
                return [
                    {"subject": row[0], "predicate": row[1], "object": row[2], "timestamp": row[3]}
                    for row in cursor.fetchall()
                ]
    
    def add_short_term(self, agent_name: str, content: str):
        """Add to short-term memory (conversational context)."""
        with self.lock:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    "INSERT INTO short_term (agent_name, content, timestamp) VALUES (?, ?, ?)",
                    (agent_name, content, datetime.now().isoformat())
                )
                conn.commit()
    
    def get_short_term(self, agent_name: str, limit: int = 5) -> List[str]:
        """Get recent short-term memory entries."""
        with self.lock:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    "SELECT content FROM short_term WHERE agent_name = ? ORDER BY timestamp DESC LIMIT ?",
                    (agent_name, limit)
                )
                return [row[0] for row in cursor.fetchall()]
    
    def clear_short_term(self, agent_name: str):
        """Clear short-term memory (e.g., session end)."""
        with self.lock:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("DELETE FROM short_term WHERE agent_name = ?", (agent_name,))
                conn.commit()


class EpisodicMemory:
    """Temporal log of episodes (interactions, events) using JSONL.
    
    Append-only log where each line is a JSON object representing an episode.
    Enables fast appends and iterative reading.
    """
    
    def __init__(self, log_path: str):
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.log_path.exists():
            self.log_path.touch()
        self.lock = threading.Lock()
    
    def record_episode(self, agent_name: str, episode_type: str, content: Dict[str, Any]):
        """Append episode to JSONL log."""
        episode = {
            "timestamp": datetime.now().isoformat(),
            "agent_name": agent_name,
            "type": episode_type,
            "content": content,
        }
        with self.lock:
            with open(self.log_path, "a") as f:
                f.write(json.dumps(episode) + "\n")
    
    def get_episodes(self, agent_name: str, episode_type: str = None, limit: int = 10) -> List[Dict]:
        """Retrieve episodes, optionally filtered by type."""
        episodes = []
        with self.lock:
            with open(self.log_path, "r") as f:
                for line in f:
                    if not line.strip():
                        continue
                    episode = json.loads(line)
                    if episode["agent_name"] == agent_name:
                        if episode_type is None or episode["type"] == episode_type:
                            episodes.append(episode)
        
        # Return most recent episodes
        return sorted(episodes, key=lambda x: x["timestamp"], reverse=True)[:limit]
    
    def get_summary(self, agent_name: str) -> str:
        """Summarize recent episodes for context."""
        episodes = self.get_episodes(agent_name, limit=3)
        if not episodes:
            return "[No episode history]"
        
        summary = f"Recent interactions ({len(episodes)} total):\n"
        for ep in episodes:
            summary += f"  - {ep['type']}: {ep['content'].get('description', 'N/A')}\n"
        return summary


class ToolCallHistory:
    """Append-only log of tool invocations and results."""
    
    def __init__(self, log_path: str):
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.log_path.exists():
            self.log_path.touch()
        self.lock = threading.Lock()
    
    def record_call(self, agent_name: str, tool_name: str, args: Dict, result: Dict, success: bool):
        """Log a tool call and its result."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "agent_name": agent_name,
            "tool_name": tool_name,
            "args": args,
            "result": result,
            "success": success,
        }
        with self.lock:
            with open(self.log_path, "a") as f:
                f.write(json.dumps(entry) + "\n")
    
    def get_calls(self, agent_name: str, tool_name: str = None, limit: int = 10) -> List[Dict]:
        """Retrieve tool calls, optionally filtered by tool name."""
        calls = []
        with self.lock:
            with open(self.log_path, "r") as f:
                for line in f:
                    if not line.strip():
                        continue
                    entry = json.loads(line)
                    if entry["agent_name"] == agent_name:
                        if tool_name is None or entry["tool_name"] == tool_name:
                            calls.append(entry)
        
        return sorted(calls, key=lambda x: x["timestamp"], reverse=True)[:limit]
    
    def get_success_rate(self, agent_name: str) -> float:
        """Calculate tool call success rate."""
        with self.lock:
            all_calls = []
            with open(self.log_path, "r") as f:
                for line in f:
                    if not line.strip():
                        continue
                    entry = json.loads(line)
                    if entry["agent_name"] == agent_name:
                        all_calls.append(entry)
        
        if not all_calls:
            return 0.0
        
        successful = sum(1 for call in all_calls if call["success"])
        return successful / len(all_calls)


class AgentMemoryManager:
    """Unified manager for all agent memory types."""
    
    def __init__(self, agent_name: str, db_dir: str = "./agent_memory"):
        self.agent_name = agent_name
        self.db_dir = Path(db_dir)
        self.db_dir.mkdir(parents=True, exist_ok=True)
        
        db_path = str(self.db_dir / "agent_memory.db")
        episodes_log = str(self.db_dir / f"{agent_name}_episodes.jsonl")
        calls_log = str(self.db_dir / f"{agent_name}_tool_calls.jsonl")
        
        self.semantic = SemanticMemory(db_path)
        self.episodic = EpisodicMemory(episodes_log)
        self.tool_calls = ToolCallHistory(calls_log)
    
    def get_context_for_reasoning(self, num_short_term: int = 5, num_episodes: int = 3) -> str:
        """Prepare memory context for LLM reasoning."""
        context = ""
        
        # Short-term memory
        short_term = self.semantic.get_short_term(self.agent_name, limit=num_short_term)
        if short_term:
            context += f"## Recent Context\n{chr(10).join(f'- {item}' for item in short_term)}\n\n"
        
        # Long-term facts
        facts = self.semantic.get_all_facts(self.agent_name)
        if facts:
            context += f"## Known Facts\n{chr(10).join(f'- {k}: {v}' for k, v in list(facts.items())[:5])}\n\n"
        
        # Recent episodes
        episodes = self.episodic.get_episodes(self.agent_name, limit=num_episodes)
        if episodes:
            context += f"## Recent History\n{chr(10).join(f'- {ep['type']}: {ep['content'].get('description', 'N/A')}' for ep in episodes)}\n\n"
        
        return context if context else "[No prior context]"
