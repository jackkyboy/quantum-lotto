def extract_paradox_numbers(freq_top10, entangled_list, schr_top10, backtest_hits, verbose=False):
    freq_set = set(str(x[0]).zfill(3) for x in freq_top10)
    entangled_set = set(str(x).zfill(3) for x in entangled_list)
    schr_set = set(str(x[0]).zfill(3) for x in schr_top10)
    backtest_set = set(str(k).zfill(3) for k in backtest_hits.keys())

    missed_by_model = backtest_set - schr_set
    predicted_never_hit = schr_set - backtest_set
    simulation_outlier = schr_set - (freq_set | entangled_set)

    paradoxical_numbers = missed_by_model | predicted_never_hit | simulation_outlier

    if verbose:
        print("\n🌀 Paradox Numbers (Model vs Reality):")
        for n in sorted(paradoxical_numbers):
            print(f"❗ {n}")

    return sorted(paradoxical_numbers)
