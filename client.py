# -*- coding: utf-8 -*-
"""
OpenClaw GenPark Inbox Liquidator - Zero-Inbox NLP Action Item & Eisenhower Matrix Triage Engine
Standard Library only: re, time, math, typing.
Extracts imperative action tasks and temporal deadlines, computes urgency vs importance
Eisenhower coordinates, and automates zero-inbox disposition (Do, Schedule, Delegate, Archive).
"""

import re
import time
import math
from typing import Dict, List, Any

class OpenClawGenParkInboxLiquidator:
    def __init__(self):
        self.action_verbs = [
            r"\b(please|kindly|could you|can you|need you to|must|request)\s+([a-z]+)",
            r"\b(review|approve|sign|schedule|send|confirm|submit|deploy|investigate|update|follow up)\b"
        ]
        self.urgent_keywords = [
            "urgent", "asap", "emergency", "blocker", "critical", "immediately", "deadline", "today"
        ]
        self.importance_keywords = [
            "contract", "agreement", "invoice", "payment", "security", "vulnerability",
            "executive", "board", "quarterly", "budget", "client", "customer", "audit"
        ]

    def extract_action_items_and_deadlines(self, email_body: str,
                                          reference_timestamp: float = None) -> List[Dict[str, Any]]:
        """
        Extracts syntactic imperative commitments, requests, and temporal deadlines from email text.
        """
        ref_time = reference_timestamp if reference_timestamp is not None else time.time()
        lines = [line.strip() for line in email_body.split("\n") if line.strip()]
        action_items = []

        for idx, line in enumerate(lines):
            # Check for action verb
            has_action = False
            for pat in self.action_verbs:
                if re.search(pat, line, re.IGNORECASE):
                    has_action = True
                    break

            # Check for deadline phrase
            deadline_str = None
            hours_remaining = None
            if re.search(r"\b(by\s+eod|today\s+by\s+5|end\s+of\s+day)\b", line, re.IGNORECASE):
                deadline_str = "TODAY_EOD"
                hours_remaining = 6.0
            elif re.search(r"\b(tomorrow|by\s+tomorrow)\b", line, re.IGNORECASE):
                deadline_str = "TOMORROW"
                hours_remaining = 24.0
            elif re.search(r"\b(by\s+friday|this\s+week)\b", line, re.IGNORECASE):
                deadline_str = "END_OF_WEEK"
                hours_remaining = 72.0
            elif re.search(r"\b(within\s+(\d+)\s+hours)\b", line, re.IGNORECASE):
                m = re.search(r"\bwithin\s+(\d+)\s+hours\b", line, re.IGNORECASE)
                h = float(m.group(1))
                deadline_str = f"WITHIN_{int(h)}_HOURS"
                hours_remaining = h

            if has_action or deadline_str:
                action_items.append({
                    "item_id": f"act_{idx+1:02d}",
                    "raw_text": line,
                    "has_imperative_request": has_action,
                    "deadline_extracted": deadline_str,
                    "estimated_hours_remaining": hours_remaining
                })

        return action_items

    def calculate_eisenhower_matrix(self, email: Dict[str, Any],
                                   vip_senders: List[str] = None) -> Dict[str, Any]:
        """
        Quantifies Urgency U in [0,1] and Importance I in [0,1] to assign Eisenhower quadrant.
        """
        vips = [v.lower() for v in (vip_senders or [])]
        sender = email.get("sender", "").lower()
        subject = email.get("subject", "").lower()
        body = email.get("body", "").lower()

        # 1. Importance Calculation
        importance_score = 0.2 # Baseline
        if any(v in sender for v in vips):
            importance_score += 0.5
        elif any(domain in sender for domain in ["@board.", "@exec.", "@legal.", "@security."]):
            importance_score += 0.4

        for kw in self.importance_keywords:
            if kw in subject:
                importance_score += 0.15
            elif kw in body:
                importance_score += 0.05
        importance_score = min(1.0, max(0.0, importance_score))

        # 2. Urgency Calculation
        urgency_score = 0.1 # Baseline
        for kw in self.urgent_keywords:
            if kw in subject:
                urgency_score += 0.25
            elif kw in body:
                urgency_score += 0.10

        # Check for extracted deadlines
        if "today" in body or "eod" in body or "asap" in body:
            urgency_score += 0.35
        urgency_score = min(1.0, max(0.0, urgency_score))

        # 3. Quadrant Determination
        if urgency_score >= 0.5 and importance_score >= 0.5:
            quadrant = "Q1_DO_FIRST"
            priority = "P0_CRITICAL"
        elif urgency_score < 0.5 and importance_score >= 0.5:
            quadrant = "Q2_SCHEDULE"
            priority = "P1_STRATEGIC"
        elif urgency_score >= 0.5 and importance_score < 0.5:
            quadrant = "Q3_DELEGATE"
            priority = "P2_OPERATIONAL"
        else:
            quadrant = "Q4_ELIMINATE"
            priority = "P3_LOW_OR_ARCHIVE"

        return {
            "sender": sender,
            "subject": email.get("subject", ""),
            "urgency_score": round(urgency_score, 3),
            "importance_score": round(importance_score, 3),
            "eisenhower_quadrant": quadrant,
            "priority": priority
        }

    def triage_and_route_email(self, email: Dict[str, Any],
                               vip_senders: List[str] = None) -> Dict[str, Any]:
        """
        Synthesizes action extraction and Eisenhower priority to generate zero-inbox triage disposition.
        """
        body = email.get("body", "")
        actions = self.extract_action_items_and_deadlines(body)
        matrix = self.calculate_eisenhower_matrix(email, vip_senders)

        quadrant = matrix["eisenhower_quadrant"]
        if quadrant == "Q1_DO_FIRST":
            action_disposition = "IMMEDIATE_EXECUTION"
            auto_archive = False
            suggested_reply = "Acknowledged. Prioritizing and executing immediately today."
        elif quadrant == "Q2_SCHEDULE":
            action_disposition = "CALENDAR_DEEP_WORK_BLOCK"
            auto_archive = False
            suggested_reply = "Received. Scheduled on dedicated work calendar for this week."
        elif quadrant == "Q3_DELEGATE":
            action_disposition = "DELEGATE_TO_SUBAGENT"
            auto_archive = False
            suggested_reply = "Forwarding to specialized agent operations for processing."
        else:
            action_disposition = "AUTO_ARCHIVE_BATCH"
            auto_archive = True
            suggested_reply = None

        return {
            "email_subject": email.get("subject", ""),
            "triage_disposition": action_disposition,
            "auto_archive_ready": auto_archive,
            "priority_tier": matrix["priority"],
            "urgency_score": matrix["urgency_score"],
            "importance_score": matrix["importance_score"],
            "action_items_count": len(actions),
            "action_items": actions,
            "suggested_reply_draft": suggested_reply
        }
