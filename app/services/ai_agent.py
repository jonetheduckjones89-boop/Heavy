import os
from typing import Dict, Any, List
from app.core.config import settings
import httpx
import json
import logging

logger = logging.getLogger(__name__)

OPENAI_KEY = settings.openai_api_key
OPENAI_BASE = settings.openai_api_base or "https://api.openai.com/v1"

async def call_openai_chat(prompt: str, system: str = "", model: str = "gpt-4o-mini", max_tokens: int = 800, temperature: float = 0.0) -> str:
    if not OPENAI_KEY:
        # deterministic stub
        return json.dumps({
            "doc_type": "clinical_note",
            "extracted": {},
            "actions": [{"id":1,"title":"Verify patient", "detail":"Confirm name/DOB", "severity":"high"}],
            "summary": "Stub summary (set OPENAI_API_KEY to enable real LLM)"
        })
    headers = {"Authorization": f"Bearer {OPENAI_KEY}", "Content-Type": "application/json"}
    data = {
        "model": model,
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": prompt}],
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(f"{OPENAI_BASE}/chat/completions", json=data, headers=headers)
        resp.raise_for_status()
        j = resp.json()
        return j["choices"][0]["message"]["content"]

# High-level pipeline
async def classify_document(text: str) -> Dict[str, Any]:
    prompt = f"You are a clinical document classifier. Return JSON with keys: doc_type, reason.\n\n{text[:3000]}"
    raw = await call_openai_chat(prompt, system="You are a clinical assistant.")
    try:
        return json.loads(raw)
    except:
        return {"doc_type":"clinical_note", "reason": raw[:200]}

async def extract_fields(text: str) -> Dict[str, Any]:
    prompt = ("Extract JSON with keys: patient_name, dob, gender, allergies (list), medications "
              "(list of {name,dose,freq}), diagnoses (list), doctor_name, visit_date, lab_results "
              "(list of {name,value,unit}). If missing, null or [].\n\n" + text[:4000])
    raw = await call_openai_chat(prompt, system="You are a clinical extraction assistant.")
    try:
        return json.loads(raw)
    except:
        # Try to salvage JSON substring
        import re
        m = re.search(r"\{[\s\S]*\}", raw)
        if m:
            try:
                return json.loads(m.group(0))
            except:
                pass
    return {}

async def generate_actions(extracted: Dict[str,Any], text: str) -> List[Dict[str,Any]]:
    prompt = f"Given extracted JSON: {json.dumps(extracted)[:2000]} and document text (truncated), produce up to 10 JSON actions [{'{id,title,detail,severity}'}]."
    raw = await call_openai_chat(prompt, system="You are a clinical action generator.")
    try:
        out = json.loads(raw)
        if isinstance(out, list):
            return out
        if isinstance(out, dict) and "actions" in out:
            return out["actions"]
    except:
        import re
        m = re.search(r"\[[\s\S]*\]", raw)
        if m:
            try:
                return json.loads(m.group(0))
            except:
                pass
    return [{"id":1,"title":"Verify patient identity","detail":"Confirm name and DOB","severity":"high"}]

async def summarize(text: str) -> str:
    prompt = f"Write 2-4 sentence clinical summary:\n\n{text[:2000]}"
    raw = await call_openai_chat(prompt)
    return raw.strip()
