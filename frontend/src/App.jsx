import { useState } from 'react'
import MessageList from './components/MessageList'
import ChatInput from './components/ChatInput'

function App() {
  const [messages, setMessages] = useState([])

  const handleSendMessage = async (message) => {
    setMessages(prevMessages => [...prevMessages, { text: message, sender: 'user' }])

    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
      })

      if (!response.ok) {
        throw new Error('Network response was not ok')
      }

      const data = await response.json()
      setMessages(prevMessages => [...prevMessages, { text: data.response, sender: 'bot' }])
    } catch (error) {
      console.error('Error:', error)
      setMessages(prevMessages => [...prevMessages, { text: 'Sorry, there was an error processing your request.', sender: 'bot' }])
    }
  }

  return (
    <div className="flex justify-center items-center min-h-screen bg-gray-100">
      <div className="w-full max-w-lg p-6 bg-white rounded-lg shadow-lg">
        <div className="flex-grow overflow-y-auto p-4 mb-4 border border-gray-200 rounded-lg h-96">
          <MessageList messages={messages} />
        </div>
        <ChatInput onSendMessage={handleSendMessage} />
      </div>
    </div>
  )
}

export default App
