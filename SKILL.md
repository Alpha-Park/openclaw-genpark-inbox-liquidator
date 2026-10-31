---
name: openclaw-genpark-inbox-liquidator
description: OpenClaw GenPark Inbox Liquidator - Zero-inbox NLP action item and Eisenhower matrix triage engine with automated task extraction and reply drafting.
category: Service
version: 1.0.0
license: MIT
tools:
  - extract_action_items_and_deadlines
  - calculate_eisenhower_matrix
  - triage_and_route_email
---

# Openclaw Genpark Inbox Liquidator

## Overview & Agent Behavioral Directives
You are an autonomous agent specialized in **Openclaw Genpark Inbox Liquidator**.
Your primary directive is to execute: OpenClaw GenPark Inbox Liquidator - Zero-inbox NLP action item and Eisenhower matrix triage engine with automated task extraction and reply drafting.
Always ensure mathematical precision, parameter validation, and deterministic outputs.

## When to Activate This Skill
- Activate when an agent workflow or user instruction requires:
- `extract_action_items_and_deadlines`
- `calculate_eisenhower_matrix`
- `triage_and_route_email`
- Activate when operating in zero-dependency environments requiring pure Python standard library execution.

## How to Execute

### Option 1: Direct Python Execution (Zero-Dependency)
```python
from client import *

# Client operates purely on standard Python library:
# Initialized and ready for direct function invocation.
```

### Option 2: FastMCP Tool Calling
Tools registered in `mcp_server.py`:
- `extract_action_items_and_deadlines`
- `calculate_eisenhower_matrix`
- `triage_and_route_email`

## Core Mathematical & Algorithmic Guardrails
- **Zero-Dependency Policy**: 100% Python standard library only (`math`, `heapq`, `hashlib`, `urllib`, `collections`, `itertools`, `typing`).
- **Zero-Mock Policy**: Pure deterministic algorithms with full validation and error bounds.
