import { BrowserRouter, Routes, Route } from "react-router-dom"
import { EditorPage } from "./pages/EditorPage"
import { ArchivePage } from "./pages/ArchivePage"

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<EditorPage />} />
        <Route path="/archive" element={<ArchivePage />} />
        <Route path="/message/:id" element={<EditorPage />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
