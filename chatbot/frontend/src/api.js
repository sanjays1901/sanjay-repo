const BASE_URL = ''; // Handled by proxy in package.json

export const chatApi = {
  async ask(query, sessionId, tenantId = 'default') {
    const response = await fetch(`${BASE_URL}/ask`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query, session_id: sessionId, tenant_id: tenantId }),
    });
    if (!response.ok) throw new Error('Failed to get answer');
    return response.json();
  },

  async getHistory(sessionId, tenantId = 'default') {
    const response = await fetch(`${BASE_URL}/chat-history?tenant_id=${tenantId}&session_id=${sessionId}`);
    if (!response.ok) throw new Error('Failed to fetch history');
    return response.json();
  },

  async getDocuments() {
    const response = await fetch(`${BASE_URL}/documents`);
    if (!response.ok) throw new Error('Failed to fetch documents');
    return response.json();
  },

  async uploadPdf(file, tenantId = 'default') {
    const formData = new FormData();
    formData.append('file', file);
    const response = await fetch(`${BASE_URL}/upload-pdf?tenant_id=${tenantId}`, {
      method: 'POST',
      body: formData,
    });
    if (!response.ok) throw new Error('Upload failed');
    return response.json();
  },

  async deleteDocument(filename) {
    const response = await fetch(`${BASE_URL}/documents/${filename}`, {
      method: 'DELETE',
    });
    if (!response.ok) throw new Error('Delete failed');
    return response.json();
  }
};