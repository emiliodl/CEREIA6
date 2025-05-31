import React, { useState } from 'react';
import './TabPanel.css';
import FilterPanel from './FilterPanel';
import EmailForm from './EmailForm';

function TabPanel({
  // Props para o FilterPanel
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
  isLoading,
  
  // Props para o EmailForm
  carteirinha,
  setCarteirinha,
  medico,
  setMedico,
  onSubmit,
  emailSent,
  emailError,
  
  // Estado dos estudos para controlar botão de enviar
  hasStudies
}) {
  const [activeTab, setActiveTab] = useState('filters');
  
  return (
    <div className="tab-panel">
      <div className="tab-header">
        <button 
          className={`tab-button ${activeTab === 'filters' ? 'active' : ''}`}
          onClick={() => setActiveTab('filters')}
        >
          Filtros
        </button>
        <button 
          className={`tab-button ${activeTab === 'submission' ? 'active' : ''}`}
          onClick={() => setActiveTab('submission')}
        >
          Submissão de Dados
        </button>
      </div>
      
      <div className="tab-content">
        {activeTab === 'filters' && (
          <div className="tab-pane">
            <FilterPanel 
              tumorTypes={tumorTypes}
              selectedTumorType={selectedTumorType}
              setSelectedTumorType={setSelectedTumorType}
              biomarkers={biomarkers}
              selectedBiomarkers={selectedBiomarkers}
              onBiomarkerChange={onBiomarkerChange}
              selectedStaging={selectedStaging}
              setSelectedStaging={setSelectedStaging}
              ecogScore={ecogScore}
              setEcogScore={setEcogScore}
              onApplyFilters={onApplyFilters}
              isLoading={isLoading}
            />
          </div>
        )}
        
        {activeTab === 'submission' && (
          <div className="tab-pane">
            <EmailForm 
              carteirinha={carteirinha}
              setCarteirinha={setCarteirinha}
              medico={medico}
              setMedico={setMedico}
              onSubmit={onSubmit}
              emailSent={emailSent}
              emailError={emailError}
              hasStudies={hasStudies}
            />
          </div>
        )}
      </div>
    </div>
  );
}

export default TabPanel;