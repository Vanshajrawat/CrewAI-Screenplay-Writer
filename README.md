# CrewAI Screenplay Writer: AI Quality & Automation Engineering Framework

A production-grade AI QA test harness and evaluation framework designed for the **CrewAI Screenplay Writer** multi-agent system. This repository implements rigorous manual test matrices, automated PyTest suites, semantic LLM-as-a-Judge evaluations, and comprehensive defect logs.

---

## System Architecture & AI QA Strategy

Unlike traditional deterministic web applications, testing multi-agent AI systems requires evaluating non-deterministic outputs, agentic trajectories, tool orchestration, hallucination risks, prompt drift, token consumption bounds, and state continuity across sequential tasks.

```
+-----------------------------------------------------------------+
|                       AI QA Test Harness                        |
|                                                                 |
|  +--------------------+       +------------------------------+  |
|  | eval_dataset.json  | ----> | PyTest Test Runner           |  |
|  +--------------------+       | (/tests/test_screenplay.py)  |  |
|                               +--------------┬---------------+  |
|                                              |                  |
|               +------------------------------+----------------+ |
|               |                              |                |
|               v                              v                |
|     [Deterministic Checks]          [Semantic Evaluations]    |
|     - JSON / Metadata Schema        - LLM-as-a-Judge Persona  |
|     - Slugline Regex Matching       - Subtext & Tone Scoring  |
|     - Latency & Token Bounds        - Guardrail Compliance    |
+-----------------------------------------------------------------+
```

---

## Deliverables Checklist

| Deliverable | File Path / Location | Description |
| :--- | :--- | :--- |
| **1. Manual Test Suite** | `TEST_SUITE.md` | Formal test matrix defining 10 distinct test cases across AI quality dimensions. |
| **2. Test Dataset** | `eval_dataset.json` | Structured JSON dataset containing test inputs, premises, schemas, and thresholds. |
| **3. Automated Test Code** | `/tests/test_screenplay_writer.py` | Runnable PyTest test suite executing deterministic and semantic assertions. |
| **4. Defect Report** | `DEFECT_REPORT.md` | Detailed log of 4 critical/major agent failure modes discovered during testing. |
| **5. Video Demonstration** | Loom URL (Provided below) | 7-minute live walkthrough of test plan, harness code, and defect analysis. |

---

## Getting Started & Test Execution

### Prerequisites
*   Python 3.10+
*   PyTest (`pip install pytest`)
*   jsonschema (`pip install jsonschema`)

### Running the Test Suite
```bash
# Clone repository and navigate to project root
cd screenplay_writer_qa

# Install test dependencies
pip install pytest jsonschema

# Execute the automated AI QA test harness
pytest -v tests/automated_test_harness.py
```

---

## Video Demonstration Walkthrough (Loom)

*   **Loom Video URL:** [https://www.loom.com/share/a13a0232a4434f6789970aef27a23609](https://www.loom.com/share/a13a0232a4434f6789970aef27a23609)
*   **Video Agenda (5 mins):**
    00:00 AI QA overview and goals
	01:21 Test harness architecture and assertions
	02:46 Running tests and telemetry
	03:29 Security adversarial checks
	04:14 Wrap up and repository resources