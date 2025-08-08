# ============================================
# 🚀 Entry Point: Quantum Lotto Main/Users/apichet/quantum_lotto/src/main.py
# ============================================
from utils.data_loader import load_json_data
from pipeline.quantum_runner import run_all_simulations

def main():
    df = load_json_data()
    run_all_simulations(df)

if __name__ == "__main__":
    main()
