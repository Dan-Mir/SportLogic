import {
  Badge,
  Box,
  Button,
  Group,
  Paper,
  SimpleGrid,
  Stack,
  Text,
  ThemeIcon,
  Title,
} from "@mantine/core";
import {
  IconArrowRight,
  IconCalendarEvent,
  IconShieldCheck,
  IconUserPlus,
} from "@tabler/icons-react";
import { Link } from "react-router-dom";
import { useAppConfig } from "../config";
import { moduleIcon } from "../moduleIcons";

export default function Dashboard() {
  const config = useAppConfig();
  const modules = config.modules.filter((m) => m.has_frontend);

  const today = new Date().toLocaleDateString("it-IT", {
    weekday: "long",
    day: "numeric",
    month: "long",
    year: "numeric",
  });

  return (
    <Stack gap="xl" maw={1120}>
      <Group className="page-intro" justify="space-between" align="flex-end" wrap="wrap" gap="md">
        <Box maw={560}>
          <Text size="sm" c="dimmed" mb={4}>
            {today.charAt(0).toUpperCase() + today.slice(1)}
          </Text>
          <Title order={1} size={34}>
            Panoramica operativa
          </Title>
          <Text size="sm" c="dimmed" mt={6}>Le informazioni principali del tuo impianto, in un unico punto.</Text>
        </Box>
        <Group gap="sm" wrap="wrap">
          <Button
            leftSection={<IconUserPlus size="1rem" stroke={1.75} />}
            component={Link}
            to="/modules/anagrafica"
          >
            Nuovo socio
          </Button>
          <Button
            variant="light"
            leftSection={<IconCalendarEvent size="1rem" stroke={1.75} />}
            component={Link}
            to="/modules/booking.fields"
          >
            Nuova prenotazione
          </Button>
        </Group>
      </Group>

      <SimpleGrid cols={{ base: 1, sm: 2 }} spacing="md">
        <Paper
          p={{ base: "md", sm: "lg" }}
          radius="lg"
          className="action-surface"
          style={{
            background: "var(--color-surface)",
          }}
        >
          <Group gap="sm" mb="md">
            <ThemeIcon variant="light" color="brand" size="lg">
              <IconCalendarEvent size="1.2rem" stroke={1.6} />
            </ThemeIcon>
            <div>
              <Title order={4}>Prossime attività</Title>
              <Text size="xs" c="dimmed">
                Corsi, campi e lezioni in calendario
              </Text>
            </div>
          </Group>
          <Stack gap="xs">
            {[1, 2].map((i) => (
              <Group
                key={i}
                justify="space-between"
                p="sm"
                style={{
                  background: "var(--color-surface-2)",
                  borderRadius: "var(--radius-md)",
                }}
              >
                <Text size="sm" c="dimmed">
                  Nessuna attività pianificata
                </Text>
                <Text size="xs" c="dimmed" className="tabular">
                  In attesa di calendario
                </Text>
              </Group>
            ))}
          </Stack>
        </Paper>

        <Paper
          p={{ base: "md", sm: "lg" }}
          radius="lg"
          className="action-surface"
          style={{
            background: "var(--color-surface)",
          }}
        >
          <Group gap="sm" mb="lg">
            <ThemeIcon variant="light" color="yellow" size="lg">
              <IconShieldCheck size="1.2rem" stroke={1.6} />
            </ThemeIcon>
            <div>
              <Title order={4}>Scadenze da attenzionare</Title>
              <Text size="xs" c="dimmed">
                Certificati medici e abbonamenti in scadenza
              </Text>
            </div>
          </Group>
          <Stack gap="xs">
            <Group
              justify="space-between"
              p="sm"
              style={{
                background: "var(--color-surface-2)",
                borderRadius: "var(--radius-md)",
              }}
            >
              <Text size="sm" c="dimmed">
                Tutto sotto controllo
              </Text>
              <Badge variant="light" color="gray">
                nessuna
              </Badge>
            </Group>
          </Stack>
        </Paper>
      </SimpleGrid>

      <Box>
        <Group justify="space-between" mb="md" align="flex-end">
          <Box>
            <Title order={3}>Aree di lavoro</Title>
            <Text size="sm" c="dimmed" mt={3}>Accedi alle funzioni disponibili per il tuo ruolo.</Text>
          </Box>
          <Text size="sm" c="dimmed" className="tabular">
            {modules.length} attive
          </Text>
        </Group>
        <SimpleGrid cols={{ base: 1, sm: 2, lg: 3 }} spacing="md">
          {modules.map((m) => {
            const Icon = moduleIcon(m.name);
            return (
              <Paper
                key={m.name}
                component={Link}
                to={`/modules/${m.name}`}
                p="lg"
                radius="lg"
                className="action-surface"
                style={{
                  background: "var(--color-surface)",
                  textDecoration: "none",
                  color: "inherit",
                }}
              >
                <Group justify="space-between" mb="md">
                  <ThemeIcon variant="light" color="gray" size="xl">
                    <Icon size="1.3rem" stroke={1.6} />
                  </ThemeIcon>
                  <IconArrowRight size="1rem" stroke={1.5} style={{ color: "var(--color-text-faint)" }} />
                </Group>
                <Text fw={650} size="sm">
                  {m.label}
                </Text>
                <Text size="xs" c="dimmed" mt={4} className="mono-label">
                  {m.name}
                </Text>
              </Paper>
            );
          })}
        </SimpleGrid>
      </Box>
    </Stack>
  );
}
