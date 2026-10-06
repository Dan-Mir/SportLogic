import {
  Badge,
  Box,
  Button,
  Group,
  Modal,
  Paper,
  Select,
  Stack,
  Table,
  Text,
  TextInput,
  Title,
} from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";
import { IconPlus, IconUsers } from "@tabler/icons-react";
import { useCallback, useEffect, useState } from "react";
import { authHeaders } from "../auth";

interface User {
  id: number;
  email: string;
  full_name: string;
  role: string;
  is_active: boolean;
}

const ROLES = ["admin", "gestore", "reception", "istruttore", "socio"];

export default function UsersPage() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [opened, { open, close }] = useDisclosure(false);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const res = await fetch("/api/core/users", { headers: authHeaders() });
      if (res.ok) setUsers(await res.json());
    } catch {
      /* ignore */
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  return (
    <Stack gap="lg" maw={960}>
      <Group justify="space-between" align="flex-end" wrap="wrap" gap="md">
        <Box>
          <Text size="sm" c="dimmed" className="mono-label" mb={4} tt="uppercase">
            Amministrazione
          </Text>
          <Title order={1} size={30}>
            Utenti
          </Title>
        </Box>
        <Button leftSection={<IconPlus size="1rem" stroke={1.75} />} onClick={open}>
          Nuovo utente
        </Button>
      </Group>

      {loading ? (
        <Text c="dimmed">Caricamento…</Text>
      ) : users.length === 0 ? (
        <Paper p="xl" radius="lg" style={{ border: "1px solid var(--color-border)" }}>
          <Stack align="center" gap="xs" py="lg">
            <IconUsers size="2rem" stroke={1.25} style={{ color: "var(--color-text-faint)" }} />
            <Text fw={600}>Nessun utente</Text>
          </Stack>
        </Paper>
      ) : (
        <Paper
          p="md"
          radius="lg"
          style={{
            background: "var(--color-surface)",
            border: "1px solid var(--color-border)",
            boxShadow: "var(--shadow-xs)",
          }}
        >
          <Table>
            <Table.Thead>
              <Table.Tr>
                <Table.Th>Nome</Table.Th>
                <Table.Th>Email</Table.Th>
                <Table.Th>Ruolo</Table.Th>
                <Table.Th>Stato</Table.Th>
              </Table.Tr>
            </Table.Thead>
            <Table.Tbody>
              {users.map((u) => (
                <Table.Tr key={u.id}>
                  <Table.Td fw={600}>{u.full_name}</Table.Td>
                  <Table.Td>{u.email}</Table.Td>
                  <Table.Td>
                    <Badge variant="light" color={u.role === "admin" ? "red" : "gray"}>
                      {u.role}
                    </Badge>
                  </Table.Td>
                  <Table.Td>
                    <Badge variant="filled" color={u.is_active ? "teal" : "gray"}>
                      {u.is_active ? "attivo" : "inattivo"}
                    </Badge>
                  </Table.Td>
                </Table.Tr>
              ))}
            </Table.Tbody>
          </Table>
        </Paper>
      )}

      <CreateUserModal opened={opened} onClose={close} onCreated={load} />
    </Stack>
  );
}

function CreateUserModal({
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
  const [role, setRole] = useState<string>("reception");

  async function submit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setSaving(true);
    setError(null);
    const data = new FormData(e.currentTarget);
    const body = {
      email: data.get("email"),
      password: data.get("password"),
      full_name: data.get("full_name"),
      role,
    };
    try {
      const res = await fetch("/api/core/users", {
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
    <Modal opened={opened} onClose={onClose} title="Nuovo utente" centered>
      <form onSubmit={submit}>
        <Stack gap="md">
          {error && <Text c="red" size="sm">{error}</Text>}
          <TextInput name="email" label="Email" type="email" required />
          <TextInput name="full_name" label="Nome completo" required />
          <TextInput name="password" label="Password" type="password" required />
          <Select
            label="Ruolo"
            data={ROLES}
            value={role}
            onChange={(v) => setRole(v || "reception")}
          />
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