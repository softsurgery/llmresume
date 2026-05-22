import { BrowserRouter, Routes, Route } from "react-router-dom";
import GeneratePage from "@/pages/GeneratePage";
import DownloadPage from "@/pages/DownloadPage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<GeneratePage />} />
        <Route path="/download/:jobId" element={<DownloadPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
