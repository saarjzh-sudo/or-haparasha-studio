import { useState, useRef, useEffect } from "react"
import { Send, Loader2 } from "lucide-react"
import { Button } from "./ui/button"

interface ChatMessage {
  role: "user" | "assistant"
  content: string
}

interface ChatPanelProps {
  messageId: string
  currentHtml: string
  onHtmlUpdate: (html: string) => void
}

export function ChatPanel({ messageId, currentHtml, onHtmlUpdate }: ChatPanelProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [input, setInput] = useState("")
  const [loading, setLoading] = useState(false)
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  const sendMessage = async () => {
    if (!input.trim() || loading) return
    const userMsg = input.trim()
    setInput("")
    setMessages((prev) => [...prev, { role: "user", content: userMsg }])
    setLoading(true)

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message_id: messageId,
          user_message: userMsg,
          current_html: currentHtml,
        }),
      })
      const data = await res.json()
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: data.assistant_message },
      ])
      if (data.updated_html) {
        onHtmlUpdate(data.updated_html)
      }
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "שגיאה בתקשורת עם השרת" },
      ])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex flex-col h-full">
      <h3 className="text-sm font-medium text-brown mb-2">צ'אט תיקונים</h3>
      <div className="flex-1 overflow-y-auto space-y-3 mb-3 min-h-0 max-h-64">
        {messages.length === 0 && (
          <p className="text-brown-light/60 text-sm text-center py-4">
            כתוב הערה ותקבל תיקון ב-HTML
          </p>
        )}
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`text-sm p-2 rounded-lg max-w-[85%] ${
              msg.role === "user"
                ? "bg-gold/10 text-brown mr-auto"
                : "bg-cream-dark text-brown ml-auto"
            }`}
          >
            {msg.content}
          </div>
        ))}
        {loading && (
          <div className="flex items-center gap-2 text-brown-light text-sm">
            <Loader2 className="w-4 h-4 animate-spin" />
            קלוד עובד על התיקון...
          </div>
        )}
        <div ref={bottomRef} />
      </div>
      <div className="flex gap-2">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          placeholder="כתוב הערה לתיקון..."
          className="flex-1 rounded-lg border border-brown-light/20 px-3 py-2 text-sm bg-white text-brown placeholder:text-brown-light/40 focus:outline-none focus:border-gold"
          disabled={loading}
        />
        <Button size="icon" onClick={sendMessage} disabled={loading || !input.trim()}>
          <Send className="w-4 h-4" />
        </Button>
      </div>
    </div>
  )
}
