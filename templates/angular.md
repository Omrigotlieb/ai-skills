# CLAUDE.md Template: Angular Project

A comprehensive template for Angular applications.

```markdown
# Project: [Name]

## Tech Stack
- **Framework:** Angular 17+ (Standalone)
- **State:** NgRx / Angular Signals
- **UI:** Angular Material / PrimeNG
- **Testing:** Jest + Testing Library
- **Styling:** SCSS / Tailwind

## Project Structure
```
src/app/
├── core/                # Singletons, guards, interceptors
│   ├── guards/
│   ├── interceptors/
│   └── services/
├── shared/              # Shared components, pipes, directives
│   ├── components/
│   ├── pipes/
│   └── directives/
├── features/            # Feature modules
│   ├── users/
│   └── dashboard/
├── app.component.ts
├── app.config.ts
└── app.routes.ts
```

## Angular 17+ Patterns

### Standalone Components (Required)
```typescript
@Component({
  selector: 'app-user-card',
  standalone: true,
  imports: [CommonModule, MatCardModule],
  template: `
    <mat-card>
      <mat-card-title>{{ user().name }}</mat-card-title>
    </mat-card>
  `
})
export class UserCardComponent {
  user = input.required<User>();
  selected = output<User>();
}
```

### Signals (Preferred for State)
```typescript
@Component({...})
export class DashboardComponent {
  // Signal state
  count = signal(0);
  doubled = computed(() => this.count() * 2);

  // Effect for side effects
  constructor() {
    effect(() => {
      console.log('Count changed:', this.count());
    });
  }

  increment() {
    this.count.update(c => c + 1);
  }
}
```

### Services
```typescript
@Injectable({ providedIn: 'root' })
export class UserService {
  private http = inject(HttpClient);

  getUsers(): Observable<User[]> {
    return this.http.get<User[]>('/api/users');
  }
}
```

## Commands
```bash
ng serve           # Development server
ng build           # Production build
ng test            # Run tests
ng generate        # Generate components, services, etc.
ng lint            # ESLint
```

## Code Standards
- **Standalone components** only (no NgModules)
- **Signals** for component state
- **inject()** function over constructor injection
- **Typed forms** with ReactiveFormsModule

## Angular-Specific Rules
- Use OnPush change detection
- Lazy load feature routes
- Prefer observables for async data
- Use the async pipe in templates

## Testing
```typescript
import { render, screen } from '@testing-library/angular'
import { UserCardComponent } from './user-card.component'

test('displays user name', async () => {
  await render(UserCardComponent, {
    inputs: { user: { name: 'John' } }
  })
  expect(screen.getByText('John')).toBeInTheDocument()
})
```

## HTTP Interceptors
```typescript
export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const token = inject(AuthService).token();
  if (token) {
    req = req.clone({
      setHeaders: { Authorization: `Bearer ${token}` }
    });
  }
  return next(req);
};
```
```

---

## Migration Notes

For projects migrating from NgModules:
1. Convert to standalone components
2. Replace RxJS state with signals where appropriate
3. Use functional interceptors
4. Update to new control flow syntax (@if, @for)
