import {
  Box,
  Button,
  ColorInput,
  Divider,
  Group,
  Modal,
  Paper,
  SimpleGrid,
  Stack,
  Text,
  TextInput,
  Title,
} from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";
import { IconDownload, IconUpload } from "@tabler/icons-react";
import { useCallback, useEffect, useState } from "react";
import { authHeaders } from "../auth";
import { useAppConfig } from "../config";

interface BrandPack {
  brand_name: string;
  brand_primary_color: string;
  public_domain: string | null;
}

export default function SettingsPage() {
  const config = useAppConfig();
  const [brand, setBrand] = useState<BrandPack>({
    brand_name: config.brand.name,
    brand_primary_color: config.brand.primaryColor,
    public_domain: config.brand.publicDomain,
  });
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [importOpened, { open: openImport, close: closeImport }] = useDisclosure(false);
  const [importData, setImportData] = useState("");

  const load = useCallback(async () => {
    try {
      const res = await fetch("/api/core/branding", { headers: authHeaders() });
      if (res.ok) {
        setBrand(await res.json());
      }
    } catch {
      // fallback to config
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  async function save() {
    setSaving(true);
    setMessage(null);
    setError(null);
    try {
      const res = await fetch("/api/core/branding", {
        method: "PUT",
        headers: { "Content-Type": "application/json", Authorization: `Bearer ${localStorage.getItem("sportlogic.access")}` },
        body: JSON.stringify(brand),
      });
      if (!res.ok) throw new Error(`Errore ${res.status}`);
      setMessage("Branding aggiornato. Ricarica la pagina per vedere i cambiamenti.");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Errore di salvataggio");
    } finally {
      setSaving(false);
    }
  }

  async function exportPack() {
    try {
      const res = await fetch("/api/core/branding/export", { headers: authHeaders() });
      const blob = new Blob([JSON.stringify(res, null, 2)], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "brand-pack.json";
      a.click();
      URL.revokeObjectURL(url);
    } catch {
      setError("Errore durante l'esportazione");
    }
  }

  async function importPack() {
    try {
      const data = JSON.parse(importData) as BrandPack;
      const res = await fetch("/api/core/branding/import", {
        method: "POST",
        headers: { "Content-Type": "application/json", Authorization: `Bearer ${localStorage.getItem("sportlogic.access")}` },
        body: JSON.stringify(data),
      });
      if (!res.ok) throw new Error(`Errore ${res.status}`);
      const updated = await res.json();
      setBrand(updated);
      setMessage("Brand pack importato.");
      closeImport();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Errore di importazione");
    }
  }

  return (
    <Stack gap="lg" maw={760}>
      <Title order={1} size={30}>
        Impostazioni
      </Title>

      {message && (
        <Text size="sm" c="teal">
          {message}
        </Text>
      )}
      {error && (
        <Text size="sm" c="red">
          {error}
        </Text>
      )}

      <Paper
        p="xl"
        radius="lg"
        style={{
          background: "var(--color-surface)",
          border: "1px solid var(--color-border)",
          boxShadow: "var(--shadow-xs)",
        }}
      >
        <Title order={4} mb="md">
          Branding
        </Title>
        <Stack gap="md">
          <TextInput
            label="Nome brand"
            value={brand.brand_name}
            onChange={(e) => setBrand({ ...brand, brand_name: e.currentTarget.value })}
          />
          <ColorInput
            label="Colore primario"
            value={brand.brand_primary_color}
            onChange={(c) => setBrand({ ...brand, brand_primary_color: c })}
            format="hex"
          />
          <TextInput
            label="Dominio pubblico"
            value={brand.public_domain || ""}
            onChange={(e) => setBrand({ ...brand, public_domain: e.currentTarget.value })}
          />
          <Group justify="flex-end">
            <Button onClick={save} loading={saving}>
              Salva branding
            </Button>
          </Group>
        </Stack>
      </Paper>

      <Paper
        p="xl"
        radius="lg"
        style={{
          background: "var(--color-surface)",
          border: "1px solid var(--color-border)",
          boxShadow: "var(--shadow-xs)",
        }}
      >
        <Title order={4} mb="md">
          Brand pack
        </Title>
        <Text size="sm" c="dimmed" mb="md">
          Esporta il pacchetto brand per usarlo su un altro impianto, o importane uno esistente.
        </Text>
        <Group>
          <Button variant="light" leftSection={<IconDownload size="1rem" stroke={1.75} />} onClick={exportPack}>
            Esporta brand pack
          </Button>
          <Button variant="light" leftSection={<IconUpload size="1rem" stroke={1.75} />} onClick={openImport}>
            Importa brand pack
          </Button>
        </Group>
      </Paper>

      <Modal opened={importOpened} onClose={closeImport} title="Importa brand pack" centered>
        <Stack gap="md">
          <Text size="sm" c="dimmed">
            Incolla il JSON del brand pack:
          </Text>
          <Box
            component="textarea"
            rows={6}
            value={importData}
            onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => setImportData(e.currentTarget.value)}
            style={{
              width: "100%",
              fontFamily: "var(--font-mono)",
              fontSize: "0.8rem",
              padding: "0.5rem",
              borderRadius: "var(--radius-md)",
              border: "1px solid var(--color-border)",
              background: "var(--color-surface-2)",
              color: "inherit",
              resize: "vertical",
            }}
          />
          <Group justify="flex-end">
            <Button variant="subtle" onClick={closeImport}>
              Annulla
            </Button>
            <Button onClick={importPack} disabled={!importData.trim()}>
              Importa
            </Button>
          </Group>
        </Stack>
      </Modal>
    </Stack>
  );
}