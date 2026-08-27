import {
  Alert,
  Box,
  Button,
  Group,
  Paper,
  PasswordInput,
  Stack,
  Text,
  TextInput,
  Title,
} from "@mantine/core";
import { useForm } from "@mantine/form";
import { IconLock } from "@tabler/icons-react";
import { useState } from "react";
import { useAuth } from "../auth";

export default function LoginPage() {
  const { login } = useAuth();
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const form = useForm({
    initialValues: { email: "", password: "" },
    validate: {
      email: (v) => (/^\S+@\S+$/.test(v) ? null : "Email non valida"),
      password: (v) => (v.length > 0 ? null : "Password obbligatoria"),
    },
  });

  async function onSubmit(values: { email: string; password: string }) {
    setLoading(true);
    setError(null);
    try {
      await login(values.email, values.password);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Errore di accesso");
    } finally {
      setLoading(false);
    }
  }

  return (
    <Box
      style={{
        minHeight: "100vh",
        display: "grid",
        placeItems: "center",
        background: "var(--color-paper)",
        padding: "1rem",
      }}
    >
      <Paper
        w="100%"
        maw={400}
        p="xl"
        radius="lg"
        style={{
          background: "var(--color-surface)",
          border: "1px solid var(--color-border)",
          boxShadow: "var(--shadow-md)",
        }}
      >
        <Stack gap="sm" mb="lg">
          <Box
            w={40}
            h={40}
            style={{
              borderRadius: 12,
              background: "var(--color-surface-3)",
              display: "grid",
              placeItems: "center",
            }}
          >
            <IconLock size="1.25rem" stroke={1.6} />
          </Box>
          <Title order={3}>Accedi</Title>
          <Text size="sm" c="dimmed">
            Inserisci le tue credenziali per entrare nel gestionale.
          </Text>
        </Stack>

        {error && (
          <Alert color="red" mb="md" title="Accesso negato">
            {error}
          </Alert>
        )}

        <form onSubmit={form.onSubmit(onSubmit)}>
          <Stack gap="md">
            <TextInput
              label="Email"
              placeholder="nome@impianto.it"
              {...form.getInputProps("email")}
            />
            <PasswordInput
              label="Password"
              placeholder="••••••••"
              {...form.getInputProps("password")}
            />
            <Button type="submit" loading={loading} fullWidth>
              Accedi
            </Button>
          </Stack>
        </form>
      </Paper>
    </Box>
  );
}
