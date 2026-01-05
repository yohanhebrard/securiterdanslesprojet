import React, { useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

interface UploadResponse {
  file_id: string;
  download_url: string;
  download_token: string;
  expires_at: string;
  filename: string;
  file_size: number;
  mime_type: string;
}

const Upload: React.FC = () => {
  const navigate = useNavigate();
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploadResult, setUploadResult] = useState<UploadResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      const selectedFile = acceptedFiles[0];

      // Check file size (100 MB)
      if (selectedFile.size > 100 * 1024 * 1024) {
        setError('Le fichier est trop volumineux (max 100 MB)');
        return;
      }

      setFile(selectedFile);
      setError(null);
      setUploadResult(null);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    maxFiles: 1,
    multiple: false,
  });

  const handleUpload = async () => {
    if (!file) return;

    setUploading(true);
    setError(null);
    setUploadProgress(0);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post<UploadResponse>(
        `${API_URL}/api/v1/upload`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
          onUploadProgress: (progressEvent) => {
            if (progressEvent.total) {
              const percentCompleted = Math.round(
                (progressEvent.loaded * 100) / progressEvent.total
              );
              setUploadProgress(percentCompleted);
            }
          },
        }
      );

      setUploadResult(response.data);
      setUploadProgress(100);
    } catch (err: any) {
      console.error('Upload error:', err);
      if (err.response?.data?.detail) {
        setError(err.response.data.detail);
      } else {
        setError('Erreur lors du téléchargement. Veuillez réessayer.');
      }
    } finally {
      setUploading(false);
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

  const copyToClipboard = async (text: string) => {
    try {
      await navigator.clipboard.writeText(text);
      alert('Lien copié dans le presse-papiers !');
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  };

  return (
    <div className="min-h-screen bg-slate-900 p-8">
      <div className="max-w-3xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <button
            onClick={() => navigate('/')}
            className="text-blue-400 hover:text-blue-300 mb-4 flex items-center gap-2"
          >
            ← Retour
          </button>
          <h1 className="text-4xl font-bold text-white mb-2">
            📤 Partager un Fichier
          </h1>
          <p className="text-slate-400">
            Téléchargez votre fichier pour obtenir un lien de partage sécurisé
          </p>
        </div>

        {!uploadResult ? (
          <>
            {/* Dropzone */}
            <div
              {...getRootProps()}
              className={`border-2 border-dashed rounded-xl p-12 text-center cursor-pointer transition-all ${
                isDragActive
                  ? 'border-blue-500 bg-blue-500/10'
                  : 'border-slate-700 bg-slate-800 hover:border-blue-500/50'
              }`}
            >
              <input {...getInputProps()} />
              <div className="text-6xl mb-4">
                {isDragActive ? '📥' : '📁'}
              </div>
              {file ? (
                <div>
                  <p className="text-white font-semibold text-xl mb-2">
                    {file.name}
                  </p>
                  <p className="text-slate-400 mb-4">
                    {formatFileSize(file.size)}
                  </p>
                  <p className="text-sm text-slate-500">
                    Cliquez pour changer de fichier
                  </p>
                </div>
              ) : (
                <div>
                  <p className="text-white text-xl mb-2">
                    Glissez-déposez votre fichier ici
                  </p>
                  <p className="text-slate-400">
                    ou cliquez pour sélectionner
                  </p>
                  <p className="text-sm text-slate-500 mt-4">
                    Taille maximale: 100 MB
                  </p>
                </div>
              )}
            </div>

            {/* Error message */}
            {error && (
              <div className="mt-4 bg-red-900/30 border border-red-500 rounded-lg p-4">
                <p className="text-red-400">⚠️ {error}</p>
              </div>
            )}

            {/* Upload button */}
            {file && !uploading && (
              <button
                onClick={handleUpload}
                className="w-full mt-6 bg-blue-600 hover:bg-blue-700 text-white font-bold py-4 px-6 rounded-lg transition-colors duration-200 flex items-center justify-center gap-2"
              >
                <span>🚀 Télécharger et Chiffrer</span>
              </button>
            )}

            {/* Progress bar */}
            {uploading && (
              <div className="mt-6">
                <div className="bg-slate-800 rounded-lg p-6">
                  <div className="flex justify-between mb-2">
                    <span className="text-white font-medium">
                      Téléchargement en cours...
                    </span>
                    <span className="text-blue-400 font-bold">
                      {uploadProgress}%
                    </span>
                  </div>
                  <div className="w-full bg-slate-700 rounded-full h-3">
                    <div
                      className="bg-blue-600 h-3 rounded-full transition-all duration-300"
                      style={{ width: `${uploadProgress}%` }}
                    ></div>
                  </div>
                  <div className="mt-4 flex flex-col gap-2 text-sm text-slate-400">
                    <div className="flex items-center gap-2">
                      <span className="text-green-400">✓</span>
                      <span>Scan antivirus en cours...</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="text-green-400">✓</span>
                      <span>Chiffrement AES-256-GCM...</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="text-green-400">✓</span>
                      <span>Stockage sécurisé...</span>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </>
        ) : (
          /* Success result */
          <div className="bg-green-900/20 border border-green-500 rounded-xl p-8">
            <div className="text-center mb-6">
              <div className="text-6xl mb-4">✅</div>
              <h2 className="text-2xl font-bold text-white mb-2">
                Fichier téléchargé avec succès !
              </h2>
              <p className="text-slate-400">
                Votre fichier est chiffré et prêt à être partagé
              </p>
            </div>

            <div className="bg-slate-800 rounded-lg p-6 mb-6">
              <div className="mb-4">
                <label className="text-sm text-slate-400 block mb-2">
                  Lien de téléchargement unique :
                </label>
                <div className="flex gap-2">
                  <input
                    type="text"
                    value={uploadResult.download_url}
                    readOnly
                    className="flex-1 bg-slate-900 border border-slate-700 rounded px-4 py-2 text-white font-mono text-sm"
                  />
                  <button
                    onClick={() => copyToClipboard(uploadResult.download_url)}
                    className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded transition-colors"
                  >
                    📋 Copier
                  </button>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="text-slate-400">Fichier :</span>
                  <p className="text-white font-medium">
                    {uploadResult.filename}
                  </p>
                </div>
                <div>
                  <span className="text-slate-400">Taille :</span>
                  <p className="text-white font-medium">
                    {formatFileSize(uploadResult.file_size)}
                  </p>
                </div>
                <div>
                  <span className="text-slate-400">Expire le :</span>
                  <p className="text-white font-medium">
                    {formatDate(uploadResult.expires_at)}
                  </p>
                </div>
                <div>
                  <span className="text-slate-400">Type :</span>
                  <p className="text-white font-medium">
                    {uploadResult.mime_type}
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-yellow-900/20 border border-yellow-600 rounded-lg p-4 mb-6">
              <p className="text-yellow-400 text-sm">
                ⚠️ <strong>Important :</strong> Ce lien ne fonctionnera qu'une seule fois.
                Après le téléchargement, le fichier sera automatiquement supprimé.
              </p>
            </div>

            <button
              onClick={() => {
                setFile(null);
                setUploadResult(null);
                setError(null);
                setUploadProgress(0);
              }}
              className="w-full bg-slate-700 hover:bg-slate-600 text-white font-bold py-3 px-6 rounded-lg transition-colors"
            >
              📤 Partager un autre fichier
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default Upload;
