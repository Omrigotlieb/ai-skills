# CLAUDE.md Template: Vue.js Project

A comprehensive template for Vue 3 applications.

```markdown
# Project: [Name]

## Tech Stack
- **Framework:** Vue 3.4+ (Composition API)
- **Build:** Vite 5
- **State:** Pinia
- **Router:** Vue Router 4
- **Styling:** Tailwind CSS / UnoCSS
- **Testing:** Vitest + Vue Test Utils

## Project Structure
```
src/
├── components/
│   ├── ui/              # Reusable UI components
│   └── features/        # Feature-specific components
├── composables/         # Composition functions
├── stores/              # Pinia stores
├── views/               # Route-level components
├── router/              # Vue Router config
├── types/               # TypeScript types
├── utils/               # Utility functions
└── App.vue
```

## Vue 3 Patterns

### Composition API (Required)
```vue
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'

const props = defineProps<{
  title: string
}>()

const emit = defineEmits<{
  (e: 'submit', value: string): void
}>()

const count = ref(0)
const doubled = computed(() => count.value * 2)
</script>
```

### Composables
```typescript
// composables/useAuth.ts
export function useAuth() {
  const user = ref<User | null>(null)
  const isAuthenticated = computed(() => !!user.value)

  async function login(credentials: Credentials) {
    // ...
  }

  return { user, isAuthenticated, login }
}
```

### Pinia Stores
```typescript
// stores/user.ts
export const useUserStore = defineStore('user', () => {
  const user = ref<User | null>(null)

  async function fetchUser() {
    user.value = await api.getUser()
  }

  return { user, fetchUser }
})
```

## Commands
```bash
pnpm dev        # Development server
pnpm build      # Production build
pnpm preview    # Preview production build
pnpm test       # Run Vitest
pnpm lint       # ESLint
```

## Code Standards
- **Script setup syntax** only
- **TypeScript** for all files
- **Composables** for reusable logic
- **Props/emits** must be typed

## Component Guidelines
- Single responsibility
- Props down, events up
- Use v-model for two-way binding
- Prefer slots over props for content

## Testing
```typescript
import { mount } from '@vue/test-utils'
import MyComponent from './MyComponent.vue'

test('renders correctly', () => {
  const wrapper = mount(MyComponent, {
    props: { title: 'Test' }
  })
  expect(wrapper.text()).toContain('Test')
})
```
```

---

## Vue vs Options API

Always use Composition API with `<script setup>`:

```vue
<!-- Good: Composition API -->
<script setup lang="ts">
const count = ref(0)
</script>

<!-- Avoid: Options API -->
<script>
export default {
  data() {
    return { count: 0 }
  }
}
</script>
```
