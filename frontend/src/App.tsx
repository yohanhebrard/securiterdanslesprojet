import React from 'react'

function App() {
  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      backgroundColor: '#0f172a',
      color: 'white',
      fontFamily: 'system-ui, -apple-system, sans-serif',
      padding: '2rem'
    }}>
      <div style={{ textAlign: 'center', maxWidth: '800px' }}>
        <h1 style={{ fontSize: '3rem', marginBottom: '1rem', color: '#60a5fa' }}>
          🔒 SecureShare
        </h1>
        <p style={{ fontSize: '1.5rem', marginBottom: '2rem', color: '#94a3b8' }}>
          Plateforme de Partage de Fichiers Sécurisée
        </p>

        <div style={{
          backgroundColor: '#1e293b',
          padding: '2rem',
          borderRadius: '1rem',
          marginBottom: '2rem',
          border: '1px solid #334155'
        }}>
          <h2 style={{ color: '#22c55e', marginBottom: '1rem' }}>
            ✅ Backend Opérationnel
          </h2>
          <p style={{ color: '#cbd5e1' }}>
            L'infrastructure DevSecOps est démarrée avec succès !
          </p>
        </div>

        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
          gap: '1rem',
          marginTop: '2rem'
        }}>
          <div style={{
            backgroundColor: '#1e293b',
            padding: '1.5rem',
            borderRadius: '0.5rem',
            border: '1px solid #334155'
          }}>
            <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>🔐</div>
            <div style={{ color: '#94a3b8' }}>Chiffrement AES-256</div>
          </div>

          <div style={{
            backgroundColor: '#1e293b',
            padding: '1.5rem',
            borderRadius: '0.5rem',
            border: '1px solid #334155'
          }}>
            <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>🛡️</div>
            <div style={{ color: '#94a3b8' }}>Scan Antivirus</div>
          </div>

          <div style={{
            backgroundColor: '#1e293b',
            padding: '1.5rem',
            borderRadius: '0.5rem',
            border: '1px solid #334155'
          }}>
            <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>⚡</div>
            <div style={{ color: '#94a3b8' }}>Usage Unique</div>
          </div>

          <div style={{
            backgroundColor: '#1e293b',
            padding: '1.5rem',
            borderRadius: '0.5rem',
            border: '1px solid #334155'
          }}>
            <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>📊</div>
            <div style={{ color: '#94a3b8' }}>RGPD Compliant</div>
          </div>
        </div>

        <div style={{ marginTop: '3rem', fontSize: '0.875rem', color: '#64748b' }}>
          <p>🎓 Projet Fil Rouge - Sécurité Intégrée</p>
          <p style={{ marginTop: '0.5rem' }}>
            Consultez <code style={{
              backgroundColor: '#334155',
              padding: '0.25rem 0.5rem',
              borderRadius: '0.25rem',
              color: '#60a5fa'
            }}>GETTING-STARTED.md</code> pour continuer
          </p>
        </div>
      </div>
    </div>
  )
}

export default App
