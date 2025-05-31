import React from 'react';
import './StudiesTable.css';

function StudiesTable({ studies, isLoading }) {
  if (isLoading) {
    return (
      <div className="card">
        <div className="card-header">
          <h2>Estudos</h2>
        </div>
        <div className="card-body loading">
          <div className="loading-icon"></div>
          <p>Carregando estudos...</p>
        </div>
      </div>
    );
  }

  if (!studies.length) {
    return (
      <div className="card">
        <div className="card-header">
          <h2>Estudos</h2>
        </div>
        <div className="card-body no-studies">
          <div className="no-studies-icon">🔍</div>
          <p>Nenhum estudo encontrado com os critérios selecionados.</p>
          <p>Tente ajustar os filtros de busca.</p>
        </div>
      </div>
    );
  }

  const matchingStudies = studies.filter(study => study.biomarcador_match).length;

  return (
    <div className="card studies-table-container">
      <div className="card-header">
        <h2>Estudos ({studies.length}) <small>| {matchingStudies} compatíveis</small></h2>
      </div>
      <div className="scrollable-table">
        <table className="studies-table">
          <thead>
            <tr>
              <th>NCT ID</th>
              <th>Título</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {studies.map((study) => (
              <tr 
                key={study.nctId} 
                className={study.biomarcador_match ? 'matching-study' : 'non-matching-study'}
              >
                <td>
                  <a 
                    href={`https://clinicaltrials.gov/study/${study.nctId}`}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    {study.nctId}
                  </a>
                </td>
                <td>{study.briefTitle}</td>
                <td>
                  {study.biomarcador_match ? (
                    <span className="study-badge badge-match">Compatível</span>
                  ) : (
                    <span className="study-badge badge-no-match">Não compatível</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default StudiesTable;