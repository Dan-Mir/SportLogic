import {
  AppShell,
  Box,
  Burger,
  Group,
  NavLink,
  ScrollArea,
  Text,
  ThemeIcon,
  Tooltip,
} from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";
import {
  IconLayoutDashboard,
  IconPuzzle,
  IconSettings,
} from "@tabler/icons-react";
import { NavLink as RouterNavLink, Outlet, useLocation } from "react-router-dom";
import { useAppConfig } from "../config";

export default function AppShellLayout() {
  const [opened, { toggle }] = useDisclosure();
  const location = useLocation();
  const config = useAppConfig();
  const modules = config.modules.filter((m) => m.has_frontend);

  return (
    <AppShell
      header={{ height: 64 }}
      navbar={{ width: 264, breakpoint: "sm", collapsed: { mobile: !opened } }}
      padding="lg"
    >
      <AppShell.Header
        px="lg"
        style={{
          borderBottom: "1px solid var(--color-border)",
          background: "var(--color-surface)",
        }}
      >
        <Group h="100%" justify="space-between" wrap="nowrap">
          <Group gap="sm" wrap="nowrap">
            <Burger opened={opened} onClick={toggle} hiddenFrom="sm" size="sm" />
            <Box
              w={32}
              h={32}
              bg={config.brand.primaryColor}
              style={{
                borderRadius: 8,
                display: "grid",
                placeItems: "center",
                flexShrink: 0,
              }}
            >
              <Text c="white" fw={700} size="sm">
                {config.brand.name.charAt(0).toUpperCase()}
              </Text>
            </Box>
            <Box style={{ lineHeight: 1.15 }}>
              <Text fw={650} size="sm">
                {config.brand.name}
              </Text>
              <Text size="xs" c="dimmed">
                Gestionale impianti
              </Text>
            </Box>
          </Group>

          <Tooltip label="Impostazioni" openDelay={800} withArrow>
            <Text
              component={RouterNavLink}
              to="/settings"
              size="xs"
              c={location.pathname === "/settings" ? "var(--color-text)" : "dimmed"}
              fw={600}
              style={{ textDecoration: "none", whiteSpace: "nowrap" }}
            >
              Impostazioni
            </Text>
          </Tooltip>
        </Group>
      </AppShell.Header>

      <AppShell.Navbar
        p="md"
        style={{
          borderRight: "1px solid var(--color-border)",
          background: "var(--color-surface)",
        }}
      >
        <AppShell.Section grow component={ScrollArea}>
          <NavLink
            label="Dashboard"
            leftSection={<IconLayoutDashboard size="1.1rem" stroke={1.5} />}
            component={RouterNavLink}
            to="/"
            active={location.pathname === "/"}
            styles={{
              root: { borderRadius: "var(--radius-md)" },
            }}
          />

          <Text
            size="xs"
            c="dimmed"
            mt="lg"
            mb={6}
            px="sm"
            fw={600}
            tt="uppercase"
            style={{ letterSpacing: "0.04em" }}
          >
            Moduli
          </Text>

          {modules.length === 0 ? (
            <Text size="sm" c="dimmed" px="sm" py="xs">
              Nessun modulo con interfaccia attivo.
            </Text>
          ) : (
            modules.map((m) => (
              <NavLink
                key={m.name}
                label={m.label}
                description={m.name}
                leftSection={
                  <ThemeIcon variant="light" size="sm" color="gray">
                    <IconPuzzle size="0.8rem" stroke={1.75} />
                  </ThemeIcon>
                }
                component={RouterNavLink}
                to={`/modules/${m.name}`}
                active={location.pathname === `/modules/${m.name}`}
                styles={{
                  root: { borderRadius: "var(--radius-md)" },
                }}
              />
            ))
          )}
        </AppShell.Section>

        <AppShell.Section>
          <NavLink
            label="Impostazioni"
            leftSection={<IconSettings size="1.1rem" stroke={1.5} />}
            component={RouterNavLink}
            to="/settings"
            active={location.pathname === "/settings"}
            styles={{
              root: { borderRadius: "var(--radius-md)" },
            }}
          />
          <Text size="xs" c="dimmed" ta="center" mt="sm" className="tabular">
            {config.brand.name} · v0.1.0
          </Text>
        </AppShell.Section>
      </AppShell.Navbar>

      <AppShell.Main>
        <Outlet />
      </AppShell.Main>
    </AppShell>
  );
}
