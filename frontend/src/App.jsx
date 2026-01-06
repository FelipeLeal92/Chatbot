import { useState, useEffect, useRef } from 'react';
import './App.css'; // Estilização do chat (Tailwind ou CSS puro)
import { v4 as uuidv4 } from 'uuid';

function App() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [sessionId] = useState(localStorage.getItem('chat_session') || uuidv4());
  
  // Comunica com o Script Loader (Pai) para redimensionar o iframe
  useEffect(() => {
    localStorage.setItem('chat_session', sessionId);
    window.parent.postMessage({ type: 'LEALVERSE_RESIZE', isOpen }, '*');
  }, [isOpen, sessionId]);

  const sendMessage = async () => {
    if (!input.trim()) return;
    
    const userMsg = { role: 'user', content: input };
    setMessages(prev => [...prev, userMsg]);
    setInput("");

    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: sessionId, message: userMsg.content })
      });
      
      const data = await response.json();
      
      const botMsg = { role: 'assistant', content: data.reply };
      setMessages(prev => [...prev, botMsg]);

      if (data.whatsapp_link) {
        setMessages(prev => [...prev, { 
           role: 'system', 
           content: <a href={data.whatsapp_link} target="_blank" className="btn-whatsapp">Falar com Consultor Agora</a> 
        }]);
      }

    } catch (error) {
      console.error("Erro no chat", error);
    }
  };

  return (
    <div className={`widget-container ${isOpen ? 'open' : 'closed'}`}>
      
      {/* Botão Flutuante (Sempre visível se fechado, ou parte do header se aberto) */}
      {!isOpen && (
        <button className="launcher-btn" onClick={() => setIsOpen(true)}>
          💬
        </button>
      )}

      {/* Janela do Chat */}
      {isOpen && (
        <div className="chat-window">
          <div className="header">
            <span>LealVerse AI</span>
            <button onClick={() => setIsOpen(false)}>X</button>
          </div>
          
          <div className="messages-area">
            {messages.map((m, i) => (
              <div key={i} className={`msg ${m.role}`}>
                {m.content}
              </div>
            ))}
          </div>

          <div className="input-area">
            <input 
              value={input} 
              onChange={(e) => setInput(e.target.value)} 
              onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
              placeholder="Digite sua dúvida..."
            />
            <button onClick={sendMessage}>Enviar</button>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;