# run/run_particle.py

# run/run_particle.py

from visualizer import (
    plot_particle_field_heatmap,
    most_common_entangled_pairs,
    track_psi_over_time,
    track_actual_psi_over_time
)

from predictors_particle import (
    extract_tail2_digits,
    predict_2digit_particle_field
)

from config import make_rngs  # ✅ ใช้สร้าง local RNG

import pandas as pd
import os
import json



def run_particle_prediction(
    df,
    seed=None,
    np_rng=None,
    save_image=False,
    return_plot_path=False,
    return_metrics=False,   # ✅ เปิดเพื่อขอข้อมูล hit5/hit10/actual/top10
):
    """
    รันทำนายเลขท้าย 2 ตัวด้วย Particle Field (deterministic ด้วย local RNG)
    - ส่ง seed หรือ np_rng เข้ามาอย่างใดอย่างหนึ่ง
    - ไม่แตะ global np.random เพื่อกันชนกันเวลา multi-request
    """
    # ✅ เตรียม RNG แบบ local
    if np_rng is None:
        if seed is None:
            raise ValueError("ต้องส่ง seed หรือ np_rng เพื่อให้ผลเป็น deterministic")
        _, np_rng = make_rngs(seed)

    # ✅ เตรียมข้อมูลย้อนหลังเลขท้าย 2 ตัว
    past_2digit_results = extract_tail2_digits(df)

    # ✅ คำนวณคู่พัวพันจากข้อมูลจริง
    ent_pairs = most_common_entangled_pairs(past_2digit_results, top_k=5)

    # ✅ ทำนายด้วย RNG ที่ส่งมา
    result_df, picks = predict_2digit_particle_field(
        past_2digits=past_2digit_results,
        k=5,
        entangled_pairs=ent_pairs,
        np_rng=np_rng,          # ใช้ local RNG
    )

    # ทำให้คีย์ psi เป็นชื่อสม่ำเสมอ + sort ก่อนแสดง/ตัดหัว
    if "Ψ(n)" in result_df.columns:
        result_df = result_df.rename(columns={"Ψ(n)": "psi"})
    if "psi" in result_df.columns:
        result_df = result_df.sort_values("psi", ascending=False).reset_index(drop=True)

    # 🗓 ข้อมูลงวดล่าสุด (ถ้ามีคอลัมน์ date)
    latest_draw = None
    last2_str = None
    if "date" in df.columns and df["date"].notna().any():
        latest_draw = df[df["date"].notna()].sort_values("date", ascending=False).iloc[0]
        latest_date_str = latest_draw["date"].strftime('%d-%m-%Y') if hasattr(latest_draw["date"], "strftime") else str(latest_draw["date"])
        last2_str = str(latest_draw.get("last2", "")).zfill(2)
        print(f"\n📅 งวดล่าสุด: {latest_date_str} | เลขที่ออก: {last2_str}")

    print("\n🎯 ทำนายเลขท้าย 2 ตัวจาก Particle Field:")
    for p in picks:
        print("🔮", p)

    # ✅ คำนวณ hit ทั้ง Top5/Top10 (ให้ตรงกับที่ API ใช้)
    metrics = None
    if last2_str is not None and "psi" in result_df.columns:
        top10 = result_df.head(10)["number"].astype(str).tolist()
        top10_set = set(top10)
        top5_set = set(map(str, picks))
        top5_hit = last2_str in top5_set
        top10_hit = last2_str in top10_set

        hit_text_5 = "✅ Top5 hit" if top5_hit else "❌ Top5 miss"
        hit_text_10 = "✅ Top10 hit" if top10_hit else "❌ Top10 miss"
        print(f"\n{hit_text_5} | {hit_text_10} (ผลจริง {last2_str})")

        metrics = {
            "actual": last2_str,
            "top5": list(top5_set),
            "top10": top10,
            "hit5": top5_hit,
            "hit10": top10_hit,
        }

    if "psi" in result_df.columns:
        print("\n🔝 Top 10 Ψ(n):")
        print(result_df.head(10))

    print("\n🧬 คู่ entangled ที่พบบ่อยที่สุด:")
    print(ent_pairs)

    # ➕ Save CSV
    output_csv = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "outputs", "particle_field_output.csv")
    )
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    result_df.to_csv(output_csv, index=False)
    print(f"\n📦 บันทึกผลที่: {output_csv}")

    # 📊 Save heatmap image (ปิดค่าเริ่มต้นเพื่อไม่ให้ API ช้า/ค้าง)
    image_path = None
    if save_image:
        image_path = plot_particle_field_heatmap(result_df, filename="particle_field_heatmap.png")

    # ✅ ส่งกลับผลลัพธ์ (compatible เดิม)
    if return_plot_path and return_metrics:
        return result_df, list(picks), image_path, metrics
    elif return_plot_path:
        return result_df, list(picks), image_path
    elif return_metrics:
        return result_df, list(picks), metrics
    else:
        return result_df, list(picks)




# ✅ CLI เรียกตรง
if __name__ == "__main__":
    import sys
    import os
    import json
    import pandas as pd

    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

    # 📥 โหลดจาก JSON
    json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "lotto_110year_full_fixed.json"))
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    df = pd.DataFrame(data)

    # 👇 ใช้ parser แบบไทยถ้ามี
    from data.parse_thai_date import parse_thai_date
    if "date" in df.columns:
        df["date"] = df["date"].apply(parse_thai_date)

    # 🔧 เตรียมคอลัมน์ "3digits"
    digit_cols = ["front3_1", "front3_2", "last3_1", "last3_2", "last3_3"]
    available_cols = [col for col in digit_cols if col in df.columns]
    if available_cols:
        df["3digits"] = df[available_cols].astype(str).values.tolist()
        # ✅ explode ให้ตรง index
        df_expanded = df.explode("3digits").reset_index(drop=True)
        df_expanded["3digits"] = df_expanded["3digits"].astype(str).str.zfill(3)
    else:
        df_expanded = df.copy()

    # 🔁 ป้องกัน date เป็น NaT
    if "date" in df_expanded.columns:
        df_expanded = df_expanded[df_expanded["date"].notna()].copy()

    # 🎯 เรียกฟังก์ชันหลัก (ตัวอย่าง seed คงที่ — ปรับได้)
    if not df_expanded.empty:
        _, np_rng = make_rngs(20250816)
        run_particle_prediction(df_expanded, np_rng=np_rng, save_image=False)
    else:
        print("❌ ไม่มีข้อมูลวันที่ที่ใช้งานได้ (date = NaT ทั้งหมด)")
