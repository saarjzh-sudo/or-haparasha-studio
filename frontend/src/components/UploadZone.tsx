import { useCallback, useState } from "react"
import { Upload, FileText, Loader2 } from "lucide-react"
import { Button } from "./ui/button"

interface UploadZoneProps {
  onUpload: (file: File) => void
  isLoading: boolean
}

export function UploadZone({ onUpload, isLoading }: UploadZoneProps) {
  const [dragOver, setDragOver] = useState(false)

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault()
      setDragOver(false)
      const file = e.dataTransfer.files[0]
      if (file?.name.endsWith(".docx")) onUpload(file)
    },
    [onUpload]
  )

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) onUpload(file)
  }

  return (
    <div
      onDragOver={(e) => {
        e.preventDefault()
        setDragOver(true)
      }}
      onDragLeave={() => setDragOver(false)}
      onDrop={handleDrop}
      className={`border-2 border-dashed rounded-xl p-8 text-center transition-colors ${
        dragOver
          ? "border-gold bg-gold/10"
          : "border-brown-light/30 hover:border-gold/50"
      }`}
    >
      {isLoading ? (
        <div className="flex flex-col items-center gap-3">
          <Loader2 className="w-10 h-10 text-gold animate-spin" />
          <p className="text-brown-light">מעבד את הקובץ...</p>
        </div>
      ) : (
        <div className="flex flex-col items-center gap-3">
          <Upload className="w-10 h-10 text-brown-light/50" />
          <p className="text-brown font-medium">גרור קובץ DOCX לכאן</p>
          <p className="text-brown-light text-sm">או לחץ לבחירת קובץ</p>
          <label>
            <input
              type="file"
              accept=".docx"
              onChange={handleFileInput}
              className="hidden"
            />
            <span className="inline-flex items-center justify-center gap-2 rounded-lg border border-gold text-gold hover:bg-gold/10 h-8 px-3 text-xs font-medium cursor-pointer">
              <FileText className="w-4 h-4" />
              בחר קובץ
            </span>
          </label>
        </div>
      )}
    </div>
  )
}
