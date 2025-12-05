from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Scenario
from .monte_carlo import simulate_paths, summarize_for_json

PARAMS = {
    "initial_balance": float,
    "mean_return": float,
    "volatility": float,
    "annual_withdrawal": float,
    "inflation": float,
    "years": int,
    "n_sims": int,
}

DEFAULTS = {
    "initial_balance": 1000000,
    "mean_return": 0.06,
    "volatility": 0.15,
    "annual_withdrawal": 40000,
    "inflation": 0.02,
    "years": 30,
    "n_sims": 1000,
}

def extract_params_from_mapping(data):
    """Takes something dict-like (request.GET or request.POST) and returns cleaned params."""
    return {
        key: cast(data.get(key, DEFAULTS[key]))
        for key, cast in PARAMS.items()
    }

def extract_params(request):
    # kept for the API (uses GET)
    return extract_params_from_mapping(request.GET)

def home(request):
    if request.method == "POST":
        try:
            params = extract_params_from_mapping(request.POST)
        except ValueError:
            # you could render with an error message here instead
            return JsonResponse({"error": "Invalid form parameters"}, status=400)

        name = request.POST.get("name") or "My Scenario"

        Scenario.objects.create(
            name=name,
            initial_balance=params["initial_balance"],
            mean_return=params["mean_return"],
            volatility=params["volatility"],
            annual_withdrawal=params["annual_withdrawal"],
            inflation=params["inflation"],
            years=params["years"],
            n_sims=params["n_sims"],
        )

        return redirect("scenario_list")

    # GET request: just render the sliders page
    context = {
        "default_initial_balance": DEFAULTS["initial_balance"],
        "default_mean_return": DEFAULTS["mean_return"],
        "default_volatility": DEFAULTS["volatility"],
        "default_annual_withdrawal": DEFAULTS["annual_withdrawal"],
        "default_inflation": DEFAULTS["inflation"],
        "default_years": DEFAULTS["years"],
        "default_n_sims": DEFAULTS["n_sims"],
    }
    return render(request, "simulator/home.html", context)


def scenario_list(request):
    scenarios = Scenario.objects.all().order_by("-created_at")
    return render(request, "simulator/scenario_list.html", {"scenarios": scenarios})


def api_simulate(request):
    try:
        params = extract_params(request)
    except ValueError:
        return JsonResponse({"error": "Invalid parameters"}, status=400)

    balances = simulate_paths(**params)

    data = summarize_for_json(balances)

    return JsonResponse(data)
