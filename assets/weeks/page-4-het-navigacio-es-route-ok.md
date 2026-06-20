# 4. hét — Navigáció és route-ok

## Cél
Ezen a héten megtanuljuk, hogyan kezeljük az alkalmazáson belüli képernyőváltásokat (navigáció). Megismerjük a beépített Stack-alapú `Navigator` működését, az adatátadást az oldalak között (mindkét irányba), a nevesített útvonalakat (Named Routes), valamint bepillantást nyerünk a modern deklaratív routing világába a `go_router` csomagon keresztül. Megépítjük az alsó navigációs sávval és lapfülekkel ellátott alkalmazásmintákat is.

---

## Elmélet

### 4.1 Alapvető Navigáció: A Navigator Stack Koncepció
A Flutter a navigációt egy verem (Stack) adatszerkezetként kezeli, amelyet a `Navigator` osztály menedzsel. 
A képernyőket (amiket a Flutterben `Route` objektumokba csomagolunk) egymás tetejére helyezzük el:
*   **`Navigator.push()`**: Új oldalt helyez a verem tetejére. Ez az új oldal le fedi az előzőt. A képernyőn az új tartalom jelenik meg, és a Flutter (ha `AppBar`-t használunk) automatikusan kitesz egy "vissza" nyilat.
*   **`Navigator.pop()`**: Eltávolítja a verem legfelső elemét. Az alatta lévő oldal újra láthatóvá válik. Ez felel meg a felhasználó által kezdeményezett "vissza" gombnyomásnak.

```mermaid
graph TD
    subgraph Képernyő Verem (Navigator Stack)
        S3[DetailsPage - Legfelül]
        S2[CategoryPage]
        S1[HomePage - Gyökér]
    end
    
    Action1[Navigator.push] -->|Új oldal hozzáadása| S3
    S3 -->|Navigator.pop| Action2[Visszalépés az előzőre]
```

A navigáció során a widgeteket leggyakrabban a `MaterialPageRoute` segítségével jelenítjük meg, ami biztosítja a platformspecifikus animációkat (Androidon alulról felfelé csúszás és halványodás, iOS-en jobbról balra csúszás).

```dart
Navigator.push(
  context,
  MaterialPageRoute(builder: (context) => const DetailsPage()),
);
```

### 4.2 Visszatérés Adattal (Aszinkron Navigáció)
Gyakran előfordul, hogy egy megnyitott képernyőtől valamilyen döntést vagy adatot várunk vissza (például egy beállító oldaltól vagy egy listás választótól).
Mivel a navigáció időbe telik, és a visszatérés tetszőlegesen később történik, ezt a Dart `Future` koncepciójával kezeljük:

1.  **Várakozás az adatra (`await`):**
    ```dart
    final selectedColor = await Navigator.push<Color>(
      context,
      MaterialPageRoute(builder: (context) => const ColorPickerPage()),
    );
    ```
2.  **Adat visszaküldése (`pop`):**
    A megnyitott oldalon a bezáráskor átadjuk az adatot a `pop` metódusnak:
    ```dart
    Navigator.pop(context, Colors.red); // Visszaküldjük a piros színt
    ```

### 4.3 Named Routes (Nevesített Útvonalak)
Nagyobb projekteknél nehézkessé válhat, ha mindenhonnan közvetlenül példányosítjuk az oldalakat. A Named Routes lehetővé teszi, hogy az útvonalakat (string alapú címkék segítségével) egyetlen központi helyen, a `MaterialApp`-ban regisztráljuk.

```dart
MaterialApp(
  initialRoute: '/',
  routes: {
    '/': (context) => const HomePage(),
    '/details': (context) => const DetailsPage(),
    '/settings': (context) => const SettingsPage(),
  },
);
```
Navigálás:
```dart
Navigator.pushNamed(context, '/details');
```

**Korlátozás:** Named routes esetén az argumentumok átadása kissé nehézkesebb (a `ModalRoute.of(context)?.settings.arguments` segítségével érhető el a céloldalon).

### 4.4 Haladó Routing: Bevezetés a go_router csomagba
A beépített Navigator 1.0 nehezen kezeli az összetettebb igényeket, mint a webre történő fejlesztés (URL sáv szinkronizációja), a mélylinkelés (deep linking) vagy az oldalak közötti feltételes átirányítások (Auth Guard). Erre a Google hivatalos deklaratív megoldása a `go_router` csomag.

Főbb go_router fogalmak:
*   **Declarative routing:** Az útvonalakat egy fastruktúrában definiáljuk.
*   **Path és Query Parameters:** Támogatja a `/product/:id` formátumú útvonal-paramétereket és a `/search?query=flutter` lekérdezési paramétereket.
*   **ShellRoute:** Lehetővé teszi, hogy egy állandó keretet (pl. alsó navigációs sávot) hozzunk létre, aminek a belsejében cserélődnek a képernyők.
*   **Redirect (Auth Guard):** Globális vagy lokális szinten ellenőrizhető a felhasználó állapota (pl. ha nincs bejelentkezve, irányítsa át a `/login` oldalra).

### 4.5 Alsó Navigáció és Lapfülek
Az alkalmazások fő navigációját általában kétféleképpen oldjuk meg:
1.  **Alsó Navigáció (`BottomNavigationBar` / `NavigationBar`):** A képernyő alján elhelyezkedő fix menüpontok (általában 3–5 darab). Material 3-ban a `NavigationBar` widget az új szabvány, amely modern és szebb animációkat használ.
2.  **Lapfülek (`TabBar` + `TabBarView`):** A képernyő tetején (vagy a Scaffold appbar-ban) elhelyezkedő fülek, amik között elhúzással (swipe) is lehet váltani. Működésükhöz egy `TabController` vagy egy `DefaultTabController` wrapper szükséges.

---

## Kódpéldák

### Teljes Futtatható Navigációs Mintakód
Ez a kód bemutatja az alsó navigációt 2 tabbal, a listából részletező képernyőre navigálást konstruktoros adatátadással, és egy adatbekérő oldalról történő aszinkron visszatérést.

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Navigációs Példa',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: const MainScreen(),
    );
  }
}

// Főképernyő alsó navigációval
class MainScreen extends StatefulWidget {
  const MainScreen({super.key});

  @override
  State<MainScreen> createState() => _MainScreenState();
}

class _MainScreenState extends State<MainScreen> {
  int _selectedIndex = 0;
  String _customText = "Nincs egyedi üzenet";

  final List<Widget> _pages = [];

  @override
  void initState() {
    super.initState();
    // Oldalak inicializálása
    _pages.addAll([
      const HomeScreen(),
      const SettingsTab(),
    ]);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: _selectedIndex == 0
          ? HomeScreen(
              customText: _customText,
              onUpdateText: (newText) {
                setState(() {
                  _customText = newText;
                });
              },
            )
          : _pages[_selectedIndex],
      bottomNavigationBar: NavigationBar(
        selectedIndex: _selectedIndex,
        onDestinationSelected: (index) {
          setState(() {
            _selectedIndex = index;
          });
        },
        destinations: const [
          NavigationDestination(icon: Icon(Icons.home), label: 'Főoldal'),
          NavigationDestination(icon: Icon(Icons.settings), label: 'Beállítások'),
        ],
      ),
    );
  }
}

// 1. Tab: Főoldal
class HomeScreen extends StatelessWidget {
  final String customText;
  final ValueChanged<String>? onUpdateText;

  const HomeScreen({
    super.key,
    required this.customText,
    this.onUpdateText,
  });

  @override
  Widget build(BuildContext context) {
    final List<String> products = ['Laptop', 'Okostelefon', 'Fejhallgató'];

    return Scaffold(
      appBar: AppBar(title: const Text('Termékek')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Üzenet sáv
            Card(
              color: Colors.deepPurple.shade50,
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Expanded(child: Text('Üzenet: $customText')),
                    TextButton(
                      onPressed: () async {
                        // Navigáció visszatérési adatra várva
                        final result = await Navigator.push<String>(
                          context,
                          MaterialPageRoute(builder: (_) => const MessageInputScreen()),
                        );
                        if (result != null && onUpdateText != null) {
                          onUpdateText!(result);
                        }
                      },
                      child: const Text('Módosít'),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 16),
            const Text('Terméklista (Kattints a részletekért):', style: TextStyle(fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            // Terméklista
            Expanded(
              child: ListView.builder(
                itemCount: products.length,
                itemBuilder: (context, index) {
                  return ListTile(
                    title: Text(products[index]),
                    trailing: const Icon(Icons.arrow_forward_ios, size: 16),
                    onTap: () {
                      // Navigáció adatátadással a részletező oldalra
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (context) => ProductDetailsScreen(productName: products[index]),
                        ),
                      );
                    },
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}

// Részletező Képernyő
class ProductDetailsScreen extends StatelessWidget {
  final String productName;

  const ProductDetailsScreen({super.key, required this.productName});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(productName)),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text('Ez a(z) $productName részletező oldala.', style: const TextStyle(fontSize: 18)),
            const SizedBox(height: 24),
            ElevatedButton(
              onPressed: () => Navigator.pop(context),
              child: const Text('Vissza a listához'),
            ),
          ],
        ),
      ),
    );
  }
}

// Szövegbeviteli képernyő (adat visszaküldése pop-pal)
class MessageInputScreen extends StatefulWidget {
  const MessageInputScreen({super.key});

  @override
  State<MessageInputScreen> createState() => _MessageInputScreenState();
}

class _MessageInputScreenState extends State<MessageInputScreen> {
  final _controller = TextEditingController();

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Új üzenet beírása')),
      body: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            TextField(
              controller: _controller,
              decoration: const InputDecoration(
                labelText: 'Írj be valamit...',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: () {
                // Adat visszaküldése
                Navigator.pop(context, _controller.text);
              },
              child: const Text('Mentés és Visszalépés'),
            ),
          ],
        ),
      ),
    );
  }
}

// 2. Tab: Beállítások (statikus lap)
class SettingsTab extends StatelessWidget {
  const SettingsTab({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Beállítások')),
      body: const Center(child: Text('Beállítások menüpont helye.')),
    );
  }
}
```

---

## Gyakorlófeladatok & Megoldások

### 1. Feladat: Egyszerű Képernyőváltás
Hozz létre egy `FirstScreen` és egy `SecondScreen` osztályt. A `FirstScreen` közepén legyen egy gomb, amely átirányít a `SecondScreen`-re. A `SecondScreen`-en legyen egy gomb, amivel vissza lehet lépni.

#### Megoldás:
```dart
import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(home: FirstScreen()));

class FirstScreen extends StatelessWidget {
  const FirstScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Első Képernyő')),
      body: Center(
        child: ElevatedButton(
          onPressed: () {
            Navigator.push(
              context,
              MaterialPageRoute(builder: (context) => const SecondScreen()),
            );
          },
          child: const Text('Tovább a második képernyőre'),
        ),
      ),
    );
  }
}

class SecondScreen extends StatelessWidget {
  const SecondScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Második Képernyő')),
      body: Center(
        child: ElevatedButton(
          onPressed: () {
            Navigator.pop(context);
          },
          child: const Text('Vissza az elsőre'),
        ),
      ),
    );
  }
}
```

### 2. Feladat: Adatátadás és Konstruktor
Módosítsd az első feladatot úgy, hogy a `FirstScreen`-en legyen egy `TextField`. Amikor a gombra kattintunk, a `SecondScreen`-nek adjuk át a szövegmező értékét a konstruktorán keresztül, és jelenítsük meg ott.

#### Megoldás:
```dart
import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(home: FirstInputScreen()));

class FirstInputScreen extends StatefulWidget {
  const FirstInputScreen({super.key});

  @override
  State<FirstInputScreen> createState() => _FirstInputScreenState();
}

class _FirstInputScreenState extends State<FirstInputScreen> {
  final _textController = TextEditingController();

  @override
  void dispose() {
    _textController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Input Küldés')),
      body: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            TextField(
              controller: _textController,
              decoration: const InputDecoration(labelText: 'Írj be egy üzenetet'),
            ),
            const SizedBox(height: 24),
            ElevatedButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => DisplayScreen(message: _textController.text),
                  ),
                );
              },
              child: const Text('Küldés'),
            ),
          ],
        ),
      ),
    );
  }
}

class DisplayScreen extends StatelessWidget {
  final String message;

  const DisplayScreen({super.key, required this.message});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Fogadott Üzenet')),
      body: Center(
        child: Text(
          message.isEmpty ? 'Nem írtál be semmit!' : 'Üzeneted:\n$message',
          textAlign: TextAlign.center,
          style: const TextStyle(fontSize: 22, fontWeight: FontWeight.w500),
        ),
      ),
    );
  }
}
```

### 3. Feladat: Bejelentkezés utáni Navigator Replacement
Készíts egy `LoginScreen`-t. A bejelentkezés gomb megnyomására navigálj a `DashboardScreen`-re úgy, hogy a felhasználó a fizikai "back" gombbal már ne tudjon visszalépni a belogoló képernyőre (azaz a LoginScreen törlődjön a veremből).

#### Megoldás:
```dart
import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(home: LoginFlowScreen()));

class LoginFlowScreen extends StatelessWidget {
  const LoginFlowScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Bejelentkezés')),
      body: Center(
        child: ElevatedButton(
          onPressed: () {
            // A push helyett pushReplacement-et használunk
            Navigator.pushReplacement(
              context,
              MaterialPageRoute(builder: (context) => const DashboardFlowScreen()),
            );
          },
          child: const Text('Sikeres Bejelentkezés (Replacement)'),
        ),
      ),
    );
  }
}

class DashboardFlowScreen extends StatelessWidget {
  const DashboardFlowScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Dashboard'),
        automaticallyImplyLeading: false, // Eltünteti a vissza gombot
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Text('Üdvözlünk a Dashboardon! (Innen nem tudsz visszalépni)', style: TextStyle(fontSize: 16)),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                // Kijelentkezéskor újra cseréljük a képernyőt
                Navigator.pushReplacement(
                  context,
                  MaterialPageRoute(builder: (context) => const LoginFlowScreen()),
                );
              },
              child: const Text('Kijelentkezés'),
            ),
          ],
        ),
      ),
    );
  }
}
```

### 4. Feladat: 3 Tabos BottomNavigationBar
Hozz létre egy vázat 3 alsó navigációs elemmel ("Kezdőlap", "Keresés", "Profil"). A lapok között váltson az alkalmazás a kiválasztott index belső állapotának megfelelően.

#### Megoldás:
```dart
import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(home: TripleTabScreen()));

class TripleTabScreen extends StatefulWidget {
  const TripleTabScreen({super.key});

  @override
  State<TripleTabScreen> createState() => _TripleTabScreenState();
}

class _TripleTabScreenState extends State<TripleTabScreen> {
  int _currentIndex = 0;

  final List<Widget> _tabs = const [
    Center(child: Text('Kezdőlap tartalom', style: TextStyle(fontSize: 20))),
    Center(child: Text('Keresés képernyő', style: TextStyle(fontSize: 20))),
    Center(child: Text('Profil adatok', style: TextStyle(fontSize: 20))),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Tab Navigáció')),
      body: _tabs[_currentIndex],
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _currentIndex,
        onTap: (index) {
          setState(() {
            _currentIndex = index;
          });
        },
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.home), label: 'Kezdőlap'),
          BottomNavigationBarItem(icon: Icon(Icons.search), label: 'Keresés'),
          BottomNavigationBarItem(icon: Icon(Icons.person), label: 'Profil'),
        ],
      ),
    );
  }
}
```

### 5. Feladat: Named Routes Paraméter átadással
Regisztrálj nevesített útvonalakat a `MaterialApp`-ban. Készíts egy útvonalat `/settings` névvel, és add át neki paraméterként, hogy a Sötét mód aktív-e (bool). Olvasd be a paramétert a Settings oldalon.

#### Megoldás:
```dart
import 'package:flutter/material.dart';

void main() {
  runApp(MaterialApp(
    initialRoute: '/',
    routes: {
      '/': (context) => const HomeScreenNamed(),
      '/settings': (context) => const SettingsScreenNamed(),
    },
  ));
}

class HomeScreenNamed extends StatelessWidget {
  const HomeScreenNamed({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Named Route Kezdőlap')),
      body: Center(
        child: ElevatedButton(
          onPressed: () {
            // Named route hívás paraméterrel (arguments)
            Navigator.pushNamed(
              context,
              '/settings',
              arguments: true, // Sötét mód állapota
            );
          },
          child: const Text('Beállítások megnyitása (Sötét mód: BE)'),
        ),
      ),
    );
  }
}

class SettingsScreenNamed extends StatelessWidget {
  const SettingsScreenNamed({super.key});

  @override
  Widget build(BuildContext context) {
    // Argumentum kiolvasása a ModalRoute-ból
    final isDarkModeActive = ModalRoute.of(context)?.settings.arguments as bool? ?? false;

    return Scaffold(
      appBar: AppBar(title: const Text('Beállítások')),
      body: Center(
        child: Text(
          'A kapott beállítás szerint a Sötét mód:\n${isDarkModeActive ? 'AKTÍV' : 'INAKTÍV'}',
          textAlign: TextAlign.center,
          style: const TextStyle(fontSize: 20),
        ),
      ),
    );
  }
}
```

---

## Heti Mini Projekt

### Recept App Navigációval
A heti mini projekt egy recept böngésző alkalmazás. Tartalmaz egy több lapból álló navigációs vázat (`BottomNavigationBar`), egy kategóriaválasztót, egy receptlistát, és egy részletes receptmegjelenítő oldalt összetevőkkel, lépésekkel, ahova navigálva adatot adunk át.

#### A Teljes Kód (`lib/main.dart`):

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const RecipeApp());
}

class RecipeApp extends StatelessWidget {
  const RecipeApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Recept Tár',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.emerald),
        useMaterial3: true,
      ),
      home: const MainTabContainer(),
    );
  }
}

// Recept adatmodell
class Recipe {
  final String title;
  final String category;
  final String duration;
  final String difficulty;
  final String icon;
  final List<String> ingredients;
  final List<String> steps;

  const Recipe({
    required this.title,
    required this.category,
    required this.duration,
    required this.difficulty,
    required this.icon,
    required this.ingredients,
    required this.steps,
  });
}

// Fő Tabos keret
class MainTabContainer extends StatefulWidget {
  const MainTabContainer({super.key});

  @override
  State<MainTabContainer> createState() => _MainTabContainerState();
}

class _MainTabContainerState extends State<MainTabContainer> {
  int _currentTab = 0;
  final List<Recipe> _favoriteRecipes = [];

  void _toggleFavorite(Recipe recipe) {
    setState(() {
      if (_favoriteRecipes.contains(recipe)) {
        _favoriteRecipes.remove(recipe);
      } else {
        _favoriteRecipes.add(recipe);
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    // Dinamikusan állítjuk össze az oldalakat, hogy átadjuk a kedvencek logikáját
    final List<Widget> pages = [
      RecipeListTab(
        favorites: _favoriteRecipes,
        onToggleFavorite: _toggleFavorite,
      ),
      FavoritesTab(
        favorites: _favoriteRecipes,
        onToggleFavorite: _toggleFavorite,
      ),
      const ProfileTab(),
    ];

    return Scaffold(
      body: pages[_currentTab],
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _currentTab,
        onTap: (index) => setState(() => _currentTab = index),
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.restaurant_menu), label: 'Receptek'),
          BottomNavigationBarItem(icon: Icon(Icons.favorite), label: 'Kedvencek'),
          BottomNavigationBarItem(icon: Icon(Icons.person), label: 'Profil'),
        ],
      ),
    );
  }
}

// 1. Tab: Receptek listája kategóriákkal
class RecipeListTab extends StatelessWidget {
  final List<Recipe> favorites;
  final Function(Recipe) onToggleFavorite;

  const RecipeListTab({
    super.key,
    required this.favorites,
    required this.onToggleFavorite,
  });

  final List<Recipe> _recipes = const [
    Recipe(
      title: 'Klasszikus Palacsinta',
      category: 'Édesség',
      duration: '30 perc',
      difficulty: 'Könnyű',
      icon: '🥞',
      ingredients: ['20 dkg liszt', '2 db tojás', '3 dl tej', '2 dl szódavíz', 'csipet só'],
      steps: ['Keverd össze a lisztet és a tojásokat.', 'Fokozatosan add hozzá a tejet és a szódát.', 'Süsd ki forró serpenyőben.'],
    ),
    Recipe(
      title: 'Paradicsomos Tészta',
      category: 'Főétel',
      duration: '20 perc',
      difficulty: 'Könnyű',
      icon: '🍝',
      ingredients: ['200g tészta', '400g paradicsomszósz', '2 gerezd fokhagyma', 'Bazsalikom', 'Parmezán'],
      steps: ['Főzd meg a tésztát sós vízben.', 'Párold meg a fokhagymát, add hozzá a paradicsomot.', 'Keverd össze és szórd meg bazsalikommal.'],
    ),
    Recipe(
      title: 'Gulyásleves',
      category: 'Leves',
      duration: '90 perc',
      difficulty: 'Közepes',
      icon: '🍲',
      ingredients: ['50 dkg marhahús', '2 fej hagyma', 'burgonya', 'sárgarépa', 'fűszerpaprika'],
      steps: ['Pirítsd meg a hagymát, majd a húst.', 'Szórd meg paprikával, öntsd fel vízzel.', 'Add hozzá a zöldségeket és főzd készre.'],
    ),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Recept Kategóriák')),
      body: ListView.builder(
        padding: const EdgeInsets.all(12.0),
        itemCount: _recipes.length,
        itemBuilder: (context, index) {
          final recipe = _recipes[index];
          final isFav = favorites.contains(recipe);

          return Card(
            margin: const EdgeInsets.symmetric(vertical: 8.0),
            child: ListTile(
              leading: Text(recipe.icon, style: const TextStyle(fontSize: 32)),
              title: Text(recipe.title, style: const TextStyle(fontWeight: FontWeight.bold)),
              subtitle: Text('${recipe.category} • ${recipe.duration} • ${recipe.difficulty}'),
              trailing: IconButton(
                icon: Icon(isFav ? Icons.favorite : Icons.favorite_border, color: Colors.red),
                onPressed: () => onToggleFavorite(recipe),
              ),
              onTap: () {
                // Részletező oldal megnyitása
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => RecipeDetailScreen(
                      recipe: recipe,
                      isFavorite: favorites.contains(recipe),
                      onToggleFavorite: onToggleFavorite,
                    ),
                  ),
                );
              },
            ),
          );
        },
      ),
    );
  }
}

// Recept Részletező Képernyő
class RecipeDetailScreen extends StatefulWidget {
  final Recipe recipe;
  final bool isFavorite;
  final Function(Recipe) onToggleFavorite;

  const RecipeDetailScreen({
    super.key,
    required this.recipe,
    required this.isFavorite,
    required this.onToggleFavorite,
  });

  @override
  State<RecipeDetailScreen> createState() => _RecipeDetailScreenState();
}

class _RecipeDetailScreenState extends State<RecipeDetailScreen> {
  late bool _favState;

  @override
  void initState() {
    super.initState();
    _favState = widget.isFavorite;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.recipe.title),
        actions: [
          IconButton(
            icon: Icon(_favState ? Icons.favorite : Icons.favorite_border, color: Colors.red),
            onPressed: () {
              widget.onToggleFavorite(widget.recipe);
              setState(() {
                _favState = !_favState;
              });
            },
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Center(
              child: Text(widget.recipe.icon, style: const TextStyle(fontSize: 80)),
            ),
            const SizedBox(height: 16),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                Chip(label: Text(widget.recipe.category)),
                Chip(label: Text(widget.recipe.duration), avatar: const Icon(Icons.timer, size: 16)),
                Chip(label: Text(widget.recipe.difficulty), avatar: const Icon(Icons.bolt, size: 16)),
              ],
            ),
            const SizedBox(height: 24),
            const Text('Összetevők:', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            ...widget.recipe.ingredients.map((ing) => Padding(
                  padding: const EdgeInsets.symmetric(vertical: 4.0),
                  child: Row(
                    children: [
                      const Icon(Icons.check_circle_outline, color: Colors.emerald, size: 18),
                      const SizedBox(width: 8),
                      Text(ing, style: const TextStyle(fontSize: 16)),
                    ],
                  ),
                )),
            const SizedBox(height: 24),
            const Text('Elkészítés menete:', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            ...widget.recipe.steps.asMap().entries.map((entry) {
              int idx = entry.key;
              String step = entry.value;
              return Padding(
                padding: const EdgeInsets.symmetric(vertical: 6.0),
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    CircleAvatar(
                      radius: 12,
                      child: Text('${idx + 1}', style: const TextStyle(fontSize: 12)),
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      child: Text(step, style: const TextStyle(fontSize: 16)),
                    ),
                  ],
                ),
              );
            }),
          ],
        ),
      ),
    );
  }
}

// 2. Tab: Kedvencek listája
class FavoritesTab extends StatelessWidget {
  final List<Recipe> favorites;
  final Function(Recipe) onToggleFavorite;

  const FavoritesTab({
    super.key,
    required this.favorites,
    required this.onToggleFavorite,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Kedvenc Receptek')),
      body: favorites.isEmpty
          ? const Center(
              child: Text('Még nincsenek kedvenc receptjeid.', style: TextStyle(fontSize: 16, color: Colors.grey)),
            )
          : ListView.builder(
              padding: const EdgeInsets.all(12.0),
              itemCount: favorites.length,
              itemBuilder: (context, index) {
                final recipe = favorites[index];
                return Card(
                  child: ListTile(
                    leading: Text(recipe.icon, style: const TextStyle(fontSize: 24)),
                    title: Text(recipe.title),
                    trailing: IconButton(
                      icon: const Icon(Icons.delete, color: Colors.red),
                      onPressed: () => onToggleFavorite(recipe),
                    ),
                    onTap: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (context) => RecipeDetailScreen(
                            recipe: recipe,
                            isFavorite: true,
                            onToggleFavorite: onToggleFavorite,
                          ),
                        ),
                      );
                    },
                  ),
                );
              },
            ),
    );
  }
}

// 3. Tab: Egyszerű Profiloldal
class ProfileTab extends StatelessWidget {
  const ProfileTab({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Profil')),
      body: const Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            CircleAvatar(
              radius: 50,
              child: Icon(Icons.person, size: 60),
            ),
            SizedBox(height: 16),
            Text('Szakács Sándor', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
            Text('Háziséf szint', style: TextStyle(color: Colors.grey)),
          ],
        ),
      ),
    );
  }
}
```

---

## Heti Ellenőrző Kérdések & Válaszok

### 1. Miért használjuk a `Navigator.pushReplacement` metódust a sima `Navigator.push` helyett (pl. login után)?
A `Navigator.push` az új oldalt ráhelyezi a meglévő oldalakra a veremben. Bejelentkezés után ha a felhasználó megnyomja a fizikai vagy szoftveres "vissza" gombot, visszajutna a Login képernyőre, ami nem kívánt működés. A `pushReplacement` ezzel szemben a verem legfelső elemét (a Login képernyőt) **kicseréli** az új képernyőre, így a korábbi oldal megszűnik a memóriában és a veremben is.

### 2. Hogyan adhatunk át adatokat egy új képernyőnek és hogyan várhatunk vissza eredményt?
*   **Adatátadás előre:** Az adatot legegyszerűbben a céleszköz widget konstruktorának paramétereként adjuk át: `MaterialPageRoute(builder: (_) => DetailsPage(data: kulsodata))`.
*   **Adat visszanyerése:** A navigáció meghívásakor az aszinkron `await` kulcsszóval megvárjuk a hívást: `final result = await Navigator.push(...)`. Amikor a céloldalt bezárjuk, a `Navigator.pop(context, visszakuldottAdat)` hívással küldjük vissza az értéket.

### 3. Mi az a named route, és milyen előnyei/hátrányai vannak a közvetlen `MaterialPageRoute` navigációval szemben?
*   **Named Route:** Egy string alapú útvonal (pl. `'/details'`), amelyet központilag regisztrálunk.
*   **Előnyei:** Központosított konfiguráció, könnyen olvasható navigáció, elkerülhető a widgetek importálgatása mindenhonnan.
*   **Hátrányai:** Típusbiztonság elvesztése (mivel stringeket használunk), és bonyolultabb paraméterátadás, ami sérülékenyebbé teszi a kódot (casting hibák).

### 4. Hogyan működik a `BottomNavigationBar` a Flutterben, és hogyan váltunk a tabok között?
A `BottomNavigationBar` egy olyan widget, ami a `Scaffold.bottomNavigationBar` tulajdonságában helyezkedik el. Tartalmaz egy `items` listát (gombokkal), egy `currentIndex` paramétert (az éppen aktív lap indexe) és egy `onTap` callback-et. A tab váltást belső állapottal (`State`) kezeljük: amikor a felhasználó megérinti valamelyik elemet, az `onTap` lefut, a `setState()` segítségével módosítjuk a `currentIndex` értékét, és a `body`-ban a listából az ennek megfelelő indexű widgetet jelenítjük meg.

### 5. Mi a `go_router` előnye a beépített Navigator 1.0-val szemben haladóbb routing (pl. deep linking, webes platform) esetén?
A `go_router` egy deklaratív navigációs csomag, ami szinkronizálja az alkalmazás belső állapotát a böngésző címsorával (web platformon kiemelten fontos). Támogatja a közvetlen mélylinkelést (pl. egy linkre kattintva a telefon a recept részletezőre ugrik), könnyedén kezel dinamikus URL paramétereket (pl. `/recipe/:id`), beépített átirányítási szabályokkal (redirect/guards) rendelkezik az autentikáció kezelésére, és egyszerűbben implementálható vele a nested navigáció (ShellRoute).
