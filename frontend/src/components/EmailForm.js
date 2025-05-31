import React from 'react';
import './EmailForm.css';

function EmailForm({ 
  carteirinha, 
  setCarteirinha, 
  medico, 
  setMedico, 
  onSubmit,
  emailSent,
  emailError 
}) {
  return (
    <div className="email-form">
      <div className="form-group">
        <label htmlFor="carteirinha">Carteirinha:</label>
        <input 
          id="carteirinha"
          type="text" 
          value={carteirinha} 
          onChange={(e) => setCarteirinha(e.target.value)} 
        />
      </div>
      
      <div className="form-group">
        <label htmlFor="medico">Médico:</label>
        <input 
          id="medico"
          type="text" 
          value={medico} 
          onChange={(e) => setMedico(e.target.value)} 
        />
      </div>
      
      <button 
        className="submit-btn" 
        onClick={onSubmit}
        disabled={emailSent}
      >
        Enviar
      </button>
      
      {emailSent && (
        <div className="success-message">Email enviado com sucesso!</div>
      )}
      
      {emailError && (
        <div className="error-message">{emailError}</div>
      )}
    </div>
  );
}

export default EmailForm;