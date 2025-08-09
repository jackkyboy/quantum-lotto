def god_tier_numbers(past_hits, entangled_digits, schrodinger_preds):
    return [
        num for num in schrodinger_preds
        if num in past_hits and any(d in num for d in entangled_digits)
    ]

def extract_god_tier_numbers(freq_top10, entangled_list, schr_top10, backtest_hits):
    freq_set = set([x[0] for x in freq_top10])
    entangled_set = set(entangled_list)
    schr_set = set([x[0] for x in schr_top10])
    backtest_set = set(backtest_hits.keys())

    god_numbers = freq_set & entangled_set & backtest_set
    if not god_numbers:
        god_numbers = (freq_set & schr_set) | (entangled_set & backtest_set)
    return sorted(god_numbers)
