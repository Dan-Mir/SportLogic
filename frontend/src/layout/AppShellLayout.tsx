import {
  AppShell,
  Box,
  Burger,
  Divider,
  Group,
  NavLink,
  ScrollArea,
  Stack,
  Text,
  ThemeIcon,
} from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";
import {
  IconLayoutDashboard,
  IconPuzzle,
  IconSettings,
} from "@tabler/icons-react";
import { NavLink as RouterNavLink, Outlet, useLocation } from "react-router-dom";
import { useAppConfig } from "../config";

const MODULE_ICONS: Record<string, typeof IconPuzzle> = {
  core: IconPuzzle,
  anagrafica: IconPuzzle,
  corsi: IconPuzzle,
  "booking.fields": IconPuzzle,
};

export default function AppShellLayout() {
  const [opened, { toggle }] = useDisclosure();
  const location = useLocation();
  const config = useAppConfig();
  const modules = config.modules.filter((m) => m.has_frontend);

  return (
    <AppShell
      header={{ height: 64 }}
      navbar={{ width: 272, breakpoint: "sm", collapsed: { mobile: !opened } }}
      padding="xl"
    >
      <AppShell.Header
        style={{
          borderBottom: "1px solid var(--color-border)",
          background: "color-mix(in oklch, var(--color-surface) 88%, transparent)",
          backdropFilter: "blur(12px)",
        }}
      >
        <Group h="100%" px="lg" justify="space-between" wrap="nowrap">
          <Group gap="sm" wrap="nowrap">
            <Burger opened={opened} onClick={toggle} hiddenFrom="sm" size="sm" />
            <Box
              w={34}
              h={34}
              bg={config.brand.primaryColor}
              style={{
                borderRadius: 10,
                display: "grid",
                placeItems: "center",
                flexShrink: 0,
                boxShadow: "0 1px 3px oklch(24% 0.014 258 / 0.18)",
              }}
            >
              <Text c="white" fw={700} size="sm">
                {config.brand.name.charAt(0).toUpperCase()}
              </Text>
            </Box>
            <Box style={{ lineHeight: 1.2 }}>
              <Text fw={650} size="sm" style={{ letterSpacing: "-0.01em" }}>
                {config.brand.name}
              </Text>
              <Text size="xs" c="dimmed" className="mono-label">
                on-premise
              </Text>
            </Box>
          </Group>

          <Group gap="lg" wrap="nowrap">
            <Text
              component={RouterNavLink}
              to="/settings"
              size="sm"
              c={
                location.pathname === "/settings"
                  ? "var(--color-text)"
                  : "dimmed"
              }
              fw={600}
              style={{ textDecoration: "none", whiteSpace: "nowrap" }}
            >
              Impostazioni
            </Text>
            <Box
              w={32}
              h={32}
              style={{
                borderRadius: "50%",
                background: "var(--color-surface-3)",
                display: "grid",
                placeItems: "center",
              }}
            >
              <Text size="xs" fw={600} c="dimmed">
                AD
              </Text>
            </Box>
          </Group>
        </Group>
      </AppShell.Header>

      <AppShell.Navbar
        p="md"
        style={{
          borderRight: "1px solid var(--color-border)",
          background: "var(--color-surface)",
        }}
      >
        <AppShell.Section grow component={ScrollArea} type="hover" scrollbarSize={8}>
          <Stack gap={2}>
            <NavLink
              label="Dashboard"
              leftSection={<IconLayoutDashboard size="1.1rem" stroke={1.5} />}
              component={RouterNavLink}
              to="/"
              active={location.pathname === "/"}
              variant="light"
            />

            <Text
              size="xs"
              c="dimmed"
              mt="lg"
              mb={4}
              px="sm"
              fw={600}
              tt="uppercase"
              className="mono-label"
            >
              Moduli
            </Text>

            {modules.length === 0 ? (
              <Text size="sm" c="dimmed" px="sm" py="xs">
                Nessun modulo con interfaccia attivo.
              </Text>
            ) : (
              modules.map((m) => {
                const Icon = MODULE_ICONS[m.name] ?? IconPuzzle;
                return (
                  <NavLink
                    key={m.name}
                    label={m.label}
                    description={m.name}
                    leftSection={
                      <ThemeIcon variant="light" size="sm" color="gray">
                        <Icon size="0.8rem" stroke={1.75} />
                      </ThemeIcon>
                    }
                    component={RouterNavLink}
                    to={`/modules/${m.name}`}
                    active={location.pathname === `/modules/${m.name}`}
                    variant="light"
                  />
                );
              })
            )}
          </Stack>
        </AppShell.Section>

        <AppShell.Section>
          <Divider mb="sm" style={{ borderColor: "var(--color-border)" }} />
          <NavLink
            label="Impostazioni"
            leftSection={<IconSettings size="1.1rem" stroke={1.5} />}
            component={RouterNavLink}
            to="/settings"
            active={location.pathname === "/settings"}
            variant="light"
          />
          <Group justify="center" gap="xs" mt="sm">
            <Text size="xs" c="dimmed" className="mono-label">
              {config.brand.name}
            </Text>
            <Text size="xs" c="dimmed" className="mono-label">
              v0.1.0
            </Text>
          </Group>
        </AppShell.Section>
      </AppShell.Navbar>

      <AppShell.Main>
        <Outlet />
      </AppShell.Main>
    </AppShell>
  );
}
