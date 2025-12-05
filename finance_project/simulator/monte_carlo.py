import numpy as np
from typing import Tuple
from typing import Tuple, Dict, Any


def simulate_paths(
    initial_balance: float,
    mean_return: float,
    volatility: float,
    annual_withdrawal: float,
    inflation: float,
    years: int,
    n_sims: int,
) -> np.ndarray:
    """simulate a given number of possible outcomes given a certain portfolio using a monte carlo model
        the output will include:
                - Success probability
                - Distribution of ending balances
                - Worst-case years
                - Median outcome
                - Charts
    """

    rng = np.random.default_rng()

    #balance table from initial year to year t
    balances = np.zeros((n_sims, years + 1), dtype=float)
    balances[:, 0] = initial_balance

    #withdrawal per year
    current_withdrawal = annual_withdrawal


    #one simulation for each year the portfolio exitsts
    for year in range(1, years + 1):
        # takes the estimated return and adds volatility for a given number of simulations
        annual_returns = rng.normal(loc=mean_return, scale=volatility, size=n_sims)

        # Apply return, then withdrawal
        prev_balance = balances[:, year - 1]
        new_balance = prev_balance * (1.0 + annual_returns) - current_withdrawal

        # Portfolio cannot go below zero
        new_balance = np.maximum(new_balance, 0.0)

        balances[:, year] = new_balance

        current_withdrawal *= (1.0 + inflation)

    return balances


def evaluate_outcomes(balances: np.ndarray) -> Tuple[float, float, float, float]:
    """
    Evaluate Monte Carlo outcomes.

    Success is defined as having a positive balance at the final year.

    Returns
    -------
    success_rate : float
        Fraction of simulations that ended with money left.
    median_ending : float
        50th percentile of ending balances.
    p10_ending : float
        10th percentile of ending balances.
    p90_ending : float
        90th percentile of ending balances.
    """
    ending_balances = balances[:, -1]
    success_rate = float(np.mean(ending_balances > 0.0))

    median_ending = float(np.percentile(ending_balances, 50))
    p10_ending = float(np.percentile(ending_balances, 10))
    p90_ending = float(np.percentile(ending_balances, 90))

    return success_rate, median_ending, p10_ending, p90_ending

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
    )

    success_rate, median_ending, p10_ending, p90_ending = evaluate_outcomes(balances)

    print(f"Success rate over {years} years: {success_rate * 100:.1f} percent")
    print(f"Median ending balance: ${median_ending:,.0f}")
    print(f"10th percentile ending balance: ${p10_ending:,.0f}")
    print(f"90th percentile ending balance: ${p90_ending:,.0f}")


if __name__ == "__main__":
    run_example()


def summarize_for_json(balances: np.ndarray) -> Dict[str, Any]:
    """
    Convenience helper to turn Monte Carlo results into JSON friendly data.
    """
    success_rate, median_ending, p10_ending, p90_ending = evaluate_outcomes(balances)

    ending_balances = balances[:, -1]
    median_idx = int(np.argsort(ending_balances)[len(ending_balances) // 2])
    median_path = balances[median_idx, :].tolist()   # ndarray -> list

    return {
        "success_rate": float(success_rate),
        "median_ending": float(median_ending),
        "p10_ending": float(p10_ending),
        "p90_ending": float(p90_ending),
        "median_path": median_path,
    }