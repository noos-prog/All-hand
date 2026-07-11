import {
  LineChart, Plug, Building2, Hammer, Code2, MessageSquare,
  Calculator, Database, Palette, GraduationCap, Edit3, HeartPulse,
  Network, Search, CheckCheck, Sprout, Crown, Syringe, FlaskConical,
  ShieldCheck, Bot,
} from 'lucide-react';
import type { LucideIcon } from 'lucide-react';

export const ICON_MAP: Record<string, LucideIcon> = {
  'chart-line': LineChart,
  plug: Plug,
  building: Building2,
  hammer: Hammer,
  code: Code2,
  comments: MessageSquare,
  calculator: Calculator,
  database: Database,
  palette: Palette,
  'graduation-cap': GraduationCap,
  edit: Edit3,
  'monitor-heart': HeartPulse,
  'network-wired': Network,
  search: Search,
  'check-double': CheckCheck,
  seedling: Sprout,
  chess: Crown,
  syringe: Syringe,
  vial: FlaskConical,
  'shield-check': ShieldCheck,
  robot: Bot,
};

export function getIcon(name: string): LucideIcon {
  return ICON_MAP[name] || Bot;
}

export const SPECIALIZATION_LABELS: Record<string, string> = {
  analyst: 'محلل',
  api_integrator: 'مدمج واجهات',
  architect: 'مهندس معماري',
  builder: 'باني',
  code_generator: 'مولد كود',
  communicator: 'وسيط تواصل',
  data_processor: 'معالج بيانات',
  db_manager: 'مدير قاعدة',
  designer: 'مصمم',
  educator: 'معلم',
  modifier: 'معدل',
  monitor: 'مراقب',
  network_client: 'عميل شبكة',
  researcher: 'باحث',
  reviewer: 'مراجع',
  self_developer: 'مطور ذاتي',
  strategist: 'استراتيجي',
  surgeon: 'جراح',
  test_runner: 'منفذ اختبارات',
  validator: 'مدقق',
  external: 'وكيل خارجي',
};
