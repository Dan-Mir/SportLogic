import { MantineProvider, createTheme } from "@mantine/core";
import "@mantine/core/styles.css";
import "@fontsource-variable/inter";
import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import App from "./App";
import { bootstrap } from "./api";

async function start() {
  const root = document.getElementById("root")!;

  let config;
  try {
    config = await bootstrap();
  } catch (err) {
    root.innerHTML = `<p style="font-family: sans-serif; padding: 2rem;">Impossibile caricare la configurazione: ${err}</p>`;
    return;
  }

  document.title = config.brand.name;

  const theme = createTheme({
    primaryColor: "brand",
    primaryShade: 6,
    fontFamily: "'Inter Variable', sans-serif",
    colors: {
      brand: config.brand.shades,
    },
  });

  ReactDOM.createRoot(root).render(
    <React.StrictMode>
      <MantineProvider theme={theme}>
        <BrowserRouter>
          <App config={config} />
        </BrowserRouter>
      </MantineProvider>
    </React.StrictMode>,
  );
}

start();
