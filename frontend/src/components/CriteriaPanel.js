import React from 'react';
import './CriteriaPanel.css';

function CriteriaPanel({ studies }) {
  if (!studies.length) {
    return (
      <div className="criteria-panel">
        <h2>Critérios de Inclusão/Exclusão</h2>
        <p>Nenhum estudo compatível encontrado.</p>
      </div>
    );
  }

  return (
    <div className="criteria-panel">
      <h2>Critérios de Inclusão/Exclusão</h2>
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
              <p>{study.eligibilityCriteria}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default CriteriaPanel;