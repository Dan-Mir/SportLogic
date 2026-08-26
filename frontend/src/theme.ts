import { createTheme, type MantineThemeOverride } from "@mantine/core";
import type { AppConfig } from "./api";

export function buildTheme(config: AppConfig): MantineThemeOverride {
  return createTheme({
    primaryColor: "brand",
    fontFamily: "var(--font-sans)",
    fontFamilyMonospace: "var(--font-mono)",
    headings: {
      fontFamily: "var(--font-sans)",
      fontWeight: "650",
    },
    defaultRadius: "md",
    primaryShade: 6,
    white: "oklch(100% 0 0)",
    black: "oklch(24% 0.012 258)",
    colors: {
      brand: config.brand.shades,
      dark: [
        "#C9CBD3",
        "#A6AAB8",
        "#82879B",
        "#5F657E",
        "#3D445F",
        "#2A3049",
        "#21263A",
        "#1A1E2E",
        "#12151F",
        "#0B0D14",
      ],
    },
    spacing: {
      xs: "0.375rem",
      sm: "0.5rem",
      md: "1rem",
      lg: "1.5rem",
      xl: "2rem",
    },
    radius: {
      xs: "var(--radius-sm)",
      sm: "var(--radius-sm)",
      md: "var(--radius-md)",
      lg: "var(--radius-lg)",
      xl: "var(--radius-xl)",
    },
    shadows: {
      xs: "0 1px 2px oklch(24% 0.012 258 / 0.04)",
      sm: "0 1px 3px oklch(24% 0.012 258 / 0.06), 0 1px 2px oklch(24% 0.012 258 / 0.04)",
      md: "0 4px 8px oklch(24% 0.012 258 / 0.06), 0 2px 4px oklch(24% 0.012 258 / 0.04)",
      lg: "0 12px 24px oklch(24% 0.012 258 / 0.08), 0 4px 8px oklch(24% 0.012 258 / 0.05)",
      xl: "0 20px 40px oklch(24% 0.012 258 / 0.10), 0 8px 16px oklch(24% 0.012 258 / 0.06)",
    },
    components: {
      Button: {
        defaultProps: { radius: "md" },
      },
      Card: {
        defaultProps: { radius: "lg" },
      },
      Paper: {
        defaultProps: { radius: "lg" },
      },
      ThemeIcon: {
        defaultProps: { radius: "md" },
      },
    },
  });
}
