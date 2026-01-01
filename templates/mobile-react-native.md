# CLAUDE.md Template: React Native Mobile App

> Copy this file to your project root as `CLAUDE.md` and customize.

---

# Project Name

## Overview
[Description of the mobile app - what it does, target platforms]

## Tech Stack
- **Framework:** React Native 0.74+ / Expo SDK 51+
- **Language:** TypeScript
- **Navigation:** React Navigation 6
- **State:** [Zustand / Redux Toolkit / Jotai]
- **API:** [React Query / RTK Query]
- **Styling:** [StyleSheet / NativeWind / Tamagui]
- **Testing:** Jest + React Native Testing Library

## Project Structure

### Expo Managed
```
├── app/                    # Expo Router pages (if using)
│   ├── (tabs)/             # Tab navigator
│   ├── (auth)/             # Auth stack
│   └── _layout.tsx         # Root layout
├── src/
│   ├── components/
│   │   ├── ui/             # Base UI components
│   │   └── features/       # Feature components
│   ├── hooks/              # Custom hooks
│   ├── lib/                # Utilities
│   ├── services/           # API services
│   ├── stores/             # State management
│   └── types/              # TypeScript types
├── assets/                 # Images, fonts
├── app.json                # Expo config
├── eas.json                # EAS Build config
└── package.json
```

### Bare React Native
```
├── android/                # Android native code
├── ios/                    # iOS native code
├── src/
│   ├── navigation/         # React Navigation setup
│   ├── screens/            # Screen components
│   ├── components/
│   ├── hooks/
│   ├── services/
│   ├── stores/
│   └── types/
├── index.js                # Entry point
├── metro.config.js
└── package.json
```

## Common Commands
```bash
# Development
npx expo start              # Start Expo dev server
npx expo start --ios        # Start on iOS simulator
npx expo start --android    # Start on Android emulator
npx expo start --web        # Start web version

# Bare React Native
npx react-native start      # Start Metro bundler
npx react-native run-ios    # Run on iOS
npx react-native run-android # Run on Android

# Building
eas build --platform ios    # Build iOS (Expo)
eas build --platform android # Build Android (Expo)
npx react-native build-ios  # Build iOS (bare)

# Testing
npm test                    # Run tests
npm test -- --watch         # Watch mode
npm test -- --coverage      # With coverage

# Code Quality
npm run lint                # ESLint
npm run typecheck           # TypeScript check

# Dependencies
npx expo install [package]  # Install with correct version
npx pod-install             # Install iOS pods
```

## Code Conventions

### Component Structure
```tsx
import { StyleSheet, View, Text } from 'react-native';

interface UserCardProps {
  user: User;
  onPress?: () => void;
}

export function UserCard({ user, onPress }: UserCardProps) {
  return (
    <Pressable style={styles.container} onPress={onPress}>
      <Text style={styles.name}>{user.name}</Text>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 16,
    backgroundColor: '#fff',
    borderRadius: 8,
  },
  name: {
    fontSize: 16,
    fontWeight: '600',
  },
});
```

### File Naming
- Components: PascalCase (`UserCard.tsx`)
- Hooks: camelCase with `use` prefix (`useAuth.ts`)
- Screens: PascalCase with `Screen` suffix (`HomeScreen.tsx`)
- Utilities: camelCase (`formatDate.ts`)

### Navigation Typing
```tsx
// src/types/navigation.ts
import { NativeStackScreenProps } from '@react-navigation/native-stack';

export type RootStackParamList = {
  Home: undefined;
  Profile: { userId: string };
  Settings: undefined;
};

export type HomeScreenProps = NativeStackScreenProps<RootStackParamList, 'Home'>;
```

### Platform-Specific Code
```tsx
import { Platform } from 'react-native';

const styles = StyleSheet.create({
  shadow: Platform.select({
    ios: {
      shadowColor: '#000',
      shadowOffset: { width: 0, height: 2 },
      shadowOpacity: 0.1,
      shadowRadius: 4,
    },
    android: {
      elevation: 4,
    },
  }),
});

// Or use .ios.tsx / .android.tsx file extensions
```

### Safe Area Handling
```tsx
import { SafeAreaView } from 'react-native-safe-area-context';

export function Screen({ children }) {
  return (
    <SafeAreaView style={{ flex: 1 }} edges={['top']}>
      {children}
    </SafeAreaView>
  );
}
```

## Testing Patterns

### Component Testing
```tsx
import { render, fireEvent } from '@testing-library/react-native';
import { UserCard } from './UserCard';

describe('UserCard', () => {
  const mockUser = { id: '1', name: 'John Doe' };

  it('renders user name', () => {
    const { getByText } = render(<UserCard user={mockUser} />);
    expect(getByText('John Doe')).toBeTruthy();
  });

  it('calls onPress when tapped', () => {
    const onPress = jest.fn();
    const { getByText } = render(
      <UserCard user={mockUser} onPress={onPress} />
    );
    fireEvent.press(getByText('John Doe'));
    expect(onPress).toHaveBeenCalled();
  });
});
```

### Mocking Native Modules
```tsx
// jest.setup.js
jest.mock('react-native/Libraries/Animated/NativeAnimatedHelper');
jest.mock('@react-native-async-storage/async-storage', () =>
  require('@react-native-async-storage/async-storage/jest/async-storage-mock')
);
```

## Environment Variables
```bash
# .env
API_URL=https://api.example.com
SENTRY_DSN=https://xxx@sentry.io/xxx
```

Use `react-native-config` or Expo's `app.config.js`:
```js
// app.config.js
export default {
  extra: {
    apiUrl: process.env.API_URL,
  },
};
```

## Key Files
- `app/_layout.tsx` - Root layout (Expo Router)
- `src/navigation/RootNavigator.tsx` - Navigation setup
- `src/services/api.ts` - API client configuration
- `src/stores/authStore.ts` - Authentication state

## Performance Considerations
- Use `memo()` for expensive list items
- Use `useCallback` for callbacks passed to children
- Virtualize long lists with `FlatList`
- Avoid inline styles in render
- Use `Hermes` engine (default in RN 0.70+)

## Patterns to Follow
- See `src/components/ui/Button.tsx` for base component
- See `src/screens/HomeScreen.tsx` for screen pattern
- See `src/hooks/useApi.ts` for data fetching hook

## Don't
- Don't use inline functions in `renderItem` - causes re-renders
- Don't ignore TypeScript errors - fix the types
- Don't use `index` as key for dynamic lists
- Don't block JS thread with heavy computation
- Don't forget to handle keyboard on forms
- Don't hardcode colors - use theme
