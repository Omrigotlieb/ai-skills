# CLAUDE.md Template: Full-Stack Application

> Copy this file to your project root as `CLAUDE.md` and customize.

---

# Project Name

## Overview
[Full-stack application description - what it does, who it's for]

## Tech Stack

### Frontend
- **Framework:** Next.js 15 (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **State:** [Zustand/Redux Toolkit]
- **Data Fetching:** React Query

### Backend
- **Runtime:** Node.js
- **Framework:** [Next.js API Routes / Express / Fastify]
- **Database:** [PostgreSQL / MongoDB]
- **ORM:** [Prisma / Drizzle]
- **Auth:** [NextAuth.js / Clerk / Auth0]

### Infrastructure
- **Hosting:** [Vercel / AWS / Railway]
- **Database:** [Supabase / PlanetScale / Neon]
- **File Storage:** [S3 / Cloudflare R2]
- **Cache:** [Redis / Upstash]

## Project Structure
```
├── src/
│   ├── app/                  # Next.js App Router
│   │   ├── (auth)/           # Auth routes group
│   │   ├── (dashboard)/      # Dashboard routes group
│   │   ├── api/              # API routes
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── components/
│   │   ├── ui/               # Base UI components
│   │   ├── features/         # Feature components
│   │   └── layouts/          # Layout components
│   ├── lib/
│   │   ├── api/              # API client
│   │   ├── auth/             # Auth utilities
│   │   ├── db/               # Database client
│   │   └── utils/            # Helpers
│   ├── hooks/                # Custom React hooks
│   ├── types/                # TypeScript types
│   └── styles/               # Global styles
├── prisma/
│   ├── schema.prisma         # Database schema
│   └── migrations/           # Migration files
├── public/                   # Static assets
└── tests/
    ├── e2e/                  # Playwright tests
    └── unit/                 # Unit tests
```

## Common Commands
```bash
# Development
npm run dev              # Start dev server (localhost:3000)

# Database
npm run db:push          # Push schema changes
npm run db:migrate       # Run migrations
npm run db:studio        # Open Prisma Studio
npm run db:seed          # Seed database

# Testing
npm run test             # Run unit tests
npm run test:e2e         # Run E2E tests

# Production
npm run build            # Production build
npm run start            # Start production server

# Code Quality
npm run lint             # ESLint
npm run typecheck        # TypeScript check
npm run format           # Prettier
```

## Architecture Patterns

### API Routes
- RESTful endpoints in `app/api/`
- Use route handlers: `route.ts` with GET/POST/etc exports
- Validate with Zod schemas
- Return consistent JSON structure

### Database Access
- Use Prisma for all database operations
- Repository pattern: `lib/db/repositories/`
- Never expose Prisma client directly to API routes

### Authentication
- Auth middleware in `lib/auth/middleware.ts`
- Protected routes use `auth()` from NextAuth
- API routes check session with `getServerSession()`

### State Management
- Server state: React Query with hooks in `hooks/queries/`
- Client state: Zustand stores in `lib/stores/`
- Form state: React Hook Form

## Environment Variables
```bash
# Database
DATABASE_URL=

# Auth
NEXTAUTH_SECRET=
NEXTAUTH_URL=

# External Services
[SERVICE]_API_KEY=
```

**Required for development:** DATABASE_URL, NEXTAUTH_SECRET

## Key Files
- `src/app/layout.tsx` - Root layout with providers
- `src/lib/db/index.ts` - Prisma client singleton
- `src/lib/auth/options.ts` - NextAuth configuration
- `prisma/schema.prisma` - Database schema

## Patterns to Follow
- See `src/app/api/users/route.ts` for API route pattern
- See `src/components/features/UserForm.tsx` for form pattern
- See `src/hooks/queries/useUsers.ts` for React Query pattern

## Testing Strategy
- Unit tests for utilities and hooks
- Integration tests for API routes
- E2E tests for critical user flows
- Run `npm run test` before committing

## Don't
- Don't access Prisma client outside of repositories
- Don't put business logic in API routes - use services
- Don't store secrets in code - use environment variables
- Don't skip TypeScript types - no `any`
