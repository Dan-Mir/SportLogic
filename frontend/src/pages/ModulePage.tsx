import {
  Alert,
  Badge,
  Card,
  Group,
  Stack,
  Text,
  Title,
} from "@mantine/core";
import { IconInfoCircle } from "@tabler/icons-react";
import { useParams } from "react-router-dom";
import { useAppConfig } from "../config";

export default function ModulePage() {
  const { name } = useParams();
  const config = useAppConfig();
  const module = config.modules.find((m) => m.name === name);

  if (!module) {
    return (
      <Alert color="red" icon={<IconInfoCircle />}>
        Modulo "{name}" non trovato o non attivo.
      </Alert>
    );
  }

  return (
    <div>
      <Group mb="xs" gap="sm" align="center">
        <Title order={2}>{module.label}</Title>
        <Badge variant="light" color="gray" className="tabular">
          v{module.version}
        </Badge>
      </Group>
      <Text c="dimmed" mb="lg">
        {module.description}
      </Text>

      <Card withBorder padding="xl" bg="var(--color-surface)">
        <Stack align="center" gap="xs" py="xl">
          <Title order={4}>Modulo in sviluppo</Title>
          <Text size="sm" c="dimmed" ta="center" maw={420}>
            La UI di questo modulo non è ancora implementata. Verrà sviluppata
            nelle fasi successive del progetto.
          </Text>
        </Stack>
      </Card>
    </div>
  );
}
