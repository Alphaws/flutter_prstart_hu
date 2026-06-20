# 2. hét — Flutter alapok és widget gondolkodás

## Cél
A hét célja a Flutter fejlesztői szemlélet megalapozása. Megértjük, hogyan épül fel egy Flutter projekt, hogyan kezeljük a függőségeket és asseteket a `pubspec.yaml`-ben. Megtanuljuk a widget-alapú gondolkodást, megismerjük a legfontosabb alapvető widgeteket, a háttérben futó háromfa (Widget, Element, RenderObject) architektúrát, valamint a StatelessWidget és StatefulWidget közötti különbségeket és a State életciklusát.

---

## Elmélet

### 2.1 A Flutter projektstruktúra és a pubspec.yaml
Amikor létrehozol egy új Flutter projektet a `flutter create <projektnev>` paranccsal, egy előre strukturált mappaszerkezetet kapsz:

*   **`lib/`**: Ez a legfontosabb mappa. Ide kerül az összes Dart kód. A belépési pont a `lib/main.dart` fájl, ebben található a `main()` függvény.
*   **`android/`, `ios/`, `web/`, `windows/`, `macos/`, `linux/`**: Platformspecifikus natív projektek mappái. A Flutter build rendszere ezeket használja fel a natív alkalmazások generálásához. Általában ritkán kell közvetlenül módosítani őket (pl. engedélyek megadásakor).
*   **`test/`**: A tesztfájlok helye. Itt írhatunk unit, widget és integrációs teszteket.
*   **`pubspec.yaml`**: A projekt konfigurációs fájlja. Itt határozzuk meg:
    *   Az alkalmazás nevét, leírását és verzióját.
    *   A minimálisan elvárt SDK verziókat.
    *   A függőségeket (a `dependencies` szekcióba mennek a külső csomagok a pub.dev-ről, a `dev_dependencies` szekcióba pedig a csak fejlesztéshez használt eszközök).
    *   Az asseteket (képek, JSON fájlok, hangok stb.) és a betűtípusokat.

A `pubspec.yaml` formázásánál a YAML szabályai szerint a behúzás (indentation) kritikus: pontosan 2 szóközt kell használni szintekhez.

```yaml
name: my_flutter_app
description: "Egy minta Flutter alkalmazás"
version: 1.0.0+1

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter
  cupertino_icons: ^1.0.5

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^3.0.0

flutter:
  uses-material-design: true
  assets:
    - assets/images/profile.png
    - assets/data/
  fonts:
    - family: CustomFont
      fonts:
        - asset: assets/fonts/CustomFont-Regular.ttf
        - asset: assets/fonts/CustomFont-Bold.ttf
          weight: 700
```

### 2.2 Alapvető UI Widgetek
Flutterben szinte minden UI elem egy widget. A widgetek egymásba ágyazásával építjük fel a felhasználói felületet. A legfontosabbak:

1.  **Strukturális widgetek:**
    *   `MaterialApp`: Az alkalmazás gyökere, amely beállítja a Material Design témát, a lokalizációt és a navigációt.
    *   `Scaffold`: Biztosítja a klasszikus Material képernyőstruktúrát (AppBar, Body, FloatingActionButton, Drawer, BottomNavigationBar).
    *   `AppBar`: A képernyő tetején lévő címsor és menüsáv.

2.  **Szöveg és Kép:**
    *   `Text`: Szöveg megjelenítésére és formázására szolgál (`TextStyle`).
    *   `Icon`: Vektorgrafikus ikonok megjelenítése a beépített `Icons` gyűjteményből.
    *   `Image`: Képek betöltése hálózatról (`Image.network`), assetekből (`Image.asset`), memóriából vagy fájlból.

3.  **Elrendezés (Layout) widgetek:**
    *   `Container`: Egy sokoldalú doboz widget, amelynek adható margó (`margin`), belső margó (`padding`), háttérszín, lekerekítés, árnyék (`decoration`) és méret.
    *   `Column`: Gyermekeit függőlegesen rendezi el.
    *   `Row`: Gyermekeit vízszintesen rendezi el.
    *   `Stack`: Lehetővé teszi a gyermekek egymásra rétegezését (pl. kép fölé szöveg).
    *   `ListView`: Görgethető lista, ami lusta betöltésre is képes (`ListView.builder`).
    *   `GridView`: Görgethető rácsos elrendezés.
    *   `Card`: Anyagszerű, lekerekített, árnyékolt kártya panel.

4.  **Interakció és Beviteli mezők:**
    *   `ElevatedButton`: Kiemelkedő, klasszikus gomb háttérszínnel.
    *   `TextButton`: Egyszerű szöveges gomb, háttér nélkül.
    *   `IconButton`: Csak ikont tartalmazó gomb.
    *   `TextField`: Felhasználói szövegbeviteli mező.

### 2.3 A Widget Fa (Widget Tree) és a Három Fa Architektúra
Amikor Flutterben kódolunk, látszólag csak egyetlen fát építünk: a Widget fát. A valóságban azonban a Flutter motor (Flutter Engine) három egymással párhuzamosan működő fát tart fenn a kiváló teljesítmény érdekében:

1.  **Widget Tree (Widget Fa):** Ez a deklaratív kódunk közvetlen leképezése. A widgetek pehelysúlyúak, olcsón létrehozhatók és megsemmisíthetők. Csak konfigurációs adatok tartói (blueprints), nem tartalmaznak renderelési logikát.
2.  **Element Tree (Element Fa):** A Widget és a RenderObject fa közötti összekötő kapocs. Az elementek reprezentálják a widgetek fizikai jelenlétét a képernyőn. Ők vezérlik az életciklust és tartják meg a widgetek állapotát (State). Ha a widget fa változik (pl. hot reload vagy `setState` miatt), a Flutter megpróbálja újrahasznosítani a meglévő elementeket, ha a típusuk és kulcsuk (`key`) megegyezik.
3.  **RenderObject Tree (RenderObject Fa):** A tényleges elrendezésért (layout) és rajzolásért (painting) felelős fa. Ezek a nehézsúlyú objektumok végzik el a méretezési számításokat (constraints) és rajzolják ki a pixeleket a kijelzőre. Csak akkor változnak meg, ha a méret vagy a megjelenés ténylegesen módosul.

```mermaid
graph TD
    subgraph Widget Tree [Widget Tree (Konfiguráció)]
        W1[Container] --> W2[Row]
        W2 --> W3[Text]
        W2 --> W4[Icon]
    end
    subgraph Element Tree [Element Tree (Életciklus / State)]
        E1[ComponentElement] --> E2[MultiChildRenderObjectElement]
        E2 --> E3[ComponentElement]
        E2 --> E4[LeafRenderObjectElement]
    end
    subgraph RenderObject Tree [RenderObject Tree (Layout / Paint)]
        R1[RenderPadding] --> R2[RenderFlex]
        R2 --> R3[RenderParagraph]
        R2 --> R4[RenderBox]
    end
    
    W1 -.-> E1
    W2 -.-> E2
    W3 -.-> E3
    W4 -.-> E4
    
    E1 -.-> R1
    E2 -.-> R2
    E3 -.-> R3
    E4 -.-> R4
```

### 2.4 StatelessWidget és StatefulWidget
A Flutterben a widgetek alapvetően két kategóriába sorolhatók aszerint, hogy változhat-e az állapotuk a futás során.

#### StatelessWidget (Állapotmentes Widget)
Az ilyen widgetek tartalma és megjelenése kizárólag a konstruktorban átadott paraméterektől függ. Egyszer épülnek fel, és nem képesek önmaguktól újrarajzolódni.
*   **Példa:** Egy fix szöveget kiíró gomb, egy ikon, egy statikus profilkártya.
*   *Minden tulajdonságuk kötelezően `final`!*

#### StatefulWidget (Állapotvezérelt Widget)
Ha egy widgetnek változhat a belső állapota (pl. egy számláló értéke növekszik, egy szövegmezőbe írnak, egy hálózati kérés töltődik), akkor StatefulWidgetot kell használnunk.
Ez a widget két osztályból áll:
1.  Maga a `StatefulWidget` osztály, ami konfigurációs blueprintként szolgál (és immutable).
2.  A `State` osztály, ami a változó adatokat őrzi, és tartalmazza a `build` metódust.

##### A State Életciklusa (Lifecycle)
A `State` objektumnak jól meghatározott életciklusa van:
*   **`createState()`**: Amikor a StatefulWidget bekerül a fába, a Flutter meghívja ezt a metódust a State objektum létrehozásához.
*   **`initState()`**: A legelső metódus, ami lefut a State létrejötte után. Ideális hely egyszeri inicializálásokhoz (pl. kontrollerek létrehozása, API hívás indítása). *Mindig meg kell hívni benne a `super.initState()`-et.*
*   **`didChangeDependencies()`**: Az `initState()` után azonnal, valamint a widget függőségeinek (pl. InheritedWidget, Theme, MediaQuery) változásakor fut le.
*   **`build(BuildContext context)`**: Meghatározza a UI-t. Akkor fut le, ha az `initState()` befejeződött, a függőségek változtak, vagy meghívtuk a `setState()` metódust.
*   **`didUpdateWidget(covariant MyWidget oldWidget)`**: Ha a szülő widget újraépül és új konfigurációs adatokat ad át a widgetnek, de az Element típus változatlan marad, ez a metódus fut le. Itt összehasonlítható az új és a régi konfiguráció.
*   **`setState(VoidCallback fn)`**: Értesíti a keretrendszert, hogy a belső állapot megváltozott, így a keretrendszer ütemezi a widget `build` metódusának újra lefutását. A változtatásokat a callback függvényen belül kell elvégezni.
*   **`dispose()`**: Amikor a widget végleg kikerül a fából és törlődik a memóriából. Itt kell lezárni a stream-eket, animációs kontrollereket és szövegmező kontrollereket a memóriaszivárgások elkerülése érdekében.

---

## Kódpéldák

Az alábbiakban egy teljes, másolható és futtatható `main.dart` példát láthatsz, amely bemutatja mindkét widget típust és a state-változást egy interaktív kártya segítségével.

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
      title: 'Flutter Alapok',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: const HomeScreen(),
    );
  }
}

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Flutter Alapozó'),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
      ),
      body: const Padding(
        padding: EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            StatusCard(title: 'Rendszer Státusz', message: 'Minden szolgáltatás üzemel.'),
            SizedBox(height: 16),
            Expanded(child: InteractiveCounter()),
          ],
        ),
      ),
    );
  }
}

// 1. StatelessWidget példa: Egy statikus státuszkártya
class StatusCard extends StatelessWidget {
  final String title;
  final String message;

  const StatusCard({
    super.key,
    required this.title,
    required this.message,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 4,
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                const Icon(Icons.info_outline, color: Colors.deepPurple),
                const SizedBox(width: 8),
                Text(
                  title,
                  style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 18),
                ),
              ],
            ),
            const SizedBox(height: 8),
            Text(message),
          ],
        ),
      ),
    );
  }
}

// 2. StatefulWidget példa: Interaktív számláló kártya
class InteractiveCounter extends StatefulWidget {
  const InteractiveCounter({super.key});

  @override
  State<InteractiveCounter> createState() => _InteractiveCounterState();
}

class _InteractiveCounterState extends State<InteractiveCounter> {
  int _counter = 0;

  @override
  void initState() {
    super.initState();
    // Belső állapot inicializálása
    _counter = 10; // Kezdőérték beállítása
  }

  void _increment() {
    setState(() {
      _counter++;
    });
  }

  void _decrement() {
    if (_counter > 0) {
      setState(() {
        _counter--;
      });
    }
  }

  @override
  void dispose() {
    // Erőforrások felszabadítása (itt most nincs controller, de jó gyakorlat)
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      color: Colors.deepPurple.shade50,
      elevation: 2,
      child: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Text(
              'Interaktív Számláló',
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 16),
            Text(
              '$_counter',
              style: Theme.of(context).textTheme.displayLarge?.copyWith(
                    color: Colors.deepPurple,
                    fontWeight: FontWeight.bold,
                  ),
            ),
            const SizedBox(height: 24),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                ElevatedButton.icon(
                  onPressed: _decrement,
                  icon: const Icon(Icons.remove),
                  label: const Text('Csökkent'),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.red.shade100,
                    foregroundColor: Colors.red.shade800,
                  ),
                ),
                ElevatedButton.icon(
                  onPressed: _increment,
                  icon: const Icon(Icons.add),
                  label: const Text('Növel'),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.green.shade100,
                    foregroundColor: Colors.green.shade800,
                  ),
                ),
              ],
            )
          ],
        ),
      ),
    );
  }
}
```

---

## Gyakorlófeladatok & Megoldások

### 1. Feladat: Névjegykártya Képernyő
Készíts egy letisztult, esztétikus névjegykártya képernyőt, amely tartalmaz egy profilképet (vagy avatár ikont), nevet, beosztást és elérhetőségeket (ikon + szöveg elrendezéssel).

#### Megoldás:
```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const MaterialApp(
    home: BusinessCardScreen(),
  ));
}

class BusinessCardScreen extends StatelessWidget {
  const BusinessCardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey.shade100,
      body: SafeArea(
        child: Center(
          child: Card(
            elevation: 8,
            margin: const EdgeInsets.all(24.0),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(16.0),
            ),
            child: Padding(
              padding: const EdgeInsets.all(24.0),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const CircleAvatar(
                    radius: 50,
                    backgroundColor: Colors.blueAccent,
                    child: Icon(Icons.person, size: 60, color: Colors.white),
                  ),
                  const SizedBox(height: 16),
                  const Text(
                    'Kovács Péter',
                    style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                  ),
                  const Text(
                    'Senior Flutter Developer',
                    style: TextStyle(
                      fontSize: 16,
                      color: Colors.blueAccent,
                      fontWeight: FontWeight.w500,
                    ),
                  ),
                  const SizedBox(height: 16),
                  const Divider(),
                  const SizedBox(height: 16),
                  const ContactRow(icon: Icons.email, text: 'peter.kovacs@email.com'),
                  const SizedBox(height: 10),
                  const ContactRow(icon: Icons.phone, text: '+36 30 123 4567'),
                  const SizedBox(height: 10),
                  const ContactRow(icon: Icons.web, text: 'www.kovacspeter.dev'),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}

class ContactRow extends StatelessWidget {
  final IconData icon;
  final String text;

  const ContactRow({super.key, required this.icon, required this.text});

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Icon(icon, color: Colors.grey.shade600),
        const SizedBox(width: 12),
        Text(
          text,
          style: TextStyle(fontSize: 16, color: Colors.grey.shade800),
        ),
      ],
    );
  }
}
```

### 2. Feladat: Számláló App Határértékekkel
Egészítsd ki a számlálót úgy, hogy az érték ne mehessen 0 alá, és ne mehessen 20 fölé. Ha eléri a korlátot, a megfelelő gomb váljon inaktívvá (`onPressed: null`).

#### Megoldás:
```dart
import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(home: BoundedCounterScreen()));

class BoundedCounterScreen extends StatefulWidget {
  const BoundedCounterScreen({super.key});

  @override
  State<BoundedCounterScreen> createState() => _BoundedCounterScreenState();
}

class _BoundedCounterScreenState extends State<BoundedCounterScreen> {
  int _counter = 0;
  static const int minLimit = 0;
  static const int maxLimit = 20;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Korlátos Számláló')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text('Érték:', style: Theme.of(context).textTheme.titleLarge),
            Text(
              '$_counter',
              style: const TextStyle(fontSize: 72, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 24),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                ElevatedButton(
                  onPressed: _counter > minLimit
                      ? () => setState(() => _counter--)
                      : null,
                  child: const Text('Csökkent'),
                ),
                const SizedBox(width: 16),
                ElevatedButton(
                  onPressed: _counter < maxLimit
                      ? () => setState(() => _counter++)
                      : null,
                  child: const Text('Növel'),
                ),
              ],
            ),
            if (_counter == maxLimit)
              const Padding(
                padding: EdgeInsets.only(top: 16.0),
                child: Text('Elérted a maximumot (20)!', style: TextStyle(color: Colors.red)),
              ),
          ],
        ),
      ),
    );
  }
}
```

### 3. Feladat: Egyszerű Bevásárlólista Képernyő
Készíts egy statikus listát, amelyben 5 darab előre meghatározott bevásárlólistás elem jelenik meg egy `ListView` és `ListTile` segítségével.

#### Megoldás:
```dart
import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(home: ShoppingListScreen()));

class ShoppingListScreen extends StatelessWidget {
  const ShoppingListScreen({super.key});

  final List<String> items = const [
    'Tej (1,5%)',
    'Teljes kiőrlésű kenyér',
    'Alma (Gála)',
    'Csirkemell filé',
    'Tojás (M-es, 10db)'
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Bevásárlólista')),
      body: ListView.builder(
        itemCount: items.length,
        itemBuilder: (context, index) {
          return Card(
            margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 6),
            child: ListTile(
              leading: CircleAvatar(
                child: Text('${index + 1}'),
              ),
              title: Text(items[index]),
              trailing: const Icon(Icons.shopping_cart_checkout),
            ),
          );
        },
      ),
    );
  }
}
```

### 4. Feladat: Profil Képernyő
Készíts egy profil képernyőt, ahol a felhasználó neve, profilképe és három statisztikai adata (pl. "Posztok", "Követők", "Követések") jelenik meg egymás mellett vízszintes sorban (`Row`).

#### Megoldás:
```dart
import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(home: ProfileScreen()));

class ProfileScreen extends StatelessWidget {
  const ProfileScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Felhasználói Profil')),
      body: Column(
        children: [
          const SizedBox(height: 24),
          const CircleAvatar(
            radius: 60,
            backgroundColor: Colors.deepPurple,
            child: Icon(Icons.person, size: 70, color: Colors.white),
          ),
          const SizedBox(height: 16),
          const Text(
            'Nagy Aliz',
            style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
          ),
          const Text(
            'Budapest, Magyarország',
            style: TextStyle(color: Colors.grey),
          ),
          const SizedBox(height: 24),
          const Divider(),
          const SizedBox(height: 16),
          const Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: [
              StatWidget(label: 'Posztok', value: '124'),
              StatWidget(label: 'Követők', value: '14.2k'),
              StatWidget(label: 'Követett', value: '382'),
            ],
          ),
        ],
      ),
    );
  }
}

class StatWidget extends StatelessWidget {
  final String label;
  final String value;

  const StatWidget({super.key, required this.label, required this.value});

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text(
          value,
          style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
        ),
        const SizedBox(height: 4),
        Text(
          label,
          style: const TextStyle(color: Colors.grey),
        ),
      ],
    );
  }
}
```

### 5. Feladat: Dinamikus Háttér és Szöveg
Készíts egy képernyőt, amelyen egy gomb megnyomására változik a képernyő háttérszíne és a rajta lévő szöveg (pl. "Nappali mód" -> sárga háttér, "Éjszakai mód" -> sötétkék háttér).

#### Megoldás:
```dart
import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(home: ToggleThemeScreen()));

class ToggleThemeScreen extends StatefulWidget {
  const ToggleThemeScreen({super.key});

  @override
  State<ToggleThemeScreen> createState() => _ToggleThemeScreenState();
}

class _ToggleThemeScreenState extends State<ToggleThemeScreen> {
  bool _isDarkMode = false;

  @override
  Widget build(BuildContext context) {
    final backgroundColor = _isDarkMode ? const Color(0xFF1A1A2E) : const Color(0xFFFFFBEB);
    final textColor = _isDarkMode ? Colors.white : Colors.black80;
    final modeText = _isDarkMode ? 'Éjszakai Mód' : 'Nappali Mód';

    return Scaffold(
      body: AnimatedContainer(
        duration: const Duration(milliseconds: 300),
        color: backgroundColor,
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(
                _isDarkMode ? Icons.dark_mode : Icons.light_mode,
                size: 80,
                color: _isDarkMode ? Colors.yellow : Colors.orange,
              ),
              const SizedBox(height: 16),
              Text(
                modeText,
                style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold, color: textColor),
              ),
              const SizedBox(height: 24),
              ElevatedButton(
                onPressed: () {
                  setState(() {
                    _isDarkMode = !_isDarkMode;
                  });
                },
                child: const Text('Mód váltása'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
```

---

## Heti Mini Projekt

### Napi Teendők App (Todo List) — Csak Memóriában
A heti mini projektünk egy teljes értékű feladatkezelő alkalmazás. Nem használunk külső adatbázist, az adatokat a State memóriájában tároljuk.

#### Megvalósított Funkciók:
*   Új feladat hozzáadása szöveges bevitellel.
*   Feladat törlése gombnyomásra.
*   Feladat befejezetté jelölése (pipálás), ami megváltoztatja a feladat stílusát (áthúzott szöveg).
*   Üres lista állapot kezelése (szép grafika/ikon és tájékoztató szöveg).
*   Egyszerű, tiszta Material 3 design.

#### A Teljes Kód (`lib/main.dart`):

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const TodoApp());
}

class TodoApp extends StatelessWidget {
  const TodoApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Teendőim',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.teal),
        useMaterial3: true,
      ),
      home: const TodoListScreen(),
    );
  }
}

// Feladat adatmodell
class TodoItem {
  final String id;
  final String title;
  bool isDone;

  TodoItem({
    required this.id,
    required this.title,
    this.isDone = false,
  });
}

class TodoListScreen extends StatefulWidget {
  const TodoListScreen({super.key});

  @override
  State<TodoListScreen> createState() => _TodoListScreenState();
}

class _TodoListScreenState extends State<TodoListScreen> {
  final List<TodoItem> _todoList = [];
  final TextEditingController _textController = TextEditingController();

  void _addTodo(String text) {
    if (text.trim().isEmpty) return;
    setState(() {
      _todoList.add(TodoItem(
        id: DateTime.now().toString(),
        title: text.trim(),
      ));
    });
    _textController.clear();
  }

  void _toggleTodo(String id) {
    setState(() {
      final item = _todoList.firstWhere((element) => element.id == id);
      item.isDone = !item.isDone;
    });
  }

  void _deleteTodo(String id) {
    setState(() {
      _todoList.removeWhere((element) => element.id == id);
    });
  }

  @override
  void dispose() {
    _textController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Napi Teendők'),
        centerTitle: true,
        backgroundColor: Theme.of(context).colorScheme.primaryContainer,
      ),
      body: Column(
        children: [
          // Szövegbeviteli mező az új teendőhöz
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _textController,
                    decoration: const InputDecoration(
                      hintText: 'Új teendő hozzáadása...',
                      border: OutlineInputBorder(),
                      contentPadding: EdgeInsets.symmetric(horizontal: 16),
                    ),
                    onSubmitted: _addTodo,
                  ),
                ),
                const SizedBox(width: 12),
                ElevatedButton(
                  onPressed: () => _addTodo(_textController.text),
                  style: ElevatedButton.styleFrom(
                    padding: const EdgeInsets.symmetric(vertical: 14, horizontal: 16),
                  ),
                  child: const Icon(Icons.add),
                ),
              ],
            ),
          ),
          
          // A teendők listája vagy az üres állapot
          Expanded(
            child: _todoList.isEmpty
                ? Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(
                          Icons.playlist_add_check,
                          size: 100,
                          color: Colors.teal.shade200,
                        ),
                        const SizedBox(height: 16),
                        Text(
                          'Mára nincs több feladatod!',
                          style: TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                            color: Colors.teal.shade700,
                          ),
                        ),
                        const Text(
                          'Írj be egyet fent a kezdéshez.',
                          style: TextStyle(color: Colors.grey),
                        ),
                      ],
                    ),
                  )
                : ListView.builder(
                    itemCount: _todoList.length,
                    itemBuilder: (context, index) {
                      final item = _todoList[index];
                      return Card(
                        margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 6),
                        elevation: 1,
                        child: ListTile(
                          leading: Checkbox(
                            value: item.isDone,
                            onChanged: (_) => _toggleTodo(item.id),
                          ),
                          title: Text(
                            item.title,
                            style: TextStyle(
                              decoration: item.isDone
                                  ? TextDecoration.lineThrough
                                  : TextDecoration.none,
                              color: item.isDone ? Colors.grey : Colors.black80,
                            ),
                          ),
                          trailing: IconButton(
                            icon: const Icon(Icons.delete, color: Colors.redAccent),
                            onPressed: () => _deleteTodo(item.id),
                          ),
                        ),
                      );
                    },
                  ),
          ),
        ],
      ),
    );
  }
}
```

---

## Heti Ellenőrző Kérdések & Válaszok

### 1. Mi a különbség a `final` és a `const` között?
*   **`final`**: Olyan változó, amelynek az értéke csak egyszer adható meg (később nem módosítható), de ez az értékadás történhet futásidőben (runtime) is. Például egy hálózati hívás eredménye vagy az aktuális időpont lehet `final`.
*   **`const`**: Olyan változó, amelynek az értéke fordítási időben (compile-time) ismertnek kell lennie. Minden `const` változó implicit módon `final` is, de fordítva ez nem igaz. A `const` használatával a Flutter optimalizálja a memóriát, mert a `const widgetek` nem épülnek újjá a szülő widgetek frissülésekor.

### 2. Mit jelent a null safety?
A Dart nyelvben a Null Safety garantálja, hogy a változók alapértelmezetten nem vehetnek fel `null` értéket, hacsak azt külön nem engedélyezzük.
*   `String name = "Aliz";` -> a `name` sosem lehet null. Ha megpróbáljuk null-ra állítani, a fordító hibát jelez.
*   `String? nickname;` -> a típus végén lévő kérdőjel jelzi, hogy ez a változó lehet `null` is (nullable).
Ez megakadályozza a gyakori futásidejű hibákat, például a hírhedt "NullPointerException"-t.

### 3. Miért hasznosak a named paraméterek?
Dartban a named (nevesített) paramétereket kapcsos zárójelek `{}` közé helyezzük a függvény deklarációjakor.
*   Segítik az olvashatóságot: pl. `ContactCard(name: 'Péter', age: 30)` sokkal egyértelműbb, mint a `ContactCard('Péter', 30)`.
*   A paraméterek sorrendje tetszőleges lehet meghíváskor.
*   A paraméterek könnyen beállíthatók opcionálisra (alapértelmezett értékkel) vagy kötelezővé a `required` kulcsszóval.

### 4. Mikor használunk `List`, `Map`, `Set` típust?
*   **`List`**: Rendezett elemek gyűjteménye, ahol az elemek index alapján érhetők el. Azonos elemek többször is szerepelhetnek benne. Akkor használjuk, ha a sorrend számít (pl. egy hírcsatorna cikkei).
*   **`Map`**: Kulcs-érték (key-value) párok gyűjteménye. Minden kulcs egyedi. Akkor használjuk, ha kulcs alapján akarunk gyorsan keresni adatokat (pl. felhasználói beállítások: `'theme': 'dark'`).
*   **`Set`**: Egyedi elemek rendezetlen gyűjteménye. Nem tartalmazhat duplikációkat. Akkor használjuk, ha csak az a lényeg, hogy egy elem benne van-e a halmazban (pl. kedvenc termékek azonosítói).

### 5. Mi a különbség hot reload és hot restart között?
*   **Hot Reload**: Csak a módosított kódváltozásokat küldi el a Dart virtuális gépnek (VM). Nem építi újra a teljes alkalmazást, így a program **megtartja az aktuális állapotot** (State). Rendkívül gyors (kevesebb mint 1 másodperc). Kiváló UI finomhangolásra.
*   **Hot Restart**: Újraindítja a teljes alkalmazást és a Dart VM-et is. **Az aktuális állapot (State) elveszik** és visszaáll a kezdőhelyzetbe. Szükséges például `initState` módosításakor, globális változók vagy a `main()` függvény módosításakor.
