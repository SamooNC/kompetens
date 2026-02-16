import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import HomePage from "./pages/HomePage";
import InventairePage from "./pages/InventairePage";
import RecruteurPage from "./pages/RecruteurPage";
import AidantPage from "./pages/AidantPage";

function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/inventaire" element={<InventairePage />} />
          <Route path="/recruteur" element={<RecruteurPage />} />
          <Route path="/aidant" element={<AidantPage />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}

export default App;
