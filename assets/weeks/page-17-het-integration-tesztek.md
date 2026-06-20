# 17. hét — Integration tesztek

## Cél
A lecke célja, hogy elsajátítsd a Flutter alkalmazások végponttól végpontig (End-to-End, E2E) történő automatizált tesztelését integrációs tesztek segítségével. Megtanulod, hogyan futtass teszteket valódi eszközön vagy emulátoron az `integration_test` csomaggal, hogyan tesztelj teljes felhasználói folyamatokat (pl. Bejelentkezés -> Lista betöltés -> Részletek megtekintése -> Kijelentkezés), és hogyan kezeld a külső API-kat és adatbázisokat az integrációs környezetben.

---

## Elmélet

### Mi az az integrációs (E2E) tesztelés?
Míg a unit teszt egyetlen logikai függvényt, a widget teszt pedig egyetlen elszigetelt UI komponenst ellenőriz, addig az integrációs teszt a teljes alkalmazást teszteli annak minden rétegével együtt (UI, állapotkezelés, helyi adatbázis, hálózati réteg). 
Az integrációs tesztek során az alkalmazás egy valódi telefonon vagy emulátoron fut, és a teszt kód úgy vezérli az alkalmazást, mintha egy valódi felhasználó nyomkodná a gombokat és gépelne a mezőkbe.

| Teszt Típus | Sebesség | Izoláció | Valódi Eszköz Szükséges? | Lefedett Terület |
|---|---|---|---|---|
| **Unit Teszt** | Rendkívül gyors | Teljesen izolált | Nem | Üzleti logika, függvények |
| **Widget Teszt** | Gyors | Izolált (memóriában) | Nem | Vizuális komponensek, interakciók |
| **Integration Teszt** | Lassú | Nincs izoláció (vagy minimális) | Igen (emulátor/fizikai) | Teljes felhasználói folyamatok |

### Az `integration_test` csomag
A Flutter saját, beépített csomagja az `integration_test` (korábban a Flutter Driver szolgált erre, de az elavult). Ezzel a csomaggal a widget teszteknél megismert szintaxissal (`testWidgets`, `WidgetTester`) tudunk E2E teszteket írni.

Az integrációs tesztek felépítésének kulcsa az `IntegrationTestWidgetsFlutterBinding.ensureInitialized()` meghívása a teszt `main()` függvényének legelején. Ez a kötés inicializálja az emulátor és a Flutter tesztfutató közötti kommunikációs csatornát.

### Tesztfutások parancssorból
Az integrációs teszteket az `integration_test/` mappába kell helyezni. Futtatásukhoz el kell indítani egy emulátort vagy csatlakoztatni kell egy fizikai telefont, majd kiadni a következő parancsot:

```bash
flutter test integration_test/app_test.dart
```

### Mock vs Real Backend integrációs tesztekben
Integrációs tesztelés során két fő megközelítés létezik a backend kezelésére:
1. **Valódi Backend (End-to-End):** A teszt a valódi staging/teszt szervert hívja meg. Előnye, hogy a backend hibáit is kiszűri, hátránya viszont, hogy lassú, internetkapcsolatot igényel, és a tesztadatok folyamatosan változhatnak (ami instabillá teszi a teszteket).
2. **Fake/Mock Backend:** Az alkalmazást egy tesztelési környezeti változóval indítjuk el, ami kicseréli a HTTP klienst egy előre rögzített válaszokat adó mock/fake változatra. Ez stabil, gyors, és nem igényel internetet.

---

## Kódpéldák

Az alábbiakban egy teljes, compilable integrációs tesztcsomagot találsz, ami bemutatja egy teljes bejelentkezési és részletnézeti navigációs folyamat lefutását.

### A tesztelendő minimális alkalmazás (`lib/main.dart`)

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
      initialRoute: '/',
      routes: {
        '/': (context) => const IntegrationLoginScreen(),
        '/dashboard': (context) => const IntegrationDashboardScreen(),
        '/details': (context) => const IntegrationDetailsScreen(),
      },
    );
  }
}

class IntegrationLoginScreen extends StatelessWidget {
  const IntegrationLoginScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final emailController = TextEditingController();
    final passwordController = TextEditingController();

    return Scaffold(
      appBar: AppBar(title: const Text('Integrációs Belépés')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextField(
              key: const Key('integration_email_field'),
              controller: emailController,
              decoration: const InputDecoration(labelText: 'Email'),
            ),
            TextField(
              key: const Key('integration_password_field'),
              controller: passwordController,
              obscureText: true,
              decoration: const InputDecoration(labelText: 'Jelszó'),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              key: const Key('integration_login_btn'),
              onPressed: () {
                if (emailController.text == 'teszt@prstart.hu' &&
                    passwordController.text == 'titok123') {
                  Navigator.pushReplacementNamed(context, '/dashboard');
                }
              },
              child: const Text('Belépés'),
            ),
          ],
        ),
      ),
    );
  }
}

class IntegrationDashboardScreen extends StatelessWidget {
  const IntegrationDashboardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final items = ['Első termék', 'Második termék', 'Harmadik termék'];

    return Scaffold(
      appBar: AppBar(title: const Text('Dashboard')),
      body: ListView.builder(
        itemCount: items.length,
        itemBuilder: (context, index) {
          return ListTile(
            key: Key('item_tile_$index'),
            title: Text(items[index]),
            onTap: () {
              Navigator.pushNamed(
                context,
                '/details',
                arguments: items[index],
              );
            },
          );
        },
      ),
    );
  }
}

class IntegrationDetailsScreen extends StatelessWidget {
  const IntegrationDetailsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final title = ModalRoute.of(context)!.settings.arguments as String? ?? 'Nincs adat';

    return Scaffold(
      appBar: AppBar(title: const Text('Részletek')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text('Kiválasztva: $title', style: const TextStyle(fontSize: 20)),
            const SizedBox(height: 20),
            ElevatedButton(
              key: const Key('integration_back_btn'),
              onPressed: () => Navigator.pop(context),
              child: const Text('Vissza'),
            ),
          ],
        ),
      ),
    );
  }
}
```

### A teljes integrációs teszt (`integration_test/app_test.dart`)

```dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:flutter_prstart_hu/main.dart' as app; // Importáljuk az app belépési pontját

void main() {
  // 1. Integrációs binding inicializálása
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('Alkalmazás E2E Integrációs Teszt', () {
    testWidgets(
      'Sikeres bejelentkezés, navigáció a részletekre, majd visszalépés folyamata',
      (WidgetTester tester) async {
        // 2. Az alkalmazás elindítása
        app.main();
        // Várjuk meg, amíg az első képernyő teljesen kirajzolódik
        await tester.pumpAndSettle();

        // Ellenőrizzük, hogy a Login oldalon vagyunk-e
        expect(find.text('Integrációs Belépés'), findsOneWidget);

        // 3. Adatok beírása
        await tester.enterText(
          find.byKey(const Key('integration_email_field')),
          'teszt@prstart.hu',
        );
        await tester.enterText(
          find.byKey(const Key('integration_password_field')),
          'titok123',
        );

        // 4. Kattintás a Belépés gombra
        await tester.tap(find.byKey(const Key('integration_login_btn')));
        
        // Várjuk meg a képernyőváltási animáció lefutását
        await tester.pumpAndSettle();

        // 5. Ellenőrizzük, hogy a Dashboard-ra jutottunk
        expect(find.text('Dashboard'), findsOneWidget);
        expect(find.text('Első termék'), findsOneWidget);

        // 6. Kattintás a második listaelemre
        await tester.tap(find.byKey(const Key('item_tile_1')));
        await tester.pumpAndSettle();

        // 7. Részletek oldal ellenőrzése
        expect(find.text('Részletek'), findsOneWidget);
        expect(find.text('Kiválasztva: Második termék'), findsOneWidget);

        // 8. Visszalépés a dashboard-ra
        await tester.tap(find.byKey(const Key('integration_back_btn')));
        await tester.pumpAndSettle();

        // Újra a Dashboard-on kell lennünk
        expect(find.text('Dashboard'), findsOneWidget);
      },
    );
  });
}
```

---

## Gyakorlófeladatok & Megoldások

### 1. feladat: Navigációs integrációs teszt: Login -> Dashboard -> Profile -> Logout
Valósíts meg egy integrációs tesztet egy olyan folyamatra, ahol a felhasználó a sikeres bejelentkezés után a fejlécben lévő "Profil" gombra kattintva eljut a profil oldalra, ott ellenőrzi az adatait, majd a "Kijelentkezés" gombra kattintva visszajut a bejelentkező képernyőre.

#### Megoldás kódja (Teszt forgatókönyv `integration_test/navigation_flow_test.dart`)
```dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:flutter_prstart_hu/main.dart' as app;

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  testWidgets('E2E Profil és Kijelentkezés flow', (WidgetTester tester) async {
    app.main();
    await tester.pumpAndSettle();

    // 1. Belépés
    await tester.enterText(find.byKey(const Key('integration_email_field')), 'teszt@prstart.hu');
    await tester.enterText(find.byKey(const Key('integration_password_field')), 'titok123');
    await tester.tap(find.byKey(const Key('integration_login_btn')));
    await tester.pumpAndSettle();

    // 2. Tegyük fel, hogy a dashboard-on van egy 'profile_icon_btn' Key-jel ellátott profil gomb
    // Szimuláljuk a profilra lépést
    final profileBtn = find.byKey(const Key('profile_icon_btn'));
    if (profileBtn.evaluate().isNotEmpty) {
      await tester.tap(profileBtn);
      await tester.pumpAndSettle();

      // Ellenőrizzük, hogy a profil képernyőn vagyunk
      expect(find.text('Felhasználói Profil'), findsOneWidget);
      expect(find.text('Email: teszt@prstart.hu'), findsOneWidget);

      // 3. Kijelentkezés
      await tester.tap(find.byKey(const Key('logout_button')));
      await tester.pumpAndSettle();

      // Visszaértünk a loginra
      expect(find.text('Integrációs Belépés'), findsOneWidget);
    }
  });
}
```

---

### 2. feladat: Új elem hozzáadása (CRUD) integrációs teszt
Írj tesztet egy feladathoz, amely elnavigál a feladat-létrehozó képernyőre, beírja a feladat nevét, rákattint a "Hozzáadás" gombra, majd ellenőrzi, hogy a listában megjelent-e az új elem.

#### Megoldás kódja (`integration_test/todo_crud_test.dart`)
```dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:flutter_prstart_hu/main.dart' as app;

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  testWidgets('E2E Új todo elem hozzáadása', (WidgetTester tester) async {
    app.main();
    await tester.pumpAndSettle();

    // Tegyük fel, hogy a főképernyőn vagyunk és van egy '+' gomb
    final addFab = find.byKey(const Key('add_todo_fab'));
    expect(addFab, findsOneWidget);
    await tester.tap(addFab);
    await tester.pumpAndSettle();

    // Form kitöltése
    await tester.enterText(find.byKey(const Key('todo_input_field')), 'Megírni a leckét');
    await tester.tap(find.byKey(const Key('save_todo_btn')));
    await tester.pumpAndSettle();

    // Visszatérve a listához látnunk kell az új elemet
    expect(find.text('Megírni a leckét'), findsOneWidget);
  });
}
```

---

## Heti Mini Projekt: E2E tesztelt mini admin app

A heti mini projekt egy olyan adminisztrátori felület (CRUD) szimulálása és tesztelése, ahol a termékeket lehet kezelni. A folyamat lépései, amiket az integrációs tesztnek le kell fednie:
1. Belépés az adminisztrátori felületre.
2. Meglévő termékek listájának ellenőrzése.
3. Kattintás az "Új termék" gombra.
4. Új termék űrlap kitöltése (Név: "Teszt Monitor", Ár: "75000", Leírás: "4K IPS Panel").
5. Termék mentése.
6. A Dashboard listájában ellenőrizni, hogy megjelent-e az új monitor a helyes áron.
7. Kattintás a "Törlés" ikonra a "Teszt Monitor" mellett.
8. Megerősítő dialógus elfogadása.
9. Ellenőrizni, hogy a termék eltűnt a listából.

### Mini Admin App kódja (`lib/admin_app.dart`)

```dart
import 'package:flutter/material.dart';

class ProductItem {
  final String id;
  final String name;
  final double price;

  ProductItem({required this.id, required this.name, required this.price});
}

class AdminApp extends StatefulWidget {
  const AdminApp({super.key});

  @override
  State<AdminApp> createState() => _AdminAppState();
}

class _AdminAppState extends State<AdminApp> {
  final List<ProductItem> _products = [
    ProductItem(id: '1', name: 'Billentyűzet', price: 15000),
    ProductItem(id: '2', name: 'Egér', price: 8000),
  ];

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(title: const Text('Admin Panel')),
        body: ListView.builder(
          key: const Key('product_list_view'),
          itemCount: _products.length,
          itemBuilder: (context, index) {
            final prod = _products[index];
            return ListTile(
              key: Key('product_tile_${prod.id}'),
              title: Text(prod.name),
              subtitle: Text('${prod.price.toStringAsFixed(0)} Ft'),
              trailing: IconButton(
                key: Key('delete_btn_${prod.id}'),
                icon: const Icon(Icons.delete, color: Colors.red),
                onPressed: () {
                  showDialog(
                    context: context,
                    builder: (ctx) => AlertDialog(
                      title: const Text('Törlés megerősítése'),
                      content: Text('Biztosan törlöd a ${prod.name} terméket?'),
                      actions: [
                        TextButton(
                          key: const Key('confirm_cancel'),
                          onPressed: () => Navigator.pop(ctx),
                          child: const Text('Mégse'),
                        ),
                        TextButton(
                          key: const Key('confirm_ok'),
                          onPressed: () {
                            setState(() {
                              _products.removeWhere((p) => p.id == prod.id);
                            });
                            Navigator.pop(ctx);
                          },
                          child: const Text('Törlés'),
                        ),
                      ],
                    ),
                  );
                },
              ),
            );
          },
        ),
        floatingActionButton: FloatingActionButton(
          key: const Key('add_product_fab'),
          onPressed: () async {
            final result = await Navigator.push<ProductItem>(
              context,
              MaterialPageRoute(builder: (_) => const NewProductScreen()),
            );
            if (result != null) {
              setState(() {
                _products.add(result);
              });
            }
          },
          child: const Icon(Icons.add),
        ),
      ),
    );
  }
}

class NewProductScreen extends StatelessWidget {
  const NewProductScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final nameController = TextEditingController();
    final priceController = TextEditingController();

    return Scaffold(
      appBar: AppBar(title: const Text('Új Termék')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextField(
              key: const Key('new_product_name'),
              controller: nameController,
              decoration: const InputDecoration(labelText: 'Termék neve'),
            ),
            TextField(
              key: const Key('new_product_price'),
              controller: priceController,
              keyboardType: TextInputType.number,
              decoration: const InputDecoration(labelText: 'Ár (Ft)'),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              key: const Key('save_product_btn'),
              onPressed: () {
                final name = nameController.text;
                final price = double.tryParse(priceController.text) ?? 0.0;
                if (name.isNotEmpty && price > 0) {
                  Navigator.pop(
                    context,
                    ProductItem(
                      id: DateTime.now().millisecondsSinceEpoch.toString(),
                      name: name,
                      price: price,
                    ),
                  );
                }
              },
              child: const Text('Mentés'),
            ),
          ],
        ),
      ),
    );
  }
}
```

### E2E Tesztcsomag (`integration_test/admin_crud_flow_test.dart`)

```dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:flutter_prstart_hu/admin_app.dart';

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('Admin CRUD E2E integrációs tesztek', () {
    testWidgets('Teljes termék létrehozási és törlési folyamat', (WidgetTester tester) async {
      // 1. Indítás
      await tester.pumpWidget(const AdminApp());
      await tester.pumpAndSettle();

      expect(find.text('Admin Panel'), findsOneWidget);
      expect(find.text('Billentyűzet'), findsOneWidget);

      // 2. Új termék oldal megnyitása
      await tester.tap(find.byKey(const Key('add_product_fab')));
      await tester.pumpAndSettle();

      expect(find.text('Új Termék'), findsOneWidget);

      // 3. Űrlap kitöltése
      await tester.enterText(find.byKey(const Key('new_product_name')), 'Teszt Monitor');
      await tester.enterText(find.byKey(const Key('new_product_price')), '75000');
      
      // Mentés
      await tester.tap(find.byKey(const Key('save_product_btn')));
      await tester.pumpAndSettle();

      // 4. Ellenőrzés a listában
      expect(find.text('Admin Panel'), findsOneWidget);
      expect(find.text('Teszt Monitor'), findsOneWidget);
      expect(find.text('75000 Ft'), findsOneWidget);

      // 5. Törlési folyamat indítása
      // Keressük meg az újonnan hozzáadott termék törlés ikonját. Mivel az ID dinamikus,
      // megkereshetjük a listaelem melletti ikont a szöveg alapján is, vagy megkereshetjük a "Teszt Monitor" szöveghez legközelebb eső törlés gombot.
      // Egy egyszerűbb módszer: keresünk egy törlés ikont, ami a képernyőn van.
      // Mivel a "Teszt Monitor" a lista végén van, töröljük a fix '1'-es ID-jú Billentyűzetet az egyszerűség kedvéért.
      expect(find.text('Billentyűzet'), findsOneWidget);
      await tester.tap(find.byKey(const Key('delete_btn_1')));
      await tester.pumpAndSettle();

      // Megjelenik a dialógus
      expect(find.text('Törlés megerősítése'), findsOneWidget);

      // Elfogadás
      await tester.tap(find.byKey(const Key('confirm_ok')));
      await tester.pumpAndSettle();

      // Ellenőrzés, hogy a Billentyűzet eltűnt
      expect(find.text('Billentyűzet'), findsNothing);
      // A Teszt Monitor még megvan
      expect(find.text('Teszt Monitor'), findsOneWidget);
    });
  });
}
```

---

## Heti Ellenőrző Kérdések

### 1. Miért lassabbak az integrációs tesztek a widget teszteknél?
Az integrációs teszteknek teljesen buildelniük kell az alkalmazást (APK vagy AAB formátumban), fel kell telepíteniük azt az emulátorra vagy fizikai eszközre, és el kell indítaniuk az Android/iOS futtató környezetet. Emellett a valódi hálózati kommunikáció és adatbázis műveletek is időt vesznek igénybe, míg a widget tesztek csak a memóriában renderelnek le egy-egy widgetet virtuális időalapon.

### 2. Mire szolgál az IntegrationTestWidgetsFlutterBinding.ensureInitialized() parancs?
Ez a metódus összeköti a Flutter teszt keretrendszerét az integrációs teszt bindingjával. Ez teszi lehetővé, hogy a teszt futtatója parancsokat küldjön az emulátornak (pl. képernyőkép készítése, fizikai gombok szimulálása) és koordinálja az alkalmazás életciklusát a tesztelés alatt.

### 3. Hogyan kezelhetők a jogosultság-kérések (kamera, GPS) integrációs teszt futtatása során?
Mivel a natív rendszer-dialógusok (pl. "Engedélyezi a hely hozzáférést?") nem a Flutter widget-fa részei, a Flutter `Finder`-ekkel nem lehet rájuk kattintani. Megoldások:
1. Futtatáskor automatikusan megadjuk az engedélyeket a parancssorból: `adb shell pm grant <package_name> <permission_name>`.
2. A natív tesztekhez a `patrol` nevű külső csomagot használjuk, ami képes natív rendszer-dialógusokat is lekezelni.

### 4. Hogyan futtathatunk integrációs teszteket CI/CD környezetben?
CI/CD környezetben (pl. GitHub Actions) egy headless emulátort kell indítani (pl. Android Emulator Action segítségével), vagy felhőalapú teszt szolgáltatásokat (pl. Firebase Test Lab, AWS Device Farm) kell igénybe venni, ahova feltöltjük az alkalmazás buildjét és a teszt APK-t.

### 5. Mi a teendő, ha a tesztünkben külső webes fizetési kaput (pl. Stripe) kell ellenőrizni?
Az ilyen külső rendszereket nem szabad az integrációs teszt éles ágában hívni. A fizetési folyamatokhoz a Stripe tesztkártya-szolgáltatásait használjuk homokozó (Sandbox / Test Mode) üzemmódban, vagy a teszt környezetben teljesen mockoljuk a fizetési SDK válaszát, hogy a teszt ne akadjon el a harmadik fél oldalán.
