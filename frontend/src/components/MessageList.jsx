import MessageItem from './MessageItem'

function MessageList({ messages }) {
  return (
    <div className="flex flex-col gap-2">
      {messages.map((message, index) => (
        <MessageItem key={index} message={message} />
      ))}
    </div>
  )
}

export default MessageList
