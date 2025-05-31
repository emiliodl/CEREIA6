import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './FilterPanel.css';

function FilterPanel({ 
  tumorTypes, 
  selectedTumorType, 
  setSelectedTumorType, 
  biomarkers,
  selectedBiomarkers,
  onBiomarkerChange,
  selectedStaging,
  setSelectedStaging,
  ecogScore,
  setEcogScore,
  onApplyFilters,
  isLoading
}) {
  const [stagingOptions, setStagingOptions] = useState([]);
  
  // Carregar opções de estadiamento formatadas corretamente
  useEffect(() => {
    axios.get('http://localhost:5000/api/staging-options')
      .then(response => setStagingOptions(response.data))
      .catch(error => console.error('Erro ao carregar opções de estadiamento:', error));
  }, []);

  return (
    <div className="filter-panel">
      <h2>Filtros</h2>
      
      <div className="filter-section">
        <label htmlFor="tumor-type">Tipo de tumor:</label>
        <select 
          id="tumor-type" 
          value={selectedTumorType} 
          onChange={(e) => setSelectedTumorType(e.target.value)}
        >
          <option value="">Selecione</option>
          {tumorTypes.map((type) => (
            <option key={type} value={type}>
              {type}
            </option>
          ))}
        </select>
      </div>
      
      <div className="filter-section">
        <label htmlFor="staging">Estadiamento:</label>
        <select 
          id="staging" 
          value={selectedStaging} 
          onChange={(e) => setSelectedStaging(e.target.value)}
        >
          <option value="">Selecione</option>
          {stagingOptions.map((stage) => (
            <option key={stage} value={stage}>
              {stage}
            </option>
          ))}
        </select>
      </div>
      
      <div className="filter-section">
        <label htmlFor="ecog">Escala ECOG:</label>
        <input 
          id="ecog" 
          type="text" 
          value={ecogScore} 
          onChange={(e) => setEcogScore(e.target.value)} 
          placeholder="Informe um valor da escala"
        />
      </div>
      
      {Object.keys(biomarkers).length > 0 && (
        <div className="filter-section biomarkers-section">
          <h3>Biomarcadores</h3>
          
          {Object.entries(biomarkers).map(([biomarker, config]) => (
            <div key={biomarker} className="biomarker-input">
              <label htmlFor={`biomarker-${biomarker}`}>
                {biomarker}:
              </label>
              
              {config.type === 'input' ? (
                <input 
                  id={`biomarker-${biomarker}`}
                  type="text" 
                  value={selectedBiomarkers[biomarker] || ''} 
                  onChange={(e) => onBiomarkerChange(biomarker, e.target.value)} 
                  placeholder={`Insira o valor para ${biomarker} (%)`}
                />
              ) : (
                <select 
                  id={`biomarker-${biomarker}`}
                  value={selectedBiomarkers[biomarker] || ''} 
                  onChange={(e) => onBiomarkerChange(biomarker, e.target.value)}
                >
                  <option value="">Selecione</option>
                  {config.options.map((option) => (
                    <option key={option} value={option}>
                      {option}
                    </option>
                  ))}
                </select>
              )}
            </div>
          ))}
        </div>
      )}
      
      <button 
        className="apply-filters-btn" 
        onClick={onApplyFilters} 
        disabled={isLoading}
      >
        {isLoading ? 'Carregando...' : 'Aplicar Filtros'}
      </button>
    </div>
  );
}

export default FilterPanel;