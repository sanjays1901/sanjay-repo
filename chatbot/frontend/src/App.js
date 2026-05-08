import React, { useState, useEffect, useRef } from 'react';
import './App.css';
import { chatApi } from './api';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';
import Sidebar from './Sidebar';
import DocumentManager from './DocumentManager';

const App = () => {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [view, setView] = useState('chat');
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  
  const messagesEndRef = useRef(null);

  const [currentSessionId, setCurrentSessionId] = useState(() => {
    let id = localStorage.getItem("session_id");
    if (!id) {
      id = crypto.randomUUID();
      localStorage.setItem("session_id", id);
    }
    return id;
  });

  const handleNewChat = () => {
    const newId = crypto.randomUUID();
    localStorage.setItem("session_id", newId);
    setCurrentSessionId(newId);
    setMessages([]);
  };

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const data = await chatApi.getHistory(currentSessionId);
        const mapped = data.history.map(h => ([
          { id: Math.random(), text: h.query, sender: 'user' },
          { id: Math.random(), text: h.answer, sender: 'bot' }
        ])).flat();
        setMessages(mapped);
      } catch (e) { console.error("History fail:", e); }
    };
    fetchHistory();
  }, [currentSessionId]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  const handleSend = async (text) => {
    const userMsg = { id: Date.now(), text, sender: 'user' };
    setMessages(prev => [...prev, userMsg]);
    setIsLoading(true);
    try {
      const data = await chatApi.ask(text, currentSessionId);
      setMessages(prev => [...prev, { id: Date.now()+1, text: data.answer, sources: data.sources, sender: 'bot' }]);
    } catch (e) {
      setMessages(prev => [...prev, { id: Date.now()+1, text: "Connection error.", sender: 'bot' }]);
    } finally { setIsLoading(false); }
  };

  return (
    <div className="app-layout">
      <Sidebar 
        currentView={view} 
        setView={setView} 
        isOpen={isSidebarOpen} 
        onNewChat={handleNewChat}
      />
      <main className="chat-container">
        <header className="chat-header">
          <button className="toggle-sidebar" onClick={() => setIsSidebarOpen(!isSidebarOpen)}>☰</button>
          <span>{view === 'chat' ? 'Current Conversation' : 'Knowledge Base'}</span>
        </header>

        {view === 'chat' ? (
          <>
            <div className="messages-wrapper">
              <div className="messages-list">
              {messages.map(m => <ChatMessage key={m.id} message={m} />)}
              {isLoading && (
                <div className="message-row bot">
                  <div className="avatar">AI</div>
                  <div className="typing-indicator">
                    <div className="dot"></div><div className="dot"></div><div className="dot"></div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
              </div>
            </div>
            <ChatInput onSend={handleSend} isLoading={isLoading} />
          </>
        ) : (
          <DocumentManager />
        )}
      </main>
    </div>
  );
};
export default App;