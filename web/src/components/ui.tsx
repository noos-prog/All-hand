import { Loader2 } from 'lucide-react';
import type { LucideIcon } from 'lucide-react';

export function Spinner({ size = 20, className = '' }: { size?: number; className?: string }) {
  return (
    <Loader2
      size={size}
      className={`animate-spin text-[#00d4ff] ${className}`}
      aria-label="loading"
    />
  );
}

export function LoadingState({ label = 'جاري التحميل...' }: { label?: string }) {
  return (
    <div className="flex items-center justify-center gap-3 py-16 text-[#9ba8c4] animate-fade-in">
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
      <div className="w-16 h-16 rounded-2xl bg-[#1a2236]/50 border border-[#2a3550] flex items-center justify-center mb-4">
        <Icon size={28} className="text-[#5c6b8a]" />
      </div>
      <div className="text-lg font-semibold text-[#9ba8c4]">{label}</div>
      {sublabel && <div className="text-sm text-[#5c6b8a] mt-1">{sublabel}</div>}
    </div>
  );
}
