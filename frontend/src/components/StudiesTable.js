import React from 'react';
import './StudiesTable.css';

function StudiesTable({ studies, isLoading }) {
  if (isLoading) {
    return <div className="loading">Carregando estudos...</div>;
  }

  if (!studies.length) {
    return <div className="no-studies">Nenhum estudo encontrado com os critérios selecionados.</div>;
  }

  return (
    <div className="studies-table-container">
      <h2>Estudos compatíveis ({studies.length})</h2>
      <div className="scrollable-table">
        <table className="studies-table">
          <thead>
            <tr>
              <th>NCT ID</th>
              <th>Título</th>
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
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default StudiesTable;