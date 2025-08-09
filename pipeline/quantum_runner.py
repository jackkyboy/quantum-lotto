from run.run_particle import run_particle_prediction
from run.run_schrodinger import run_schrodinger_simulation, run_unitary_collapse, run_backtest
from run.run_visualizations import run_quantum_field_visualizations
from ml.features import add_date_features, add_digit_features
from ml.model_pipeline import run_ml_pipeline
from config import get_seed


def run_all_simulations(df):
    lock_seed(get_seed())

    # Run Particle Prediction
    run_particle_prediction(df)

    # Schrödinger Simulation
    run_schrodinger_simulation(df)
    run_unitary_collapse()
    run_backtest(df)

    # Quantum Field Visualization
    run_quantum_field_visualizations()

    # ML Pipeline
    df = add_date_features(df)
    df = add_digit_features(df)
    run_ml_pipeline(df)
