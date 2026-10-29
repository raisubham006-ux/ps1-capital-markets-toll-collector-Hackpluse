"""
Monte Carlo Simulation & Regulatory Stress-Testing Engine for CAMS vs Peers
Simulates 10,000 trials of capital market scenarios to test portfolio risk for INR 500 Cr allocation.
"""

import sys
import numpy as np
import pandas as pd

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def run_monte_carlo(n_simulations=10000, seed=42):
    np.random.seed(seed)
    
    # Capital Market Variables (Annual Distributions)
    # 1. Broad Market Equity Return (Nifty 50) ~ Normal(mu=12%, sigma=16%)
    market_returns = np.random.normal(loc=0.12, scale=0.16, size=n_simulations)
    
    # 2. Industry Gross Monthly SIP Inflows (INR Cr) ~ Normal(mu=25000, sigma=3000)
    monthly_sips = np.random.normal(loc=25000, scale=3000, size=n_simulations)
    monthly_sips = np.clip(monthly_sips, 16000, 36000)
    annual_sip_inflows_cr = monthly_sips * 12
    
    # 3. Derivatives Volume Growth Factor (Subject to SEBI curbs) ~ Truncated Normal
    # High downside skew due to Oct 2024 circular
    derivatives_growth = np.random.normal(loc=-0.15, scale=0.20, size=n_simulations)
    derivatives_growth = np.clip(derivatives_growth, -0.60, 0.35)
    
    # 4. Regulatory TER Compression (bps) ~ Exponential shock
    reg_fee_cut_bps = np.random.exponential(scale=0.15, size=n_simulations) # basis point cut
    reg_fee_cut_bps = np.clip(reg_fee_cut_bps, 0.0, 0.60)
    
    # -------------------------------------------------------------
    # Simulation: CAMS Return Profile
    # -------------------------------------------------------------
    # CAMS AUM dynamic: Base AUM * (1 + market_return) + Net SIP flow (~75% retained)
    # Beta to market equity is ~0.65; direct F&O impact is 0.0%
    cams_aum_growth = 0.60 * market_returns + (annual_sip_inflows_cr / 3800000) - (reg_fee_cut_bps / 3.0)
    cams_ebitda_growth = cams_aum_growth * 1.08 + 0.04 # Non-MF kicker
    
    # Multiple re-rating based on growth & sentiment
    cams_exit_pe = 45.4 * (1.0 + 0.4 * market_returns)
    cams_exit_pe = np.clip(cams_exit_pe, 32.0, 56.0)
    
    cams_1y_stock_returns = ((1.0 + cams_ebitda_growth) * (cams_exit_pe / 45.4)) - 1.0 + 0.025 # 2.5% div yield
    
    # -------------------------------------------------------------
    # Simulation: BSE Return Profile (High sensitivity to F&O)
    # -------------------------------------------------------------
    # BSE Revenue is heavily driven by options turnover (>65% incremental)
    bse_ebitda_growth = 0.70 * derivatives_growth + 0.30 * market_returns
    bse_exit_pe = 65.2 * (1.0 + 0.8 * derivatives_growth + 0.5 * market_returns)
    bse_exit_pe = np.clip(bse_exit_pe, 26.0, 72.0)
    bse_1y_stock_returns = ((1.0 + bse_ebitda_growth) * (bse_exit_pe / 65.2)) - 1.0 + 0.012
    
    # Summary Risk Metrics
    cams_mean_ret = np.mean(cams_1y_stock_returns)
    cams_median_ret = np.median(cams_1y_stock_returns)
    cams_var_95 = np.percentile(cams_1y_stock_returns, 5)
    cams_var_99 = np.percentile(cams_1y_stock_returns, 1)
    cams_prob_positive = np.mean(cams_1y_stock_returns > 0)
    
    bse_mean_ret = np.mean(bse_1y_stock_returns)
    bse_median_ret = np.median(bse_1y_stock_returns)
    bse_var_95 = np.percentile(bse_1y_stock_returns, 5)
    bse_var_99 = np.percentile(bse_1y_stock_returns, 1)
    bse_prob_positive = np.mean(bse_1y_stock_returns > 0)
    
    print("="*80)
    print(f"MONTE CARLO SIMULATION RESULTS ({n_simulations:,} TRIALS)")
    print("="*80)
    print(f"{'Metric':<35} | {'CAMS (Recommended)':<20} | {'BSE Ltd (High Risk)':<20}")
    print("-" * 80)
    print(f"{'Mean Expected 1Y Return':<35} | {cams_mean_ret*100:>18.2f}% | {bse_mean_ret*100:>18.2f}%")
    print(f"{'Median 1Y Return':<35} | {cams_median_ret*100:>18.2f}% | {bse_median_ret*100:>18.2f}%")
    print(f"{'Probability of Positive Return':<35} | {cams_prob_positive*100:>18.1f}% | {bse_prob_positive*100:>18.1f}%")
    print(f"{'Value at Risk (VaR 95% 1-Year)':<35} | {cams_var_95*100:>18.2f}% | {bse_var_95*100:>18.2f}%")
    print(f"{'Value at Risk (VaR 99% 1-Year)':<35} | {cams_var_99*100:>18.2f}% | {bse_var_99*100:>18.2f}%")
    print("-" * 80)
    print(f"INR 500 Cr Portfolio VaR (95% 1Y)   | -INR {abs(cams_var_95)*500:>14.2f} Cr | -INR {abs(bse_var_95)*500:>14.2f} Cr")
    print("="*80)
    
    return {
        "cams_mean": cams_mean_ret,
        "cams_var95": cams_var_95,
        "bse_mean": bse_mean_ret,
        "bse_var95": bse_var_95
    }

if __name__ == "__main__":
    run_monte_carlo()
