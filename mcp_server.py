# -*- coding: utf-8 -*-
import sys, json
from client import OpenClawGenParkInboxLiquidator

client = OpenClawGenParkInboxLiquidator()

TOOLS = [
    {
        "name": "extract_action_items_and_deadlines",
        "description": "Extracts imperative action tasks and temporal deadlines from email body.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "email_body": {"type": "string"},
                "reference_timestamp": {"type": "number"}
            },
            "required": ["email_body"]
        }
    },
    {
        "name": "calculate_eisenhower_matrix",
        "description": "Quantifies urgency and importance scores to assign email to Eisenhower quadrant.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "email": {"type": "object"},
                "vip_senders": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["email"]
        }
    },
    {
        "name": "triage_and_route_email",
        "description": "Executes full zero-inbox triage: extract actions, score priority, suggest reply draft.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "email": {"type": "object"},
                "vip_senders": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["email"]
        }
    }
]

def handle_request(req):
    method = req.get("method")
    rid = req.get("id")
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": rid, "result": {"tools": TOOLS}}
    elif method == "tools/call":
        params = req.get("params", {})
        tname = params.get("name")
        args = params.get("arguments", {})
        if tname == "extract_action_items_and_deadlines":
            res = client.extract_action_items_and_deadlines(args["email_body"], args.get("reference_timestamp"))
            return {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        elif tname == "calculate_eisenhower_matrix":
            res = client.calculate_eisenhower_matrix(args["email"], args.get("vip_senders"))
            return {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        elif tname == "triage_and_route_email":
            res = client.triage_and_route_email(args["email"], args.get("vip_senders"))
            return {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32601, "message": "Method not found"}}
    return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32600, "message": "Invalid Request"}}

def main():
    for line in sys.stdin:
        if not line.strip(): continue
        try:
            try:
                req = json.loads(line)
            except json.JSONDecodeError as exc:
                print(json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(exc)}}), flush=True)
                continue
            if not isinstance(req, dict) or req.get("jsonrpc") != "2.0" or not isinstance(req.get("method"), str):
                print(json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": -32600, "message": "Invalid Request"}}), flush=True)
                continue
            # JSON-RPC notifications never receive a response or execute request-only tools.
            if "id" not in req:
                continue
            if req["method"] == "initialize":
                print(json.dumps({"jsonrpc": "2.0", "id": req["id"], "result": {
                    "protocolVersion": "2024-11-05", "capabilities": {"tools": {}},
                    "serverInfo": {"name": 'openclaw-genpark-inbox-liquidator', "version": "1.0.0"}
                }}), flush=True)
                continue
            if req["method"] == "ping":
                print(json.dumps({"jsonrpc": "2.0", "id": req["id"], "result": {}}), flush=True)
                continue
            if req["method"] not in ("tools/list", "tools/call"):
                print(json.dumps({"jsonrpc": "2.0", "id": req["id"], "error": {"code": -32601, "message": "Method not found"}}), flush=True)
                continue
            if req["method"] == "tools/call":
                params = req.get("params")
                if not isinstance(params, dict) or not isinstance(params.get("arguments", {}), dict) or params.get("name") not in ('extract_action_items_and_deadlines', 'calculate_eisenhower_matrix', 'triage_and_route_email'):
                    print(json.dumps({"jsonrpc": "2.0", "id": req["id"], "error": {"code": -32602, "message": "Unknown tool or invalid arguments"}}), flush=True)
                    continue
            resp = handle_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": req.get("id") if isinstance(req, dict) else None, "error": {"code": -32700, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
