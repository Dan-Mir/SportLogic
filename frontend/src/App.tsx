import { Navigate, Route, Routes } from "react-router-dom";
import { AppConfig } from "./api";
import { AppConfigContext } from "./config";
import AppShellLayout from "./layout/AppShellLayout";
import Dashboard from "./pages/Dashboard";
import ModulePage from "./pages/ModulePage";
import SettingsPage from "./pages/SettingsPage";

export default function App({ config }: { config: AppConfig }) {
  return (
    <AppConfigContext.Provider value={config}>
      <Routes>
        <Route element={<AppShellLayout />}>
          <Route path="/" element={<Dashboard />} />
          <Route path="/modules/:name" element={<ModulePage />} />
          <Route path="/settings" element={<SettingsPage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Route>
      </Routes>
    </AppConfigContext.Provider>
  );
}
