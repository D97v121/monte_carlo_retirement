from monte_carlo import simulate_paths, evaluate_outcomes
def run_example() -> None:
    initial_balance = 1_000_000.0
    mean_return = 0.06         # 6 percent average annual return
    volatility = 0.15          # 15 percent standard deviation
    annual_withdrawal = 40_000.0
    inflation = 0.02           # 2 percent inflation
    years = 30
    n_sims = 10_000

    balances = simulate_paths(
        initial_balance=initial_balance,
        mean_return=mean_return,
        volatility=volatility,
        annual_withdrawal=annual_withdrawal,
        inflation=inflation,
        years=years,
        n_sims=n_sims,
        seed=0,
    )

    success_rate, median_ending, p10_ending, p90_ending = evaluate_outcomes(balances)

    print(f"Success rate over {years} years: {success_rate * 100:.1f} percent")
    print(f"Median ending balance: ${median_ending:,.0f}")
    print(f"10th percentile ending balance: ${p10_ending:,.0f}")
    print(f"90th percentile ending balance: ${p90_ending:,.0f}")


if __name__ == "__main__":
    run_example()
