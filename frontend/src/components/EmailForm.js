import React from 'react';
import './EmailForm.css';

function EmailForm({ 
  carteirinha, 
  setCarteirinha, 
  medico, 
  setMedico, 
  onSubmit,
  emailSent,
  emailError,
  hasStudies
}) {
  return (
    <div className="email-form">
      <div className="form-group">
        <label htmlFor="carteirinha">Carteirinha</label>
        <input 
          id="carteirinha"
          type="text" 
          value={carteirinha} 
          onChange={(e) => setCarteirinha(e.target.value)} 
          placeholder="Informe o número da carteirinha"
        />
      </div>
      
      <div className="form-group">
        <label htmlFor="medico">Médico</label>
        <input 
          id="medico"
          type="text" 
          value={medico} 
          onChange={(e) => setMedico(e.target.value)} 
          placeholder="Nome do médico responsável"
        />
      </div>
      
      <div className="button-container">
        <button 
          className="submit-btn" 
          onClick={onSubmit}
          disabled={emailSent || !hasStudies}
        >
          {emailSent ? 'Enviado' : 'Enviar'}
        </button>
      </div>
      
      {!hasStudies && (
        <div className="warning-message">
          <span className="warning-icon">⚠</span>
          <span>Aplique filtros e busque estudos antes de enviar dados</span>
        </div>
      )}
      
      {emailSent && (
        <div className="success-message">
          <span className="message-icon">✓</span>
          Email enviado com sucesso!
        </div>
      )}
      
      {emailError && (
        <div className="error-message">
          <span className="message-icon">⚠</span>
          {emailError}
        </div>
      )}
    </div>
  );
}

export default EmailForm;