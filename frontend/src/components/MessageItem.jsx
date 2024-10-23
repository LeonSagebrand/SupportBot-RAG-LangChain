function MessageItem({ message }) {
  const style = message.sender === 'user'
    ? 'bg-blue-500 text-white self-end'
    : 'bg-gray-200 text-gray-800 self-start'

  return (
    <div className={`max-w-xs p-3 rounded-lg mb-2 ${style}`}>
      {message.text}
    </div>
  )
}

export default MessageItem
