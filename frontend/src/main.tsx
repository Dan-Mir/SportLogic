import { MantineProvider } from "@mantine/core";
import "@mantine/core/styles.css";
import "@fontsource-variable/inter";
import "@fontsource-variable/jetbrains-mono";
import "./tokens.css";
import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import App from "./App";
import { bootstrap } from "./api";
import { buildTheme } from "./theme";

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

  const theme = buildTheme(config);

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
