import { generateColors } from "@mantine/colors-generator";
import type { MantineColorsTuple } from "@mantine/core";

export interface ModuleInfo {
  name: string;
  label: string;
  description: string;
  version: string;
  has_frontend: boolean;
}

export interface BrandConfig {
  name: string;
  primaryColor: string;
  publicDomain: string;
  shades: MantineColorsTuple;
}

export interface AppConfig {
  brand: BrandConfig;
  modules: ModuleInfo[];
}

async function fetchJson<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(path, init);
  if (!res.ok) {
    throw new Error(`Richiesta fallita (${res.status})`);
  }
  return res.json();
}

interface InfoResponse {
  brand: { name?: string; primary_color?: string; public_domain?: string };
}

interface ModulesResponse {
  modules: ModuleInfo[];
}

export async function bootstrap(): Promise<AppConfig> {
  const [info, modules] = await Promise.all([
    fetchJson<InfoResponse>("/api/core/info"),
    fetchJson<ModulesResponse>("/api/modules"),
  ]);

  const primaryColor = info.brand.primary_color ?? "#2563eb";

  return {
    brand: {
      name: info.brand.name ?? "SportLogic",
      primaryColor,
      publicDomain: info.brand.public_domain ?? "",
      shades: generateColors(primaryColor),
    },
    modules: modules.modules ?? [],
  };
}
