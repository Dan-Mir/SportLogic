import { Navigate, Route, Routes } from "react-router-dom";
import { AppConfig } from "./api";
import { AppConfigContext } from "./config";
import { AuthContext, useAuthProvider } from "./auth";
import AppShellLayout from "./layout/AppShellLayout";
import Dashboard from "./pages/Dashboard";
import LoginPage from "./pages/LoginPage";
import MembersPage from "./pages/MembersPage";
import ModulePage from "./pages/ModulePage";
import SettingsPage from "./pages/SettingsPage";

export default function App({ config }: { config: AppConfig }) {
  const auth = useAuthProvider();

  return (
    <AppConfigContext.Provider value={config}>
      <AuthContext.Provider value={auth}>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route element={auth.token ? <AppShellLayout /> : <Navigate to="/login" replace />}>
            <Route path="/" element={<Dashboard />} />
            <Route path="/modules/anagrafica" element={<MembersPage />} />
            <Route path="/modules/:name" element={<ModulePage />} />
            <Route path="/settings" element={<SettingsPage />} />
          </Route>
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </AuthContext.Provider>
    </AppConfigContext.Provider>
  );
}
