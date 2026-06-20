# Flutter mobilfejlesztés profi módon — teljes tananyag nulláról

**Készítve:** 2026-06-20  
**Cél:** Flutter mobilfejlesztés megtanulása kezdő szintről professzionális, munkaképes szintig.  
**Ajánlott tempó:** heti 5 nap, napi 1–2 óra gyakorlás; hétvégén projektmunka vagy ismétlés.  
**Fő platform:** Android. iOS is szerepel, de iOS buildhez macOS és Apple Developer fiók szükséges.  
**Előfeltétel:** programozási alapok előny, de a tananyag nulláról indul.  

---

## 0. Mit fogsz tudni a tananyag végére?

A tananyag végére képes leszel:

- Flutter projektet létrehozni, strukturálni és karbantartani.
- Dart nyelven tiszta, null-safe, modern kódot írni.
- Reszponzív, szép, többképernyős mobilalkalmazásokat készíteni.
- API-kat fogyasztani, hibákat kezelni, betöltési állapotokat megjeleníteni.
- Helyi adatbázist és offline működést használni.
- State management megoldásokat érteni és tudatosan választani.
- Profi architektúrában gondolkodni: UI, application/business logic, data layer.
- Autentikációt, jogosultságkezelést és biztonsági alapokat alkalmazni.
- Unit, widget és integration teszteket írni.
- Android release buildet készíteni, aláírni és publikálásra előkészíteni.
- CI/CD pipeline-t építeni GitHub Actions-szel.
- Portfólióképes Flutter alkalmazást elkészíteni.

---

## 1. Tanulási stratégia

A Fluttert nem érdemes csak videók nézésével tanulni. A hatékony út:

1. **Olvasd el a leckét.**
2. **Írd be kézzel a példakódot.**
3. **Módosíts rajta.**
4. **Készíts mini-feladatot.**
5. **Hetente építs egy kis projektet.**
6. **Minden hónap végén készíts egy nagyobb projektet.**
7. **Dokumentáld GitHubon.**

A cél nem az, hogy “ismerd” a Fluttert, hanem hogy tudd használni valós problémákra.

---

## 2. Tanulási időterv áttekintése

| Szakasz | Időtartam | Fókusz |
|---|---:|---|
| 1. Alapozás | 1–2. hét | Dart, fejlesztői környezet, Flutter alapok |
| 2. UI és navigáció | 3–5. hét | Widgetek, layout, többképernyős appok |
| 3. Adat és állapot | 6–9. hét | State management, API, async, JSON |
| 4. Profi app alapok | 10–14. hét | Architektúra, lokális DB, auth, offline működés |
| 5. Tesztelés és minőség | 15–18. hét | Unit/widget/integration tesztek, lint, hibakezelés |
| 6. Haladó Flutter | 19–22. hét | Animáció, platform channel, performance, native funkciók |
| 7. Publikálás és portfólió | 23–24. hét | Release, CI/CD, Play Store, záróprojekt |

---

# I. SZAKASZ — Alapozás

---

## 1. hét — Fejlesztői környezet és Dart alapok

### Cél

Megérteni, hogy mi a Flutter, mi a Dart szerepe, hogyan épül fel egy projekt, és hogyan futtatunk alkalmazást emulátoron vagy valódi telefonon.

### Tananyag

#### 1.1 Flutter fogalma

A Flutter egy Google által fejlesztett, nyílt forrású UI SDK, amellyel egy kódbázisból lehet alkalmazást készíteni Androidra, iOS-re, webre és desktopra.

Fontos fogalmak:

- **Flutter SDK**
- **Dart nyelv**
- **Widget**
- **Hot reload**
- **Hot restart**
- **Material Design**
- **Cupertino widgetek**
- **pub.dev csomagkezelés**

#### 1.2 Szükséges eszközök

Telepítendő:

- Flutter SDK
- Dart SDK, a Flutterrel együtt jön
- Android Studio
- Android SDK
- VS Code vagy Android Studio
- Flutter és Dart plugin
- Git
- Java JDK
- fizikai Android telefon vagy emulátor

#### 1.3 Ellenőrző parancsok

```bash
flutter doctor
flutter --version
dart --version
flutter devices
```

#### 1.4 Első projekt

```bash
flutter create hello_flutter
cd hello_flutter
flutter run
```

#### 1.5 Dart alapok

Tanulandó:

- változók: `var`, `final`, `const`
- típusok: `int`, `double`, `String`, `bool`
- lista, map, set
- függvények
- osztályok
- konstruktorok
- named parameters
- optional parameters
- null safety
- enum
- extension
- records
- pattern matching alapok

### Gyakorlófeladatok

1. Írj Dart programot, amely kiszámolja egy kosár végösszegét.
2. Készíts `Product` osztályt névvel, árral, készlettel.
3. Készíts `User` osztályt opcionális telefonszámmal.
4. Készíts listát termékekből, majd szűrd azokat, amelyek ára nagyobb mint 5000 Ft.
5. Készíts függvényt, amely kedvezményt számol.

### Mini projekt

**Kosár kalkulátor konzolos Dartban**

Funkciók:

- terméklista
- kosárba tétel
- összegzés
- kedvezmény
- ÁFA számítás
- hibás adat kezelése

### Heti ellenőrző kérdések

- Mi a különbség a `final` és a `const` között?
- Mit jelent a null safety?
- Miért hasznosak a named paraméterek?
- Mikor használunk `List`, `Map`, `Set` típust?
- Mi a különbség hot reload és hot restart között?

---

## 2. hét — Flutter alapok és widget gondolkodás

### Cél

Megérteni, hogy Flutterben minden UI elem widget, és hogyan épül fel egy egyszerű képernyő.

### Tananyag

#### 2.1 Projektstruktúra

Alapmappák:

```text
lib/
  main.dart
android/
ios/
web/
test/
pubspec.yaml
```

Fontos fájl:

```yaml
pubspec.yaml
```

Itt kezeljük:

- app nevét
- verziót
- függőségeket
- asseteket
- fontokat

#### 2.2 Alap widgetek

Tanulandó:

- `MaterialApp`
- `Scaffold`
- `AppBar`
- `Text`
- `Icon`
- `Image`
- `Container`
- `Column`
- `Row`
- `Stack`
- `ListView`
- `GridView`
- `Card`
- `ElevatedButton`
- `TextButton`
- `IconButton`
- `TextField`

#### 2.3 StatelessWidget és StatefulWidget

**StatelessWidget:** nincs belső változó állapota.  
**StatefulWidget:** képes változó állapotot tárolni.

Példa:

```dart
class CounterPage extends StatefulWidget {
  const CounterPage({super.key});

  @override
  State<CounterPage> createState() => _CounterPageState();
}

class _CounterPageState extends State<CounterPage> {
  int counter = 0;

  void increment() {
    setState(() {
      counter++;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Számláló')),
      body: Center(child: Text('Érték: $counter')),
      floatingActionButton: FloatingActionButton(
        onPressed: increment,
        child: const Icon(Icons.add),
      ),
    );
  }
}
```

### Gyakorlófeladatok

1. Készíts névjegykártya képernyőt.
2. Készíts számláló appot.
3. Készíts egyszerű bevásárlólista képernyőt.
4. Készíts profil képernyőt képpel, névvel, adatokkal.
5. Készíts gombot, amely megváltoztatja a háttérszöveget.

### Mini projekt

**Napi teendők app — csak memóriában**

Funkciók:

- teendő hozzáadása
- teendő törlése
- kész/nem kész állapot
- üres lista állapot
- egyszerű design

---

# II. SZAKASZ — UI, layout, navigáció

---

## 3. hét — Layout mélyebben

### Cél

Megtanulni reszponzív és jól strukturált felületeket készíteni.

### Tananyag

#### 3.1 Layout alapelvek

Flutter layout gondolkodás:

- a parent constraintet ad
- a child méretet választ
- a parent pozicionál

Tanulandó widgetek:

- `Expanded`
- `Flexible`
- `Spacer`
- `Padding`
- `Align`
- `Center`
- `SizedBox`
- `AspectRatio`
- `Wrap`
- `LayoutBuilder`
- `MediaQuery`
- `SafeArea`

#### 3.2 Gyakori hibák

- `Column` belsejében végtelen magasságú `ListView`
- overflow hiba
- rosszul használt `Expanded`
- túl nagy widgetfa
- hardcoded méretek
- ismétlődő UI-kód

#### 3.3 Reszponzív gondolkodás

Mobilon:

- kis kijelző
- billentyűzet megjelenése
- portrait/landscape
- notch és system bar
- nagy betűméret hozzáférhetőség miatt

### Gyakorlófeladatok

1. Készíts login képernyőt.
2. Készíts termékkártyát.
3. Készíts dashboard képernyőt.
4. Készíts kétoszlopos tablet layoutot `LayoutBuilder` segítségével.
5. Készíts lista + részletező nézetet.

### Mini projekt

**Mobil webshop katalógus UI**

Funkciók:

- terméklista
- termékkártya
- keresősáv
- kategória chip-ek
- termék részletező képernyő
- reszponzív layout

---

## 4. hét — Navigáció és route-ok

### Cél

Többképernyős alkalmazások készítése, argumentumátadás, visszalépés, tabos navigáció.

### Tananyag

#### 4.1 Alap navigáció

```dart
Navigator.push(
  context,
  MaterialPageRoute(
    builder: (context) => const DetailsPage(),
  ),
);
```

#### 4.2 Visszatérés adattal

```dart
final result = await Navigator.push(
  context,
  MaterialPageRoute(builder: (_) => const SelectPage()),
);
```

#### 4.3 Named routes

```dart
MaterialApp(
  routes: {
    '/': (_) => const HomePage(),
    '/details': (_) => const DetailsPage(),
  },
);
```

#### 4.4 Haladó routing

Profi appoknál gyakran használt csomag:

- `go_router`

Tanulandó:

- nested routes
- shell route
- auth guard
- deep link
- route parameter
- query parameter

#### 4.5 Alsó navigáció

Widgetek:

- `BottomNavigationBar`
- `NavigationBar`
- `NavigationRail`
- `TabBar`
- `TabBarView`

### Gyakorlófeladatok

1. Home → Details navigáció.
2. Listaelemről részletező oldal.
3. Login után dashboard.
4. Bottom navigation 3 tabbal.
5. Route paraméter alapján termék megnyitása.

### Mini projekt

**Recept app navigációval**

Funkciók:

- főoldal
- receptlista
- recept részletek
- kedvencek tab
- profil tab
- route paraméterezés

---

## 5. hét — Design, theme, assetek

### Cél

Szép, egységes, modern mobil UI készítése.

### Tananyag

#### 5.1 ThemeData

Tanulandó:

- color scheme
- typography
- button theme
- input decoration theme
- card theme
- dark mode
- light mode

#### 5.2 Assetek

```yaml
flutter:
  assets:
    - assets/images/
```

#### 5.3 Fontok

```yaml
flutter:
  fonts:
    - family: Inter
      fonts:
        - asset: assets/fonts/Inter-Regular.ttf
```

#### 5.4 Design rendszer

Profi appban legyen:

- színpaletta
- tipográfia
- spacing rendszer
- gombstílusok
- input stílusok
- ikonhasználat
- loading state
- empty state
- error state

### Gyakorlófeladatok

1. Készíts saját theme fájlt.
2. Készíts reusable `PrimaryButton` widgetet.
3. Készíts reusable `AppTextField` widgetet.
4. Készíts light/dark mode váltást.
5. Készíts üres állapot komponenst.

### Mini projekt

**Saját UI kit Flutterben**

Komponensek:

- gombok
- inputok
- kártyák
- badge-ek
- loading indicator
- error box
- empty state
- app shell

---

# III. SZAKASZ — Adat, állapot, API

---

## 6. hét — State management alapok

### Cél

Megérteni, mi az állapot, miért nem elég mindenre a `setState`, és hogyan kezelünk app-szintű adatokat.

### Tananyag

#### 6.1 Mi az állapot?

Példák állapotra:

- bejelentkezett felhasználó
- kosár tartalma
- kiválasztott téma
- API betöltés státusza
- űrlap validáció
- offline/online állapot

#### 6.2 setState

Jó:

- kis, lokális UI állapothoz
- checkbox
- counter
- egyszerű form mező

Nem jó:

- több képernyő között megosztott adathoz
- bonyolult üzleti logikához
- nagy apphoz

#### 6.3 Ajánlott irány

Tanulási sorrend:

1. `setState`
2. `ValueNotifier`
3. `ChangeNotifier`
4. `Provider`
5. `Riverpod` vagy `Bloc`

Ebben a tananyagban a profi irány:

- alap megértéshez Provider
- nagyobb apphoz Riverpod
- enterprise/csapatmunkához Bloc ismeret

### Gyakorlófeladatok

1. Kosár állapot `setState`-tel.
2. Kosár állapot `ChangeNotifier`-rel.
3. Theme váltás Providerrel.
4. Login állapot kezelése.
5. Loading/error/success állapot modellezése.

### Mini projekt

**Kosár app state managementtel**

Funkciók:

- terméklista
- kosárba tétel
- darabszám növelés/csökkentés
- végösszeg
- állapot megosztása több képernyő között

---

## 7. hét — Async, Future, Stream, API

### Cél

Megtanulni szerverrel kommunikálni.

### Tananyag

#### 7.1 Future

```dart
Future<String> loadName() async {
  await Future.delayed(const Duration(seconds: 1));
  return 'Imre';
}
```

#### 7.2 FutureBuilder

```dart
FutureBuilder<List<Product>>(
  future: productRepository.getProducts(),
  builder: (context, snapshot) {
    if (snapshot.connectionState == ConnectionState.waiting) {
      return const CircularProgressIndicator();
    }

    if (snapshot.hasError) {
      return Text('Hiba: ${snapshot.error}');
    }

    final products = snapshot.data ?? [];
    return ListView(...);
  },
);
```

#### 7.3 HTTP

Gyakori csomagok:

- `http`
- `dio`

Tanulandó:

- GET
- POST
- PUT/PATCH
- DELETE
- headers
- token
- timeout
- retry
- error handling
- JSON parse

#### 7.4 JSON modellezés

Kézzel:

```dart
class Product {
  final int id;
  final String name;
  final int price;

  Product({
    required this.id,
    required this.name,
    required this.price,
  });

  factory Product.fromJson(Map<String, dynamic> json) {
    return Product(
      id: json['id'],
      name: json['name'],
      price: json['price'],
    );
  }
}
```

Később profi megoldás:

- `json_serializable`
- `freezed`

### Gyakorlófeladatok

1. Kérj le adatot publikus API-ból.
2. Készíts model osztályt.
3. Kezeld a loading állapotot.
4. Kezeld a hibát.
5. Készíts retry gombot.

### Mini projekt

**Hírolvasó vagy termékkatalógus API-ról**

Funkciók:

- lista API-ból
- részletező oldal
- loading
- error
- refresh
- keresés

---

## 8. hét — Űrlapok és validáció

### Cél

Profi adatbevitel: login, regisztráció, profil szerkesztés, validáció.

### Tananyag

Tanulandó:

- `TextEditingController`
- `Form`
- `GlobalKey<FormState>`
- validator
- autovalidate
- password field
- checkbox
- dropdown
- date picker
- image picker alapok

Példa:

```dart
TextFormField(
  decoration: const InputDecoration(labelText: 'Email'),
  validator: (value) {
    if (value == null || value.isEmpty) {
      return 'Az email kötelező';
    }
    if (!value.contains('@')) {
      return 'Érvénytelen email';
    }
    return null;
  },
);
```

### Gyakorlófeladatok

1. Login form validációval.
2. Regisztráció jelszó megerősítéssel.
3. Profil szerkesztő képernyő.
4. Termék létrehozó form.
5. Hibaüzenetek egységesítése.

### Mini projekt

**Regisztrációs folyamat**

Funkciók:

- többmezős form
- validáció
- jelszó láthatóság váltás
- checkbox elfogadás
- siker képernyő
- hibák kezelése

---

## 9. hét — Riverpod vagy Bloc alapok

### Cél

Megtanulni modern, skálázható state managementet.

### Ajánlott fő irány: Riverpod

Miért jó tanuláshoz és profi apphoz?

- nem függ közvetlenül a BuildContexttől
- jól tesztelhető
- tiszta dependency injection irány
- jól kezeli az async állapotokat
- modern Flutter projektekben gyakori

Tanulandó:

- Provider
- StateProvider
- FutureProvider
- StateNotifier / Notifier
- AsyncValue
- ref.watch
- ref.read
- provider override teszteléshez

### Alternatíva: Bloc

Miért hasznos?

- enterprise környezetben gyakori
- esemény → állapot gondolkodás
- nagyon strukturált
- jól dokumentálható

Tanulandó Bloc fogalmak:

- Event
- State
- Bloc
- Cubit
- BlocBuilder
- BlocListener
- Repository injection

### Gyakorlófeladatok

1. Counter Riverpoddal.
2. API lista FutureProviderrel.
3. Kosár állapot Notifierrel.
4. Login állapot AsyncValue-val.
5. Ugyanez Cubit/Bloc irányban vázlatosan.

### Mini projekt

**Időjárás app Riverpoddal**

Funkciók:

- város keresése
- API hívás
- loading/error/data
- kedvenc városok
- mentett utolsó keresés

---

# IV. SZAKASZ — Profi app alapok

---

## 10. hét — Tiszta architektúra Flutterben

### Cél

Megtanulni úgy felépíteni egy appot, hogy később ne essen szét.

### Ajánlott mappaszerkezet

```text
lib/
  main.dart
  app/
    app.dart
    router.dart
    theme.dart
  core/
    config/
    errors/
    network/
    utils/
    widgets/
  features/
    auth/
      data/
        models/
        datasources/
        repositories/
      domain/
        entities/
        repositories/
        usecases/
      presentation/
        pages/
        widgets/
        providers/
    products/
      data/
      domain/
      presentation/
```

Egyszerűbb projektnél:

```text
lib/
  app/
  core/
  features/
    todo/
      data/
      logic/
      ui/
```

### Rétegek

#### Presentation layer

- widgetek
- page-ek
- UI állapot
- ViewModel / Notifier / Bloc

#### Domain / logic layer

- üzleti szabályok
- use case-ek
- entity-k

#### Data layer

- API
- adatbázis
- repository implementáció
- DTO/model

### Aranyszabályok

- UI ne hívjon közvetlenül HTTP-t.
- Repository rejtse el, honnan jön az adat.
- Model és entity ne legyen mindig ugyanaz.
- Hibákat egységesen kezeld.
- Feature-ök legyenek külön mappában.
- Közös widgetek menjenek `core/widgets` alá.

### Gyakorlófeladatok

1. Bontsd szét a korábbi termék appot feature-alapú struktúrára.
2. Készíts repository interface-t.
3. Készíts mock repositoryt.
4. Készíts API repositoryt.
5. Cseréld a mockot API-ra UI módosítás nélkül.

### Mini projekt

**Clean Todo App**

Funkciók:

- todo lista
- hozzáadás
- törlés
- készre állítás
- repository pattern
- mock + local data source
- Riverpod/Bloc state

---

## 11. hét — Lokális adattárolás

### Cél

Adatok mentése telefonon.

### Lehetőségek

| Igény | Megoldás |
|---|---|
| egyszerű kulcs-érték | shared_preferences |
| biztonságos token | flutter_secure_storage |
| relációs adat | sqflite / drift |
| objektum alapú gyors DB | hive / isar |
| nagyobb offline app | drift vagy isar |

### Tananyag

Tanulandó:

- shared preferences
- secure storage
- cache stratégia
- adatbázis migráció
- lokális repository
- offline-first alapok

### Gyakorlófeladatok

1. Theme mentése.
2. Login token mentése secure storage-ba.
3. Todo lista mentése lokális DB-be.
4. Cache törlés funkció.
5. App induláskor mentett állapot betöltése.

### Mini projekt

**Offline jegyzet app**

Funkciók:

- jegyzet létrehozás
- szerkesztés
- törlés
- keresés
- lokális mentés
- kedvencek
- dark mode mentése

---

## 12. hét — Auth és biztonság

### Cél

Bejelentkezés, token kezelés, jogosultságok, biztonságos adattárolás.

### Tananyag

Tanulandó:

- email + jelszó login
- JWT token
- refresh token
- secure storage
- interceptor
- 401 kezelés
- logout
- auth guard
- role alapú UI
- biometrikus azonosítás alapok
- HTTPS fontossága

### Token kezelés alapelv

- Access token rövid életű.
- Refresh token hosszabb életű.
- Token ne sima shared preferencesben legyen.
- Logout törölje a tokeneket.
- 401 esetén refresh próbálkozás, majd logout.

### Gyakorlófeladatok

1. Login képernyő.
2. Token mentés secure storage-ba.
3. Auth repository.
4. Dio interceptor.
5. Protected route.

### Mini projekt

**Bejelentkezős profil app**

Funkciók:

- login
- logout
- profil lekérés
- token tárolás
- automatikus beléptetés
- lejárt session kezelése

---

## 13. hét — Backend kapcsolat Django/Laravel API-val

### Cél

Valós backenddel működő Flutter app készítése.

### Tananyag

Tanulandó:

- REST API
- pagination
- filter
- search
- sorting
- authentication header
- file upload
- image upload
- error response
- DTO mapping

### Backend elvárt végpontok példához

```text
POST /api/login
POST /api/refresh
GET /api/me
GET /api/products
GET /api/products/{id}
POST /api/products
PUT /api/products/{id}
DELETE /api/products/{id}
```

### Gyakorlófeladatok

1. Kapcsold a termék appot backendhez.
2. Kezeld a lapozást.
3. Készíts keresést.
4. Készíts új termék felvitelt.
5. Készíts képfeltöltést.

### Mini projekt

**Mobil admin panel API-val**

Funkciók:

- login
- terméklista
- termék részletek
- létrehozás
- módosítás
- törlés
- kép feltöltés
- hibakezelés

---

## 14. hét — Offline-first és szinkronizáció

### Cél

Olyan app készítése, amely gyenge internet mellett is használható.

### Tananyag

Fogalmak:

- cache
- local first
- offline queue
- sync status
- conflict resolution
- optimistic update
- retry
- background sync

### Tipikus stratégia

1. UI lokális adatból rajzol.
2. Háttérben API frissít.
3. Sikeres API után lokális DB frissül.
4. Offline módosítás queue-ba kerül.
5. Internet visszatérésekor sync fut.
6. Konfliktusnál szabály dönt.

### Gyakorlófeladatok

1. Offline todo létrehozás.
2. Online visszatéréskor sync.
3. Sync státusz megjelenítése.
4. Sikertelen sync újrapróbálása.
5. Konfliktus jelzése.

### Mini projekt

**Offline raktárkészlet app**

Funkciók:

- terméklista lokálisan
- készlet módosítás offline
- szinkronizáció API-val
- sync napló
- hibás tételek újraküldése

---

# V. SZAKASZ — Tesztelés, minőség, karbantarthatóság

---

## 15. hét — Unit tesztek

### Cél

Üzleti logika automatikus tesztelése.

### Tananyag

Tesztelendő:

- use case
- validator
- formatter
- repository mockkal
- számítási logika
- entity szabályok

Példa:

```dart
import 'package:test/test.dart';

void main() {
  test('kedvezmény számítás', () {
    final price = calculateDiscount(10000, 10);
    expect(price, 9000);
  });
}
```

### Gyakorlófeladatok

1. Teszteld a kosár végösszeget.
2. Teszteld a login validátort.
3. Teszteld az árformázót.
4. Teszteld a repository hibakezelést.
5. Teszteld a use case-et mock adatokkal.

### Mini projekt

**Tesztelt domain layer**

Készíts legalább 20 unit tesztet egy korábbi projektedhez.

---

## 16. hét — Widget tesztek

### Cél

UI komponensek tesztelése.

### Tananyag

Tanulandó:

- `testWidgets`
- `WidgetTester`
- `pumpWidget`
- `find.text`
- `find.byType`
- gombnyomás tesztelése
- form validáció tesztelése
- provider override tesztben

Példa:

```dart
testWidgets('megjelenik a cím', (tester) async {
  await tester.pumpWidget(const MyApp());
  expect(find.text('Főoldal'), findsOneWidget);
});
```

### Gyakorlófeladatok

1. Teszteld a login képernyőt.
2. Teszteld, hogy hibás emailre hibaüzenet jelenik meg.
3. Teszteld a gomb állapotát.
4. Teszteld a lista üres állapotát.
5. Teszteld a loading állapotot.

### Mini projekt

**UI tesztcsomag**

Legalább 15 widget teszt egy apphoz.

---

## 17. hét — Integration tesztek

### Cél

Teljes app flow-k tesztelése.

### Tananyag

Tesztelendő flow-k:

- app indulás
- login
- lista betöltés
- részletező oldal
- CRUD folyamat
- logout

Tanulandó:

- `integration_test`
- emulatoron futtatás
- fake backend
- tesztadatok
- CI-ben futtatás alapjai

### Gyakorlófeladatok

1. Login flow teszt.
2. Termék létrehozás flow.
3. Keresés flow.
4. Offline állapot flow.
5. Logout flow.

### Mini projekt

**E2E tesztelt mini admin app**

---

## 18. hét — Kódminőség, lint, hibakezelés

### Cél

Olyan kódot írni, amit később is mersz módosítani.

### Tananyag

Tanulandó:

- `flutter_lints`
- custom lint szabályok
- `dart format`
- `dart analyze`
- logging
- crash reporting
- error boundary jellegű megoldások
- Sentry/Firebase Crashlytics alapok
- feature flag
- config kezelés

### Ajánlott parancsok

```bash
dart format .
flutter analyze
flutter test
flutter test --coverage
```

### Gyakorlófeladatok

1. Állíts be szigorú lintet.
2. Javíts ki minden analyze hibát.
3. Készíts egységes error modelt.
4. Készíts logger service-t.
5. Készíts release/debug configot.

### Mini projekt

**Production readiness audit**

Ellenőrizd egy korábbi appodat:

- nincs analyze hiba
- van legalább 30 teszt
- van error state
- van loading state
- van empty state
- működik debug és release configgal

---

# VI. SZAKASZ — Haladó Flutter

---

## 19. hét — Animációk

### Cél

Modern, élő, igényes UI animációkkal.

### Tananyag

Tanulandó:

- implicit animációk
- explicit animációk
- `AnimatedContainer`
- `AnimatedOpacity`
- `Hero`
- `AnimationController`
- `Tween`
- `CurvedAnimation`
- page transition
- skeleton loading
- micro-interactions

### Gyakorlófeladatok

1. Animált kártya.
2. Hero transition lista és részletező között.
3. Animált login form.
4. Skeleton loading.
5. Kedvenc ikon animáció.

### Mini projekt

**Animált recept app**

---

## 20. hét — Platform specifikus funkciók

### Cél

Telefonos képességek használata.

### Tananyag

Tanulandó:

- kamera
- galéria
- fájlválasztás
- GPS
- térkép alapok
- push notification
- local notification
- permissions
- contacts alapok
- bluetooth alapok
- battery/network info
- background task alapok

### Fontos csomagok

- `permission_handler`
- `image_picker`
- `geolocator`
- `google_maps_flutter`
- `firebase_messaging`
- `flutter_local_notifications`
- `connectivity_plus`
- `device_info_plus`

### Gyakorlófeladatok

1. Kép kiválasztása galériából.
2. GPS pozíció lekérése.
3. Jogosultság kérés.
4. Local notification küldése.
5. Online/offline állapot figyelése.

### Mini projekt

**Helyalapú jegyzet app**

Funkciók:

- jegyzet létrehozás
- aktuális GPS mentése
- kép csatolása
- térképes megjelenítés
- lokális mentés

---

## 21. hét — Natív integráció: Platform Channel és FFI

### Cél

Megérteni, hogyan kommunikál a Flutter natív Android/iOS kóddal.

### Tananyag

Tanulandó:

- MethodChannel
- EventChannel
- BasicMessageChannel
- Android Kotlin oldal
- iOS Swift oldal
- plugin készítés alapjai
- FFI alapfogalom
- mikor kell natív kód

### Mikor kell platform channel?

- nincs megfelelő Flutter plugin
- speciális hardver
- gyártói SDK
- natív rendszerfunkció
- meglévő Android/iOS kód integráció

### Gyakorlófeladatok

1. Kérd le natív oldalról az akkumulátor szintet.
2. Küldj paramétert Dartból Kotlinba.
3. Kapj vissza eredményt.
4. Kezeld a hibát.
5. Készíts egyszerű saját plugint.

### Mini projekt

**Natív rendszerinformáció app**

---

## 22. hét — Teljesítmény és optimalizálás

### Cél

Gyors, sima, stabil app készítése.

### Tananyag

Tanulandó:

- build method optimalizálás
- const widgetek
- repaint boundary
- image cache
- lazy loading
- pagination
- isolates
- DevTools
- memory leak
- jank
- shader compilation
- listák optimalizálása
- release profiling

### Gyakori hibák

- nagy számítás UI threaden
- túl sok rebuild
- hatalmas képek tömörítés nélkül
- végtelen lista egyszerre renderelve
- felesleges state fent túl magasan
- rosszul kezelt stream subscription

### Gyakorlófeladatok

1. Optimalizálj hosszú listát.
2. Mérj DevTools-szal.
3. Készíts paginationt.
4. Nagy JSON parse menjen isolate-ba.
5. Képek lazy loadingja.

### Mini projekt

**Nagy termékkatalógus app**

Funkciók:

- 1000+ elem
- keresés
- szűrés
- pagination
- kép cache
- gyors görgetés

---

# VII. SZAKASZ — Publikálás, CI/CD, portfólió

---

## 23. hét — Build, release, Play Store előkészítés

### Cél

Android release build és publikálásra kész app.

### Tananyag

Tanulandó:

- app ikon
- splash screen
- package name
- verziózás
- keystore
- signing
- AAB build
- ProGuard/R8 alapok
- privacy policy
- permissions indoklás
- Play Console alapok
- internal testing track
- staged rollout

### Android build

```bash
flutter build apk --release
flutter build appbundle --release
```

### Ellenőrzőlista publikálás előtt

- app név végleges
- ikon kész
- splash kész
- permissionök rendben
- nincs debug banner
- release config aktív
- API prod endpointot használ
- crash reporting aktív
- privacy policy kész
- screenshotok kész
- store leírás kész
- tesztelve valódi telefonon

### Mini projekt

**Release candidate készítése**

Válassz egy korábbi appot, és készíts belőle release buildet.

---

## 24. hét — CI/CD és záró portfólióprojekt

### Cél

Profi fejlesztési folyamat kialakítása.

### Tananyag

Tanulandó:

- GitHub repository struktúra
- branch stratégia
- Pull Request
- GitHub Actions
- analyze futtatás
- test futtatás
- build futtatás
- verziókezelés
- release note
- changelog
- README
- issue template

### Példa GitHub Actions

```yaml
name: Flutter CI

on:
  push:
    branches: [ main, dev ]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: subosito/flutter-action@v2
        with:
          channel: stable

      - run: flutter pub get
      - run: dart format --set-exit-if-changed .
      - run: flutter analyze
      - run: flutter test
```

### Záróprojekt-választék

Válassz egyet:

#### A) Mobil webshop / katalógus

Funkciók:

- login
- terméklista
- kategóriák
- keresés
- termék részletek
- kosár
- kedvencek
- API kapcsolat
- lokális cache
- tesztek
- release build

#### B) Tanulókártya / oktató app

Funkciók:

- tantárgyak
- leckék
- kvízek
- eredmények
- offline mentés
- API szinkron
- statisztika
- dark mode

#### C) Okosotthon vezérlő app

Funkciók:

- eszközlista
- szobák
- kapcsolók
- státusz lekérés
- MQTT/API kapcsolat
- kedvenc eszközök
- offline státusz
- notification

#### D) Raktár / készletkezelő app

Funkciók:

- login
- termékek
- vonalkódolvasás
- készletmódosítás
- offline queue
- sync log
- jogosultságok

### Záróprojekt elvárt minőség

- legalább 8 képernyő
- tiszta mappastruktúra
- state management Riverpod vagy Bloc
- REST API vagy mock API
- lokális adattárolás
- loading/error/empty state
- legalább 30 unit/widget teszt
- legalább 3 integration flow
- GitHub Actions pipeline
- README képernyőképekkel
- release build
- portfólió leírás

---

# 3. Részletes heti tanulási rutin

## Hétfő — Új elmélet

- 30 perc olvasás
- 60 perc kódpélda
- 30 perc jegyzet

## Kedd — Gyakorlás és mélyítés

- 3–5 kisebb feladat
- refaktor
- Git commit

## Szerda — Saját mini projekt

- egy kisebb funkció önálló megírása
- hibakezelés
- UI állapotok

## Csütörtök — Kódolvasás és refaktorálás

- unit/widget teszt
- analyze
- format
- kód tisztítás

## Péntek — Hétvégi projekt előkészítése

- heti mini projekt
- README frissítés
- screenshot

## Szombat — Projekt nap

- nehéz részek újranézése
- refaktor
- hibák javítása

## Vasárnap — Pihenő vagy könnyű ötletelés

- app ötletek
- UI inspiráció
- következő hét tervezése

---

# 4. Profi Flutter fejlesztői készségtérkép

## Junior szint

Tudja:

- Flutter projekt létrehozása
- alap widgetek
- egyszerű navigáció
- alap formok
- API hívás
- egyszerű állapotkezelés
- alap hibakezelés

Portfólió:

- todo app
- időjárás app
- recept app
- egyszerű webshop UI

## Medior szint

Tudja:

- feature alapú struktúra
- Riverpod/Bloc
- repository pattern
- tokenes auth
- lokális adatmentés
- tesztek
- release build
- Git workflow

Portfólió:

- bejelentkezős admin app
- offline jegyzet app
- API alapú katalógus
- térképes app

## Senior/profi szint

Tudja:

- clean architecture
- CI/CD
- integration tesztek
- performance profiling
- natív integráció
- offline-first sync
- crash reporting
- store publikálás
- skálázható csapatmunka

Portfólió:

- raktárkezelő app
- okosotthon app
- LMS mobil app
- webshop mobil app
- SaaS companion app

---

# 5. Ajánlott csomagok témakörönként

## Routing

- `go_router`

## State management

- `flutter_riverpod`
- `bloc`
- `flutter_bloc`
- `provider`

## HTTP/API

- `dio`
- `http`
- `retrofit`
- `pretty_dio_logger`

## Modellezés

- `freezed`
- `json_serializable`
- `equatable`

## Lokális adattárolás

- `shared_preferences`
- `flutter_secure_storage`
- `drift`
- `sqflite`
- `hive`
- `isar`

## UI

- `flutter_svg`
- `cached_network_image`
- `shimmer`
- `lottie`

## Eszközfunkciók

- `permission_handler`
- `image_picker`
- `geolocator`
- `connectivity_plus`
- `device_info_plus`

## Firebase

- `firebase_core`
- `firebase_auth`
- `cloud_firestore`
- `firebase_messaging`
- `firebase_crashlytics`
- `firebase_analytics`

## Teszt

- `mocktail`
- `build_runner`
- `integration_test`

## Minőség

- `flutter_lints`
- `very_good_analysis`

---

# 6. Saját projektötletek neked

A korábbi technológiai irányaidhoz illeszkedve ezek jó portfólióprojektek lehetnek.

## 6.1 Sephir ERP mobil app

Funkciók:

- workspace választás
- terméklista
- partnerlista
- rendelés felvitel
- raktárkészlet
- vonalkódolvasás
- offline mód
- API token

Miért jó?

- üzleti app
- valós backend
- jogosultságok
- profi portfólió

## 6.2 Oktatási app prstart.hu-hoz

Funkciók:

- tantárgyak
- leckék
- kvízek
- fejlődési statisztika
- offline lecke mentés
- gyerekbarát UI

Miért jó?

- kapcsolódik az LMS projekthez
- jól demózható
- később valódi termék lehet

## 6.3 Okosotthon mobil app

Funkciók:

- szobák
- eszközök
- kapcsolók
- fogyasztás
- kamera linkek
- MQTT/API kapcsolat
- kedvencek

Miért jó?

- saját házban kipróbálható
- IoT + mobil + backend együtt
- erős portfólió

## 6.4 Raktárkezelő / vonalkódos app

Funkciók:

- termékkeresés
- vonalkódolvasás
- készletmódosítás
- offline queue
- sync
- jogosultságok

Miért jó?

- piacképes üzleti app
- sok cégnek hasznos
- jól lehet belőle pénzt csinálni

---

# 7. Vizsgafeladatok saját ellenőrzéshez

## 1. szint — Alap

Készíts appot, amely:

- bekéri a neved
- elmenti lokálisan
- újraindítás után megjeleníti
- dark mode-ot tud váltani

## 2. szint — UI

Készíts termékkatalógus UI-t:

- lista
- részletező
- kedvencek
- keresés
- kategória szűrés

## 3. szint — API

Készíts appot, amely:

- API-ból tölt adatot
- loading/error/empty állapotot kezel
- részletező oldalt nyit
- refresh gombbal újratölt

## 4. szint — Auth

Készíts appot:

- login
- token mentés
- profil lekérés
- logout
- protected route

## 5. szint — Offline

Készíts appot:

- lokálisan ment adatot
- offline is módosítható
- net visszatérésekor szinkronizál

## 6. szint — Profi

Készíts appot:

- clean architecture
- Riverpod/Bloc
- tesztek
- CI
- release build
- README
- screenshotok

---

# 8. Ajánlott tanulási sorrend röviden

1. Dart alapok
2. Flutter widgetek
3. Layout
4. Navigáció
5. Formok
6. API
7. JSON/modellezés
8. State management
9. Architektúra
10. Lokális adat
11. Auth
12. Offline-first
13. Tesztelés
14. Animáció
15. Natív funkciók
16. Teljesítmény
17. Release
18. CI/CD
19. Záróprojekt

---

# 9. Parancsgyűjtemény

## Projekt

```bash
flutter create my_app
cd my_app
flutter run
```

## Csomag hozzáadása

```bash
flutter pub add dio
flutter pub add flutter_riverpod
flutter pub add go_router
```

## Dev dependency

```bash
flutter pub add --dev build_runner
flutter pub add --dev json_serializable
```

## Kódgenerálás

```bash
dart run build_runner build --delete-conflicting-outputs
```

## Elemzés

```bash
dart format .
flutter analyze
```

## Teszt

```bash
flutter test
flutter test --coverage
```

## Build

```bash
flutter build apk --release
flutter build appbundle --release
```

## Takarítás

```bash
flutter clean
flutter pub get
```

---

# 10. Git workflow

## Alap branch modell

```text
main        production-ready
dev         fejlesztési ág
feature/*   új funkciók
fix/*       hibajavítások
```

## Commit példa

```bash
git add .
git commit -m "feat: add product list screen"
git push
```

## Jó commit típusok

- `feat:` új funkció
- `fix:` hibajavítás
- `refactor:` átszervezés működésváltozás nélkül
- `test:` teszt
- `docs:` dokumentáció
- `chore:` technikai karbantartás

---

# 11. Portfólió README sablon

```markdown
# App neve

## Rövid leírás

Ez egy Flutter alkalmazás, amely ...

## Fő funkciók

- Login
- API kapcsolat
- Offline működés
- State management
- Tesztek

## Technológiák

- Flutter
- Dart
- Riverpod
- Dio
- Drift
- GoRouter

## Architektúra

- Feature-first mappaszerkezet
- Repository pattern
- Data / Domain / Presentation rétegek

## Képernyőképek

Ide jönnek a screenshotok.

## Futtatás

```bash
flutter pub get
flutter run
```

## Teszt

```bash
flutter test
```

## Build

```bash
flutter build appbundle --release
```
```

---

# 12. Kötelező fogalmak listája

A tananyag végére ezeket érteni kell:

- Widget tree
- BuildContext
- StatelessWidget
- StatefulWidget
- State
- Lifecycle
- setState
- InheritedWidget alapfogalom
- Provider
- Riverpod
- Bloc
- Future
- Stream
- async/await
- JSON
- DTO
- Entity
- Repository
- Use case
- Dependency injection
- Navigation
- Deep link
- Form validation
- Secure storage
- JWT
- Refresh token
- Offline cache
- Sync queue
- Unit test
- Widget test
- Integration test
- Platform channel
- FFI
- Isolate
- Release signing
- CI/CD

---

# 13. Minimum portfóliócsomag

Ha munkára vagy komolyabb megbízásra készülsz, legalább ezek legyenek GitHubon:

1. **Todo/Notes app**
   - lokális DB
   - dark mode
   - tesztek

2. **API katalógus app**
   - REST API
   - keresés
   - részletező
   - error handling

3. **Auth admin app**
   - login
   - token
   - protected routes
   - CRUD

4. **Offline-first app**
   - lokális adat
   - sync
   - queue
   - konfliktuskezelés alapok

5. **Záróprojekt**
   - legalább 8 képernyő
   - state management
   - CI
   - release build
   - dokumentáció

---

# 14. Ellenőrző mérföldkövek

## 1 hónap után

Tudsz:

- egyszerű Flutter appot készíteni
- layoutot építeni
- több képernyőt használni
- formot validálni

## 2 hónap után

Tudsz:

- API-ból adatot lekérni
- state managementet használni
- modelleket írni
- hibákat kezelni

## 3 hónap után

Tudsz:

- tiszta struktúrát építeni
- authot kezelni
- lokálisan adatot menteni
- közepes appot felépíteni

## 4 hónap után

Tudsz:

- teszteket írni
- offline működést építeni
- appot refaktorálni
- minőséget mérni

## 5 hónap után

Tudsz:

- animációt
- natív funkciókat
- performance optimalizálást
- platform channel alapokat

## 6 hónap után

Tudsz:

- release buildet készíteni
- CI/CD-t használni
- Play Store-ra felkészíteni
- portfólió appot bemutatni

---

# 15. Javasolt első 30 nap konkrét menetrend

## 1. nap

- Flutter telepítés
- `flutter doctor`
- első app futtatása

## 2. nap

- Dart változók, típusok
- mini számológép

## 3. nap

- Dart függvények, osztályok
- Product/User model

## 4. nap

- null safety
- lista/map gyakorlatok

## 5. nap

- első saját Flutter képernyő

## 6. nap

- Column, Row, Container

## 7. nap

- ismétlés + GitHub repo

## 8. nap

- StatelessWidget vs StatefulWidget

## 9. nap

- számláló app

## 10. nap

- TextField, gombok

## 11. nap

- bevásárlólista app

## 12. nap

- ListView, Card

## 13. nap

- Todo app alap

## 14. nap

- Todo app befejezés

## 15. nap

- layout mélyítés

## 16. nap

- login UI

## 17. nap

- termékkártya UI

## 18. nap

- responsive layout

## 19. nap

- webshop katalógus UI

## 20. nap

- webshop részletező UI

## 21. nap

- refaktor + README

## 22. nap

- Navigator alapok

## 23. nap

- route argumentumok

## 24. nap

- bottom navigation

## 25. nap

- theme alapok

## 26. nap

- dark mode

## 27. nap

- assetek, képek

## 28. nap

- UI kit komponensek

## 29. nap

- mini projekt összerakása

## 30. nap

- kód tisztítás, screenshot, GitHub

---

# 16. Források és hivatalos dokumentáció

Ezeket érdemes folyamatosan használni:

- Flutter főoldal: https://flutter.dev/
- Flutter dokumentáció: https://docs.flutter.dev/
- Flutter telepítés és SDK archive: https://docs.flutter.dev/install/archive
- Dart dokumentáció: https://dart.dev/
- Dart language tour: https://dart.dev/language
- Dart null safety: https://dart.dev/null-safety/understanding-null-safety
- Dart concurrency: https://dart.dev/language/concurrency
- Flutter architecture: https://docs.flutter.dev/app-architecture
- Flutter architecture guide: https://docs.flutter.dev/app-architecture/guide
- Flutter architecture concepts: https://docs.flutter.dev/app-architecture/concepts
- Flutter state management: https://docs.flutter.dev/data-and-backend/state-mgmt/options
- Flutter navigation: https://docs.flutter.dev/ui/navigation
- Flutter platform channels: https://docs.flutter.dev/platform-integration/platform-channels
- Flutter testing: https://docs.flutter.dev/testing
- Widget testing cookbook: https://docs.flutter.dev/cookbook/testing/widget/introduction
- Android release: https://docs.flutter.dev/deployment/android
- iOS release: https://docs.flutter.dev/deployment/ios
- pub.dev: https://pub.dev/
- pub.dev package scoring: https://pub.dev/help/scoring

---

# 17. Záró tanács

A Fluttert akkor fogod igazán megtanulni, amikor egy saját, valós problémára készítesz appot. Ne csak demókat építs. Válassz egy projektet a saját világodból:

- Sephir ERP mobil kliens
- prstart.hu tanuló app
- okosotthon vezérlő
- vonalkódos raktár app

Ezek közül bármelyikből lehet komoly portfólió vagy később valódi termék.
