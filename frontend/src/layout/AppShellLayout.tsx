import {
  AppShell,
  Box,
  Burger,
  Group,
  NavLink,
  ScrollArea,
  Stack,
  Text,
  Drawer,
} from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";
import {
  IconLayoutDashboard,
  IconSettings,
} from "@tabler/icons-react";
import { NavLink as RouterNavLink, Outlet, useLocation } from "react-router-dom";
import { useAppConfig } from "../config";
import { moduleIcon } from "../moduleIcons";

export default function AppShellLayout() {
  const [opened, { toggle, close }] = useDisclosure();
  const location = useLocation();
  const config = useAppConfig();
  const modules = config.modules.filter((m) => m.has_frontend);

  const isActive = (path: string) => location.pathname === path;

  const today = new Date().toLocaleDateString("it-IT", {
    weekday: "long",
    day: "numeric",
    month: "long",
  });

  const navItems = (
    <Stack gap={2}>
      <NavLink
        label="Dashboard"
        leftSection={<IconLayoutDashboard size="1.15rem" stroke={1.5} />}
        component={RouterNavLink}
        to="/"
        active={isActive("/")}
        variant="light"
        onClick={close}
      />
      {modules.map((m) => {
        const Icon = moduleIcon(m.name);
        return (
          <NavLink
            key={m.name}
            label={m.label}
            leftSection={<Icon size="1.15rem" stroke={1.5} />}
            component={RouterNavLink}
            to={`/modules/${m.name}`}
            active={isActive(`/modules/${m.name}`)}
            variant="light"
            onClick={close}
          />
        );
      })}
      <Box mt="xl" mb={4} px="sm">
        <Text size="xs" c="dimmed" fw={600} tt="uppercase" className="mono-label">
          Sistema
        </Text>
      </Box>
      <NavLink
        label="Impostazioni"
        leftSection={<IconSettings size="1.15rem" stroke={1.5} />}
        component={RouterNavLink}
        to="/settings"
        active={isActive("/settings")}
        variant="light"
        onClick={close}
      />
    </Stack>
  );

  return (
    <AppShell
      header={{ height: 64 }}
      padding={0}
      style={{ background: "var(--color-paper)" }}
    >
      <AppShell.Header
        px={{ base: "md", sm: "xl" }}
        style={{
          borderBottom: "1px solid var(--color-border)",
          background: "color-mix(in oklch, var(--color-surface) 90%, transparent)",
          backdropFilter: "blur(14px)",
        }}
      >
        <Group h="100%" justify="space-between" wrap="nowrap">
          <Group gap="sm" wrap="nowrap">
            <Burger opened={opened} onClick={toggle} hiddenFrom="sm" size="sm" />
            <Box
              w={36}
              h={36}
              bg={config.brand.primaryColor}
              style={{
                borderRadius: 10,
                display: "grid",
                placeItems: "center",
                flexShrink: 0,
              }}
            >
              <Text c="white" fw={700} size="md">
                {config.brand.name.charAt(0).toUpperCase()}
              </Text>
            </Box>
            <Box style={{ lineHeight: 1.2 }} visibleFrom="sm">
              <Text fw={700} size="sm" style={{ letterSpacing: "-0.01em" }}>
                {config.brand.name}
              </Text>
              <Text size="xs" c="dimmed" className="mono-label">
                on-premise
              </Text>
            </Box>
          </Group>

          <Group gap="xl" wrap="nowrap">
            <Box ta="right" style={{ lineHeight: 1.2 }} visibleFrom="sm">
              <Text size="sm" fw={600} className="tabular">
                {today}
              </Text>
            </Box>
            <Box
              w={34}
              h={34}
              style={{
                borderRadius: "50%",
                background: "var(--color-surface-3)",
                display: "grid",
                placeItems: "center",
              }}
            >
              <Text size="xs" fw={600}>
                AD
              </Text>
            </Box>
          </Group>
        </Group>
      </AppShell.Header>

      <AppShell.Main>
        <Group
          align="stretch"
          wrap="nowrap"
          gap={0}
          style={{ minHeight: "calc(100vh - 64px)" }}
        >
          <Box
            visibleFrom="sm"
            w={260}
            p="md"
            style={{
              borderRight: "1px solid var(--color-border)",
              background: "var(--color-surface)",
              flexShrink: 0,
            }}
          >
            <ScrollArea type="hover" scrollbarSize={8} h="100%">
              {navItems}
              <Group justify="space-between" mt="xl" px={2}>
                <Text size="xs" c="dimmed" className="mono-label">
                  v0.1.0
                </Text>
              </Group>
            </ScrollArea>
          </Box>

          <Box style={{ flex: 1, minWidth: 0 }} p={{ base: "md", sm: "xl" }}>
            <Outlet />
          </Box>
        </Group>
      </AppShell.Main>

      <Drawer
        opened={opened}
        onClose={close}
        title={config.brand.name}
        size={300}
        padding="md"
        hiddenFrom="sm"
      >
        {navItems}
      </Drawer>
    </AppShell>
  );
}
