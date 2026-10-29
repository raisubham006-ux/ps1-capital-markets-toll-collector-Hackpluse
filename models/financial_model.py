"""
PS1: Equity Research & Consulting - Toll Collector of India's Capital Markets
Integrated Quantitative Valuation, FDD, and Scenario Engine for CAMS vs BSE, CDSL, KFin
Author: Zetheta x IIT Patna Hackathon Quantitative Research Team
Target Allocation: INR 500 Crore Long-Only Allocation
"""

import sys
import numpy as np
import pandas as pd

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# ==============================================================================
# 1. HISTORICAL & COMPARATIVE PEER METRICS (FY21 - FY25E)
# ==============================================================================

PEER_DATA = {
    "CAMS": {
        "Ticker": "CAMS.NS",
        "CMP_INR": 3985.0,
        "Shares_Out_Cr": 4.93,
        "Market_Cap_Cr": 19646.0,
        "Net_Cash_Cr": 485.0,
        "EV_Cr": 19161.0,
        "FY24_Rev_Cr": 1136.5,
        "FY24_EBITDA_Cr": 508.8,
        "FY24_PAT_Cr": 353.6,
        "FY25E_Rev_Cr": 1345.0,
        "FY25E_EBITDA_Cr": 612.0,
        "FY25E_PAT_Cr": 432.0,
        "FY26E_PAT_Cr": 525.0,
        "P_E_FY25E": 45.4,
        "EV_EBITDA_FY25E": 31.3,
        "RoCE_pct": 51.4,
        "RoE_pct": 41.8,
        "FCF_Conversion_pct": 88.5,  # FCF / EBITDA
        "Capex_Sales_pct": 2.8,
        "Dividend_Payout_pct": 72.0,
        "MF_Market_Share_pct": 68.5,
        "FO_Curbs_Exposure": "ZERO (0% Direct)",
        "ADV_30D_Cr": 68.5,
        "Moat_Type": "Switching Costs + Mission-Critical RTA Duopoly"
    },
    "BSE": {
        "Ticker": "BSE.NS",
        "CMP_INR": 4720.0,
        "Shares_Out_Cr": 13.54,
        "Market_Cap_Cr": 63908.0,
        "Net_Cash_Cr": 2850.0,
        "EV_Cr": 61058.0,
        "FY24_Rev_Cr": 1618.0,
        "FY24_EBITDA_Cr": 685.0,
        "FY24_PAT_Cr": 420.0,
        "FY25E_Rev_Cr": 2450.0,
        "FY25E_EBITDA_Cr": 1280.0,
        "FY25E_PAT_Cr": 980.0,
        "FY26E_PAT_Cr": 1120.0,
        "P_E_FY25E": 65.2,
        "EV_EBITDA_FY25E": 47.7,
        "RoCE_pct": 24.5,
        "RoE_pct": 22.1,
        "FCF_Conversion_pct": 68.0,
        "Capex_Sales_pct": 8.5,
        "Dividend_Payout_pct": 35.0,
        "MF_Market_Share_pct": 0.0,
        "FO_Curbs_Exposure": "SEVERE HIGH (>70% Growth at Risk)",
        "ADV_30D_Cr": 310.0,
        "Moat_Type": "Exchange Network Effects (Vulnerable to SEBI curbs)"
    },
    "CDSL": {
        "Ticker": "CDSL.NS",
        "CMP_INR": 1540.0,
        "Shares_Out_Cr": 20.90,
        "Market_Cap_Cr": 32186.0,
        "Net_Cash_Cr": 1250.0,
        "EV_Cr": 30936.0,
        "FY24_Rev_Cr": 812.0,
        "FY24_EBITDA_Cr": 490.0,
        "FY24_PAT_Cr": 361.0,
        "FY25E_Rev_Cr": 1050.0,
        "FY25E_EBITDA_Cr": 635.0,
        "FY25E_PAT_Cr": 475.0,
        "FY26E_PAT_Cr": 560.0,
        "P_E_FY25E": 67.7,
        "EV_EBITDA_FY25E": 48.7,
        "RoCE_pct": 32.8,
        "RoE_pct": 29.5,
        "FCF_Conversion_pct": 91.0,
        "Capex_Sales_pct": 3.2,
        "Dividend_Payout_pct": 55.0,
        "MF_Market_Share_pct": 0.0,
        "FO_Curbs_Exposure": "LOW-MODERATE (Cash Delivery/KYC impact)",
        "ADV_30D_Cr": 145.0,
        "Moat_Type": "Retail Demat Account Scale Duopoly"
    },
    "KFintech": {
        "Ticker": "KFINTECH.NS",
        "CMP_INR": 1080.0,
        "Shares_Out_Cr": 17.15,
        "Market_Cap_Cr": 18522.0,
        "Net_Cash_Cr": 320.0,
        "EV_Cr": 18202.0,
        "FY24_Rev_Cr": 837.5,
        "FY24_EBITDA_Cr": 372.0,
        "FY24_PAT_Cr": 246.0,
        "FY25E_Rev_Cr": 1025.0,
        "FY25E_EBITDA_Cr": 455.0,
        "FY25E_PAT_Cr": 305.0,
        "FY26E_PAT_Cr": 375.0,
        "P_E_FY25E": 60.7,
        "EV_EBITDA_FY25E": 40.0,
        "RoCE_pct": 22.4,
        "RoE_pct": 19.8,
        "FCF_Conversion_pct": 74.5,
        "Capex_Sales_pct": 6.8,
        "Dividend_Payout_pct": 30.0,
        "MF_Market_Share_pct": 31.5,
        "FO_Curbs_Exposure": "ZERO (0% Direct)",
        "ADV_30D_Cr": 55.0,
        "Moat_Type": "RTA + International Fund Administration"
    }
}

# ==============================================================================
# 2. CAMS 3-STATEMENT INTEGRATED FINANCIAL MODEL
# ==============================================================================

def get_cams_3statement_model():
    years = ["FY22", "FY23", "FY24", "FY25E", "FY26E", "FY27E", "FY28E", "FY29E"]
    
    mf_equity_aus = [18.2, 21.5, 29.8, 38.5, 46.2, 55.4, 65.4, 76.5] # Lakh Cr
    mf_debt_cash_aus = [8.5, 8.8, 9.6, 11.0, 12.1, 13.3, 14.6, 16.0] # Lakh Cr
    
    rev_mf = [825.0, 870.0, 1002.5, 1175.0, 1365.0, 1585.0, 1820.0, 2075.0]
    rev_non_mf = [84.4, 102.4, 134.0, 170.0, 225.0, 295.0, 380.0, 485.0]
    total_rev = [r1 + r2 for r1, r2 in zip(rev_mf, rev_non_mf)]
    
    employee_exp = [318.0, 355.0, 402.0, 470.0, 535.0, 608.0, 688.0, 775.0]
    tech_comm_exp = [105.0, 122.0, 150.0, 178.0, 205.0, 235.0, 268.0, 302.0]
    other_opex = [62.0, 77.0, 75.7, 85.0, 95.0, 106.0, 118.0, 130.0]
    total_opex = [e + t + o for e, t, o in zip(employee_exp, tech_comm_exp, other_opex)]
    
    ebitda = [r - o for r, o in zip(total_rev, total_opex)]
    ebitda_margin = [round(e / r * 100, 2) for e, r in zip(ebitda, total_rev)]
    
    deprec = [48.0, 55.0, 62.0, 70.0, 78.0, 86.0, 95.0, 104.0]
    ebit = [eb - d for eb, d in zip(ebitda, deprec)]
    
    other_income = [28.0, 34.0, 45.0, 58.0, 68.0, 78.0, 90.0, 105.0]
    finance_cost = [7.0, 8.5, 10.0, 11.0, 11.0, 11.0, 11.0, 11.0]
    
    pbt = [eb + oi - fc for eb, oi, fc in zip(ebit, other_income, finance_cost)]
    tax = [round(p * 0.2517, 1) for p in pbt]
    pat = [p - t for p, t in zip(pbt, tax)]
    pat_margin = [round(p / r * 100, 2) for p, r in zip(pat, total_rev)]
    
    cfo = [round(eb * 0.92, 1) for eb in ebitda]
    capex = [round(r * 0.028, 1) for r in total_rev]
    fcf = [round(cf - cx, 1) for cf, cx in zip(cfo, capex)]
    dividends = [round(p * 0.72, 1) for p in pat]
    
    net_worth = [620.0, 740.0, 890.0, 1020.0, 1180.0, 1365.0, 1580.0, 1825.0]
    net_cash = [320.0, 390.0, 485.0, 610.0, 760.0, 940.0, 1160.0, 1420.0]
    roce = [round((eb / (nw - nc + 100)) * 100, 1) for eb, nw, nc in zip(ebit, net_worth, net_cash)]
    roe = [round((p / nw) * 100, 1) for p, nw in zip(pat, net_worth)]
    
    df = pd.DataFrame({
        "Metric": [
            "MF Equity AUS (Lakh Cr)", "MF Debt/Liquid AUS (Lakh Cr)",
            "MF Revenue (INR Cr)", "Non-MF Revenue (INR Cr)", "Total Revenue (INR Cr)",
            "Operating Expenses (INR Cr)", "EBITDA (INR Cr)", "EBITDA Margin (%)",
            "Depreciation (INR Cr)", "EBIT (INR Cr)", "Other Treasury Income (INR Cr)",
            "PBT (INR Cr)", "PAT (INR Cr)", "PAT Margin (%)",
            "Cash Flow from Operations (INR Cr)", "Capex (INR Cr)", "Free Cash Flow (FCF) (INR Cr)",
            "Dividends Paid (INR Cr)", "Net Cash & Equivalents (INR Cr)",
            "RoCE (%)", "RoE (%)"
        ]
    })
    
    for i, yr in enumerate(years):
        df[yr] = [
            mf_equity_aus[i], mf_debt_cash_aus[i],
            rev_mf[i], rev_non_mf[i], total_rev[i],
            total_opex[i], ebitda[i], ebitda_margin[i],
            deprec[i], ebit[i], other_income[i],
            pbt[i], pat[i], pat_margin[i],
            cfo[i], capex[i], fcf[i],
            dividends[i], net_cash[i],
            roce[i], roe[i]
        ]
        
    return df

# ==============================================================================
# 3. DCF VALUATION MODEL FOR CAMS (2-STAGE GROWTH MODEL)
# ==============================================================================

def calculate_dcf():
    """
    Performs institutional 10-year 2-stage DCF valuation for CAMS.
    """
    rf = 0.0685        # India 10Y G-Sec Yield (6.85%)
    erp = 0.0540       # Equity Risk Premium (5.40%)
    beta = 0.75        # Asset-light toll-booth, low market sensitivity
    ke = rf + (beta * erp) # Cost of Equity = 10.90%
    wacc = ke          # 100% equity funded core operations
    terminal_growth = 0.055 # 5.50% terminal growth (India nominal GDP proxy)
    
    # 10-Year Explicit FCF Forecast (FY26E - FY35E) in INR Cr
    fcf_10y = [
        625.5,   # FY26E (+22% growth)
        745.0,   # FY27E (+19% growth)
        885.0,   # FY28E (+19% growth)
        1045.0,  # FY29E (+18% growth)
        1225.0,  # FY30E (+17% growth)
        1415.0,  # FY31E (+15.5% growth)
        1615.0,  # FY32E (+14% growth)
        1825.0,  # FY33E (+13% growth)
        2045.0,  # FY34E (+12% growth)
        2275.0   # FY35E (+11% growth)
    ]
    
    t = np.arange(1, 11)
    discount_factors = 1.0 / ((1.0 + wacc) ** t)
    pv_fcf = np.array(fcf_10y) * discount_factors
    sum_pv_fcf = np.sum(pv_fcf)
    
    # Terminal Value at FY35E
    terminal_fcf = fcf_10y[-1] * (1.0 + terminal_growth)
    terminal_value = terminal_fcf / (wacc - terminal_growth)
    pv_terminal_value = terminal_value / ((1.0 + wacc) ** 10)
    
    # Enterprise Value to Equity Value
    enterprise_value = sum_pv_fcf + pv_terminal_value
    net_cash_fy25e = 610.0 # Net cash & treasury surplus at start of FY26
    equity_value = enterprise_value + net_cash_fy25e
    
    shares_outstanding_cr = 4.93
    fair_value_per_share = equity_value / shares_outstanding_cr
    
    cmp = PEER_DATA["CAMS"]["CMP_INR"]
    upside_pct = ((fair_value_per_share / cmp) - 1.0) * 100.0
    
    return {
        "Risk_Free_Rate": rf,
        "ERP": erp,
        "Beta": beta,
        "Ke_WACC": round(wacc, 4),
        "Terminal_Growth": terminal_growth,
        "Sum_PV_Explicit_FCF_Cr": round(sum_pv_fcf, 2),
        "Terminal_Value_FY35E_Cr": round(terminal_value, 2),
        "PV_Terminal_Value_Cr": round(pv_terminal_value, 2),
        "Enterprise_Value_Cr": round(enterprise_value, 2),
        "Net_Cash_Cr": net_cash_fy25e,
        "Equity_Value_Cr": round(equity_value, 2),
        "DCF_Target_Price_INR": round(fair_value_per_share, 2),
        "CMP_INR": cmp,
        "Upside_pct": round(upside_pct, 2)
    }

# ==============================================================================
# 4. SCENARIO ANALYSIS & SENSITIVITY MATRIX (BULL / BASE / BEAR)
# ==============================================================================

def get_scenario_analysis():
    scenarios = {
        "Bull Case": {
            "Narrative": "Accelerated Financialization: Systematic SIPs reach INR 32,000 Cr/month, Equity AUM grows 22% CAGR, Non-MF (AIF/PMS + CAMSPay) surges at 35% CAGR, operating leverage expands EBITDA margin to 48.0%.",
            "CAMS_FY26E_PAT_Cr": 595.0,
            "Target_PE_Multiple": 52.0,
            "Target_Price_INR": 6280.0,
            "Implied_Upside_Downside_pct": 57.6,
            "Derivatives_Impact": "Zero direct impact; CAMS captures displaced retail cash into systematic equity mutual funds.",
            "Equity_Drawdown_Impact": "+15% market rally expands AUM basis point fees.",
            "Probability": 0.25
        },
        "Base Case": {
            "Narrative": "Steady Compounding: Systematic SIP inflows steady at INR 24,000-26,000 Cr/month, Equity AUM grows 16% CAGR, Non-MF grows 22% CAGR, EBITDA margin stable at 45.5%.",
            "CAMS_FY26E_PAT_Cr": 525.0,
            "Target_PE_Multiple": 48.0,
            "Target_Price_INR": 5120.0,
            "Implied_Upside_Downside_pct": 28.5,
            "Derivatives_Impact": "Zero direct impact.",
            "Equity_Drawdown_Impact": "Normal historical volatility absorbed by monthly SIP rupee-cost averaging.",
            "Probability": 0.50
        },
        "Bear Case": {
            "Narrative": "Defensible Bear Case: 20% equity index correction, retail SIP growth moderates, SEBI mandates 5% incremental TER reduction on RTAs, Non-MF growth decelerates to 10%, EBITDA margin contracts to 41.5%.",
            "CAMS_FY26E_PAT_Cr": 435.0,
            "Target_PE_Multiple": 38.5,
            "Target_Price_INR": 3410.0,
            "Implied_Upside_Downside_pct": -14.4,
            "Derivatives_Impact": "Zero direct impact; superior defensibility vs exchange peers.",
            "Equity_Drawdown_Impact": "AUM contracts 12% (buffered by INR 2.5L Cr annual SIP inflows); dividend yield (3.2%) and net cash floor protect downside.",
            "Probability": 0.25
        }
    }
    
    peer_stress = {
        "BSE": {
            "Derivatives_Shock_30pct": "Catastrophic: F&O transaction fees represent >65% of incremental revenue; PAT drops 38%, P/E de-rates from 65x to 32x -> Stock drawdown -52.0%",
            "Equity_Drawdown_20pct": "Cash delivery turnover drops 25%, clearing volumes drop -> Stock drawdown -28.0%",
            "Combined_Bear_Drawdown_pct": -54.0
        },
        "CDSL": {
            "Derivatives_Shock_30pct": "Minimal direct F&O impact; affects intraday KYC account growth velocity -> Stock drawdown -12.0%",
            "Equity_Drawdown_20pct": "Delivery debit transactions fall 22%, retail IPO demat openings dry up -> Stock drawdown -32.0%",
            "Combined_Bear_Drawdown_pct": -32.0
        },
        "CAMS": {
            "Derivatives_Shock_30pct": "ZERO DIRECT IMPACT. Net positive as speculative churn shifts to long-term mutual fund SIPs -> 0.0% direct earnings impact",
            "Equity_Drawdown_20pct": "Mark-to-market AUM drops 12% (buffered by sticky INR 2.5L Cr annual SIPs); PAT down 10% -> Max drawdown -14.4%",
            "Combined_Bear_Drawdown_pct": -14.4
        },
        "KFintech": {
            "Derivatives_Shock_30pct": "Zero direct F&O impact -> 0.0% direct impact",
            "Equity_Drawdown_20pct": "Domestic equity AUM drops 14%, issuer services slowdown -> Stock drawdown -24.5%",
            "Combined_Bear_Drawdown_pct": -24.5
        }
    }
    
    return scenarios, peer_stress

# ==============================================================================
# 5. INR 500 CRORE POSITION SIZING & EXECUTION FRAMEWORK
# ==============================================================================

def get_position_sizing():
    total_allocation_cr = 500.0
    cams_cmp = PEER_DATA["CAMS"]["CMP_INR"]
    market_cap_cr = PEER_DATA["CAMS"]["Market_Cap_Cr"]
    adv_30d_cr = PEER_DATA["CAMS"]["ADV_30D_Cr"]
    
    allocation_ownership_pct = (total_allocation_cr / market_cap_cr) * 100.0
    total_shares_to_buy = (total_allocation_cr * 1e7) / cams_cmp
    
    tranches = [
        {
            "Tranche": "Tranche 1: Immediate Institutional Anchor",
            "Weight_pct": 40.0,
            "Amount_Cr": 200.0,
            "Execution_Days": 5,
            "Daily_Absorption_Cr": 40.0,
            "Daily_ADV_Participation_pct": round((40.0 / adv_30d_cr) * 100, 1),
            "Trigger_Condition": "At market on IC approval (CMP +/- 2%)"
        },
        {
            "Tranche": "Tranche 2: Valuation Dip Accumulation",
            "Weight_pct": 35.0,
            "Amount_Cr": 175.0,
            "Execution_Days": 5,
            "Daily_Absorption_Cr": 35.0,
            "Daily_ADV_Participation_pct": round((35.0 / adv_30d_cr) * 100, 1),
            "Trigger_Condition": "On any 3-5% market pullback or quarterly result volatility"
        },
        {
            "Tranche": "Tranche 3: Momentum / Non-MF Expansion Catalytic Add",
            "Weight_pct": 25.0,
            "Amount_Cr": 125.0,
            "Execution_Days": 4,
            "Daily_Absorption_Cr": 31.25,
            "Daily_ADV_Participation_pct": round((31.25 / adv_30d_cr) * 100, 1),
            "Trigger_Condition": "On confirmation of Non-MF revenue growth exceeding 25% YoY"
        }
    ]
    
    safe_daily_absorption_cr = adv_30d_cr * 0.15
    days_to_liquidate_full = total_allocation_cr / safe_daily_absorption_cr
    
    exit_triggers = [
        {
            "ID": "TRIGGER_1",
            "Name": "Structural AMC Client Defection",
            "Metric": "CAMS MF AUS Market Share drops below 62.0% (Current: 68.5%)",
            "Rationale": "CAMS's core economic moat is zero AMC switching. In the history of Indian mutual funds, no top-tier AMC has migrated away. If a top-5 AMC departs to KFintech or develops in-house RTA systems, the mission-critical pricing power thesis is fundamentally broken. Mandatory complete liquidation."
        },
        {
            "ID": "TRIGGER_2",
            "Name": "Draconian Regulatory Fee Cap on RTAs",
            "Metric": "SEBI mandates fixed cap on RTA fees slashing blended basis points by >25%",
            "Rationale": "If SEBI eliminates ad-valorem basis point fees and caps RTA processing fees at flat per-transaction rates, operational leverage will permanently compress. Mandatory full liquidation within 5 trading sessions."
        },
        {
            "ID": "TRIGGER_3",
            "Name": "Structural SIP Stagnation & Sustained Net Redemptions",
            "Metric": "Industry gross monthly SIP inflows decline >20% YoY for two consecutive quarters alongside continuous equity net outflows",
            "Rationale": "Invalidates the structural household financialization thesis. Signals macroeconomic balance sheet distress or tax policy reversal away from capital markets. Exit to preserve fund capital."
        }
    ]
    
    return {
        "Total_Allocation_Cr": total_allocation_cr,
        "Ownership_pct_CAMS": round(allocation_ownership_pct, 2),
        "Total_Shares_to_Acquire": int(total_shares_to_buy),
        "ADV_30D_Cr": adv_30d_cr,
        "Days_to_Liquidate_15pct_ADV": round(days_to_liquidate_full, 1),
        "Tranches": tranches,
        "Exit_Triggers": exit_triggers
    }

if __name__ == "__main__":
    print("="*80)
    print("PS1 CAPITAL MARKETS RESEARCH ENGINE: RUNNING CAMS VALUATION & SCENARIOS")
    print("="*80)
    
    dcf_res = calculate_dcf()
    print("\n--- DCF VALUATION SUMMARY ---")
    for k, v in dcf_res.items():
        print(f"  {k:30s}: {v}")
        
    scenarios, peer_stress = get_scenario_analysis()
    print("\n--- SCENARIO ANALYSIS ---")
    for sc, data in scenarios.items():
        print(f"\n[{sc.upper()}] (Prob: {data['Probability']})")
        print(f"  Target Price: INR {data['Target_Price_INR']} ({data['Implied_Upside_Downside_pct']:+.1f}%)")
        print(f"  Rationale: {data['Narrative']}")
        
    pos = get_position_sizing()
    print("\n--- POSITION SIZING FOR INR 500 CR ALLOCATION ---")
    print(f"  Fund Ownership: {pos['Ownership_pct_CAMS']}% of CAMS equity")
    print(f"  Total Shares to Acquire: {pos['Total_Shares_to_Acquire']:,}")
    print(f"  Days to liquidate at 15% ADV: {pos['Days_to_Liquidate_15pct_ADV']} days")
    print("\nEngine executed successfully.")
