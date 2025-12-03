import numpy as np
from typing import Tuple

def simulate_paths(
    initial_balance: float,
    mean_return: float,
    volatility: float,
    annual_withdrawal: float,
    inflation: float,
    years: int,
    n_sims: int,
    seed: int | None = None,
) -> np.ndarray:
    """simulate a given number of possible outcomes given a certain portfolio using a monte carlo model
        the output will include:
                - Success probability
                - Distribution of ending balances
                - Worst-case years
                - Median outcome
                - Charts
    """

    rng = np.random.default_rng(seed)

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
