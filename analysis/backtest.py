# src/analysis/backtest.py

from collections import Counter

def backtest_schr_simulation(past_results, top_k=10):
    """
    ใช้ผลลัพธ์ Schrödinger มาย้อนตรวจสอบกับข้อมูลจริง

    Parameters:
        past_results (list of str): ผล 3 ตัวจริงย้อนหลัง
        top_k (int): จำนวนที่เลือกมาทำนาย

    Returns:
        hits (list): รายการที่ตรง
        top_preds (list): เลขที่ใช้ทำนาย
    """
    c = Counter(past_results)
    top_preds = [num for num, _ in c.most_common(top_k)]
    hits = [n for n in past_results if n in top_preds]
    return hits, top_preds
