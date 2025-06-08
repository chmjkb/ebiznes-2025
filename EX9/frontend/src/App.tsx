import { useState, useRef, useEffect } from 'react'
import './App.css'

interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}

function App() {
  const [messages, setMessages] = useState<Message[]>([])
  const [inputMessage, setInputMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const messagesContainerRef = useRef<HTMLDivElement>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    if (messagesContainerRef.current) {
      messagesContainerRef.current.scrollTop = messagesContainerRef.current.scrollHeight
    }
  }

  useEffect(() => {
    // Only scroll to bottom when new messages are added
    if (messages.length > 0) {
      scrollToBottom()
    }
  }, [messages.length])

  const sendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: inputMessage,
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInputMessage('')
    setIsLoading(true)
    setError(null)

    try {
      // Build conversation history including the new message
      // we basically want the chat completion for entire chat
      const conversationHistory = [
        ...messages.map(msg => ({
          role: msg.role,
          content: msg.content
        })),
        {
          role: 'user',
          content: inputMessage
        }
      ]

      const response = await fetch('http://localhost:8000/api/chat_completion', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          messages: conversationHistory,
          model: 'llama3-8b-8192',
          temperature: 0.7,
          max_tokens: 1024
        })
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: data.response,
        timestamp: new Date()
      }

      setMessages(prev => [...prev, assistantMessage])
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  const conversationStarters = [
    "Hello! How are you today?",
    "Can you help me write a creative story?",
    "What's the weather like in space?",
    "Explain quantum physics in simple terms",
    "Tell me something interesting!"
  ]

  const conversationClosings = [
    "Thanks! 👋",
    "Goodbye!",
    "Perfect!",
    "Great chat!",
    "Take care!"
  ]

  const handleExampleClick = (example: string) => {
    setInputMessage(example)
    // Auto-send the message directly
    sendExampleMessage(example)
  }

  const sendExampleMessage = async (message: string) => {
    if (!message.trim() || isLoading) return

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: message,
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInputMessage('')
    setIsLoading(true)
    setError(null)

    try {
      const conversationHistory = [
        ...messages.map(msg => ({
          role: msg.role,
          content: msg.content
        })),
        {
          role: 'user',
          content: message
        }
      ]

      const response = await fetch('http://localhost:8000/api/chat_completion', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          messages: conversationHistory,
          model: 'llama3-8b-8192',
          temperature: 0.7,
          max_tokens: 1024
        })
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: data.response,
        timestamp: new Date()
      }

      setMessages(prev => [...prev, assistantMessage])
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="chat-container">
      <div className="chat-header">
        <h1>AI Chat</h1>
        <p>Powered by Groq</p>
      </div>

      <div className="messages-container" ref={messagesContainerRef}>
        {messages.length === 0 && (
          <div className="empty-state">
            <p>Start a conversation with one of these examples:</p>
            <div className="example-messages">
              {conversationStarters.map((example, index) => (
                <button 
                  key={index}
                  className="example-button"
                  onClick={() => handleExampleClick(example)}
                  disabled={isLoading}
                >
                  {example}
                </button>
              ))}
            </div>
            <p className="or-divider">or type your own message below</p>
          </div>
        )}

        {messages.length > 0 && (
          <div className="conversation-closings">
            <p className="closings-title">Quick closings:</p>
            <div className="example-messages closings">
              {conversationClosings.map((closing, index) => (
                <button 
                  key={index}
                  className="example-button closing-button"
                  onClick={() => handleExampleClick(closing)}
                  disabled={isLoading}
                >
                  {closing}
                </button>
              ))}
            </div>
          </div>
        )}
        
        {messages.map((message) => (
          <div key={message.id} className={`message ${message.role}`}>
            <div className="message-content">
              {message.content}
            </div>
            <div className="message-timestamp">
              {message.timestamp.toLocaleTimeString()}
            </div>
          </div>
        ))}
        
        {isLoading && (
          <div className="message assistant loading">
            <div className="loading-dots">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}
        
        {error && (
          <div className="error-message">
            Error: {error}
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      <div className="input-container">
        <textarea
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type your message..."
          disabled={isLoading}
          rows={1}
        />
        <button 
          onClick={sendMessage} 
          disabled={!inputMessage.trim() || isLoading}
        >
          {isLoading ? 'Sending...' : 'Send'}
        </button>
      </div>
    </div>
  )
}

export default App