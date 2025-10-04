import { useState, useRef, useEffect } from 'react'
import './App.css'

const API_BASE_URL = 'http://localhost:5000/api'

function App() {
  const [isInterviewActive, setIsInterviewActive] = useState(false)
  const [isRecording, setIsRecording] = useState(false)
  const [isProcessing, setIsProcessing] = useState(false)
  const [isSpeaking, setIsSpeaking] = useState(false)
  const [conversationHistory, setConversationHistory] = useState([])
  const [statusMessage, setStatusMessage] = useState('')
  
  const mediaRecorderRef = useRef(null)
  const audioChunksRef = useRef([])
  const audioContextRef = useRef(null)
  const currentAudioRef = useRef(null)

  const startInterview = async () => {
    try {
      setStatusMessage('Starting interview...')
      setIsProcessing(true)
      
      const response = await fetch(`${API_BASE_URL}/start-interview`, {
        method: 'POST'
      })
      
      if (response.ok) {
        const audioBlob = await response.blob()
        await playAudio(audioBlob)
        
        setIsInterviewActive(true)
        setConversationHistory([{
          role: 'assistant',
          text: "Hello, Myself Talkito Technician Assistant at ElevenLabs California. So tell me about your web development journey."
        }])
        setStatusMessage('Interview started! Click "Start Speaking" to respond.')
      } else {
        setStatusMessage('Failed to start interview. Please check your backend.')
      }
    } catch (error) {
      console.error('Error starting interview:', error)
      setStatusMessage('Error: Could not connect to server.')
    } finally {
      setIsProcessing(false)
    }
  }

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      
      const mediaRecorder = new MediaRecorder(stream, {
        mimeType: 'audio/webm'
      })
      
      audioChunksRef.current = []
      
      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data)
        }
      }
      
      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' })
        await sendAudioToServer(audioBlob)
        
        // Stop all tracks
        stream.getTracks().forEach(track => track.stop())
      }
      
      mediaRecorderRef.current = mediaRecorder
      mediaRecorder.start()
      setIsRecording(true)
      setStatusMessage('Recording... Click "Stop Speaking" when done.')
      
    } catch (error) {
      console.error('Error accessing microphone:', error)
      setStatusMessage('Error: Could not access microphone.')
    }
  }

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop()
      setIsRecording(false)
      setIsProcessing(true)
      setStatusMessage('Processing your response...')
    }
  }

  const sendAudioToServer = async (audioBlob) => {
    try {
      const formData = new FormData()
      formData.append('audio', audioBlob, 'recording.webm')
      
      const response = await fetch(`${API_BASE_URL}/process-audio`, {
        method: 'POST',
        body: formData
      })
      
      if (response.ok) {
        const data = await response.json()
        
        // Add user message to history
        setConversationHistory(prev => [...prev, {
          role: 'user',
          text: data.user_text
        }])
        
        // Add AI response to history
        setConversationHistory(prev => [...prev, {
          role: 'assistant',
          text: data.ai_response
        }])
        
        // Generate and play AI speech
        const audioResponse = await fetch(`${API_BASE_URL}/text-to-speech`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ text: data.ai_response })
        })
        
        if (audioResponse.ok) {
          const audioBlob = await audioResponse.blob()
          await playAudio(audioBlob)
        }
        
        setStatusMessage('Ready for your next response.')
      } else {
        setStatusMessage('Error processing audio. Please try again.')
      }
    } catch (error) {
      console.error('Error sending audio:', error)
      setStatusMessage('Error: Could not process your response.')
    } finally {
      setIsProcessing(false)
    }
  }

  const playAudio = (audioBlob) => {
    return new Promise((resolve) => {
      const audioUrl = URL.createObjectURL(audioBlob)
      const audio = new Audio(audioUrl)
      
      currentAudioRef.current = audio
      setIsSpeaking(true)
      
      audio.onended = () => {
        setIsSpeaking(false)
        URL.revokeObjectURL(audioUrl)
        resolve()
      }
      
      audio.onerror = () => {
        setIsSpeaking(false)
        URL.revokeObjectURL(audioUrl)
        resolve()
      }
      
      audio.play()
    })
  }

  const resetInterview = () => {
    setIsInterviewActive(false)
    setIsRecording(false)
    setIsProcessing(false)
    setIsSpeaking(false)
    setConversationHistory([])
    setStatusMessage('')
    
    if (currentAudioRef.current) {
      currentAudioRef.current.pause()
      currentAudioRef.current = null
    }
  }

  return (
    <div className="app">
      <header className="header">
        <h1>🎙️ Talkito AI Interview</h1>
        <p className="subtitle">AI-Powered Technical Interview Assistant</p>
      </header>

      <main className="main-content">
        <div className="interview-container">
          {!isInterviewActive ? (
            <div className="start-section">
              <div className="welcome-card">
                <h2>Welcome to Your AI Interview</h2>
                <p>Get ready to discuss your web development journey with our AI interviewer powered by ElevenLabs and Gemini AI.</p>
                <button 
                  className="btn btn-primary btn-large"
                  onClick={startInterview}
                  disabled={isProcessing}
                >
                  {isProcessing ? 'Starting...' : 'Start Interview'}
                </button>
              </div>
            </div>
          ) : (
            <div className="interview-active">
              <div className="controls">
                <button
                  className={`btn ${isRecording ? 'btn-danger' : 'btn-success'} btn-large`}
                  onClick={isRecording ? stopRecording : startRecording}
                  disabled={isProcessing || isSpeaking}
                >
                  {isRecording ? '⏹️ Stop Speaking' : '🎤 Start Speaking'}
                </button>
                
                <button
                  className="btn btn-secondary"
                  onClick={resetInterview}
                  disabled={isRecording || isProcessing}
                >
                  End Interview
                </button>
              </div>

              {statusMessage && (
                <div className={`status-message ${isSpeaking ? 'speaking' : ''}`}>
                  {isSpeaking && <span className="speaker-icon">🔊</span>}
                  {statusMessage}
                </div>
              )}

              <div className="conversation">
                <h3>Conversation</h3>
                <div className="messages">
                  {conversationHistory.map((message, index) => (
                    <div 
                      key={index} 
                      className={`message ${message.role}`}
                    >
                      <div className="message-header">
                        {message.role === 'assistant' ? '🤖 Talkito' : '👤 You'}
                      </div>
                      <div className="message-content">
                        {message.text}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      </main>

      <footer className="footer">
        <p>Powered by ElevenLabs • Gemini AI • FFmpeg</p>
      </footer>
    </div>
  )
}

export default App
