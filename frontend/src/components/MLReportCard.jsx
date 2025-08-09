// /Users/apichet/quantum_lotto/frontend/src/components/MLReportCard.jsx
import React from 'react';

const pct = (v) => (typeof v === 'number' ? (v * 100).toFixed(2) + '%' : 'N/A');
const badgeClass = (v) => {
  if (typeof v !== 'number') return 'badge bg-secondary';
  if (v >= 0.9) return 'badge bg-success';
  if (v >= 0.7) return 'badge bg-info';
  if (v >= 0.5) return 'badge bg-warning text-dark';
  return 'badge bg-danger';
};

function MLReportCard({ accuracy = {} }) {
  const { logreg, rf, xgb } = accuracy || {};
  return (
    <div className="card">
      <div className="card-body">
        <h6 className="card-title mb-3">🤖 ML Model Accuracy</h6>
        <ul className="list-unstyled mb-0">
          <li className="mb-1">Logistic Regression: <span className={badgeClass(logreg)}>{pct(logreg)}</span></li>
          <li className="mb-1">Random Forest: <span className={badgeClass(rf)}>{pct(rf)}</span></li>
          <li>	XGBoost: <span className={badgeClass(xgb)}>{pct(xgb)}</span></li>
        </ul>
      </div>
    </div>
  );
}

export default MLReportCard;
