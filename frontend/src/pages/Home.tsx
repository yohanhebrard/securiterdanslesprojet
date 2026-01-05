import React from 'react';
import { useNavigate } from 'react-router-dom';

const Home: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-slate-900 flex flex-col items-center justify-center p-8">
      <div className="max-w-4xl w-full text-center">
        {/* Header */}
        <div className="mb-12">
          <h1 className="text-6xl font-bold text-blue-400 mb-4">
            🔒 SecureShare
          </h1>
          <p className="text-2xl text-slate-400">
            Partage de Fichiers Sécurisé & Éphémère
          </p>
        </div>

        {/* Main CTA */}
        <div className="bg-slate-800 rounded-2xl p-8 border border-slate-700 mb-8">
          <h2 className="text-3xl font-semibold text-white mb-6">
            Partagez vos fichiers en toute sécurité
          </h2>
          <p className="text-slate-300 mb-8 text-lg">
            Téléchargement unique • Chiffrement AES-256 • Scan antivirus • Auto-destruction
          </p>
          <button
            onClick={() => navigate('/upload')}
            className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-4 px-8 rounded-lg text-xl transition-colors duration-200 shadow-lg hover:shadow-xl"
          >
            📤 Partager un Fichier
          </button>
        </div>

        {/* Security Features */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-12">
          <div className="bg-slate-800 p-6 rounded-lg border border-slate-700">
            <div className="text-4xl mb-3">🔐</div>
            <h3 className="text-white font-semibold mb-2">Chiffrement</h3>
            <p className="text-slate-400 text-sm">AES-256-GCM end-to-end</p>
          </div>

          <div className="bg-slate-800 p-6 rounded-lg border border-slate-700">
            <div className="text-4xl mb-3">🛡️</div>
            <h3 className="text-white font-semibold mb-2">Antivirus</h3>
            <p className="text-slate-400 text-sm">Scan ClamAV automatique</p>
          </div>

          <div className="bg-slate-800 p-6 rounded-lg border border-slate-700">
            <div className="text-4xl mb-3">⚡</div>
            <h3 className="text-white font-semibold mb-2">Usage Unique</h3>
            <p className="text-slate-400 text-sm">Auto-destruction après téléchargement</p>
          </div>

          <div className="bg-slate-800 p-6 rounded-lg border border-slate-700">
            <div className="text-4xl mb-3">📊</div>
            <h3 className="text-white font-semibold mb-2">RGPD</h3>
            <p className="text-slate-400 text-sm">Anonymisation des données</p>
          </div>
        </div>

        {/* How it works */}
        <div className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
          <h3 className="text-xl font-semibold text-white mb-4">Comment ça marche ?</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-left">
            <div>
              <div className="bg-blue-600 text-white w-8 h-8 rounded-full flex items-center justify-center font-bold mb-3">1</div>
              <h4 className="text-white font-medium mb-2">Téléchargez</h4>
              <p className="text-slate-400 text-sm">Sélectionnez votre fichier (max 100 MB)</p>
            </div>
            <div>
              <div className="bg-blue-600 text-white w-8 h-8 rounded-full flex items-center justify-center font-bold mb-3">2</div>
              <h4 className="text-white font-medium mb-2">Partagez</h4>
              <p className="text-slate-400 text-sm">Recevez un lien sécurisé unique</p>
            </div>
            <div>
              <div className="bg-blue-600 text-white w-8 h-8 rounded-full flex items-center justify-center font-bold mb-3">3</div>
              <h4 className="text-white font-medium mb-2">Auto-destruction</h4>
              <p className="text-slate-400 text-sm">Le fichier est supprimé après le téléchargement</p>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="mt-12 text-slate-500 text-sm">
          <p>🎓 Projet Fil Rouge - Sécurité Intégrée dès la Conception</p>
          <p className="mt-2">
            Conforme OWASP Top 10 • ISO 27001 • RGPD
          </p>
        </div>
      </div>
    </div>
  );
};

export default Home;
