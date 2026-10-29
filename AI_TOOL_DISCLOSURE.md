# MANDATORY AI TOOL DISCLOSURE DECLARATION

**Competition:** Zetheta Algorithms × IIT Patna Trading & Investment Club (TIC) 24-Hour Hackathon  
**Track:** PS1: Equity Research & Consulting — Toll Collector of India's Capital Markets  
**Submission Protocol Compliance:** Section 2 (Universal Competition Rules - Mandatory Tool Disclosure)

---

### Official Tool Declaration Matrix

In accordance with Section 2 of the Official Competition Rulebook, our team submits the following exhaustive disclosure of all Artificial Intelligence models, Large Language Models (LLMs), and programmatic libraries utilized during this project, along with their precise functional applications:

```
+-------------------------------------------------------------------------------------------------------------------------+
| AI & COMPUTATIONAL TOOL DISCLOSURE                                                                                      |
+--------------------------+-----------------------+--------------------------+-------------------------------------------+
| Tool / Model Name        | Version / Build       | Provider / Source        | Functional Application in Project         |
+--------------------------+-----------------------+--------------------------+-------------------------------------------+
| Claude 3.5 Sonnet /      | API Build Oct 2024 /  | Anthropic / Google       | Synthesizing regulatory circulars,        |
| Gemini 1.5 Pro           | Direct Workspace      | DeepMind                 | drafting IC memorandum structure, and     |
|                          |                       |                          | structuring markdown documentation.       |
| Python 3.13 Quantitative | 3.13.14 (x64)         | Python Software          | Core quantitative modeling, 10,000-trial  |
| Engine                   |                       | Foundation               | Monte Carlo simulation, and DCF engine.   |
| NumPy                    | 2.5.2                 | Open Source              | Vectorized cash flow discounting, matrix  |
|                          |                       |                          | mathematics, and random normal sampling.  |
| Pandas                   | 3.0.5                 | Open Source              | 3-statement financial table integration,  |
|                          |                       |                          | peer comp benchmarking, and time-series.  |
| OpenPyXL                 | 3.1.5                 | Open Source              | Programmatic institutional Excel financial|
|                          |                       |                          | model workbook generation (.xlsx).        |
| Matplotlib & Seaborn     | 3.11.1 / 0.13.2       | Open Source              | High-resolution publication-quality chart |
|                          |                       |                          | generation and stress-test visual plots.  |
| ReportLab PDF Engine     | 5.1.0                 | ReportLab Inc.           | Direct programmatic compilation of the    |
|                          |                       |                          | 8-page selectable-text final report PDF.  |
+--------------------------+-----------------------+--------------------------+-------------------------------------------+
```

### Reproducibility & Integrity Confirmation:
* **Zero Look-Ahead Bias:** All models, projections, and valuation targets utilize data available up to the official cut-off date (October 2024). No forward look-ahead leakage occurred.
* **100% Code-Driven Reproducibility:** Every figure, table, DCF output, Monte Carlo VaR metric, and Excel sheet is generated programmatically from the scripts included in the repository (`models/financial_model.py`, `models/generate_model_excel.py`, `models/stress_test_simulation.py`, and `scripts/generate_report_pdf.py`).
* **Human Verification:** All regulatory citations (SEBI circulars, AMFI data, MCA statutory filings) were independently verified against official gazettes.
