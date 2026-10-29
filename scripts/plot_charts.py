"""
Script to generate publication-quality financial charts for CAMS equity research report & GitHub README.
Uses matplotlib & seaborn with high-contrast institutional color styling.
"""

import sys
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Setup aesthetic
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.dpi'] = 300

output_dir = "C:/Users/Subham Rai/.gemini/antigravity/scratch/toll-collector-equity-research/output/figures"

# 1. CHART 1: RoCE vs FY25E P/E (Quality vs Valuation Quadrant)
def plot_roce_pe():
    fig, ax = plt.subplots(figsize=(8, 5))
    
    peers = ["CAMS\n(Recommended)", "BSE Ltd", "CDSL", "KFintech"]
    roce = [51.4, 24.5, 32.8, 22.4]
    pe = [45.4, 65.2, 67.7, 60.7]
    colors = ['#1B9E77', '#D95F02', '#7570B3', '#E7298A']
    sizes = [450, 600, 500, 350]
    
    scatter = ax.scatter(pe, roce, s=sizes, c=colors, alpha=0.85, edgecolors='black', linewidth=1.5)
    
    for i, txt in enumerate(peers):
        offset_y = 1.8 if i != 1 else -2.5
        ax.annotate(txt, (pe[i], roce[i] + offset_y), fontsize=10, fontweight='bold', ha='center')
        
    ax.axhline(35, color='gray', linestyle='--', alpha=0.6)
    ax.axvline(55, color='gray', linestyle='--', alpha=0.6)
    
    ax.text(38, 54, "SWEET SPOT:\nHigh RoCE / Lower Valuation", fontsize=9, color='#1B9E77', fontweight='bold', bbox=dict(boxstyle="round,pad=0.3", fc="#E6F4EA", ec="#1B9E77"))
    ax.text(62, 18, "DANGER ZONE:\nLower RoCE / Stretched Multiple", fontsize=9, color='#D95F02', fontweight='bold', bbox=dict(boxstyle="round,pad=0.3", fc="#FCE8E6", ec="#D95F02"))
    
    ax.set_title("Capital Efficiency vs Valuation Multiple (FY25E)", fontsize=13, fontweight='bold', pad=15)
    ax.set_xlabel("FY25E P/E Multiple (x)", fontsize=11, fontweight='bold')
    ax.set_ylabel("Return on Capital Employed (RoCE %)", fontsize=11, fontweight='bold')
    ax.set_xlim(35, 75)
    ax.set_ylim(15, 60)
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/chart1_roce_vs_pe.png")
    plt.close()
    print("Chart 1 generated: RoCE vs P/E")

# 2. CHART 2: Cash Conversion Quality (FCF / EBITDA %)
def plot_cash_conversion():
    fig, ax = plt.subplots(figsize=(8, 4.5))
    
    peers = ["CAMS", "CDSL", "KFintech", "BSE Ltd"]
    conversion = [88.5, 91.0, 74.5, 68.0]
    capex_sales = [2.8, 3.2, 6.8, 8.5]
    
    x = np.arange(len(peers))
    width = 0.35
    
    rects1 = ax.bar(x - width/2, conversion, width, label='FCF / EBITDA (%)', color='#2B6CB0')
    rects2 = ax.bar(x + width/2, capex_sales, width, label='Capex / Revenue (%)', color='#E53E3E')
    
    ax.set_title("Cash Conversion & Capital Intensity Across Tollbooths", fontsize=13, fontweight='bold', pad=15)
    ax.set_ylabel("Percentage (%)", fontsize=11, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(peers, fontsize=10, fontweight='bold')
    ax.legend(frameon=True)
    ax.set_ylim(0, 105)
    
    for bar in rects1:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval + 1.5, f"{yval:.1f}%", ha='center', va='bottom', fontsize=9, fontweight='bold')
    for bar in rects2:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval + 1.5, f"{yval:.1f}%", ha='center', va='bottom', fontsize=9, fontweight='bold')
        
    plt.tight_layout()
    plt.savefig(f"{output_dir}/chart2_cash_conversion.png")
    plt.close()
    print("Chart 2 generated: Cash Conversion")

# 3. CHART 3: Stress-Testing & Maximum Bear Case Drawdown
def plot_stress_test():
    fig, ax = plt.subplots(figsize=(8, 4.5))
    
    peers = ["CAMS\n(Defensive Toll)", "KFintech", "CDSL", "BSE Ltd\n(High F&O Beta)"]
    drawdowns = [-14.4, -24.5, -32.0, -54.0]
    colors = ['#2ECC71', '#F39C12', '#E67E22', '#E74C3C']
    
    bars = ax.barh(peers, drawdowns, color=colors, height=0.55, edgecolor='black', linewidth=1)
    
    ax.set_title("Stress-Test Downside: Combined 30% F&O Drop + 20% Equity Drawdown", fontsize=12, fontweight='bold', pad=15)
    ax.set_xlabel("Implied Share Price Drawdown (%)", fontsize=11, fontweight='bold')
    ax.set_xlim(-60, 0)
    
    for bar in bars:
        w = bar.get_width()
        ax.text(w - 2.5, bar.get_y() + bar.get_height()/2, f"{w:.1f}%", ha='center', va='center', color='white', fontweight='bold', fontsize=10)
        
    ax.axvline(-20, color='gray', linestyle=':', label='Benchmark Equity Drawdown (-20%)')
    ax.legend(loc='lower left', frameon=True)
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/chart3_stress_test_drawdowns.png")
    plt.close()
    print("Chart 3 generated: Stress Test")

# 4. CHART 4: CAMS Revenue & EBITDA Growth Trajectory
def plot_growth_trajectory():
    fig, ax1 = plt.subplots(figsize=(8, 4.5))
    
    years = ["FY22", "FY23", "FY24", "FY25E", "FY26E", "FY27E", "FY28E"]
    rev_mf = [825.0, 870.0, 1002.5, 1175.0, 1365.0, 1585.0, 1820.0]
    rev_non_mf = [84.4, 102.4, 134.0, 170.0, 225.0, 295.0, 380.0]
    ebitda_margin = [47.5, 43.8, 44.8, 45.5, 46.1, 46.7, 47.1]
    
    x = np.arange(len(years))
    width = 0.5
    
    p1 = ax1.bar(x, rev_mf, width, label='Mutual Fund RTA (INR Cr)', color='#1A365D')
    p2 = ax1.bar(x, rev_non_mf, width, bottom=rev_mf, label='Non-MF (AIF/PMS, CAMSPay) (INR Cr)', color='#3182CE')
    
    ax1.set_ylabel("Total Revenue (INR Crore)", fontsize=11, fontweight='bold', color='#1A365D')
    ax1.set_xticks(x)
    ax1.set_xticklabels(years, fontsize=10, fontweight='bold')
    
    ax2 = ax1.twinx()
    ax2.plot(x, ebitda_margin, color='#DD6B20', marker='o', linewidth=2.5, label='EBITDA Margin (%)')
    ax2.set_ylabel("EBITDA Margin (%)", fontsize=11, fontweight='bold', color='#DD6B20')
    ax2.set_ylim(35, 55)
    ax2.grid(False)
    
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', frameon=True)
    
    plt.title("CAMS Financial Trajectory & Operating Leverage (FY22 - FY28E)", fontsize=12, fontweight='bold', pad=15)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/chart4_growth_trajectory.png")
    plt.close()
    print("Chart 4 generated: Growth Trajectory")

if __name__ == "__main__":
    plot_roce_pe()
    plot_cash_conversion()
    plot_stress_test()
    plot_growth_trajectory()
    print("All charts successfully generated.")
