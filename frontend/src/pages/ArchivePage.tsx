import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"
import { FileText, Clock, Send, ChevronLeft } from "lucide-react"
import { Button } from "../components/ui/button"

interface Message {
  id: string
  parsha_name: string
  message_type: string
  subject: string
  status: string
  created_at: string
  docx_filename: string
}

const STATUS_LABELS: Record<string, { label: string; color: string }> = {
  draft: { label: "טיוטה", color: "bg-gray-200 text-gray-700" },
  test_sent: { label: "טסט נשלח", color: "bg-yellow-100 text-yellow-800" },
  approved: { label: "מאושר", color: "bg-blue-100 text-blue-800" },
  sent: { label: "נשלח", color: "bg-green-100 text-green-800" },
}

function formatDate(iso: string) {
  return new Date(iso).toLocaleDateString("he-IL", {
    day: "numeric",
    month: "long",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  })
}

export function ArchivePage() {
  const [messages, setMessages] = useState<Message[]>([])
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    fetch("/api/messages")
      .then((r) => r.json())
      .then((data) => setMessages(data))
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

  return (
    <div className="max-w-4xl mx-auto py-8 px-4">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-brown">ארכיון מסרים</h1>
        <Button onClick={() => navigate("/")} variant="outline" size="sm">
          <FileText className="w-4 h-4" />
          מסר חדש
        </Button>
      </div>

      {loading ? (
        <p className="text-center text-brown-light py-12">טוען...</p>
      ) : messages.length === 0 ? (
        <div className="text-center py-16">
          <FileText className="w-12 h-12 text-brown-light/30 mx-auto mb-4" />
          <p className="text-brown-light">אין מסרים עדיין</p>
          <p className="text-brown-light/60 text-sm mt-1">
            העלה קובץ DOCX כדי ליצור את המסר הראשון
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {messages.map((msg) => {
            const status = STATUS_LABELS[msg.status] || STATUS_LABELS.draft
            return (
              <div
                key={msg.id}
                onClick={() => navigate(`/message/${msg.id}`)}
                className="bg-white rounded-lg border border-brown-light/15 p-4 flex items-center gap-4 hover:border-gold/40 hover:shadow-sm transition-all cursor-pointer"
              >
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <h3 className="font-medium text-brown truncate">
                      {msg.parsha_name || msg.docx_filename || "ללא שם"}
                    </h3>
                    <span
                      className={`text-xs px-2 py-0.5 rounded-full ${status.color}`}
                    >
                      {status.label}
                    </span>
                  </div>
                  {msg.subject && (
                    <p className="text-sm text-brown-light truncate">
                      {msg.subject}
                    </p>
                  )}
                  <div className="flex items-center gap-3 mt-1.5 text-xs text-brown-light/60">
                    <span className="flex items-center gap-1">
                      <Clock className="w-3 h-3" />
                      {formatDate(msg.created_at)}
                    </span>
                    <span className="flex items-center gap-1">
                      {msg.message_type === "parsha" ? "פרשה" : "מוצ\"ש"}
                    </span>
                  </div>
                </div>
                <ChevronLeft className="w-5 h-5 text-brown-light/30" />
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}
