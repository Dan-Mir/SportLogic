import {
  Box,
  ColorSwatch,
  Divider,
  Group,
  Paper,
  SimpleGrid,
  Stack,
  Text,
  Title,
  Tooltip,
} from "@mantine/core";
import { useAppConfig } from "../config";

export default function SettingsPage() {
  const config = useAppConfig();

  return (
    <Stack gap="lg" maw={760}>
      <Title order={1} size={30}>
        Impostazioni
      </Title>

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
        <SimpleGrid cols={{ base: 1, sm: 2 }} spacing="lg">
          <Box>
            <Text size="sm" c="dimmed" mb={2}>
              Nome brand
            </Text>
            <Text fw={600}>{config.brand.name}</Text>
          </Box>
          <Box>
            <Text size="sm" c="dimmed" mb={2}>
              Dominio pubblico
            </Text>
            <Text fw={600}>{config.brand.publicDomain || "—"}</Text>
          </Box>
        </SimpleGrid>
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
        <Text size="xs" c="dimmed" className="mono-label">
          {config.brand.primaryColor}
        </Text>
      </Paper>
    </Stack>
  );
}
