import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import TabPanel from './components/TabPanel';
import StudiesTable from './components/StudiesTable';
import CriteriaPanel from './components/CriteriaPanel';

const API_URL = 'http://localhost:5000/api';

function App() {
  const [tumorTypes, setTumorTypes] = useState([]);
  const [selectedTumorType, setSelectedTumorType] = useState('');
  const [biomarkers, setBiomarkers] = useState({});
  const [selectedBiomarkers, setSelectedBiomarkers] = useState({});
  const [selectedStaging, setSelectedStaging] = useState('');
  const [ecogScore, setEcogScore] = useState('');
  const [studies, setStudies] = useState([]);
  const [filteredStudies, setFilteredStudies] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  
  // Estado para formulário de email
  const [carteirinha, setCarteirinha] = useState('');
  const [medico, setMedico] = useState('');
  const [emailSent, setEmailSent] = useState(false);
  const [emailError, setEmailError] = useState('');

  useEffect(() => {
    // Carregar tipos de tumor
    axios.get(`${API_URL}/tumor-types`)
      .then(response => setTumorTypes(response.data))
      .catch(error => console.error('Erro ao carregar tipos de tumor:', error));
  }, []);

  // Carregar biomarcadores quando o tipo de tumor é selecionado
  useEffect(() => {
    if (selectedTumorType) {
      axios.get(`${API_URL}/biomarkers?tumor_type=${selectedTumorType}`)
        .then(response => setBiomarkers(response.data))
        .catch(error => console.error('Erro ao carregar biomarcadores:', error));
    } else {
      setBiomarkers({});
      setSelectedBiomarkers({});
    }
  }, [selectedTumorType]);

  // Função para aplicar filtros
  const applyFilters = () => {
    setIsLoading(true);
    
    axios.post(`${API_URL}/studies`, {
      tipo_tumor: selectedTumorType,
      estadiamento: selectedStaging,
      valor_ecog: ecogScore,
      biomarcadores: selectedBiomarkers
    })
    .then(response => {
      setStudies(response.data);
      setFilteredStudies(response.data.filter(study => study.biomarcador_match));
      setIsLoading(false);
    })
    .catch(error => {
      console.error('Erro ao buscar estudos:', error);
      setIsLoading(false);
    });
  };

  const handleBiomarkerChange = (biomarker, value) => {
    setSelectedBiomarkers(prev => ({
      ...prev,
      [biomarker]: value
    }));
  };

  const handleSendEmail = () => {
    if (!carteirinha.trim()) {
      setEmailError('Por favor, informe o número da carteirinha');
      return;
    }

    const idsEstudos = studies.map(study => study.nctId);
    
    axios.post(`${API_URL}/send-email`, {
      carteirinha,
      medico,
      filtros: {
        tipo_tumor: selectedTumorType,
        estadiamento: selectedStaging,
        valor_ecog: ecogScore,
        biomarcadores: selectedBiomarkers
      },
      ids_estudos: idsEstudos
    })
    .then(response => {
      if (response.data.success) {
        setEmailSent(true);
        setEmailError('');
      } else {
        setEmailError('Falha ao enviar o email');
      }
    })
    .catch(error => {
      console.error('Erro ao enviar email:', error);
      setEmailError('Erro ao enviar o email');
    });
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>Interface de Estudos Clínicos</h1>
      </header>
      
      <div className="main-content">
        <div className="filter-column">
          <TabPanel 
            // Props para FilterPanel
            tumorTypes={tumorTypes}
            selectedTumorType={selectedTumorType}
            setSelectedTumorType={setSelectedTumorType}
            biomarkers={biomarkers}
            selectedBiomarkers={selectedBiomarkers}
            onBiomarkerChange={handleBiomarkerChange}
            selectedStaging={selectedStaging}
            setSelectedStaging={setSelectedStaging}
            ecogScore={ecogScore}
            setEcogScore={setEcogScore}
            onApplyFilters={applyFilters}
            isLoading={isLoading}
            
            // Props para EmailForm
            carteirinha={carteirinha}
            setCarteirinha={setCarteirinha}
            medico={medico}
            setMedico={setMedico}
            onSubmit={handleSendEmail}
            emailSent={emailSent}
            emailError={emailError}
            
            // Estado dos estudos
            hasStudies={studies.length > 0}
          />
        </div>
        
        <div className="results-column">
          <StudiesTable studies={studies} isLoading={isLoading} />
        </div>
        
        <div className="criteria-column">
          <CriteriaPanel studies={filteredStudies} />
        </div>
      </div>
    </div>
  );
}

export default App;
