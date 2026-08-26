import {
  Badge,
  Box,
  Group,
  Paper,
  Stack,
  Text,
  ThemeIcon,
  Title,
} from "@mantine/core";
import { IconAlertTriangle } from "@tabler/icons-react";
import { useParams } from "react-router-dom";
import { useAppConfig } from "../config";
import { moduleIcon } from "../moduleIcons";

export default function ModulePage() {
  const { name } = useParams();
  const config = useAppConfig();
  const module = config.modules.find((m) => m.name === name);

  if (!module) {
    return (
      <Paper
        p="xl"
        radius="lg"
        style={{
          background: "var(--color-surface)",
          border: "1px solid var(--color-border)",
        }}
      >
        <Group gap="sm">
          <ThemeIcon variant="light" color="red" size="lg">
            <IconAlertTriangle size="1.2rem" stroke={1.6} />
          </ThemeIcon>
          <Text fw={600}>Modulo "{name}" non trovato o non attivo.</Text>
        </Group>
      </Paper>
    );
  }

  const Icon = moduleIcon(module.name);

  return (
    <Stack gap="lg" maw={1120}>
      <Group gap="sm" align="center">
        <ThemeIcon variant="light" color="brand" size="xl">
          <Icon size="1.4rem" stroke={1.5} />
        </ThemeIcon>
        <Box>
          <Group gap="xs" align="center">
            <Title order={1} size={30}>
              {module.label}
            </Title>
            <Badge variant="light" color="gray" className="mono-label">
              v{module.version}
            </Badge>
          </Group>
          <Text c="dimmed" size="sm">
            {module.description}
          </Text>
        </Box>
      </Group>

      <Paper
        p="xl"
        radius="lg"
        style={{
          background: "var(--color-surface)",
          border: "1px solid var(--color-border)",
          boxShadow: "var(--shadow-xs)",
        }}
      >
        <Stack align="center" gap="xs" py="xl">
          <Title order={4}>Modulo in sviluppo</Title>
          <Text size="sm" c="dimmed" ta="center" maw={440}>
            La UI di questo modulo non è ancora implementata. Verrà sviluppata
            nelle fasi successive del progetto.
          </Text>
        </Stack>
      </Paper>
    </Stack>
  );
}
