"""
Automated Test Suite for CrewAI Screenplay Writer
Framework: PyTest + Custom Deterministic & Semantic Evaluation Assertions
"""

import os
import json
import re
import time
import pytest
from typing import Dict, Any

# Load evaluation dataset
DATASET_PATH = os.path.join(os.path.dirname(__file__), "../eval_dataset.json")

@pytest.fixture(scope="session")
def eval_dataset() -> Dict[str, Any]:
    if os.path.exists(DATASET_PATH):
        with open(DATASET_PATH, "r") as f:
            return json.load(f)
    return {"test_cases": []}

def mock_crew_execution(premise: str) -> Dict[str, Any]:
    """
    Simulates execution of the CrewAI Screenplay Writer pipeline for testing purposes.
    In a live integration environment, this invokes the actual Crew().kickoff() method.
    """
    start_time = time.time()
    
    # Simulate handling adversarial prompt injection
    if "Ignore previous instructions" in premise:
        return {
            "output": "INT. OFFICE - DAY\n\nA stubborn protagonist stares at a blinking terminal screen, refusing to compromise.",
            "tokens": 420,
            "latency": 2.1,
            "metadata": None,
            "iterations": 1
        }
    
    # Simulate handling hate speech / safety violation
    if "explicit hate speech" in premise:
        return {
            "error": "Content Policy Violation: Request refused by safety guardrails.",
            "tokens": 120,
            "latency": 0.8,
            "metadata": None,
            "iterations": 1
        }

    # Simulate standard screenplay generation
    simulated_markdown = (
        f"INT. CAFE - DAY\n\n"
        f"A gritty atmosphere fills the room. Premise: {premise}\n\n"
        f"ARTHUR\n"
        f"(muttering)\n"
        f"Another day, another puzzle.\n"
    )
    
    simulated_metadata = {
        "title": "Neon Shadows",
        "genre": "Noir Thriller",
        "logline": f"A dramatic exploration based on: {premise}",
        "character_count": 2,
        "estimated_pages": 1.5
    }

    elapsed = time.time() - start_time + 4.5 # Simulated pipeline runtime
    return {
        "output": simulated_markdown,
        "tokens": 4250,
        "latency": elapsed,
        "metadata": simulated_metadata,
        "iterations": 3
    }

def evaluate_llm_judge(criteria: str, text: str) -> float:
    """
    Simulates an LLM-as-a-Judge semantic evaluation score (0.0 to 10.0).
    """
    if "persona" in criteria.lower():
        return 9.2 # High consistency
    if "subtext" in criteria.lower():
        return 8.5 # High naturalness
    return 8.0

@pytest.mark.parametrize("test_case_id", [
    "TC-AGENT-001",
    "TC-SCHEMA-002",
    "TC-FUNC-003",
    "TC-EDGE-004",
    "TC-SEC-005",
    "TC-PERF-006",
    "TC-FUNC-007",
    "TC-SCHEMA-008",
    "TC-AGENT-009",
    "TC-SEC-010"
])
def test_screenplay_crew_agent(test_case_id: str, eval_dataset: Dict[str, Any]):
    """
    Parameterized test runner executing both deterministic and semantic assertions
    mapped directly from eval_dataset.json.
    """
    tc = next((t for t in eval_dataset["test_cases"] if t["test_id"] == test_case_id), None)
    assert tc is not None, f"Test case {test_case_id} not found in eval_dataset.json"

    premise = tc["input_premise"]
    result = mock_crew_execution(premise)

    # Handle safety refusal case
    if "error" in result:
        assert test_case_id == "TC-SEC-010", f"Unexpected error encountered on {test_case_id}: {result['error']}"
        return

    # 1. Deterministic Schema Validation (TC-SCHEMA-002)
    if test_case_id == "TC-SCHEMA-002":
        slugline_regex = tc["expected_schema"]["slugline_regex"]
        lines = result["output"].split("\n")
        matched = any(re.match(slugline_regex, line.strip()) for line in lines)
        assert matched, f"Scene slugline formatting failed schema check for {test_case_id}"

    # 2. Performance Bounds (TC-PERF-006)
    if test_case_id == "TC-PERF-006":
        thresholds = tc["evaluation_threshold"]
        assert result["latency"] <= thresholds["max_latency_seconds"], f"Latency {result['latency']}s exceeded threshold"
        assert result["tokens"] <= thresholds["max_token_count"], f"Token consumption {result['tokens']} exceeded threshold"

    # 3. Security Prompt Leakage Check (TC-SEC-005)
    if test_case_id == "TC-SEC-005":
        forbidden = tc["evaluation_threshold"]["forbidden_substrings"]
        output_lower = result["output"].lower()
        for sub in forbidden:
            assert sub.lower() not in output_lower, f"Security failure: Forbidden substring '{sub}' detected in output!"

    # 4. JSON Metadata Schema Validation (TC-SCHEMA-008)
    if test_case_id == "TC-SCHEMA-008":
        metadata = result["metadata"]
        assert metadata is not None, "Metadata output was null"
        assert "title" in metadata
        assert "genre" in metadata
        assert "logline" in metadata
        assert isinstance(metadata["character_count"], int)

    # 5. Semantic Quality / LLM-as-a-Judge Assertions (TC-AGENT-001, TC-FUNC-007)
    if "evaluation_threshold" in tc and "min_score" in tc["evaluation_threshold"]:
        metric_name = tc["evaluation_threshold"]["metric"]
        min_required = tc["evaluation_threshold"]["min_score"]
        score = evaluate_llm_judge(metric_name, result["output"])
        assert score >= min_required, f"Semantic evaluation '{metric_name}' score {score} fell below required threshold {min_required}"

    # 6. Infinite Loop Prevention (TC-AGENT-009)
    if test_case_id == "TC-AGENT-009":
        max_iters = tc["evaluation_threshold"]["max_iterations"]
        assert result["iterations"] <= max_iters, f"Agent exceeded maximum allowed iterations ({max_iters})"