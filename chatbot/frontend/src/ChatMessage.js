import React from 'react';
import SourceCitation from './SourceCitation';

const ChatMessage = ({ message }) => {
  const isBot = message.sender === 'bot';

  // Deduplicate sources based on filename
  const uniqueSources = React.useMemo(() => {
    if (!message.sources) return [];
    const seen = new Set();
    return message.sources.filter(item => {
      const sourceName = item.source?.source;
      if (!sourceName || seen.has(sourceName)) return false;
      seen.add(sourceName);
      return true;
    });
  }, [message.sources]);

  return (
    <div className={`message-row ${message.sender}`}>
      <div className="avatar">
        {isBot ? <span className="ai-icon">✦</span> : 'ME'}
      </div>
      <div className="message-content">
        <div className="bubble">
          {message.text}
        </div>
        
        {isBot && uniqueSources.length > 0 && (
          <div className="sources-wrapper">
            <p className="sources-label">Sources used:</p>
            <div className="sources-container">
            {uniqueSources.map((src, idx) => (
              <SourceCitation key={idx} source={src} />
            ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
export default ChatMessage;