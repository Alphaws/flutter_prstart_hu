# 16. hét — Widget tesztek

## Cél
A lecke célja, hogy megtanuld a Flutter grafikus felületének (UI) automatizált tesztelését widget tesztek (komponenstesztek) segítségével. Megérted, hogyan építi fel a Flutter a tesztkörnyezetben a widget-fát, hogyan keress meg elemeket különböző Finder-ekkel, hogyan szimulálj felhasználói interakciókat (koppintás, gépelés, görgetés), és hogyan kezelj összetett állapotokat és függőségeket widget szinten.

---

## Elmélet

### Mi az a widget tesztelés?
A widget tesztelés (más platformokon komponens- vagy integrációs UI tesztelés) a Flutter felületének egy-egy elkülönített részét – egy gombot, egy kártyát vagy akár egy teljes képernyőt – vizsgálja. Nem futtatja le a teljes alkalmazást valódi telefonon vagy emulátoron, hanem a Flutter teszt-keretrendszerének saját "könnyűsúlyú" grafikus motorján rendereli le a widgetet memóriában. Ezáltal a widget tesztek nagyságrendekkel gyorsabbak az emulátoros UI teszteknél, miközben ellenőrzik a vizuális elrendezést és a felhasználói interakciókat.

### A WidgetTester és a pumpálás fogalma
A widget tesztben a `testWidgets()` függvényt használjuk, amely egy `WidgetTester` példányt ad át. Ez a tester objektum az átjáró a tesztelt widgetünkhöz.

Legfontosabb fogalmak:
- **`pumpWidget(Widget widget)`:** Felépíti és rendereli a megadott widget-fát a tesztkörnyezetben. Fontos, hogy a widgeteket szinte mindig be kell burkolni egy `MaterialApp` (vagy `MediaQuery`, `Directionality`) widgetbe, különben a Material komponensek nem találnak megfelelő kontextust és összeomlanak.
- **`pump(Duration? duration)`:** Kér egy új képkocka-kirajzolást (rebuild). Ha a widgetünk állapota megváltozik (például egy kattintás után), a `pump()` hívása szükséges ahhoz, hogy a felület újrarenderelődjön és láthatóvá váljon a változás.
- **`pumpAndSettle()`:** Ismételten meghívja a `pump()` függvényt egy adott ideig (alapértelmezetten 100 ezredmásodpercenként), amíg a widget-fán nincsenek folyamatban lévő animációk, áttűnések vagy mikrotaskok. Hasznos animációk, betöltő képernyők megvárásához.

> [!WARNING]
> Ha a kódunkban végtelen animáció fut (pl. egy végtelenül forgó `CircularProgressIndicator`), a `pumpAndSettle()` időtúllépési hibával (timeout) el fog szállni. Ilyenkor sima `pump(Duration)`-t kell használni fix ideig.

### Finder-ek: Elemek keresése a fán
Ahhoz, hogy ellenőrizzük egy szöveg meglétét, vagy megnyomjunk egy gombot, meg kell találnunk azt a widget-fán. Erre valók a `find` osztály metódusai:
- `find.text('Keresett szöveg')`: Szöveges tartalom alapján keres.
- `find.byType(ElevatedButton)`: A widget konkrét osztály-típusa alapján keres.
- `find.byIcon(Icons.add)`: Ikon alapján keres.
- `find.byKey(const Key('my_widget_key'))`: A widgethez rendelt egyedi kulcs (Key) alapján keres (ez a legbiztosabb módszer dinamikus felületeknél).
- `find.widgetWithText(ElevatedButton, 'Mentés')`: Olyan `ElevatedButton`-t keres, aminek a gyermekében szerepel a megadott szöveg.

### Felhasználói interakciók szimulálása
A `WidgetTester` segítségével szimulálhatjuk a fizikai interakciókat:
- `await tester.tap(Finder finder)`: Rákattint a talált elemre.
- `await tester.enterText(Finder finder, String text)`: Beírja a megadott szöveget egy beviteli mezőbe (`TextField`).
- `await tester.drag(Finder finder, Offset offset)`: Elhúzza a widgetet.

---

## Kódpéldák

Az alábbiakban egy teljes, compilable példát láthatsz egy `LoginScreen` widget tesztelésére, ahol ellenőrizzük a form validációt és a sikeres gombnyomást.

### A tesztelendő kód (`lib/ui/login_screen.dart`)

```dart
import 'package:flutter/material.dart';

class LoginScreen extends StatefulWidget {
  final void Function(String email, String password) onLoginSuccess;

  const LoginScreen({
    super.key,
    required this.onLoginSuccess,
  });

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _formKey = GlobalKey<FormState>();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();

  void _submit() {
    if (_formKey.currentState!.validate()) {
      widget.onLoginSuccess(
        _emailController.text,
        _passwordController.text,
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Bejelentkezés')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: Column(
            children: [
              TextFormField(
                key: const Key('email_field'),
                controller: _emailController,
                decoration: const InputDecoration(labelText: 'Email'),
                validator: (value) {
                  if (value == null || !value.contains('@')) {
                    return 'Érvénytelen email';
                  }
                  return null;
                },
              ),
              TextFormField(
                key: const Key('password_field'),
                controller: _passwordController,
                obscureText: true,
                decoration: const InputDecoration(labelText: 'Jelszó'),
                validator: (value) {
                  if (value == null || value.length < 6) {
                    return 'Túl rövid jelszó';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 24),
              ElevatedButton(
                key: const Key('login_button'),
                onPressed: _submit,
                child: const Text('Belépés'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
```

### A teszt kód (`test/ui/login_screen_test.dart`)

```dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_prstart_hu/ui/login_screen.dart'; // Virtuális import

void main() {
  group('LoginScreen - Widget tesztek', () {
    // Változó a callback tesztelésére
    late String capturedEmail;
    late String capturedPassword;
    late bool callbackCalled;

    setUp(() {
      capturedEmail = '';
      capturedPassword = '';
      callbackCalled = false;
    });

    // Helper a widget inicializálására MaterialApp-pal burkolva
    Widget createWidgetUnderTest() {
      return MaterialApp(
        home: LoginScreen(
          onLoginSuccess: (email, password) {
            capturedEmail = email;
            capturedPassword = password;
            callbackCalled = true;
          },
        ),
      );
    }

    testWidgets(
      'megjelennek az alapértelmezett UI elemek a képernyőn',
      (WidgetTester tester) async {
        // Renderelés
        await tester.pumpWidget(createWidgetUnderTest());

        // Assert
        expect(find.text('Bejelentkezés'), findsOneWidget);
        expect(find.byKey(const Key('email_field')), findsOneWidget);
        expect(find.byKey(const Key('password_field')), findsOneWidget);
        expect(find.byKey(const Key('login_button')), findsOneWidget);
      },
    );

    testWidgets(
      'üres mezőkkel való beküldéskor megjelennek a validációs hibaüzenetek',
      (WidgetTester tester) async {
        await tester.pumpWidget(createWidgetUnderTest());

        // Kattintás a bejelentkezés gombra
        await tester.tap(find.byKey(const Key('login_button')));
        // Rebuild kérése a hibaüzenetek kirajzolásához
        await tester.pump();

        // Assert
        expect(find.text('Érvénytelen email'), findsOneWidget);
        expect(find.text('Túl rövid jelszó'), findsOneWidget);
        expect(callbackCalled, isFalse);
      },
    );

    testWidgets(
      'helyes adatok megadásakor a callback lefut a megfelelő paraméterekkel',
      (WidgetTester tester) async {
        await tester.pumpWidget(createWidgetUnderTest());

        // Szövegek beírása a mezőkbe
        await tester.enterText(
          find.byKey(const Key('email_field')),
          'teszt@prstart.hu',
        );
        await tester.enterText(
          find.byKey(const Key('password_field')),
          'titkos123',
        );

        // Kattintás
        await tester.tap(find.byKey(const Key('login_button')));
        await tester.pump();

        // Assert
        expect(find.text('Érvénytelen email'), findsNothing);
        expect(find.text('Túl rövid jelszó'), findsNothing);
        expect(callbackCalled, isTrue);
        expect(capturedEmail, equals('teszt@prstart.hu'));
        expect(capturedPassword, equals('titkos123'));
      },
    );
  });
}
```

---

## Gyakorlófeladatok & Megoldások

### 1. feladat: Számláló (Counter) widget tesztelése
Készíts egy egyszerű számláló oldalt (`CounterWidget`), amely tartalmaz egy `Text` widgetet a számláló értékével, valamint egy `FloatingActionButton` gombot plusz ikonnal. Teszteld le, hogy a gombra kattintva az érték növekszik-e.

#### Megoldás kódja (`lib/ui/counter_widget.dart`)
```dart
import 'package:flutter/material.dart';

class CounterWidget extends StatefulWidget {
  const CounterWidget({super.key});

  @override
  State<CounterWidget> createState() => _CounterWidgetState();
}

class _CounterWidgetState extends State<CounterWidget> {
  int _counter = 0;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Text(
          'Darabszám: $_counter',
          style: const TextStyle(fontSize: 24),
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          setState(() {
            _counter++;
          });
        },
        child: const Icon(Icons.add),
      ),
    );
  }
}
```

#### Teszt kódja (`test/ui/counter_widget_test.dart`)
```dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_prstart_hu/ui/counter_widget.dart';

void main() {
  testWidgets('számláló növekedése gombnyomásra', (WidgetTester tester) async {
    // 1. Renderelés
    await tester.pumpWidget(const MaterialApp(home: CounterWidget()));

    // 2. Kezdőállapot ellenőrzése
    expect(find.text('Darabszám: 0'), findsOneWidget);
    expect(find.text('Darabszám: 1'), findsNothing);

    // 3. Gomb megnyomása
    await tester.tap(find.byType(FloatingActionButton));
    
    // 4. UI frissítése
    await tester.pump();

    // 5. Új állapot ellenőrzése
    expect(find.text('Darabszám: 0'), findsNothing);
    expect(find.text('Darabszám: 1'), findsOneWidget);
  });
}
```

---

### 2. feladat: Lista üres és betöltött állapotának tesztelése
Írj egy `TodoListView` widgetet, amely kap egy `List<String> items` paramétert és egy `isLoading` bool értéket.
- Ha `isLoading` igaz, jelenjen meg egy `CircularProgressIndicator`.
- Ha hamis és a lista üres, jelenjen meg a "Nincs teendő mára!" szöveg.
- Ha van benne elem, egy `ListView` formájában jelenítse meg őket. Teszteld le mind a három állapotot!

#### Megoldás kódja (`lib/ui/todo_list_view.dart`)
```dart
import 'package:flutter/material.dart';

class TodoListView extends StatelessWidget {
  final List<String> items;
  final bool isLoading;

  const TodoListView({
    super.key,
    required this.items,
    required this.isLoading,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: isLoading
          ? const Center(child: CircularProgressIndicator())
          : items.isEmpty
              ? const Center(child: Text('Nincs teendő mára!'))
              : ListView.builder(
                  itemCount: items.length,
                  itemBuilder: (context, index) {
                    return ListTile(
                      title: Text(items[index]),
                    );
                  },
                ),
    );
  }
}
```

#### Teszt kódja (`test/ui/todo_list_view_test.dart`)
```dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_prstart_hu/ui/todo_list_view.dart';

void main() {
  group('TodoListView - Állapot tesztek', () {
    testWidgets('betöltés alatt CircularProgressIndicator jelenik meg', (WidgetTester tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: TodoListView(items: [], isLoading: true),
        ),
      );

      expect(find.byType(CircularProgressIndicator), findsOneWidget);
      expect(find.text('Nincs teendő mára!'), findsNothing);
    });

    testWidgets('üres lista esetén a megfelelő tájékoztató szöveg látható', (WidgetTester tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: TodoListView(items: [], isLoading: false),
        ),
      );

      expect(find.byType(CircularProgressIndicator), findsNothing);
      expect(find.text('Nincs teendő mára!'), findsOneWidget);
    });

    testWidgets('ha vannak elemek, a ListView listázza azokat', (WidgetTester tester) async {
      final todos = ['Bevásárlás', 'Kódolás', 'Edzés'];

      await tester.pumpWidget(
        MaterialApp(
          home: TodoListView(items: todos, isLoading: false),
        ),
      );

      expect(find.byType(CircularProgressIndicator), findsNothing);
      expect(find.text('Nincs teendő mára!'), findsNothing);
      expect(find.byType(ListTile), findsNWidgets(3));
      expect(find.text('Bevásárlás'), findsOneWidget);
      expect(find.text('Kódolás'), findsOneWidget);
      expect(find.text('Edzés'), findsOneWidget);
    });
  });
}
```

---

## Heti Mini Projekt: UI tesztcsomag

A mini projekt feladat egy összetett webshop termékkártya widget (`ProductCard`) tesztcsomagjának elkészítése.
A kártya specifikációi:
- Megjeleníti a termék képét (`NetworkImage` helyett tesztben használjunk egyszerű helyettesítő ikont vagy `Placeholder`-t).
- Megjeleníti a nevet és az árat.
- Ha a termék akciós (`isDiscounted`), kiír egy zöld százalékos badge-et (pl. "-20%") és áthúzva mutatja az eredeti árat.
- Tartalmaz egy "Kedvenc" (`IconButton`) és egy "Kosárba" (`ElevatedButton`) gombot.
- Mindkét gomb lenyomásakor a szülő widget által átadott callback-nek le kell futnia.

### Implementáció (`lib/widgets/product_card.dart`)

```dart
import 'package:flutter/material.dart';

class ProductCard extends StatelessWidget {
  final String id;
  final String title;
  final double originalPrice;
  final double discountPercent; // pl. 0.20 a 20%-hoz
  final Void staticVoidCallback; // Kosárba gomb callback
  final void Function(bool newFavState) onFavoriteChanged;
  final bool isFavorite;

  const ProductCard({
    super.key,
    required this.id,
    required this.title,
    required this.originalPrice,
    required this.discountPercent,
    required this.staticVoidCallback,
    required this.onFavoriteChanged,
    this.isFavorite = false,
  });

  bool get isDiscounted => discountPercent > 0;
  double get discountedPrice => originalPrice * (1 - discountPercent);

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 4,
      child: Padding(
        padding: const EdgeInsets.all(12.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Placeholder(
              key: Key('product_image_placeholder'),
              fallbackHeight: 120,
            ),
            const SizedBox(height: 8),
            Text(
              title,
              style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
            ),
            const SizedBox(height: 4),
            Row(
              children: [
                if (isDiscounted) ...[
                  Text(
                    '${discountedPrice.toStringAsFixed(0)} Ft',
                    style: const TextStyle(color: Colors.red, fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(width: 8),
                  Text(
                    '${originalPrice.toStringAsFixed(0)} Ft',
                    style: const TextStyle(
                      decoration: TextDecoration.lineThrough,
                      color: Colors.grey,
                    ),
                  ),
                  const SizedBox(width: 8),
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                    decoration: BoxDecoration(
                      color: Colors.green,
                      border_radius: BorderRadius.circular(4),
                    ),
                    child: Text(
                      '-${(discountPercent * 100).toStringAsFixed(0)}%',
                      style: const TextStyle(color: Colors.white, fontSize: 12),
                    ),
                  ),
                ] else
                  Text(
                    '${originalPrice.toStringAsFixed(0)} Ft',
                    style: const TextStyle(fontWeight: FontWeight.bold),
                  ),
              ],
            ),
            const Spacer(),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                IconButton(
                  key: const Key('favorite_button'),
                  icon: Icon(
                    isFavorite ? Icons.favorite : Icons.favorite_border,
                    color: isFavorite ? Colors.red : Colors.grey,
                  ),
                  onPressed: () => onFavoriteChanged(!isFavorite),
                ),
                ElevatedButton(
                  key: const Key('add_to_cart_button'),
                  onPressed: staticVoidCallback,
                  child: const Text('Kosárba'),
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

### Tesztcsomag (`test/widgets/product_card_test.dart`)

```dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_prstart_hu/widgets/product_card.dart';

void main() {
  group('ProductCard - Összetett UI tesztcsomag', () {
    late bool cartCallbackFired;
    late bool favStatePassed;
    late bool favCallbackFired;

    setUp(() {
      cartCallbackFired = false;
      favStatePassed = false;
      favCallbackFired = false;
    });

    Widget buildTestableWidget({
      required double discount,
      required bool isFavorite,
    }) {
      return MaterialApp(
        home: Scaffold(
          body: SizedBox(
            width: 250,
            height: 300,
            child: ProductCard(
              id: 'prod-abc',
              title: 'Profi Flutter Könyv',
              originalPrice: 10000.0,
              discountPercent: discount,
              staticVoidCallback: () {
                cartCallbackFired = true;
              },
              onFavoriteChanged: (val) {
                favCallbackFired = true;
                favStatePassed = val;
              },
              isFavorite: isFavorite,
            ),
          ),
        ),
      );
    }

    testWidgets('akció nélküli normál termék helyes megjelenítése', (WidgetTester tester) async {
      await tester.pumpWidget(buildTestableWidget(discount: 0.0, isFavorite: false));

      expect(find.text('Profi Flutter Könyv'), findsOneWidget);
      expect(find.text('10000 Ft'), findsOneWidget);
      // Nincs akciós ár (ami 8000 Ft lenne)
      expect(find.text('8000 Ft'), findsNothing);
      expect(find.text('-20%'), findsNothing);

      // Kedvenc ikon üres kell legyen
      final iconButton = tester.widget<IconButton>(find.byKey(const Key('favorite_button')));
      final icon = iconButton.icon as Icon;
      expect(icon.icon, equals(Icons.favorite_border));
    });

    testWidgets('akciós termék esetén az árak és a zöld százalékos badge megjelenítése', (WidgetTester tester) async {
      await tester.pumpWidget(buildTestableWidget(discount: 0.20, isFavorite: false));

      expect(find.text('Profi Flutter Könyv'), findsOneWidget);
      // Megjelenik a kedvezményes ár
      expect(find.text('8000 Ft'), findsOneWidget);
      // Megjelenik az áthúzott eredeti ár is
      expect(find.text('10000 Ft'), findsOneWidget);
      expect(find.text('-20%'), findsOneWidget);
    });

    testWidgets('a Kosárba gombra kattintva lefut a hozzá tartozó callback', (WidgetTester tester) async {
      await tester.pumpWidget(buildTestableWidget(discount: 0.0, isFavorite: false));

      await tester.tap(find.byKey(const Key('add_to_cart_button')));
      await tester.pump();

      expect(cartCallbackFired, isTrue);
    });

    testWidgets('kedvenc gomb működése: ha hamis volt, igaz értékkel hívja meg a callback-et', (WidgetTester tester) async {
      await tester.pumpWidget(buildTestableWidget(discount: 0.0, isFavorite: false));

      // Első állapot ellenőrzése
      final iconButtonBefore = tester.widget<IconButton>(find.byKey(const Key('favorite_button')));
      expect((iconButtonBefore.icon as Icon).icon, equals(Icons.favorite_border));

      // Kattintás
      await tester.tap(find.byKey(const Key('favorite_button')));
      await tester.pump();

      expect(favCallbackFired, isTrue);
      expect(favStatePassed, isTrue); // A megváltozott új értéknek igaznak kell lennie
    });

    testWidgets('kedvenc gomb működése: ha igaz volt, kedvenc ikon és hamis callback paraméter', (WidgetTester tester) async {
      await tester.pumpWidget(buildTestableWidget(discount: 0.0, isFavorite: true));

      final iconButtonBefore = tester.widget<IconButton>(find.byKey(const Key('favorite_button')));
      expect((iconButtonBefore.icon as Icon).icon, equals(Icons.favorite));

      await tester.tap(find.byKey(const Key('favorite_button')));
      await tester.pump();

      expect(favCallbackFired, isTrue);
      expect(favStatePassed, isFalse); // Új állapot hamis
    });
  });
}
```

---

## Heti Ellenőrző Kérdések

### 1. Mi a különbség a tester.pump() és a tester.pumpAndSettle() között?
- A `tester.pump()` pontosan egy képkocka (frame) újrarajzolását végzi el. Akkor használjuk, ha egyazon pillanatban végbemenő UI változást (pl. egy egyszerű `setState` utáni gomb felirat módosulást) akarunk érvényesíteni.
- A `tester.pumpAndSettle()` addig pumpálja az új képkockákat (maximum 10 percig), amíg az összes animáció, áttűnés vagy aszinkron feladat be nem fejeződik és a felület teljesen nyugalmi állapotba nem kerül.

### 2. Hogyan tudjuk a hálózati képeket (Image.network) widget tesztben renderelni?
A widget teszt környezetben nincs valós internetkapcsolat, így a `Image.network` vagy a `CachedNetworkImage` hibát dobna a kép letöltésekor. Két megoldás létezik:
1. A tesztben a képet egy `Placeholder` widgettel vagy mock ikonnal helyettesítjük.
2. A `flutter_test` könyvtár lehetőséget ad egy egyedi HTTP kliens (`MockHttpClient`) beállítására, amely lemezképként (pl. egy üres 1x1 pixeles átlátszó GIF-ként) válaszol minden hálózati kérésre, megakadályozva az összeomlást.

### 3. Mire való a Key és hogyan segít a widgetek megkeresésében a tesztek során?
A `Key` (különösen a `ValueKey` vagy `Key`) egyedi azonosítóként szolgál a widgetekhez. A teszt kódjában a `find.byKey(const Key('egyedi_kulcs'))` segítségével pontosan meg tudunk találni egy elemet a fán, függetlenül attól, hogy a szövege vagy az ikonja megváltozott-e. Ez teszi a teszteket ellenállóvá a dizájn- és szövegmódosításokkal szemben.

### 4. Hogyan tudunk aszinkron eseményeket szimulálni widget tesztben?
A widget tesztekben a `WidgetTester` beépített virtuális időt (fake async) használ. Az aszinkron feladatok befejeződését és a jövőbeli értékek felületre jutását a `await tester.pump()` meghívásával tudjuk szimulálni. Ha hosszabb aszinkron várakozást szimulálunk (pl. egy `Future.delayed` hívást), a `await tester.pump(const Duration(seconds: 2))` használható az idő előreléptetésére.

### 5. Miért fontos a MaterialApp burkolás a pumpWidget hívásakor?
A Flutter Material widgetjei (mint a `Scaffold`, `TextField`, `Card`, `ElevatedButton`) megkövetelik a szülő kontextustól a Material Design témák, irányultságok (`Directionality`), méret-arányok és egyéb alapértelmezett beállítások meglétét. A `MaterialApp` biztosítja ezeket a globális szolgáltatásokat (Theme, Navigator, Media Query). Burkolás nélkül a Material widgetek renderelése azonnali hibát dob a tesztben.
