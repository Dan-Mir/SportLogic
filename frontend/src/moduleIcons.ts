import {
  IconCalendarEvent,
  IconPuzzle,
  IconUsers,
  IconBallFootball,
  IconShieldLock,
} from "@tabler/icons-react";

export const MODULE_ICONS: Record<string, typeof IconPuzzle> = {
  core: IconShieldLock,
  anagrafica: IconUsers,
  corsi: IconCalendarEvent,
  "booking.fields": IconBallFootball,
};

export function moduleIcon(name: string): typeof IconPuzzle {
  return MODULE_ICONS[name] ?? IconPuzzle;
}
