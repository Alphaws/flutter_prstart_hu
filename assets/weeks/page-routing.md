# Routing

A Flutter gyári navigációja nagyobb alkalmazásokban nehezen kezelhetővé válhat. A modern projektekben a deklaratív és URL-alapú navigációt részesítjük előnyben.

## 📦 Ajánlott Csomag: `go_router`
A `go_router` a Flutter hivatalos deklaratív navigációs csomagja, amely megkönnyíti a route-ok kezelését, a paraméterek átadását és a deep linkek támogatását.

### Példa konfiguráció:
```dart
final GoRouter _router = GoRouter(
  initialLocation: '/',
  routes: [
    GoRoute(
      path: '/',
      builder: (context, state) => const HomeScreen(),
    ),
    GoRoute(
      path: '/details/:id',
      builder: (context, state) {
        final id = state.pathParameters['id']!;
        return DetailsScreen(id: id);
      },
    ),
  ],
);
```

### Előnyök:
* **Deklaratív:** Könnyen átlátható útvonal struktúra.
* **Deep Linking:** Natív támogatás a külső linkekről való megnyitásra.
* **Auth Guard:** Könnyen beilleszthető bejelentkezést ellenőrző logika.