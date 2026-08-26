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
    white: "var(--color-surface)",
    black: "var(--color-text)",
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
      gray: [
        "#F6F7F9",
        "#ECEEF2",
        "#DDE0E6",
        "#C8CDD6",
        "#AEB5C2",
        "#939CAC",
        "#6F7A8C",
        "#55606F",
        "#3C4552",
        "#232A35",
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
      xs: "var(--shadow-xs)",
      sm: "var(--shadow-sm)",
      md: "var(--shadow-md)",
      lg: "var(--shadow-lg)",
      xl: "var(--shadow-lg)",
    },
    components: {
      Button: {
        defaultProps: { radius: "md" },
      },
      Card: {
        defaultProps: { radius: "lg", bg: "var(--color-surface)" },
        styles: {
          root: {
            border: "1px solid var(--color-border)",
            boxShadow: "var(--shadow-xs)",
          },
        },
      },
      Paper: {
        defaultProps: { radius: "lg" },
      },
      ThemeIcon: {
        defaultProps: { radius: "md" },
      },
      NavLink: {
        styles: {
          root: {
            borderRadius: "var(--radius-md)",
            fontWeight: 500,
          },
        },
      },
      Title: {
        styles: {
          root: {
            letterSpacing: "-0.015em",
          },
        },
      },
    },
  });
}
