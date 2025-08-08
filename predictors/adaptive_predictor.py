from predictors.boosted import generate_boosted_quantum_picks
from predictors.simulation import multi_run_stability
from predictors.interference import generate_multi_wave_top_k
from predictors.reshaped_collapse import generate_rescaled_schrodinger_superposition
from analysis.bias import detect_bias_from_history, detect_blackhole_digits

def adaptive_predictor(context_data, entangled_pairs, wave, monthly_top, results):
    bias_score = detect_bias_from_history(results)
    blackholes = set(detect_blackhole_digits(results))

    print("\n🧠 Adaptive Conditions:")
    print(f"• Entangled Strength = {context_data['entangled_strength']:.3f}")
    print(f"• Stability Score    = {context_data['stability_score']:.3f}")
    print(f"• Bias Score         = {bias_score:.3f}")
    print(f"• Blackhole Count    = {len(blackholes)}")

    if context_data["entangled_strength"] > 0.7:
        print("🔮 Mode: Boosted Quantum Picks")
        return generate_boosted_quantum_picks(entangled_pairs, seed=42)

    elif context_data["stability_score"] > 0.5:
        print("🔮 Mode: Stability Sampling")
        return [x[0] for x in multi_run_stability(seed=42)[:5]]

    elif bias_score > 0.3:
        print("🔮 Mode: Multi-Wave with Blackhole Filter")
        entangled_digits = set(d for pair, _ in entangled_pairs for d in pair)
        candidates = generate_multi_wave_top_k(wave, entangled_digits, monthly_top.to_dict(), k=10)
        filtered = [x for x in candidates if x not in blackholes]
        return filtered[:5] if len(filtered) >= 5 else candidates[:5]

    else:
        print("🔮 Mode: Schrödinger Simulation (default)")
        _, samples = generate_rescaled_schrodinger_superposition(k=5, seed=42)
        return samples
