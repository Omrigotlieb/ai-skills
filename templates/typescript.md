# CLAUDE.md Template: TypeScript Project

A comprehensive template for TypeScript projects.

```markdown
# Project: [Name]

## Tech Stack
- **Language:** TypeScript 5.x
- **Runtime:** Node.js 20+ / Bun / Deno
- **Package Manager:** pnpm / npm / yarn

## Project Structure
```
src/
├── index.ts          # Entry point
├── types/            # Type definitions
├── utils/            # Utility functions
├── services/         # Business logic
└── lib/              # Shared libraries
```

## TypeScript Configuration
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  }
}
```

## Code Standards

### Types
- **Prefer interfaces** for object shapes
- **Use type** for unions, intersections, primitives
- **Avoid any** - use unknown if type is truly unknown
- **Export types** from dedicated files

### Patterns
```typescript
// Use branded types for type safety
type UserId = string & { readonly __brand: 'UserId' };

// Use discriminated unions
type Result<T> =
  | { success: true; data: T }
  | { success: false; error: Error };

// Use const assertions
const ROUTES = {
  home: '/',
  about: '/about',
} as const;
```

### Null Handling
- Use optional chaining: `user?.profile?.name`
- Use nullish coalescing: `value ?? defaultValue`
- Prefer explicit checks over type assertions

## Commands
```bash
pnpm dev        # Development with hot reload
pnpm build      # Production build
pnpm typecheck  # Type checking only
pnpm lint       # ESLint
pnpm test       # Run tests
```

## Testing
- **Framework:** Vitest / Jest
- **Coverage target:** 80%+
- **Type testing:** tsd for type assertions

## Guidelines
- Run `pnpm typecheck` before committing
- Keep functions pure where possible
- Document complex generics
- Use zod for runtime validation
```

---

## Key Principles

1. **Strict Mode Always** - Enable all strict checks
2. **Types as Documentation** - Well-named types are self-documenting
3. **Avoid Type Assertions** - Let TypeScript infer when possible
4. **Validate at Boundaries** - Use zod/yup for external data
