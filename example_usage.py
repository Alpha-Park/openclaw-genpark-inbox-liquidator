# -*- coding: utf-8 -*-
from client import OpenClawGenParkInboxLiquidator

liquidator = OpenClawGenParkInboxLiquidator()

sample_email = {
    "sender": "sarah.chen@board.alphapark.ai",
    "subject": "URGENT: Final Board Review & Signature on Master Agreement",
    "body": """
Hi Team,
Please review the attached Master Agreement contract before EOD today.
We must submit the executed doc to legal by 5pm.
Also, could you confirm the final compute budget for next quarter?
Thanks,
Sarah
"""
}

# 1. Action Items
actions = liquidator.extract_action_items_and_deadlines(sample_email["body"])
print(f"Extracted {len(actions)} action items:")
for a in actions:
    print(f"  [{a['item_id']}] Deadline: {a['deadline_extracted']} -> {a['raw_text']}")

# 2. Eisenhower Matrix
matrix = liquidator.calculate_eisenhower_matrix(sample_email, vip_senders=["sarah.chen@board.alphapark.ai"])
print(f"\nEisenhower Analysis: {matrix['eisenhower_quadrant']} ({matrix['priority']})")
print(f"  Urgency: {matrix['urgency_score']}, Importance: {matrix['importance_score']}")

# 3. Triage Disposition
triage = liquidator.triage_and_route_email(sample_email, vip_senders=["sarah.chen@board.alphapark.ai"])
print(f"\nTriage Result: {triage['triage_disposition']}")
print(f"  Suggested Reply: '{triage['suggested_reply_draft']}'")
