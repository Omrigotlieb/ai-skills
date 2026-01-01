# CLAUDE.md Template: Monorepo

> Copy this file to your project root as `CLAUDE.md` and customize.

---

# Project Name (Monorepo)

## Overview
[Description of what this monorepo contains and its purpose]

## Tech Stack
- **Package Manager:** [pnpm / npm / yarn] with workspaces
- **Build System:** [Turborepo / Nx / Lerna]
- **Language:** TypeScript (strict mode)

## Monorepo Structure
```
├── apps/
│   ├── web/                  # Main web application (Next.js)
│   ├── api/                  # Backend API (Node.js/Express)
│   ├── admin/                # Admin dashboard
│   └── docs/                 # Documentation site
├── packages/
│   ├── ui/                   # Shared UI components
│   ├── config/               # Shared configs (ESLint, TypeScript, etc.)
│   ├── database/             # Database client and schemas
│   ├── utils/                # Shared utilities
│   └── types/                # Shared TypeScript types
├── tooling/
│   ├── eslint-config/        # ESLint configurations
│   ├── typescript-config/    # TypeScript configurations
│   └── tailwind-config/      # Tailwind configurations
├── turbo.json                # Turborepo configuration
├── pnpm-workspace.yaml       # Workspace definition
└── package.json              # Root package.json
```

## Apps

### apps/web
Main customer-facing web application.
- **Tech:** Next.js 15, React, Tailwind
- **Port:** 3000
- **Start:** `pnpm dev --filter web`

### apps/api
Backend REST API.
- **Tech:** Node.js, Express/Fastify, Prisma
- **Port:** 4000
- **Start:** `pnpm dev --filter api`

### apps/admin
Internal admin dashboard.
- **Tech:** Next.js, React Admin
- **Port:** 3001
- **Start:** `pnpm dev --filter admin`

## Packages

### packages/ui
Shared UI component library.
```typescript
import { Button, Card, Input } from '@repo/ui';
```

### packages/database
Database client, schemas, and migrations.
```typescript
import { prisma, User, Post } from '@repo/database';
```

### packages/utils
Shared utility functions.
```typescript
import { formatDate, slugify, cn } from '@repo/utils';
```

### packages/types
Shared TypeScript types and interfaces.
```typescript
import type { User, ApiResponse } from '@repo/types';
```

## Common Commands
```bash
# Development
pnpm dev                     # Start all apps
pnpm dev --filter web        # Start specific app
pnpm dev --filter web...     # App + its dependencies

# Building
pnpm build                   # Build all packages
pnpm build --filter web      # Build specific package

# Testing
pnpm test                    # Run all tests
pnpm test --filter api       # Test specific package

# Linting
pnpm lint                    # Lint all packages
pnpm lint --filter web       # Lint specific package

# Type Checking
pnpm typecheck               # Check all packages

# Database (from packages/database)
pnpm --filter database db:push
pnpm --filter database db:migrate

# Add dependency
pnpm add lodash --filter web          # Add to specific package
pnpm add -D typescript -w             # Add to root
pnpm add @repo/ui --filter web        # Add internal package
```

## Dependency Rules

### Internal Packages
- Apps can depend on any package
- `packages/ui` can depend on `packages/utils` and `packages/types`
- `packages/database` can depend on `packages/types`
- `packages/utils` and `packages/types` should have no internal dependencies

### External Dependencies
- Shared dependencies go in root `package.json`
- App-specific dependencies go in app's `package.json`
- Keep versions in sync across packages

## Turborepo Pipeline
```json
// turbo.json
{
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    },
    "test": {
      "dependsOn": ["build"]
    },
    "lint": {}
  }
}
```

## Environment Variables
Each app has its own `.env`:
- `apps/web/.env.local`
- `apps/api/.env`

Shared env vars go in root `.env` (loaded by Turborepo).

## Key Patterns

### Creating a New App
1. Copy existing app as template
2. Update `package.json` name to `@repo/new-app`
3. Add to `pnpm-workspace.yaml` if not auto-detected
4. Configure in `turbo.json` if special behavior needed

### Creating a New Package
1. Create folder in `packages/`
2. Add `package.json` with name `@repo/package-name`
3. Add `tsconfig.json` extending shared config
4. Export from `index.ts`

### Sharing Code Between Apps
1. Create package in `packages/`
2. Export functionality from package
3. Import in apps: `import { thing } from '@repo/package';`
4. Turborepo handles build order

## Don't
- Don't duplicate code across apps - create a package
- Don't install same dependency in multiple packages - hoist to root
- Don't skip the `@repo/` prefix for internal packages
- Don't import between apps directly - use packages
- Don't put app-specific code in shared packages
