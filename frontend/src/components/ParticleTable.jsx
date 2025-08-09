// src/components/ParticleTable.jsx
import React from 'react';

function ParticleTable({ data }) {
  if (!data || data.length === 0) return <p className="text-muted">⌛ ยังไม่มีข้อมูล</p>;

  return (
    <div className="table-responsive">
      <table className="table table-bordered table-sm mt-2">
        <thead className="thead-light">
          <tr>
            <th>เลข</th>
            <th>Bias</th>
            <th>Entangled</th>
            <th>Wave</th>
            <th>Ψ(n)</th>
          </tr>
        </thead>
        <tbody>
          {data.map((row, i) => {
            const psi = row.psi ?? row['Ψ(n)'];
            return (
              <tr key={i}>
                <td><strong>{row.number}</strong></td>
                <td>{row.bias !== undefined ? Number(row.bias).toFixed(4) : '-'}</td>
                <td>{row.entangled !== undefined ? Number(row.entangled).toFixed(4) : '-'}</td>
                <td>{row.wave !== undefined ? Number(row.wave).toFixed(4) : '-'}</td>
                <td className="badge-mono">{psi !== undefined ? Number(psi).toFixed(6) : '-'}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

export default ParticleTable;
