import {
  Badge,
  Button,
  Group,
  Paper,
  SimpleGrid,
  Stack,
  Text,
  Title,
} from "@mantine/core";
import { IconCreditCard, IconPlus } from "@tabler/icons-react";
import { useEffect, useState } from "react";
import { authHeaders } from "../auth";

interface Plan {
  id: number;
  name: string;
  billing_type: string;
  price: string;
  duration_days: number;
  included_entries: number | null;
  is_active: boolean;
}

interface Subscription {
  id: number;
  member_id: number;
  plan: Plan;
  starts_on: string;
  ends_on: string;
  status: string;
}

export default function SubscriptionsPage() {
  const [plans, setPlans] = useState<Plan[]>([]);
  const [subscriptions, setSubscriptions] = useState<Subscription[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([
      fetch("/api/abbonamenti/plans", { headers: authHeaders() }),
      fetch("/api/abbonamenti/subscriptions", { headers: authHeaders() }),
    ])
      .then(async ([plansRes, subscriptionsRes]) => {
        if (!plansRes.ok || !subscriptionsRes.ok) throw new Error("Errore di caricamento");
        setPlans(await plansRes.json());
        setSubscriptions(await subscriptionsRes.json());
      })
      .catch((e: unknown) => setError(e instanceof Error ? e.message : "Errore di caricamento"));
  }, []);

  return (
    <Stack gap="xl" maw={1120}>
      <Group justify="space-between" align="flex-end">
        <div>
          <Text size="sm" c="dimmed" className="mono-label" tt="uppercase">Fase 2</Text>
          <Title order={1} size={30}>Abbonamenti</Title>
          <Text c="dimmed" size="sm" mt={4}>Piani, iscrizioni e pagamenti registrati in reception.</Text>
        </div>
        <Button leftSection={<IconPlus size="1rem" />} disabled>Nuovo abbonamento</Button>
      </Group>
      {error && <Text c="red">{error}</Text>}
      <SimpleGrid cols={{ base: 1, sm: 2, lg: 3 }} spacing="md">
        {plans.map((plan) => (
          <Paper key={plan.id} p="lg" radius="lg" style={{ border: "1px solid var(--color-border)" }}>
            <Group justify="space-between" mb="md">
              <IconCreditCard size="1.4rem" stroke={1.5} />
              <Badge color={plan.is_active ? "teal" : "gray"} variant="light">
                {plan.is_active ? "attivo" : "archiviato"}
              </Badge>
            </Group>
            <Text fw={650}>{plan.name}</Text>
            <Text size="xl" fw={700} mt="xs">€ {Number(plan.price).toFixed(2)}</Text>
            <Text size="sm" c="dimmed">{plan.duration_days} giorni · {plan.billing_type}</Text>
          </Paper>
        ))}
      </SimpleGrid>
      <Paper p="lg" radius="lg" style={{ border: "1px solid var(--color-border)" }}>
        <Title order={4} mb="md">Abbonamenti attivi</Title>
        {subscriptions.length === 0 ? (
          <Text c="dimmed" size="sm">Nessun abbonamento registrato.</Text>
        ) : subscriptions.map((subscription) => (
          <Group key={subscription.id} justify="space-between" py="xs">
            <Text size="sm">Socio #{subscription.member_id} · {subscription.plan.name}</Text>
            <Badge variant="light">{subscription.status}</Badge>
          </Group>
        ))}
      </Paper>
    </Stack>
  );
}
