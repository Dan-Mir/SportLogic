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
        "#D6D3CD",
        "#B4B0A6",
        "#8E8A7D",
        "#6B675C",
        "#49463D",
        "#3A372F",
        "#2D2A24",
        "#211F1A",
        "#161411",
        "#0C0B09",
      ],
      gray: [
        "#F7F5F1",
        "#EFECE6",
        "#E2DED6",
        "#CEC8BD",
        "#B6AFA1",
        "#9C9588",
        "#7A7468",
        "#5C574E",
        "#3F3B34",
        "#24211C",
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
          root: { borderRadius: "var(--radius-md)", fontWeight: 500 },
        },
      },
      Title: {
        styles: { root: { letterSpacing: "-0.02em" } },
      },
      Divider: {
        styles: { root: { borderColor: "var(--color-border)" } },
      },
    },
  });
}
