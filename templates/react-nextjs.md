# CLAUDE.md Template: React/Next.js

> Copy this file to your project root as `CLAUDE.md` and customize.

---

# Project Name

## Overview
[Brief description of what this project does]

## Tech Stack
- **Framework:** Next.js 15 (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **State:** [Zustand/Redux/Context]
- **Data Fetching:** [React Query/SWR]
- **Testing:** [Jest/Vitest] + React Testing Library

## Project Structure
```
src/
├── app/              # Next.js App Router pages
│   ├── layout.tsx    # Root layout
│   ├── page.tsx      # Home page
│   └── [feature]/    # Feature routes
├── components/       # Reusable components
│   ├── ui/           # Base UI components
│   └── features/     # Feature-specific components
├── lib/              # Utilities and helpers
├── hooks/            # Custom React hooks
├── types/            # TypeScript types
└── styles/           # Global styles
```

## Common Commands
```bash
npm run dev          # Start development server (localhost:3000)
npm run build        # Production build
npm run test         # Run tests
npm run lint         # Run ESLint
npm run typecheck    # TypeScript check
```

## Code Conventions

### Components
- Use functional components with TypeScript
- Props interface above component: `interface ComponentProps { ... }`
- One component per file, named same as file
- Use named exports: `export function Component() { ... }`

### File Naming
- Components: PascalCase (`Button.tsx`, `UserProfile.tsx`)
- Utilities: camelCase (`formatDate.ts`, `useAuth.ts`)
- Types: PascalCase with `.types.ts` suffix when separate

### Styling
- Use Tailwind utility classes
- Extract repeated patterns to `@apply` in global CSS
- Use `cn()` helper for conditional classes

### State Management
- Local state: `useState` for component state
- Shared state: [Zustand store / Redux slice / Context]
- Server state: [React Query / SWR]

## Testing
```bash
npm run test              # Run all tests
npm run test -- --watch   # Watch mode
npm run test:coverage     # With coverage
```

- Tests live next to files: `Component.test.tsx`
- Use `screen` queries from Testing Library
- Prefer `userEvent` over `fireEvent`

## Environment Variables
```
NEXT_PUBLIC_API_URL=     # Public API endpoint
DATABASE_URL=            # Database connection
```

Required for development: [list required vars]

## Key Files
- `src/app/layout.tsx:1` - Root layout with providers
- `src/lib/api.ts:1` - API client configuration
- `src/components/ui/` - Base component library

## Patterns to Follow
- See `src/components/ui/Button.tsx` for component pattern
- See `src/hooks/useAuth.ts` for custom hook pattern
- See `src/app/users/page.tsx` for data fetching pattern

## Known Issues
- [Any quirks or workarounds to be aware of]

## Don't
- Don't use `any` type - define proper types
- Don't put business logic in components - use hooks/lib
- Don't import from `src/` - use `@/` alias
