import { useState } from "react"
import { Monitor, Smartphone } from "lucide-react"
import { Button } from "./ui/button"

interface EmailPreviewProps {
  html: string
}

export function EmailPreview({ html }: EmailPreviewProps) {
  const [view, setView] = useState<"desktop" | "mobile">("desktop")

  return (
    <div className="flex flex-col h-full">
      <div className="flex items-center gap-2 mb-3">
        <span className="text-sm font-medium text-brown">תצוגה מקדימה</span>
        <div className="flex gap-1 mr-auto">
          <Button
            variant={view === "desktop" ? "default" : "ghost"}
            size="icon"
            onClick={() => setView("desktop")}
          >
            <Monitor className="w-4 h-4" />
          </Button>
          <Button
            variant={view === "mobile" ? "default" : "ghost"}
            size="icon"
            onClick={() => setView("mobile")}
          >
            <Smartphone className="w-4 h-4" />
          </Button>
        </div>
      </div>
      <div
        className="flex-1 bg-white rounded-lg border border-brown-light/20 overflow-hidden flex justify-center"
        style={{ minHeight: 500 }}
      >
        <iframe
          srcDoc={html}
          title="Email Preview"
          className="border-0"
          style={{
            width: view === "desktop" ? "100%" : 375,
            height: "100%",
            minHeight: 500,
          }}
        />
      </div>
    </div>
  )
}
