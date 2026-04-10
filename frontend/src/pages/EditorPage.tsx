import { useState, useEffect } from "react"
import { Link, useParams } from "react-router-dom"
import { UploadZone } from "../components/UploadZone"
import { EmailPreview } from "../components/EmailPreview"
import { ChatPanel } from "../components/ChatPanel"
import { SendControls } from "../components/SendControls"
import { Link2, Archive, Upload, Loader2 } from "lucide-react"
import { Button } from "../components/ui/button"

export function EditorPage() {
  const { id } = useParams()
  const [messageId, setMessageId] = useState("")
  const [html, setHtml] = useState("")
  const [subject, setSubject] = useState("")
  const [parshaName, setParshaName] = useState("")
  const [uploading, setUploading] = useState(false)
  const [pdfUrl, setPdfUrl] = useState("")
  const [moreshetUrl, setMoreshetUrl] = useState("")
  const [loading, setLoading] = useState(false)
  const [driveUploading, setDriveUploading] = useState(false)

  useEffect(() => {
    if (!id) return
    setLoading(true)
    fetch(`/api/messages/${id}`)
      .then((res) => res.json())
      .then((data) => {
        if (data.id) {
          setMessageId(data.id)
          setHtml(data.html_content || "")
          setSubject(data.subject || "")
          setParshaName(data.parsha_name || "")
          setPdfUrl(data.pdf_url || "")
          setMoreshetUrl(data.moreshet_url || "")
        }
      })
      .catch(() => alert("שגיאה בטעינת המסר"))
      .finally(() => setLoading(false))
  }, [id])

  const handleUpload = async (file: File) => {
    setUploading(true)
    const formData = new FormData()
    formData.append("file", file)
    formData.append("message_type", "parsha")

    try {
      const res = await fetch("/api/upload", {
        method: "POST",
        body: formData,
      })
      const data = await res.json()
      setMessageId(data.message_id)
      setHtml(data.html_content)
      setSubject(data.subject_suggestion || "")
      setParshaName(data.parsha_name || "")
    } catch {
      alert("שגיאה בהעלאת הקובץ")
    } finally {
      setUploading(false)
    }
  }

  if (loading) {
    return (
      <div className="max-w-xl mx-auto py-20 px-4 text-center">
        <p className="text-brown-light">טוען מסר...</p>
      </div>
    )
  }

  if (!html) {
    return (
      <div className="max-w-xl mx-auto py-20 px-4">
        <h1 className="text-2xl font-bold text-brown text-center mb-2">
          אור הפרשה Studio
        </h1>
        <p className="text-brown-light text-center mb-8">
          העלה קובץ DOCX כדי להתחיל
        </p>
        <UploadZone onUpload={handleUpload} isLoading={uploading} />
        <div className="mt-6 text-center">
          <Link to="/archive">
            <Button variant="ghost" size="sm">
              <Archive className="w-4 h-4" />
              ארכיון מסרים
            </Button>
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="h-screen flex flex-col">
      {/* Header */}
      <header className="bg-white border-b border-brown-light/20 px-4 py-3 flex items-center gap-4">
        <h1 className="text-lg font-bold text-brown">
          {parshaName || "אור הפרשה"}
        </h1>
        <input
          value={subject}
          onChange={(e) => setSubject(e.target.value)}
          placeholder="נושא המייל..."
          className="flex-1 rounded-lg border border-brown-light/20 px-3 py-1.5 text-sm bg-cream text-brown focus:outline-none focus:border-gold"
        />
      </header>

      {/* Main layout */}
      <div className="flex-1 flex min-h-0">
        {/* Preview — left side (in RTL: right visually) */}
        <div className="flex-1 p-4 overflow-auto">
          <EmailPreview html={html} />
        </div>

        {/* Sidebar — right side (in RTL: left visually) */}
        <div className="w-96 border-r border-brown-light/20 bg-white flex flex-col p-4 gap-4 overflow-auto">
          {/* Upload new */}
          <UploadZone onUpload={handleUpload} isLoading={uploading} />

          {/* Links */}
          <div className="space-y-2">
            <div className="flex items-center gap-2">
              <Link2 className="w-4 h-4 text-brown-light" />
              <input
                value={pdfUrl}
                onChange={(e) => setPdfUrl(e.target.value)}
                placeholder="קישור PDF..."
                className="flex-1 rounded border border-brown-light/20 px-2 py-1 text-sm bg-cream text-brown focus:outline-none focus:border-gold"
              />
              <label className="cursor-pointer">
                <input
                  type="file"
                  accept=".pdf"
                  className="hidden"
                  onChange={async (e) => {
                    const file = e.target.files?.[0]
                    if (!file) return
                    setDriveUploading(true)
                    const formData = new FormData()
                    formData.append("file", file)
                    formData.append("folder_name", "אור הפרשה")
                    try {
                      const res = await fetch("/api/upload-to-drive", {
                        method: "POST",
                        body: formData,
                      })
                      const data = await res.json()
                      if (data.link) {
                        setPdfUrl(data.link)
                      } else if (data.error) {
                        alert(`שגיאה: ${data.error}`)
                      }
                    } catch {
                      alert("שגיאה בהעלאה לדרייב")
                    } finally {
                      setDriveUploading(false)
                    }
                  }}
                />
                <Button variant="outline" size="sm" disabled={driveUploading} asChild={false}
                  onClick={(e) => {
                    const input = (e.currentTarget as HTMLElement).parentElement?.querySelector('input[type="file"]') as HTMLInputElement
                    input?.click()
                    e.preventDefault()
                  }}
                >
                  {driveUploading ? <Loader2 className="w-3 h-3 animate-spin" /> : <Upload className="w-3 h-3" />}
                </Button>
              </label>
            </div>
            <div className="flex items-center gap-2">
              <Link2 className="w-4 h-4 text-brown-light" />
              <input
                value={moreshetUrl}
                onChange={(e) => setMoreshetUrl(e.target.value)}
                placeholder="קישור מורשת..."
                className="flex-1 rounded border border-brown-light/20 px-2 py-1 text-sm bg-cream text-brown focus:outline-none focus:border-gold"
              />
            </div>
          </div>

          {/* Divider */}
          <hr className="border-brown-light/10" />

          {/* Chat */}
          <div className="flex-1 min-h-0">
            <ChatPanel
              messageId={messageId}
              currentHtml={html}
              onHtmlUpdate={setHtml}
            />
          </div>

          {/* Divider */}
          <hr className="border-brown-light/10" />

          {/* Send */}
          <SendControls subject={subject} htmlContent={html} messageId={messageId} />
        </div>
      </div>
    </div>
  )
}
