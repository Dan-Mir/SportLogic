import { Navigate, Route, Routes } from "react-router-dom";
import { AppConfig } from "./api";
import { AppConfigContext } from "./config";
import { AuthContext, useAuthProvider } from "./auth";

// Base neutra post-refactoring: il contratto di routing e il gate di auth
// restano stabili. Le pagine verranno rigenerate da zero (vedi
// prompts/2026-10-07_brief-frontend.md) senza riferimenti al vecchio UI.
export default function App({ config }: { config: AppConfig }) {
  const auth = useAuthProvider();

  return (
    <AppConfigContext.Provider value={config}>
      <AuthContext.Provider value={auth}>
        <Routes>
          <Route path="*" element={<div>Frontend in rigenerazione.</div>} />
        </Routes>
      </AuthContext.Provider>
    </AppConfigContext.Provider>
  );
}
