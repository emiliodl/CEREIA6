import React from 'react';
import './CriteriaPanel.css';

function CriteriaPanel({ studies }) {
  if (!studies.length) {
    return (
      <div className="card criteria-panel">
        <div className="card-header">
          <h2>Critérios de Inclusão/Exclusão</h2>
        </div>
        <div className="card-body empty-criteria">
          <div className="empty-criteria-icon">📋</div>
          <p>Nenhum estudo compatível encontrado para exibir critérios.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="card criteria-panel">
      <div className="card-header">
        <h2>Critérios de Inclusão/Exclusão</h2>
      </div>
      <div className="criteria-scrollable">
        {studies.map((study) => (
          <div key={study.nctId} className="criteria-item">
            <div className="criteria-header">
              <a 
                href={`https://clinicaltrials.gov/study/${study.nctId}`}
                target="_blank"
                rel="noopener noreferrer"
              >
                {study.nctId}
              </a>
            </div>
            <div className="criteria-content">
              <p className="criteria-title">Critérios de elegibilidade:</p>
              <p>{study.eligibilityCriteria}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default CriteriaPanel;