import {
  Badge,
  Box,
  Button,
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
import { IconPlus, IconUsers } from "@tabler/icons-react";
import { useCallback, useEffect, useState } from "react";
import { authHeaders } from "../auth";

interface Member {
  id: number;
  first_name: string;
  last_name: string;
  fiscal_code: string | null;
  email: string | null;
  phone: string | null;
  city: string | null;
  is_active: boolean;
}

export default function MembersPage() {
  const [members, setMembers] = useState<Member[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [q, setQ] = useState("");
  const [opened, { open, close }] = useDisclosure(false);

  const load = useCallback(async (search?: string) => {
    setLoading(true);
    setError(null);
    try {
      const url = search ? `/api/anagrafica/members?q=${encodeURIComponent(search)}` : "/api/anagrafica/members";
      const res = await fetch(url, { headers: authHeaders() });
      if (!res.ok) throw new Error(`Errore ${res.status}`);
      setMembers(await res.json());
    } catch (e) {
      setError(e instanceof Error ? e.message : "Errore di caricamento");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  return (
    <Stack gap="lg" maw={1120}>
      <Group justify="space-between" align="flex-end" wrap="wrap" gap="md">
        <Box>
          <Text size="sm" c="dimmed" className="mono-label" mb={4} tt="uppercase">
            Anagrafica
          </Text>
          <Title order={1} size={30}>
            Soci
          </Title>
        </Box>
        <Button leftSection={<IconPlus size="1rem" stroke={1.75} />} onClick={open}>
          Nuovo socio
        </Button>
      </Group>

      <Group gap="sm">
        <TextInput
          placeholder="Cerca per nome, cognome o codice fiscale…"
          w={320}
          value={q}
          onChange={(e) => setQ(e.currentTarget.value)}
          onKeyDown={(e) => e.key === "Enter" && load(q)}
        />
        <Button variant="light" onClick={() => load(q)}>
          Cerca
        </Button>
      </Group>

      {error && <Text c="red">{error}</Text>}

      {loading ? (
        <Text c="dimmed">Caricamento…</Text>
      ) : members.length === 0 ? (
        <Paper p="xl" radius="lg" style={{ border: "1px solid var(--color-border)" }}>
          <Stack align="center" gap="xs" py="lg">
            <IconUsers size="2rem" stroke={1.25} style={{ color: "var(--color-text-faint)" }} />
            <Text fw={600}>Nessun socio registrato</Text>
            <Text size="sm" c="dimmed" ta="center" maw={380}>
              Aggiungi il primo socio per iniziare a gestire iscrizioni e tessere.
            </Text>
          </Stack>
        </Paper>
      ) : (
        <SimpleGrid cols={{ base: 1, sm: 2, lg: 3 }} spacing="md">
          {members.map((m) => (
            <Paper key={m.id} p="lg" radius="lg" style={{ border: "1px solid var(--color-border)" }}>
              <Group justify="space-between" mb="xs">
                <Text fw={650}>
                  {m.last_name} {m.first_name}
                </Text>
                <Badge variant="light" color={m.is_active ? "teal" : "gray"}>
                  {m.is_active ? "attivo" : "inattivo"}
                </Badge>
              </Group>
              <Stack gap={2}>
                <Text size="xs" c="dimmed" className="mono-label">
                  {m.fiscal_code ?? "CF non indicato"}
                </Text>
                <Text size="sm" c="dimmed">
                  {m.email ?? "—"}
                </Text>
                <Text size="sm" c="dimmed">
                  {m.city ? `${m.city}${m.phone ? ` · ${m.phone}` : ""}` : (m.phone ?? "—")}
                </Text>
              </Stack>
            </Paper>
          ))}
        </SimpleGrid>
      )}

      <CreateMemberModal opened={opened} onClose={close} onCreated={() => load(q)} />
    </Stack>
  );
}

function CreateMemberModal({
  opened,
  onClose,
  onCreated,
}: {
  opened: boolean;
  onClose: () => void;
  onCreated: () => void;
}) {
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function submit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setSaving(true);
    setError(null);
    const data = new FormData(e.currentTarget);
    const body = {
      first_name: data.get("first_name"),
      last_name: data.get("last_name"),
      fiscal_code: data.get("fiscal_code") || null,
      email: data.get("email") || null,
      phone: data.get("phone") || null,
      city: data.get("city") || null,
    };
    try {
      const res = await fetch("/api/anagrafica/members", {
        method: "POST",
        headers: { "Content-Type": "application/json", ...authHeaders() },
        body: JSON.stringify(body),
      });
      if (!res.ok) throw new Error(`Errore ${res.status}`);
      onCreated();
      onClose();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Errore di salvataggio");
    } finally {
      setSaving(false);
    }
  }

  return (
    <Modal opened={opened} onClose={onClose} title="Nuovo socio" centered>
      <form onSubmit={submit}>
        <Stack gap="md">
          {error && <Text c="red" size="sm">{error}</Text>}
          <SimpleGrid cols={2}>
            <TextInput name="first_name" label="Nome" required />
            <TextInput name="last_name" label="Cognome" required />
          </SimpleGrid>
          <TextInput name="fiscal_code" label="Codice fiscale" />
          <TextInput name="email" label="Email" type="email" />
          <SimpleGrid cols={2}>
            <TextInput name="phone" label="Telefono" />
            <TextInput name="city" label="Città" />
          </SimpleGrid>
          <Group justify="flex-end">
            <Button variant="subtle" onClick={onClose}>
              Annulla
            </Button>
            <Button type="submit" loading={saving}>
              Salva
            </Button>
          </Group>
        </Stack>
      </form>
    </Modal>
  );
}
