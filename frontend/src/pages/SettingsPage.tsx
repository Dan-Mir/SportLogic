import {
  Card,
  ColorSwatch,
  Divider,
  Group,
  SimpleGrid,
  Text,
  Title,
  Tooltip,
} from "@mantine/core";
import { useAppConfig } from "../config";

export default function SettingsPage() {
  const config = useAppConfig();

  return (
    <div>
      <Title order={2} mb="lg">
        Impostazioni
      </Title>

      <Card withBorder padding="lg" mb="md" bg="var(--color-surface)">
        <Title order={4} mb="md">
          Branding
        </Title>
        <SimpleGrid cols={{ base: 1, sm: 2 }} spacing="lg">
          <div>
            <Text size="sm" c="dimmed" mb={2}>
              Nome brand
            </Text>
            <Text fw={600}>{config.brand.name}</Text>
          </div>
          <div>
            <Text size="sm" c="dimmed" mb={2}>
              Dominio pubblico
            </Text>
            <Text fw={600}>{config.brand.publicDomain || "—"}</Text>
          </div>
        </SimpleGrid>
      </Card>

      <Card withBorder padding="lg" bg="var(--color-surface)">
        <Title order={4} mb="md">
          Colore primario
        </Title>
        <Group gap="xs">
          {config.brand.shades.map((shade, i) => (
            <Tooltip key={i} label={shade} openDelay={800} withArrow>
              <ColorSwatch color={shade} size={28} />
            </Tooltip>
          ))}
        </Group>
        <Divider my="lg" />
        <Text size="xs" c="dimmed" className="tabular">
          {config.brand.primaryColor}
        </Text>
      </Card>
    </div>
  );
}
