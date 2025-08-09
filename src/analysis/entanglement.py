from collections import defaultdict

def find_entangled_pairs(series):
    pairs = defaultdict(int)
    for val in series:
        if not isinstance(val, str):
            continue
        digits = set(val)
        for d1 in digits:
            for d2 in digits:
                if d1 != d2:
                    key = tuple(sorted((d1, d2)))
                    pairs[key] += 1
    return sorted(pairs.items(), key=lambda x: -x[1])
