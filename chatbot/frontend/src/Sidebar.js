import React from 'react';

const Sidebar = ({ currentView, setView, isOpen, onNewChat }) => {
  return (
    <aside className={`sidebar ${isOpen ? '' : 'collapsed'}`}>
      <div className="sidebar-header">
        <div className="app-logo">
          <span className="logo-icon">✦</span>
          <span>AI Workspace</span>
        </div>
      </div>
      
      <button className="new-chat-btn" onClick={onNewChat}>
        <span className="plus-icon">+</span> New Chat
      </button>

      <nav className="sidebar-nav">
        <div className="nav-group">
          <button 
            className={`nav-item ${currentView === 'chat' ? 'active' : ''}`}
            onClick={() => setView('chat')}>
            <span className="icon">💬</span> Chat
          </button>
          <button 
            className={`nav-item ${currentView === 'docs' ? 'active' : ''}`}
            onClick={() => setView('docs')}>
            <span className="icon">📂</span> Documents
          </button>
        </div>

        <div className="nav-group history">
          <p className="group-label">Recent Conversations</p>
          <div className="history-item placeholder">
            <span className="icon">⌛</span> Previous Chat 1
          </div>
          <div className="history-item placeholder">
            <span className="icon">⌛</span> Previous Chat 2
          </div>
        </div>
      </nav>
      
      <div className="sidebar-footer">
        <div className="user-profile">
          <div className="avatar small">JD</div>
          <span>John Doe</span>
        </div>
      </div>
    </aside>
  );
};
export default Sidebar;