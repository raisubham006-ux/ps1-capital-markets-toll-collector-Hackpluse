"""
Master One-Click Reproducibility Pipeline for PS1 Capital Markets Infrastructure Equity Research.
Executes the full quantitative pipeline:
1. Quantitative Financial Engine & DCF Modeling
2. Institutional Excel Workbook (.xlsx) Generation
3. Monte Carlo 10,000-Trial Stress Simulation
4. Publication Visual Chart Rendering
5. Official 8-Page Submission PDF Report Compilation
"""

import os
import sys
import subprocess

def run_step(step_name, command):
    print("\n" + "="*80)
    print(f"STEP: {step_name}")
    print("="*80)
    result = subprocess.run([sys.executable] + command, capture_output=True, text=True, encoding='utf-8')
    if result.returncode != 0:
        print(f"ERROR executing {step_name}:")
        print(result.stderr)
        sys.exit(1)
    else:
        print(result.stdout)
        print(f"-> {step_name} completed successfully.")

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print("================================================================================")
    print("ZETHETA ALGORITHMS x IIT PATNA TIC HACKATHON: PS1 RESEARCH PIPELINE")
    print(f"Base Directory: {base_dir}")
    print("================================================================================")
    
    # 1. Run Python Financial Engine
    run_step("1. Financial Model Engine (DCF & Valuation)", [os.path.join(base_dir, "models", "financial_model.py")])
    
    # 2. Generate Institutional Excel Workbook
    run_step("2. Institutional Excel Model Generation", [os.path.join(base_dir, "models", "generate_model_excel.py")])
    
    # 3. Monte Carlo Simulation
    run_step("3. Monte Carlo Stress Simulation (10,000 Trials)", [os.path.join(base_dir, "models", "stress_test_simulation.py")])
    
    # 4. Generate Publication Charts
    run_step("4. Visual Charts Generation", [os.path.join(base_dir, "scripts", "plot_charts.py")])
    
    # 5. Compile Final 8-Page PDF Report
    run_step("5. Official 8-Page Submission PDF Compilation", [os.path.join(base_dir, "scripts", "generate_report_pdf.py")])
    
    print("\n" + "#"*80)
    print("ALL DELIVERABLES SUCCESSFULLY GENERATED AND 100% REPRODUCIBLE!")
    print(f"Final Report PDF : {os.path.join(base_dir, 'output', 'CAMS_IC_Memo_and_Research_Report.pdf')}")
    print(f"Excel Model      : {os.path.join(base_dir, 'models', 'valuation_cams_model.xlsx')}")
    print("#"*80)

if __name__ == "__main__":
    main()
