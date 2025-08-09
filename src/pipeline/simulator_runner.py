import glob
import os
import pandas as pd
from thai_lottery_simulator_v2 import ThaiLotterySimulatorV2

def run_simulator_and_load_latest_data(seed=2025):
    sim = ThaiLotterySimulatorV2(seed=seed, force_pass_committee=True)
    draw = sim.run(verbose=True)
    draws = sim.draw_history

    csv_list = glob.glob("/Users/apichet/Downloads/lotto_110year_*.csv")
    if not csv_list:
        raise FileNotFoundError("❌ ไม่พบไฟล์ lotto_110year_*.csv ใน Downloads")

    latest_csv = max(csv_list, key=os.path.getctime)
    print(f"📂 โหลดไฟล์: {os.path.basename(latest_csv)}")
    df = pd.read_csv(latest_csv)
    df["3digits"] = df["3digits"].astype(str).str.zfill(3)
    df["date"] = pd.to_datetime(df["date"])

    return sim, draw, draws, df
