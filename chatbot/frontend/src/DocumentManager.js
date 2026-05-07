import React, { useState, useEffect } from 'react';
import { chatApi } from './api';

const DocumentManager = () => {
  const [docs, setDocs] = useState([]);
  const [uploading, setUploading] = useState(false);

  const loadDocs = async () => {
    try {
      const data = await chatApi.getDocuments();
      setDocs(data.documents);
    } catch (e) { console.error(e); }
  };

  useEffect(() => { loadDocs(); }, []);

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setUploading(true);
    try {
      await chatApi.uploadPdf(file);
      loadDocs();
    } catch (e) { alert("Upload failed"); }
    finally { setUploading(false); }
  };

  const handleDelete = async (name) => {
    if (!window.confirm(`Delete ${name}?`)) return;
    try {
      await chatApi.deleteDocument(name);
      loadDocs();
    } catch (e) { console.error(e); }
  };

  return (
    <div style={{ padding: '2rem', maxWidth: '1000px', margin: '0 auto', width: '100%' }}>
      <h2 style={{ marginBottom: '1.5rem' }}>Knowledge Base</h2>
      <div style={{ marginBottom: '2rem', padding: '2rem', border: '2px dashed var(--border-color)', borderRadius: '12px', textAlign: 'center' }}>
        <input type="file" onChange={handleUpload} disabled={uploading} accept=".pdf" id="file-upload" style={{ display: 'none' }} />
        <label htmlFor="file-upload" style={{ cursor: 'pointer', color: 'var(--primary-color)', fontWeight: 'bold' }}>
          {uploading ? 'Ingesting PDF...' : 'Click to upload PDF'}
        </label>
      </div>

      <div className="doc-list">
        {docs.length === 0 && <p>No documents uploaded yet.</p>}
        {docs.map(doc => (
          <div key={doc} style={{ display: 'flex', justifyContent: 'space-between', padding: '1rem', background: '#f8fafc', borderRadius: '8px', marginBottom: '0.5rem', alignItems: 'center' }}>
            <span>{doc}</span>
            <button onClick={() => handleDelete(doc)} style={{ background: '#fee2e2', color: '#ef4444', border: 'none', padding: '4px 8px', borderRadius: '4px', cursor: 'pointer' }}>Delete</button>
          </div>
        ))}
      </div>
    </div>
  );
};
export default DocumentManager;