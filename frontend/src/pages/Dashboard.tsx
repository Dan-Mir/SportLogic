import {
  ActionIcon,
  Box,
  Button,
  Card,
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
  IconCash,
  IconHeartbeat,
  IconPuzzle,
  IconUserPlus,
  IconUsers,
} from "@tabler/icons-react";
import { useAppConfig } from "../config";

const stats = [
  {
    label: "Soci attivi",
    icon: IconUsers,
    color: "blue",
    tint: "oklch(95% 0.03 250)",
  },
  {
    label: "Prenotazioni oggi",
    icon: IconCalendarEvent,
    color: "teal",
    tint: "oklch(96% 0.03 180)",
  },
  {
    label: "Incassi del mese",
    icon: IconCash,
    color: "violet",
    tint: "oklch(96% 0.03 300)",
  },
  {
    label: "Certificati in scadenza",
    icon: IconHeartbeat,
    color: "red",
    tint: "oklch(96% 0.03 20)",
  },
];

const quickActions = [
  { label: "Nuovo socio", icon: IconUserPlus, color: "brand" },
  { label: "Nuova prenotazione", icon: IconCalendarEvent, color: "teal" },
];

export default function Dashboard() {
  const config = useAppConfig();

  return (
    <Stack gap="xl">
      <Group justify="space-between" align="flex-end" wrap="wrap">
        <div>
          <Title order={2} mb={4}>
            Benvenuto in {config.brand.name}
          </Title>
          <Text c="dimmed" size="sm">
            Panoramica dell'impianto. I dati reali arriveranno con i moduli
            corrispondenti (Fase 1).
          </Text>
        </div>
        <Group gap="xs">
          {quickActions.map((a) => (
            <Button
              key={a.label}
              variant="light"
              color={a.color}
              leftSection={<a.icon size="1rem" stroke={1.75} />}
            >
              {a.label}
            </Button>
          ))}
        </Group>
      </Group>

      <SimpleGrid cols={{ base: 1, sm: 2, lg: 4 }} spacing="md">
        {stats.map((s) => (
          <Card
            key={s.label}
            padding="lg"
            className="hover-lift"
            bg="var(--color-surface)"
          >
            <Group justify="space-between" align="flex-start">
              <ThemeIcon
                variant="light"
                color={s.color}
                size={42}
                radius="md"
              >
                <s.icon size="1.3rem" stroke={1.6} />
              </ThemeIcon>
            </Group>
            <Text fz={32} fw={700} mt="md" lh={1} className="tabular">
              —
            </Text>
            <Text size="sm" c="dimmed" mt={4}>
              {s.label}
            </Text>
          </Card>
        ))}
      </SimpleGrid>

      <Card padding="lg" bg="var(--color-surface)">
        <Group justify="space-between" mb="md">
          <Title order={4}>Moduli attivi</Title>
          <Text size="sm" c="dimmed" className="mono-label">
            {config.modules.length} caricati
          </Text>
        </Group>

        <SimpleGrid cols={{ base: 1, sm: 2, lg: 3 }} spacing="sm">
          {config.modules.map((m) => (
            <Paper
              key={m.name}
              p="md"
              radius="md"
              className="hover-lift"
              style={{
                background: "var(--color-surface)",
                border: "1px solid var(--color-border)",
              }}
            >
              <Group gap="sm" wrap="nowrap">
                <ThemeIcon variant="light" size="lg" color="gray">
                  <IconPuzzle size="1.05rem" stroke={1.6} />
                </ThemeIcon>
                <Box style={{ flex: 1, minWidth: 0 }}>
                  <Text fw={600} size="sm">
                    {m.label}
                  </Text>
                  <Text size="xs" c="dimmed" className="mono-label">
                    {m.name} · v{m.version}
                  </Text>
                </Box>
                <ActionIcon variant="subtle" color="gray" size="md" radius="md">
                  <IconArrowRight size="1rem" stroke={1.75} />
                </ActionIcon>
              </Group>
            </Paper>
          ))}
        </SimpleGrid>
      </Card>
    </Stack>
  );
}
