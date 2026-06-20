# 18. hét — Kódminőség, lint, hibakezelés

## Cél
A lecke célja, hogy megtanuld, hogyan írj éles üzemre kész (production-ready), stabil és könnyen karbantartható Flutter kódot. Elsajátítod a statikus kódelemzés (linter) konfigurálását és használatát, egy egységes globális és lokális hibakezelő rendszer felépítését, a biztonságos és strukturált naplózást (logging), valamint az automatizált crash reporting alapjait.

---

## Elmélet

### Kódminőség és linter Flutterben
A kódminőség nem esztétikai kérdés, hanem a karbantarthatóság alapköve. Csapatmunkában elengedhetetlen, hogy minden fejlesztő azonos stílusirányzatokat kövessen. Erre szolgál a **linter**, ami a kód futtatása nélkül (statikus elemzéssel) vizsgálja meg a kódbázist, és figyelmeztet a potenciális hibákra, stilisztikai eltérésekre vagy elavult mintákra.

A Flutter alapértelmezetten a `flutter_lints` csomagot használja, de professzionális projekteknél a szabályokat szigorítani szoktuk az `analysis_options.yaml` fájlban. A statikus elemzőt a következő paranccsal futtathatjuk:
```bash
flutter analyze
```

### Hibakezelés rétegei
Egy jó alkalmazás sosem omlik össze váratlanul a felhasználó kezében. A hibákat rétegenként kell kezelni:
1. **Adat/Logikai réteg (Data/Domain):** Itt kapjuk el az API vagy adatbázis hibákat (pl. 404, No Internet), és ezeket egyedi, az üzleti logikának megfelelő kivételekké (`AppException`) alakítjuk.
2. **Prezentációs réteg (UI):** A widget szinten elkapott hibákat nem hagyjuk kezeletlenül. Hiba esetén egy szép, újratervezett hiba-képernyőt vagy hibaüzenetet (`Error state`) mutatunk a felhasználónak ahelyett, hogy a betöltő ikon pörögne a végtelenségig.
3. **Globális szint:** Ha egy váratlan hiba mégis átjut a védelmi vonalakon, a Flutter globális hibaelfogói (pl. `FlutterError.onError`, `PlatformDispatcher.instance.onError`) elkapják azt, és beküldik a crash reporting rendszerbe (pl. Sentry vagy Firebase Crashlytics).

### Logging: miért ne használjunk `print`-et?
A sima `print()` függvény lassú, szinkron módon ír a konzolra (blokkolhatja a UI szálat), és a kiírt üzenetek benne maradnak a release buildben is. Ez komoly biztonsági kockázatot jelent, mert a felhasználók vagy kártevő szoftverek a fizikai telefon logjából kiolvashatják az érzékeny adatokat (pl. tokenek, személyes adatok).
Helyette használjuk a `debugPrint()`-et vagy egy dedikált logger csomagot (pl. `logger`), ami lehetővé teszi a naplózási szintek (Verbose, Debug, Info, Warning, Error, Wtf) beállítását és a logok kikapcsolását produkciós környezetben.

---

## Kódpéldák

### 1. Szigorú linter konfiguráció (`analysis_options.yaml`)

Ez az `analysis_options.yaml` konfigurációs fájl megköveteli a szigorú típusellenőrzést, a vesszők használatát a szebb formázásért, és megtiltja a `print` használatát.

```yaml
# analysis_options.yaml
include: package:flutter_lints/flutter.yaml

analyzer:
  language:
    strict-casts: true
    strict-inference: true
    strict-raw-types: true
  exclude:
    - "**/*.g.dart"
    - "**/*.freezed.dart"
    - "build/**"

linter:
  rules:
    # Kerüljük a print használatát a kódban
    avoid_print: true
    # Kötelező záróvesszők a szebb formázásért
    require_trailing_commas: true
    # Mindig határozzuk meg a változók típusát tagváltozóknál
    always_specify_types: true
    # Kerüljük az üres catch blokkokat
    empty_catches: true
    # Preferáljuk a const kulcsszót a widgeteknél
    prefer_const_constructors: true
    # Tiltja a felesleges null ellenőrzéseket
    avoid_redundant_argument_values: true
```

### 2. Egységes hibakezelési és logger rendszer (`lib/core/`)

#### A Logger szerviz (`lib/core/logger_service.dart`)
```dart
import 'package:flutter/foundation.dart';
import 'package:logger/logger.dart';

class LoggerService {
  static final Logger _logger = Logger(
    printer: PrettyPrinter(
      methodCount: 2,
      errorMethodCount: 8,
      lineLength: 120,
      colors: true,
      printEmojis: true,
    ),
  );

  static void d(String message) {
    if (kDebugMode) {
      _logger.d(message);
    }
  }

  static void i(String message) {
    _logger.i(message);
  }

  static void w(String message) {
    _logger.w(message);
  }

  static void e(String message, [dynamic error, StackTrace? stackTrace]) {
    _logger.e(message, error: error, stackTrace: stackTrace);
    // Itt küldhetnénk tovább a hibát Firebase Crashlytics-be vagy Sentry-be
    // if (!kDebugMode) {
    //   FirebaseCrashlytics.instance.recordError(error, stackTrace);
    // }
  }
}
```

#### Globális hiba képernyő és inicializálás (`lib/main.dart`)
```dart
import 'package:flutter/material.dart';
import 'package:flutter_prstart_hu/core/logger_service.dart'; // Virtuális import

void main() {
  // Globális Flutter hibák elkapása (pl. renderelési hibák)
  FlutterError.onError = (FlutterErrorDetails details) {
    LoggerService.e('Globális Flutter Hiba!', details.exception, details.stack);
  };

  // Globális UI összeomlás (vörös halálképernyő) felülírása egy szép kártyás felületre
  ErrorWidget.builder = (FlutterErrorDetails details) {
    return MaterialApp(
      home: Scaffold(
        body: Center(
          child: Padding(
            padding: const EdgeInsets.all(24.0),
            child: Card(
              color: Colors.red.shade50,
              elevation: 4,
              child: Padding(
                padding: const EdgeInsets.all(24.0),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    const Icon(Icons.error_outline, color: Colors.red, size: 64),
                    const SizedBox(height: 16),
                    const Text(
                      'Valami elromlott...',
                      style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: Colors.red),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      kReleaseMode 
                          ? 'Az alkalmazás váratlan hibát észlelt. A fejlesztőket értesítettük.'
                          : details.exception.toString(),
                      textAlign: TextAlign.center,
                      style: const TextStyle(fontSize: 14, color: Colors.black87),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ),
      ),
    );
  };

  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Production Ready App',
      home: const HomeScreen(),
    );
  }
}

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Kezdőlap')),
      body: Center(
        child: ElevatedButton(
          onPressed: () {
            LoggerService.i('Gomb megnyomva, hibát szimulálunk...');
            // Szándékos hiba generálása a teszteléshez
            throw StateError('Ez egy szimulált prezentációs hiba!');
          },
          child: const Text('Hiba előidézése'),
        ),
      ),
    );
  }
}
```

---

## Gyakorlófeladatok & Megoldások

### 1. feladat: Custom AppException osztály különböző alosztályokkal
Készíts egy zárt (`sealed`) `AppException` osztályt, aminek vannak dedikált alosztályai:
- `NetworkException` (üzenettel és HTTP státuszkóddal).
- `DatabaseException` (lokális SQL hibákhoz).
- `ValidationException` (mező-szintű űrlap hibákhoz).
Mindegyiknek legyen egy szép olvasható `toString()` megvalósítása.

#### Megoldás kódja (`lib/core/app_exception.dart`)
```dart
sealed class AppException implements Exception {
  final String message;

  const AppException(this.message);

  @override
  String toString() => message;
}

class NetworkException extends AppException {
  final int? statusCode;

  const NetworkException(super.message, {this.statusCode});

  @override
  String toString() => 'Hálózati Hiba ($statusCode): $message';
}

class DatabaseException extends AppException {
  final String query;

  const DatabaseException(super.message, {required this.query});

  @override
  String toString() => 'Adatbázis Hiba: $message (Lekérdezés: $query)';
}

class ValidationException extends AppException {
  final String fieldName;

  const ValidationException(super.message, {required this.fieldName});

  @override
  String toString() => 'Validációs Hiba [$fieldName]: $message';
}
```

#### Teszt kódja (`test/core/app_exception_test.dart`)
```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_prstart_hu/core/app_exception.dart';

void main() {
  group('AppException tesztek', () {
    test('NetworkException helyes formátumú toString-et ad', () {
      const ex = NetworkException('Szerver nem elérhető', statusCode: 500);
      expect(ex.toString(), equals('Hálózati Hiba (500): Szerver nem elérhető'));
    });

    test('DatabaseException helyes formátumú toString-et ad', () {
      const ex = DatabaseException('Egyedi kulcs megsértése', query: 'INSERT INTO users...');
      expect(ex.toString(), contains('Adatbázis Hiba'));
      expect(ex.toString(), contains('INSERT INTO users...'));
    });
  });
}
```

---

## Heti Mini Projekt: Production Readiness Audit

A projekt feladatod egy meglévő alkalmazás "élesítés előtti ellenőrzése" (Production Readiness Audit). Az alábbi lépéseket kell elvégezned és dokumentálnod:

1. **Linting:** Hozz létre egy egyedi `analysis_options.yaml` fájlt a fenti kódpélda alapján. Futtasd le a `flutter analyze` parancsot a projekten, és javítsd ki az összes jelzett hibát (pl. hiányzó `const` kulcsszavak, dinamikus típusok szigorítása).
2. **Katasztrófa-kezelés:** Implementáld a globális `ErrorWidget.builder` felülírást, hogy a felhasználók sose lássanak szürke/piros hibaképernyőket.
3. **Tesztlefedettség:** Futtasd le a teszteket lefedettség generálással, és ellenőrizd az eredményt a terminálban:
   ```bash
   flutter test --coverage
   ```
   A generált `coverage/lcov.info` fájlból határozd meg a kritikus üzleti logika lefedettségét (a cél legalább 80% lefedettség).

---

## Heti Ellenőrző Kérdések

### 1. Mi a különbség a print(), debugPrint(), és a log() (dart:developer) között?
- **`print()`:** Sima kimenet, ami a konzolra ír. Lassú, és a release buildben is fut, ami biztonsági kockázatot jelenthet.
- **`debugPrint()`:** A Flutter beépített wrapper függvénye, ami darabolja az üzeneteket, ha túl hosszúak (így az Android naplózója nem dobja el a sorokat), és testreszabható a viselkedése.
- **`log()`:** A `dart:developer` csomag része. Lehetővé teszi komplex adatszerkezetek küldését, szintek megadását, és nem szemeteli össze a konzolt, hanem közvetlenül a Dart DevTools naplójába küldi az információt.

### 2. Hogyan tudjuk elkerülni, hogy érzékeny adatok (pl. tokenek) kikerüljenek a logokba?
A logger szervizben vagy a HTTP kliens interceptorban szűrni kell a kimeneteket. Például a Dio interceptorban az `Authorization` headert vagy a `password` törzsadatot le kell maszkolni (pl. `***` helyettesítéssel), mielőtt kiíratnánk a konzolra vagy elküldenénk a hibakövető rendszerbe.

### 3. Mire jó a lints szabályoknál az avoid_print és a require_trailing_commas?
- **`avoid_print`:** Figyelmeztet, ha véletlenül benne felejtettél egy `print()` hívást, megóvva az alkalmazást a felesleges konzol-szemeteléstől és a biztonsági résektől.
- **`require_trailing_commas`:** Megköveteli, hogy minden többparaméteres függvény vagy widget konstruktor végén legyen vessző. Ezzel a `dart format` parancs sokkal szebben, függőlegesen tagolva rendezi át a kódot, javítva az olvashatóságot.

### 4. Mit csinál az ErrorWidget.builder és mikor fut le?
Az `ErrorWidget.builder` egy globális callback, ami akkor fut le, amikor a Flutter renderelő motorja hibát észlel egy widget `build()` metódusában (például null pointer hiba renderelés közben). Alapértelmezetten ez rajzolja ki a fejlesztés közben látható piros hátterű hibaüzenetet, de éles buildben ezt felül kell írnunk egy felhasználóbarát felülettel.

### 5. Hogyan tesztelhetjük a váratlan összeomlások kezelését?
A teszteléshez érdemes szimulálni a hibákat:
1. Egy gombnyomásra dobunk egy szándékos `StateError`-t vagy `TypeError`-t, és ellenőrizzük, hogy a globális `ErrorWidget` helyesen renderel-e.
2. Unit tesztekben a `throwsA` matchel ellenőrizzük, hogy a kódunk megfelelően kezeli és továbbdobja-e a várt kivételeket.
3. A Crashlytics integráció teszteléséhez az SDK rendelkezik egy `FirebaseCrashlytics.instance.crash()` metódussal, ami azonnali natív összeomlást idéz elő a teszteléshez.
