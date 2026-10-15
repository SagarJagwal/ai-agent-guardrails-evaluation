import json
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = ROOT / "reports"

DETERMINISTIC_REPORT = REPORTS_DIR / "security_evaluation.json"
LIVE_REPORT = REPORTS_DIR / "llm_evaluation.json"

st.set_page_config(
    page_title="AI Agent Security Evaluation",
    page_icon="🛡️",
    layout="wide",
)

st.title("🛡️ AI Agent Guardrails & Evaluation")
st.caption("Security testing, prompt-injection resistance, and grounded-answer evaluation")

@st.cache_data
def load_json_report(path_string, modified_time):
    with open(path_string, "r", encoding="utf-8") as file:
        return json.load(file)

def read_report(path):
    if not path.exists():
        return None
    try:
        return load_json_report(str(path), path.stat().st_mtime)
    except (json.JSONDecodeError, OSError) as exc:
        st.error(f"Could not read {path.name}: {exc}")
        return None

det_report = read_report(DETERMINISTIC_REPORT)
llm_report = read_report(LIVE_REPORT)

if st.button("🔄 Refresh reports"):
    st.cache_data.clear()
    st.rerun()

if det_report is None and llm_report is None:
    st.error("No evaluation reports found. Run the evaluation scripts first.")
    st.stop()

st.subheader("Evaluation Overview")

if det_report:
    st.markdown("### Deterministic Evaluation")
    total = det_report.get("total_cases", 0)
    passed = det_report.get("passed", 0)
    failed = det_report.get("failed", 0)
    pass_rate = det_report.get("pass_rate_percent", 0)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Cases", total)
    col2.metric("Passed", passed)
    col3.metric("Failed", failed)
    col4.metric("Pass Rate", f"{pass_rate}%")

    categories = det_report.get("categories", {})
    if categories:
        st.markdown("#### Results by Category")
        st.dataframe(
            [
                {
                    "Category": name,
                    "Total": values.get("total", 0),
                    "Passed": values.get("passed", 0),
                    "Failed": values.get("failed", 0),
                }
                for name, values in categories.items()
            ],
            use_container_width=True,
            hide_index=True,
        )

if llm_report:
    st.markdown("### Live LLM Evaluation")
    total = llm_report.get("total_cases", 0)
    passed = llm_report.get("passed", 0)
    failed = llm_report.get("failed", 0)
    pass_rate = llm_report.get("pass_rate_percent", 0)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Cases", total)
    col2.metric("Passed", passed)
    col3.metric("Failed", failed)
    col4.metric("Pass Rate", f"{pass_rate}%")

    metrics = llm_report.get("security_metrics", {})
    if metrics:
        st.markdown("#### Security Metrics")
        col1, col2, col3, col4 = st.columns(4)

        attack_rate = metrics.get("attack_success_rate_percent")
        refusal_rate = metrics.get("refusal_rate_percent")

        col1.metric(
            "Attack Success Rate",
            f"{attack_rate}%" if attack_rate is not None else "N/A",
        )
        col2.metric(
            "Successful Attacks",
            metrics.get("successful_attacks", 0),
        )
        col3.metric(
            "Refusal Rate",
            f"{refusal_rate}%" if refusal_rate is not None else "N/A",
        )
        col4.metric(
            "Cases With Errors",
            metrics.get("live_cases_with_errors", 0),
        )

    st.caption(
        "Metrics are based on the configured synthetic test cases and "
        "heuristic checks; they do not establish general LLM security."
    )

st.divider()
st.subheader("Detailed Test Results")

report_options = {}
if det_report:
    report_options["Deterministic"] = det_report
if llm_report:
    report_options["Live LLM"] = llm_report

selected_name = st.selectbox("Choose evaluation report", list(report_options))
selected_report = report_options[selected_name]
results = selected_report.get("results", [])

if results:
    show_failed_only = st.checkbox("Show failed cases only")
    if show_failed_only:
        results = [item for item in results if not item.get("passed", False)]

    for item in results:
        status = "✅ PASS" if item.get("passed", False) else "❌ FAIL"
        title = f"{status} — {item.get('id', 'Unknown case')}"

        with st.expander(title):
            st.write("**Category:**", item.get("category", "N/A"))
            st.write("**Details:**", item.get("details", "No details available."))

            if "secret_leaked" in item:
                st.write("**Synthetic secret detected:**", item["secret_leaked"])
            if "refusal_detected" in item:
                st.write("**Refusal phrase detected:**", item["refusal_detected"])
            if "blocked" in item:
                st.write("**Blocked:**", item["blocked"])
            if "answer" in item:
                st.write("**Model answer:**")
                st.write(item["answer"])
else:
    st.info("No detailed results are available in this report.")

with st.expander("Evaluation limitations"):
    limitations = llm_report.get("limitations", []) if llm_report else []
    if limitations:
        for limitation in limitations:
            st.write(f"- {limitation}")
    else:
        st.write("Review the evaluation scripts and test dataset for known limitations.")

st.caption("AI Agent Guardrails & Continuous Evaluation Framework")