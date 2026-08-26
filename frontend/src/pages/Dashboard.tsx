import {
  Card,
  Group,
  SimpleGrid,
  Text,
  ThemeIcon,
  Title,
} from "@mantine/core";
import {
  IconCalendarEvent,
  IconCreditCard,
  IconHeartbeat,
  IconUsers,
} from "@tabler/icons-react";
import { useAppConfig } from "../config";

const stats = [
  { label: "Soci attivi", icon: IconUsers, color: "brand" },
  { label: "Prenotazioni oggi", icon: IconCalendarEvent, color: "teal" },
  { label: "Incassi del mese", icon: IconCreditCard, color: "violet" },
  { label: "Certificati in scadenza", icon: IconHeartbeat, color: "red" },
];

export default function Dashboard() {
  const config = useAppConfig();

  return (
    <div>
      <Title order={2} mb="xs">
        Benvenuto in {config.brand.name}
      </Title>
      <Text c="dimmed" mb="lg">
        Panoramica dell'impianto. I dati reali arriveranno con i moduli
        corrispondenti (Fase 1).
      </Text>

      <SimpleGrid cols={{ base: 1, sm: 2, lg: 4 }} spacing="md" mb="lg">
        {stats.map((s) => (
          <Card key={s.label} withBorder padding="lg" bg="var(--color-surface)">
            <Group justify="space-between" align="flex-start">
              <ThemeIcon variant="light" color={s.color} size="lg">
                <s.icon size="1.25rem" stroke={1.5} />
              </ThemeIcon>
            </Group>
            <Text fz={30} fw={700} mt="md" lh={1} className="tabular">
              —
            </Text>
            <Text size="sm" c="dimmed" mt={4}>
              {s.label}
            </Text>
          </Card>
        ))}
      </SimpleGrid>

      <Card withBorder padding="lg" bg="var(--color-surface)">
        <Title order={4} mb="md">
          Moduli attivi ({config.modules.length})
        </Title>
        <SimpleGrid cols={{ base: 1, sm: 2, lg: 3 }} spacing="md">
          {config.modules.map((m) => (
            <Group key={m.name} gap="sm" wrap="nowrap">
              <div>
                <Text fw={600} size="sm">
                  {m.label}
                </Text>
                <Text size="xs" c="dimmed" className="tabular">
                  {m.name} · v{m.version}
                </Text>
              </div>
            </Group>
          ))}
        </SimpleGrid>
      </Card>
    </div>
  );
}
