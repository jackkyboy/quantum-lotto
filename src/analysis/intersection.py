from collections import Counter

def intersect_particle_schrodinger(particle_df, schrodinger_samples, top_n=10):
    top_particle_2digits = particle_df.head(top_n)["number"].tolist()
    tail2_from_sch = [n[-2:] for n in schrodinger_samples]
    tail2_counts = Counter(tail2_from_sch)

    intersected = [(n, tail2_counts[n]) for n in top_particle_2digits if n in tail2_counts]

    print("\n🔗 เลข 2 หลักที่ซ้อนกันระหว่าง Particle Field และ Schrödinger:")
    for n, count in intersected:
        print(f"🎯 {n} → ปรากฏ {count} ครั้งใน Schrödinger Collapse")

    return intersected
