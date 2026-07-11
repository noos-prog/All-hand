/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        deep: '#060912',
        base: '#0a0e1a',
        card: '#111827',
        elevated: '#1a2236',
        hover: '#232d44',
        border: {
          DEFAULT: '#2a3550',
          light: '#364260',
        },
        primary: {
          DEFAULT: '#e8ecf4',
          secondary: '#9ba8c4',
          muted: '#5c6b8a',
        },
        accent: {
          DEFAULT: '#00d4ff',
          dim: '#0099cc',
          glow: 'rgba(0, 212, 255, 0.15)',
        },
        success: {
          DEFAULT: '#00e676',
          dim: '#00c853',
        },
        warning: '#ffab40',
        error: {
          DEFAULT: '#ff5252',
          dim: '#d32f2f',
        },
      },
      fontFamily: {
        sans: ['Cairo', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      animation: {
        'fade-in': 'fadeIn 0.3s ease-out',
        'slide-up': 'slideUp 0.4s cubic-bezier(0.16, 1, 0.3, 1)',
        'slide-down': 'slideDown 0.3s ease-out',
        'pulse-glow': 'pulseGlow 2s ease-in-out infinite',
        'spin-slow': 'spin 2s linear infinite',
        'shimmer': 'shimmer 2s linear infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { opacity: '0', transform: 'translateY(12px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        slideDown: {
          '0%': { opacity: '0', transform: 'translateY(-12px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        pulseGlow: {
          '0%, 100%': { boxShadow: '0 0 20px rgba(0, 212, 255, 0.1)' },
          '50%': { boxShadow: '0 0 30px rgba(0, 212, 255, 0.25)' },
        },
        shimmer: {
          '0%': { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' },
        },
      },
    },
  },
  plugins: [],
};
