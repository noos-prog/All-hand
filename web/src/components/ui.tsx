import { Loader2 } from 'lucide-react';
import type { LucideIcon } from 'lucide-react';

export function Spinner({ size = 20, className = '' }: { size?: number; className?: string }) {
  return (
    <Loader2
      size={size}
      className={`animate-spin text-accent ${className}`}
      aria-label="loading"
    />
  );
}

export function LoadingState({ label = 'جاري التحميل...' }: { label?: string }) {
  return (
    <div className="flex items-center justify-center gap-3 py-16 text-primary-secondary animate-fade-in">
      <Spinner />
      <span>{label}</span>
    </div>
  );
}

export function EmptyState({
  icon: Icon,
  label,
  sublabel,
}: {
  icon: LucideIcon;
  label: string;
  sublabel?: string;
}) {
  return (
    <div className="flex flex-col items-center justify-center py-20 text-center animate-fade-in">
      <div className="w-16 h-16 rounded-2xl bg-elevated/50 border border-border flex items-center justify-center mb-4">
        <Icon size={28} className="text-primary-muted" />
      </div>
      <div className="text-lg font-semibold text-primary-secondary">{label}</div>
      {sublabel && <div className="text-sm text-primary-muted mt-1">{sublabel}</div>}
    </div>
  );
}
