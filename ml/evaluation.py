import matplotlib.pyplot as plt
import pandas as pd
from typing import List, Union

def match_predictions_to_winning(
    predictions: Union[list, pd.Series],
    actual_results: Union[list, pd.Series],
    export_csv_path: str = "matched_predictions.csv"
) -> List[str]:
    matched = [p for p in predictions if p in actual_results]
    print(f"\n✅ Matches Found: {len(matched)} / {len(predictions)}")
    for m in matched:
        print(f"🎯 Matched: {m}")

    df = pd.DataFrame({"prediction": predictions})
    df["matched"] = df["prediction"].isin(actual_results)
    df.to_csv(export_csv_path, index=False)
    print(f"📦 Exported match results to {export_csv_path}")

    plt.figure(figsize=(10, 4))
    plt.bar(df["prediction"], df["matched"].astype(int), color=["green" if x else "grey" for x in df["matched"]])
    plt.title("🎯 Match Predictions Visualization")
    plt.xlabel("Predicted Numbers")
    plt.ylabel("Match (1=True, 0=False)")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.show()

    return matched
