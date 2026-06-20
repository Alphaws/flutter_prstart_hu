# 24. hét — CI/CD és záró portfólióprojekt

## Cél
A lecke célja, hogy a tanuló megismerje és beállítsa az automatizált folyamatos integrációs és szállítási (CI/CD) folyamatokat GitHub Actions segítségével. Áttekintjük a szakaszos branching és Pull Request alapú munkafolyamatot, megtervezzük a képzést lezáró, komplex portfólió Záróprojektet, és megtanuljuk, hogyan kell azt professzionális módon prezentálni a GitHubon a leendő munkaadók számára.

---

## Elmélet

### 1. Mi az a CI/CD a mobilfejlesztésben?
- **CI (Continuous Integration - Folyamatos Integráció):** Olyan automatizált folyamat, amely minden kódmódosítás (pl. Git push vagy Pull Request) esetén automatikusan lefut egy tiszta szerveren. Letölti a kódunkat, ellenőrzi a formázást, lefuttatja a statikus kódelemzőt (linter/analyzer) és végrehajtja a teszteket (unit és widget tesztek). Ha bármi elromlik, a fejlesztő azonnal értesítést kap. Ez megakadályozza, hogy hibás kód kerüljön a fő ágba.
- **CD (Continuous Delivery/Deployment - Folyamatos Szállítás):** A sikeres integráció után az automatizáció lefordítja a release buildet (AAB/APK), aláírja a kulccsal, és automatikusan feltölti a Google Play Console belső tesztelési sávjába vagy a Firebase App Distribution-be.

### 2. GitHub Actions Alapfogalmak
A GitHub beépített CI/CD eszköze. A projekt `.github/workflows/` könyvtárában elhelyezett YAML konfigurációs fájlokkal vezérelhető.
- **Workflow (Munkafolyamat):** Egy automatizált eljárás, amely egy vagy több esemény (push, pull_request) hatására indul el.
- **Job (Feladat):** Lépések sorozata, amelyek egy közös virtuális gépen (Runner, pl. `ubuntu-latest` vagy `macos-latest`) futnak le.
- **Step (Lépés):** Egy konkrét végrehajtandó feladat (pl. egy shell parancs futtatása vagy egy előre elkészített Action meghívása).
- **Secrets (Titkok):** Titkosított kulcsok (pl. API jelszavak, Base64 keystore), amelyeket a GitHub felületén adunk meg, és a workflow kódjában biztonságosan, maszkolva érhetünk el.

### 3. Branching Stratégiák Mobilprojekteknél
Mobilalkalmazásoknál kiemelten fontos a tiszta Git ág-kezelés, mert a hibás kód azonnal megakadást jelenthet a store-ban.
- **Trunk-based Development:** Egyetlen fő ág van (`main`), ahová a fejlesztők rövid életű feature ágakról, szigorú Pull Request és automata tesztelés után azonnal mergelnek.
- **GitFlow (Standard):**
  - `main`: Csak a stabil, store-ban lévő verziókat tartalmazza (Production).
  - `dev` vagy `develop`: A fejlesztési főág. Ide kerülnek be az új funkciók.
  - `feature/*`: Egy-egy konkrét új funkció ága, ami a `dev`-ből ágazik le és oda tér vissza PR után.
  - `release/*`: A kiadás előkészítő ága, itt történik az utolsó tesztelés és bugfixelés.

### 4. Záróprojekt Architektúra: Clean Architecture
Egy portfólió projektnek bizonyítania kell, hogy képes vagy tiszta, skálázható kódot írni. A javasolt struktúra a **Clean Architecture (Feature-first)** elrendezés:

```text
lib/
  main.dart
  core/                  # Globális segédosztályok, hálózati kliens, témák
    theme/
    network/
  features/              # Funkcióalapú felosztás
    products/            # Pl. Termékek feature
      data/              # Adatréteg: API kliens, adatbázis táblák, DTO-k
        models/
        repositories/
      domain/            # Üzleti logikai réteg: Repository interfészek, Entity-k, Use Case-ek
        entities/
        repositories/
      presentation/      # Megjelenítési réteg: UI, Widgetek, State Management (Riverpod/Bloc)
        controllers/
        screens/
        widgets/
```

---

## Kódpéldák

### 1. Haladó GitHub Actions Workflow (`.github/workflows/flutter_ci.yml`)
Ez a fájl automatikusan lefut minden push és PR esetén a `main` és `dev` ágakon. Gyorsítótárazza (Cache) a Flutter SDK-t és a csomagokat a gyors futás érdekében, majd elemzi és teszteli a kódot, végül lefordítja a release APK-t.

```yaml
name: Flutter CI/CD Pipeline

on:
  push:
    branches: [ main, dev ]
  pull_request:
    branches: [ main, dev ]

jobs:
  analyze_and_test:
    name: Kódminőség és Tesztelés
    runs-on: ubuntu-latest

    steps:
      # 1. Kódbázis letöltése a virtuális gépre
      - name: Checkout Repository
        uses: actions/checkout@v4

      # 2. Java környezet beállítása (szükséges az Android buildhez)
      - name: Set up JDK 17
        uses: actions/setup-java@v3
        with:
          distribution: 'zulu'
          java-version: '17'

      # 3. Flutter SDK telepítése és gyorsítótárazása
      - name: Set up Flutter
        uses: subosito/flutter-action@v2
        with:
          channel: 'stable'
          cache: true # Aktiválja a beépített cache-elést

      # 4. Függőségek letöltése
      - name: Install Dependencies
        run: flutter pub get

      # 5. Kód formázásának ellenőrzése
      - name: Check Formatting
        run: dart format --set-exit-if-changed .

      # 6. Statikus kódelemzés futtatása (linter szabályok)
      - name: Analyze Code
        run: flutter analyze

      # 7. Unit és Widget tesztek futtatása lefedettségi riporttal
      - name: Run Tests
        run: flutter test --coverage

      # 8. Release APK lefordítása (aláírás nélkül, teszt célból)
      - name: Build Release APK
        run: flutter build apk --no-pub --release

      # 9. Elkészült APK mentése GitHub Artifactként
      - name: Upload Build Artifact
        uses: actions/upload-artifact@v4
        with:
          name: release-apk
          path: build/app/outputs/flutter-apk/app-release.apk
```

### 2. Professzionális Portfólió `README.md` Sablon
A jó README elengedhetetlen ahhoz, hogy egy HR-es vagy Tech Lead egyáltalán megnézze a kódodat. Itt egy kitöltendő struktúra:

```markdown
# GeoNotes - Helyalapú Jegyzetelő Mobilalkalmazás

[![Flutter CI/CD Pipeline](https://github.com/felhasznalonev/geonotes/actions/workflows/flutter_ci.yml/badge.svg)](https://github.com/felhasznalonev/geonotes/actions)

## 📝 Leírás
A GeoNotes egy modern, offline-first Flutter mobilalkalmazás Androidra és iOS-re, amellyel a felhasználók jegyzeteket rögzíthetnek fotókkal és automatikus GPS helymeghatározással kiegészítve.

## 🚀 Fő Funkciók
- **Offline Működés:** SQLite alapú Drift adatbázis a helyi perzisztens tároláshoz.
- **Hardver Integráció:** GPS koordináták lekérése (`geolocator`), fotók készítése (`image_picker`).
- **State Management:** Riverpod az aszinkron állapot és az üzleti logika tiszta szétválasztására.
- **Modern Design:** Space-dark téma reszponzív elrendezéssel.

## 🛠️ Alkalmazott Technológiák
- **Keretrendszer:** Flutter (Dart 3)
- **Állapotkezelés:** `flutter_riverpod` + `riverpod_generator`
- **Adatbázis:** `drift` (SQLite)
- **Navigáció:** `go_router`
- **Tesztelés:** `flutter_test`, `mockito`

## 📐 Architektúra
Az alkalmazás a **Clean Architecture** elveit követi **Feature-first** mappastruktúrával:
- `Presentation réteg`: UI képernyők, widgetek és state notifier controller-ek.
- `Domain réteg`: Üzleti entitások és repository interfészek.
- `Data réteg`: Adatbázis sémák, API hívások és a repository implementációk.

## 📸 Képernyőképek
| Főoldal | Új Jegyzet | Térkép |
|---|---|---|
| ![Screenshot 1](https://via.placeholder.com/200x400) | ![Screenshot 2](https://via.placeholder.com/200x400) | ![Screenshot 3](https://via.placeholder.com/200x400) |

## 💻 Lokális Futtatás

1. Függőségek letöltése:
   ```bash
   flutter pub get
   ```
2. Kódgenerátor futtatása (Drift / Riverpod):
   ```bash
   dart run build_runner build --delete-conflicting-outputs
   ```
3. Futtatás debug módban:
   ```bash
   flutter run
   ```

## 🧪 Tesztelés
A tesztlefedettség meghaladja a 80%-ot. Tesztek futtatása:
```bash
flutter test
```
```

---

## Gyakorlófeladatok & Megoldások

### 1. Feladat: Csak tesztet futtató egyszerű GitHub Actions workflow
Írj egy minimalista GitHub Actions YAML fájlt `.github/workflows/test_only.yml` néven, amely minden Pull Request megnyitásakor elindítja a teszteket.

#### Megoldás:
```yaml
name: PR Test Check

on:
  pull_request:
    branches: [ main, dev ]

jobs:
  run_tests:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Setup Flutter
        uses: subosito/flutter-action@v2
        with:
          channel: 'stable'

      - name: Get Dependencies
        run: flutter pub get

      - name: Execute Flutter Tests
        run: flutter test
```

### 2. Feladat: Szigorúbb linter szabályok beállítása
Módosítsd az `analysis_options.yaml` fájlt a projekt gyökerében úgy, hogy a formázási hibák és a be nem zárt sink-ek (pl. stream controller-ek) fordítási szintű figyelmeztetést (warning/error) adjanak.

#### Megoldás:
Írd felül az `analysis_options.yaml` fájlt az alábbi tartalommal:

```yaml
include: package:flutter_lints/flutter.yaml

analyzer:
  language:
    strict-casts: true
    strict-inference: true
    strict-raw-types: true
  errors:
    # Formázási és kódminőségi szabályok szigorítása
    missing_required_param: error
    missing_return: error
    todo: ignore
    invalid_annotation_target: ignore
    close_sinks: error # Be nem zárt stream-ek hibát dobnak a build alatt

linter:
  rules:
    - always_declare_return_types
    - cancel_subscriptions
    - close_sinks
    - prefer_const_constructors
    - prefer_final_locals
    - use_key_in_widget_constructors
```

### 3. Feladat: GitHub Secrets beállítása környezeti változóhoz
Magyarázd el és mutasd be kóddal, hogyan használhatsz egy titkosított API kulcsot (pl. `MAPS_API_KEY`) GitHub Actions-ben úgy, hogy azt a build során beillessze az Android `AndroidManifest.xml` fájljába anélkül, hogy a kulcs bekerülne a Git-be.

#### Megoldás:
1. Menj a GitHub repódba: **Settings -> Secrets and variables -> Actions -> New repository secret**.
2. Hozd létre a secretet: Név: `MAPS_API_KEY`, Érték: `AIzaSyYourSecretKeyFromGoogle`.
3. A `.github/workflows/flutter_ci.yml` build lépésébe szúrd be ezt a replace lépést a build parancs futtatása elé:

```yaml
      - name: Inject Maps API Key
        run: |
          sed -i 's/YOUR_MAPS_API_KEY_PLACEHOLDER/${{ secrets.MAPS_API_KEY }}/g' android/app/src/main/AndroidManifest.xml
```
4. Az `AndroidManifest.xml` fájlban a kulcs helyére írd a következőt:
```xml
<meta-data android:name="com.google.android.geo.API_KEY"
           android:value="YOUR_MAPS_API_KEY_PLACEHOLDER"/>
```

### 4. Feladat: Pull Request Sablon (PR Template) létrehozása
Hozz létre egy Pull Request sablont, amely automatikusan kitöltésre kerül, amikor a fejlesztők új PR-t nyitnak meg a repóban. A sablon tartalmazzon egy ellenőrzőlistát a kódminőségről és a tesztekről.

#### Megoldás:
Hozz létre egy `.github/pull_request_template.md` fájlt a repóban az alábbi tartalommal:

```markdown
## 📝 Leírás
Kérjük, írd le röviden az elvégzett módosításokat és a megvalósított funkciót.

## 🔗 Kapcsolódó Task / Issue
Fixes # (issue száma)

## 🛠️ Elvégzett változtatások típusa
- [ ] Bug fix (nem törő hibajavítás)
- [ ] Új funkció (nem törő kódmódosítás)
- [ ] Breaking change (olyan módosítás, ami miatt a meglévő kód nem fut le)
- [ ] Refaktor / Dokumentáció frissítése

## 🧪 Hogyan lett tesztelve?
- [ ] Unit tesztek futtatva
- [ ] Manuális tesztelés emulátoron
- [ ] Manuális tesztelés fizikai eszközön

## 📋 Ellenőrzőlista a kód átadása előtt:
- [ ] A kódom követi a projekt linter és formázási szabályait.
- [ ] Hozzáadtam teszteket az új kódhoz (ahol szükséges).
- [ ] A meglévő tesztek sikeresen lefutnak.
- [ ] Frissítettem a dokumentációt / README-t (ahol szükséges).
- [ ] Nincsenek felesleges print hívások vagy kommentelt kódok.
```

### 5. Feladat: Changelog (Változtatási napló) automatizálása
Magyarázd el a Conventional Commits használatát, és hogyan segít ez az automatikus verzióléptetésben és changelog generálásban.

#### Megoldás:
A **Conventional Commits** egy szabvány, amely meghatározza a commit üzenetek formátumát:
- `feat: add Google Maps integration` -> Új funkció (Minor verzióléptetést jelent: 1.0.0 -> 1.1.0)
- `fix: resolve GPS location crash on Android 14` -> Hibajavítás (Patch verzióléptetést jelent: 1.0.0 -> 1.0.1)
- `feat!: change repository contract` vagy `BREAKING CHANGE:` -> Breaking change (Major verzióléptetést jelent: 1.0.0 -> 2.0.0)

**Automatizálás:**
Ha a csapat tartja magát ehhez a mintához, a CI/CD pipeline-ban olyan eszközök, mint a `semantic-release` vagy a `release-please` képesek automatikusan:
1. Elemezni a legutóbbi commitokat a merge után.
2. Kiszámolni a következő verziószámot a `pubspec.yaml`-ben.
3. Készíteni egy szép `CHANGELOG.md` összefoglalót, összegyűjtve az új funkciókat és javításokat.
4. Generálni egy új GitHub Release tag-et a lefordított APK csatolásával.

---

## Záróprojekt: Komplex Záróprojekt Specifikáció

Az alábbiakban bemutatjuk a képzést lezáró Záróprojekt elvárt funkcionális követelményeit és az indító kódszerkezetet. Válassz egyet a négy téma közül (Mobil Webshop, Tanulókártya, Okosotthon Vezérlő, Raktárkezelő), és készítsd el.

### Elvárt Minimális Minőség
- **Minimum 8 egyedi képernyő** (pl. Splash, Login, Főoldal/Dashboard, Lista, Részletek, Kosár/Kedvencek, Profil, Beállítások).
- **Riverpod vagy BLoC** alapú tiszta állapotkezelés.
- **SQLite (Drift/Floor)** vagy **Hive** perzisztens lokális adatbázis (offline-first működés).
- **REST API** kapcsolat (pl. mockAPI.io vagy valós publikus API) hálózati hibák, betöltő és üres állapotok lekezelésével.
- Legalább **30 unit/widget teszt** és legalább **3 integration flow** (pl. bejelentkezési vagy vásárlási folyamat integrációs tesztelése).
- Működő **GitHub Actions** CI workflow.

### Kiinduló Projektstruktúra és Riverpod Váz (`lib/main.dart`)
A projekt elindításához add hozzá a `pubspec.yaml`-hez:
```yaml
dependencies:
  flutter:
    sdk: flutter
  flutter_riverpod: ^2.5.1
  go_router: ^13.2.0
```

Itt a záróprojekt kiinduló `main.dart` vázszerkezete, amely beállítja a Riverpod-ot, a GoRouter-t, a sötét témát és szimulál egy bejelentkezési folyamatot (Auth Guard):

```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

void main() {
  // A Riverpod ProviderScope-ba kell csomagolni a teljes alkalmazást
  runApp(
    const ProviderScope(
      child: FinalPortfolioApp(),
    ),
  );
}

// ==========================================================================
// STATE MANAGEMENT (RIVERPOD PROVIDERS)
// ==========================================================================

/// Bejelentkezési állapotot kezelő egyszerű notifier
class AuthNotifier extends StateNotifier<bool> {
  AuthNotifier() : super(false); // Kezdetben nincs bejelentkezve

  void login() {
    state = true;
  }

  void logout() {
    state = false;
  }
}

final authProvider = StateNotifierProvider<AuthNotifier, bool>((ref) {
  return AuthNotifier();
});

// ==========================================================================
// ROUTING (GO_ROUTER CONFIGURE WITH AUTH GUARD)
// ==========================================================================

final routerProvider = Provider<GoRouter>((ref) {
  final isLoggedIn = ref.watch(authProvider);

  return GoRouter(
    initialLocation: '/',
    redirect: (context, state) {
      final goingToLogin = state.matchedLocation == '/login';

      // Auth guard logikája
      if (!isLoggedIn && !goingToLogin) {
        return '/login'; // Ha nincs bejelentkezve és nem a loginra megy, átirányítjuk oda
      }
      if (isLoggedIn && goingToLogin) {
        return '/'; // Ha be van jelentkezve és a loginra menne, átirányítjuk a főoldalra
      }
      return null; // Nincs átirányítás
    },
    routes: [
      GoRoute(
        path: '/login',
        builder: (context, state) => const LoginPage(),
      ),
      GoRoute(
        path: '/',
        builder: (context, state) => const DashboardPage(),
      ),
      GoRoute(
        path: '/details/:id',
        builder: (context, state) {
          final id = state.pathParameters['id'] ?? '0';
          return DetailsPage(itemId: id);
        },
      ),
    ],
  );
});

// ==========================================================================
// MAIN APPLICATION COMPONENT
// ==========================================================================

class FinalPortfolioApp extends ConsumerWidget {
  const FinalPortfolioApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final GoRouter router = ref.watch(routerProvider);

    return MaterialApp.router(
      title: 'Portfolio Záróprojekt',
      theme: ThemeData(
        brightness: Brightness.dark,
        primaryColor: Colors.cyan,
        scaffoldBackgroundColor: const Color(0xFF0B0F19),
        colorScheme: const ColorScheme.dark(
          primary: Colors.cyan,
          secondary: Colors.cyanAccent,
          surface: Color(0xFF1E293B),
        ),
        useMaterial3: true,
        fontFamily: 'Inter',
      ),
      routerConfig: router,
    );
  }
}

// ==========================================================================
// SCREEN WIDGETS
// ==========================================================================

/// Bejelentkező képernyő UI
class LoginPage extends ConsumerWidget {
  const LoginPage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      body: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const Icon(Icons.lock_open, size: 80, color: Colors.cyanAccent),
              const SizedBox(height: 20),
              const Text(
                'Záróprojekt Belépés',
                textAlign: TextAlign.center,
                style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold, color: Colors.white),
              ),
              const SizedBox(height: 30),
              const TextField(
                decoration: InputDecoration(
                  labelText: 'Felhasználónév',
                  border: OutlineInputBorder(),
                ),
              ),
              const SizedBox(height: 16),
              const TextField(
                obscureText: true,
                decoration: InputDecoration(
                  labelText: 'Jelszó',
                  border: OutlineInputBorder(),
                ),
              ),
              const SizedBox(height: 24),
              ElevatedButton(
                onPressed: () {
                  ref.read(authProvider.notifier).login();
                },
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.cyan,
                  foregroundColor: Colors.black,
                  padding: const EdgeInsets.symmetric(vertical: 14),
                ),
                child: const Text('Bejelentkezés', style: TextStyle(fontWeight: FontWeight.bold)),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

/// Dashboard (Főoldal) UI
class DashboardPage extends ConsumerWidget {
  const DashboardPage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Dashboard'),
        backgroundColor: const Color(0xFF111827),
        actions: [
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: () {
              ref.read(authProvider.notifier).logout();
            },
          ),
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Üdvözöllek a Záróprojektben!',
              style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: Colors.white),
            ),
            const SizedBox(height: 20),
            Expanded(
              child: ListView.builder(
                itemCount: 5,
                itemBuilder: (context, index) {
                  final itemId = index + 1;
                  return Card(
                    color: Theme.of(context).colorScheme.surface,
                    margin: const EdgeInsets.symmetric(vertical: 8),
                    child: ListTile(
                      title: Text('Katalógus Elem #$itemId'),
                      subtitle: const Text('Kattints a részletekért'),
                      trailing: const Icon(Icons.chevron_right, color: Colors.cyanAccent),
                      onPressed: () {
                        context.push('/details/$itemId');
                      },
                    ),
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

/// Részletező Képernyő UI
class DetailsPage extends StatelessWidget {
  final String itemId;
  const DetailsPage({super.key, required this.itemId});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Elem #$itemId részletei'),
        backgroundColor: const Color(0xFF111827),
      ),
      body: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const Icon(Icons.info, size: 100, color: Colors.cyanAccent),
            const SizedBox(height: 20),
            Text(
              'Ez a(z) $itemId. sorszámú elem részletes leíró oldala.',
              textAlign: TextAlign.center,
              style: const TextStyle(fontSize: 18),
            ),
            const SizedBox(height: 40),
            ElevatedButton(
              onPressed: () => context.pop(),
              style: ElevatedButton.styleFrom(backgroundColor: Colors.cyan, foregroundColor: Colors.black),
              child: const Text('Vissza a Dashboardra'),
            ),
          ],
        ),
      ),
    );
  }
}
```

---

## Heti Ellenőrző Kérdések

### 1. Kérdés: Mi az a „build runner” és a „code generation” (kódgenerálás) a Flutterben? Miért kell futtatni a `dart run build_runner build` parancsot a Git klónozás után?
**Válasz:**
A Flutterben számos népszerű könyvtár (mint a Drift adatbázis, a Riverpod annotációk vagy a Freezed modellek) kódgenerálásra támaszkodik, hogy típusbiztos, optimalizált boilerplate kódot hozzon létre a háttérben. Ez megkíméli a fejlesztőt a manuális JSON parsolók vagy SQL leképezések megírásától.
Mivel a generált fájlok (pl. `*.g.dart` vagy `*.freezed.dart`) nagyon hosszúak és gép által írtak, a Git repository-ba a `.gitignore` szabályai miatt nem kerülnek feltöltésre (tisztaság és a kódkonfliktusok elkerülése végett). Ezért a Git klónozás után első lépésként a `flutter pub get` mellett le kell futtatni a `dart run build_runner build` parancsot is, hogy a lokális környezetünkben is legenerálódjanak a hiányzó fájlok, különben az alkalmazás nem fog lefordulni.

### 2. Kérdés: Mi a különbség a folyamatos integráció (CI) és a folyamatos szállítás (CD) között?
**Válasz:**
- A **CI (Continuous Integration)** a kódminőségre és a tesztelésre fókuszál. Célja annak ellenőrzése, hogy az újonnan beküldött kód megfelel-e a formázási szabályoknak, átmegy-e a linteren, és nem töri-e el a meglévő teszteket. Automatikusan fut minden branch commitnál vagy PR nyitásnál.
- A **CD (Continuous Delivery/Deployment)** a szoftver kiadására fókuszál. A sikeres CI fázis után automatikusan legenerálja az aláírt release állományt (AAB/APK), verziószámot léptet, és feltölti a tesztelési vagy éles csatornákra (pl. Google Play Console, Firebase App Distribution, App Store Connect).

### 3. Kérdés: Miért érdemes gyorsítótárazást (Caching) használni a GitHub Actions workflow lépéseiben?
**Válasz:**
A GitHub Actions runner-ek (virtuális gépek) minden egyes futtatáskor teljesen tiszta állapotból indulnak. Gyorsítótárazás nélkül a virtuális gépnek minden alkalommal nulláról le kell töltenie a teljes Flutter SDK-t, valamint az alkalmazás összes külső csomagját (pub.dev dependency-k). Ez akár 5-10 percig is eltarthat, ami lassítja a fejlesztést és feleslegesen pazarolja a GitHub ingyenes build perceit.
A gyorsítótárazással (pl. a `subosito/flutter-action` `cache: true` paraméterével vagy az `actions/cache` használatával) a korábbi buildekből megőrzött függőségeket a GitHub szerverei azonnal betöltik a runner-be, amivel a pipeline futási ideje akár 70-80%-kal (pl. 8 percről 2 percre) lecsökkenthető.

### 4. Kérdés: Mit jelent a Pull Request (PR) alapú munkafolyamat, és miért hasznos a kód felülvizsgálata (Code Review)?
**Válasz:**
A PR alapú munkafolyamat azt jelenti, hogy a fejlesztő nem írhat kódot közvetlenül a fő fejlesztési ágakba (`main`, `dev`). Ehelyett egy külön ágon (`feature/uj-funkcio`) dolgozik, majd amikor elkészült, egy Pull Request-et (lekérési kérelmet) nyit meg.
Ez két okból hasznos:
1. **Automata ellenőrzés (CI):** A PR megnyitásakor a CI pipeline azonnal lefut, és jelzi, ha a kód szintaktikailag hibás, nem fordul le, vagy elrontotta a teszteket.
2. **Emberi felülvizsgálat (Code Review):** Legalább egy másik fejlesztő átnézi a módosításokat, véleményezi a kódot, javaslatokat tesz a tisztább megoldásokra, ellenőrzi az architektúra betartását, és megosztja a tudást. Ez drasztikusan javítja a kód minőségét és csökkenti a bugok számát.

### 5. Kérdés: Hogyan teszi portfólió-képessé a záróprojektedet egy minőségi README fájl és a GitHub Actions beállítása?
**Válasz:**
Amikor egy leendő munkaadó (pl. HR-es vagy vezető fejlesztő) rákattint a GitHub linkedre, az első dolog, amit lát, a README.md. Ha a README strukturált, tartalmaz képernyőképeket, leírja az architektúrát, az alkalmazott technológiákat és a lokális futtatás pontos lépéseit, az professzionális benyomást kelt és bizonyítja a rendszerszemléletedet.
A GitHub Actions zöld „Passing” badge-e (folyamatjelző címkéje) a README elején jelzi, hogy a kódod ténylegesen működik, lefordul, és a tesztek sikeresek. Ez kiemeli a pályázatodat a többi junior fejlesztő közül, mert bizonyítja, hogy nemcsak kódot tudsz írni, hanem érted és használod a modern szoftverfejlesztési iparági sztenderd eszközöket (CI/CD, automatizáció) is.
