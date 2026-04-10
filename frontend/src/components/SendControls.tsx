import { useState } from "react"
import { Send, AlertTriangle, TestTube, Loader2 } from "lucide-react"
import { Button } from "./ui/button"

interface SendControlsProps {
  subject: string
  htmlContent: string
  messageId: string
  onStatusChange?: (status: string) => void
}

export function SendControls({ subject, htmlContent, messageId, onStatusChange }: SendControlsProps) {
  const [testLoading, setTestLoading] = useState(false)
  const [liveLoading, setLiveLoading] = useState(false)
  const [showConfirm, setShowConfirm] = useState(false)
  const [result, setResult] = useState<string | null>(null)

  const sendTest = async () => {
    setTestLoading(true)
    setResult(null)
    try {
      const res = await fetch("/api/send/test", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ subject, html_content: htmlContent, message_id: messageId }),
      })
      const data = await res.json()
      setResult(data.error ? `שגיאה: ${data.error}` : "טסט נשלח בהצלחה!")
      onStatusChange?.("test_sent")
    } catch {
      setResult("שגיאה בשליחה")
    } finally {
      setTestLoading(false)
    }
  }

  const sendLive = async () => {
    setLiveLoading(true)
    setResult(null)
    try {
      const res = await fetch("/api/send/live", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          subject,
          html_content: htmlContent,
          list_ids: [1017498, 1017499],
          message_id: messageId,
        }),
      })
      const data = await res.json()
      setResult(data.error ? `שגיאה: ${data.error}` : "נשלח בהצלחה!")
      onStatusChange?.("sent")
    } catch {
      setResult("שגיאה בשליחה")
    } finally {
      setLiveLoading(false)
      setShowConfirm(false)
    }
  }

  return (
    <div className="space-y-3">
      <h3 className="text-sm font-medium text-brown">שליחה</h3>
      <div className="flex gap-2">
        <Button
          variant="outline"
          onClick={sendTest}
          disabled={testLoading || !subject}
        >
          {testLoading ? (
            <Loader2 className="w-4 h-4 animate-spin" />
          ) : (
            <TestTube className="w-4 h-4" />
          )}
          שלח טסט
        </Button>
        <Button
          variant="default"
          onClick={() => setShowConfirm(true)}
          disabled={liveLoading || !subject}
        >
          <Send className="w-4 h-4" />
          שגר לחי
        </Button>
      </div>

      {showConfirm && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 space-y-3">
          <div className="flex items-center gap-2 text-red-700 font-medium">
            <AlertTriangle className="w-5 h-5" />
            אישור שליחה לרשימות אמיתיות
          </div>
          <p className="text-sm text-red-600">
            נושא: {subject}
          </p>
          <div className="flex gap-2">
            <Button variant="destructive" onClick={sendLive} disabled={liveLoading}>
              {liveLoading ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : (
                "אשר ושלח"
              )}
            </Button>
            <Button variant="ghost" onClick={() => setShowConfirm(false)}>
              ביטול
            </Button>
          </div>
        </div>
      )}

      {result && (
        <p className={`text-sm ${result.includes("שגיאה") ? "text-red-600" : "text-green-700"}`}>
          {result}
        </p>
      )}
    </div>
  )
}
