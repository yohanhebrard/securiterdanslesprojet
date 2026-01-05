import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

interface FileInfo {
  filename: string;
  file_size: number;
  mime_type: string;
  uploaded_at: string;
  expires_at: string;
  is_available: boolean;
  antivirus_status: string;
}

const Download: React.FC = () => {
  const { token } = useParams<{ token: string }>();
  const navigate = useNavigate();

  const [loading, setLoading] = useState(true);
  const [fileInfo, setFileInfo] = useState<FileInfo | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [downloading, setDownloading] = useState(false);
  const [downloaded, setDownloaded] = useState(false);

  useEffect(() => {
    if (token) {
      fetchFileInfo();
    }
  }, [token]);

  const fetchFileInfo = async () => {
    try {
      const response = await axios.get<FileInfo>(
        `${API_URL}/api/v1/download/info/${token}`
      );
      setFileInfo(response.data);
      setError(null);
    } catch (err: any) {
      console.error('Error fetching file info:', err);
      if (err.response?.status === 404) {
        setError('Fichier introuvable');
      } else if (err.response?.status === 410) {
        setError(err.response.data.detail || 'Fichier non disponible');
      } else {
        setError('Erreur lors de la récupération des informations');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = async () => {
    if (!token) return;

    setDownloading(true);
    setError(null);

    try {
      const response = await axios.get(
        `${API_URL}/api/v1/download/${token}`,
        {
          responseType: 'blob',
        }
      );

      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', fileInfo?.filename || 'download');
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);

      setDownloaded(true);
    } catch (err: any) {
      console.error('Download error:', err);
      if (err.response?.status === 410) {
        setError('Ce fichier a déjà été téléchargé ou a expiré');
      } else {
        setError('Erreur lors du téléchargement');
      }
    } finally {
      setDownloading(false);
    }
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
  };

  const formatDate = (dateString: string): string => {
    const date = new Date(dateString);
    return date.toLocaleString('fr-FR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-900 flex items-center justify-center">
        <div className="text-center">
          <div className="text-6xl mb-4 animate-pulse">📦</div>
          <p className="text-white text-xl">Chargement...</p>
        </div>
      </div>
    );
  }

  if (error && !fileInfo) {
    return (
      <div className="min-h-screen bg-slate-900 p-8">
        <div className="max-w-2xl mx-auto">
          <button
            onClick={() => navigate('/')}
            className="text-blue-400 hover:text-blue-300 mb-8 flex items-center gap-2"
          >
            ← Retour à l'accueil
          </button>
          <div className="bg-red-900/30 border border-red-500 rounded-xl p-12 text-center">
            <div className="text-6xl mb-4">❌</div>
            <h2 className="text-2xl font-bold text-white mb-4">
              Fichier Non Disponible
            </h2>
            <p className="text-red-400 text-lg">{error}</p>
          </div>
        </div>
      </div>
    );
  }

  if (downloaded) {
    return (
      <div className="min-h-screen bg-slate-900 p-8">
        <div className="max-w-2xl mx-auto">
          <div className="bg-green-900/20 border border-green-500 rounded-xl p-12 text-center">
            <div className="text-6xl mb-4">✅</div>
            <h2 className="text-2xl font-bold text-white mb-4">
              Téléchargement Réussi !
            </h2>
            <p className="text-slate-400 mb-6">
              Le fichier a été téléchargé et déchiffré avec succès.
            </p>
            <div className="bg-yellow-900/20 border border-yellow-600 rounded-lg p-4 mb-6">
              <p className="text-yellow-400 text-sm">
                🔥 Ce fichier a été automatiquement supprimé de nos serveurs.
                Le lien n'est plus valide.
              </p>
            </div>
            <button
              onClick={() => navigate('/')}
              className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg transition-colors"
            >
              Retour à l'accueil
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-900 p-8">
      <div className="max-w-2xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <button
            onClick={() => navigate('/')}
            className="text-blue-400 hover:text-blue-300 mb-4 flex items-center gap-2"
          >
            ← Retour
          </button>
          <h1 className="text-4xl font-bold text-white mb-2">
            📥 Télécharger le Fichier
          </h1>
          <p className="text-slate-400">
            Fichier sécurisé prêt pour le téléchargement
          </p>
        </div>

        {fileInfo && (
          <div className="bg-slate-800 rounded-xl p-8 border border-slate-700">
            {/* File info */}
            <div className="mb-6">
              <div className="text-center mb-6">
                <div className="text-6xl mb-4">📄</div>
                <h2 className="text-2xl font-bold text-white mb-2">
                  {fileInfo.filename}
                </h2>
                <p className="text-slate-400">
                  {formatFileSize(fileInfo.file_size)} • {fileInfo.mime_type}
                </p>
              </div>

              <div className="grid grid-cols-2 gap-4 text-sm">
                <div className="bg-slate-900 rounded-lg p-4">
                  <span className="text-slate-400 block mb-1">Téléchargé le</span>
                  <p className="text-white font-medium">
                    {formatDate(fileInfo.uploaded_at)}
                  </p>
                </div>
                <div className="bg-slate-900 rounded-lg p-4">
                  <span className="text-slate-400 block mb-1">Expire le</span>
                  <p className="text-white font-medium">
                    {formatDate(fileInfo.expires_at)}
                  </p>
                </div>
              </div>
            </div>

            {/* Security badges */}
            <div className="grid grid-cols-2 gap-3 mb-6">
              <div className="bg-green-900/30 border border-green-600 rounded-lg p-3 flex items-center gap-2">
                <span className="text-2xl">🛡️</span>
                <div>
                  <p className="text-green-400 font-semibold text-sm">Antivirus</p>
                  <p className="text-green-300 text-xs">
                    {fileInfo.antivirus_status === 'clean' ? 'Fichier sain' : fileInfo.antivirus_status}
                  </p>
                </div>
              </div>
              <div className="bg-blue-900/30 border border-blue-600 rounded-lg p-3 flex items-center gap-2">
                <span className="text-2xl">🔐</span>
                <div>
                  <p className="text-blue-400 font-semibold text-sm">Chiffré</p>
                  <p className="text-blue-300 text-xs">AES-256-GCM</p>
                </div>
              </div>
            </div>

            {/* Warning */}
            <div className="bg-yellow-900/20 border border-yellow-600 rounded-lg p-4 mb-6">
              <p className="text-yellow-400 text-sm">
                ⚠️ <strong>Attention :</strong> Ce fichier ne peut être téléchargé qu'une seule fois.
                Après le téléchargement, il sera automatiquement supprimé.
              </p>
            </div>

            {/* Download button */}
            {fileInfo.is_available ? (
              <button
                onClick={handleDownload}
                disabled={downloading}
                className={`w-full font-bold py-4 px-6 rounded-lg transition-all duration-200 flex items-center justify-center gap-2 ${
                  downloading
                    ? 'bg-slate-700 cursor-not-allowed'
                    : 'bg-blue-600 hover:bg-blue-700 text-white hover:shadow-lg'
                }`}
              >
                {downloading ? (
                  <>
                    <span className="animate-spin">⏳</span>
                    <span>Téléchargement en cours...</span>
                  </>
                ) : (
                  <>
                    <span>⬇️</span>
                    <span>Télécharger et Déchiffrer</span>
                  </>
                )}
              </button>
            ) : (
              <div className="bg-red-900/30 border border-red-500 rounded-lg p-4 text-center">
                <p className="text-red-400">
                  ❌ Ce fichier n'est plus disponible
                </p>
              </div>
            )}

            {error && (
              <div className="mt-4 bg-red-900/30 border border-red-500 rounded-lg p-4">
                <p className="text-red-400 text-sm">⚠️ {error}</p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default Download;
