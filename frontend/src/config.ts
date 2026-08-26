import { createContext, useContext } from "react";
import { AppConfig } from "./api";

export const AppConfigContext = createContext<AppConfig | null>(null);

export function useAppConfig(): AppConfig {
  const ctx = useContext(AppConfigContext);
  if (!ctx) {
    throw new Error("AppConfigContext non fornito");
  }
  return ctx;
}
