import React, { useRef, useEffect } from 'react';

const ChatInput = ({ onSend, isLoading }) => {
  const [text, setText] = React.useState('');
  const textareaRef = useRef(null);

  useEffect(() => {
    if (!isLoading) textareaRef.current?.focus();
  }, [isLoading]);

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (text.trim()) {
        onSend(text);
        setText('');
      }
    }
  };

  return (
    <div className="input-area">
      <div className="input-wrapper">
        <textarea
          ref={textareaRef}
          rows="1"
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask anything..."
          disabled={isLoading}
        />
        <button className="send-btn" onClick={() => { onSend(text); setText(''); }} disabled={!text.trim() || isLoading}>
          {isLoading ? '...' : 'Send'}
        </button>
      </div>
    </div>
  );
};
export default ChatInput;