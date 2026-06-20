# -*- coding: utf-8 -*-
import os

WEEKS_DIR = '/home/alphaws/Dev/Projects/flutter_prstart_hu/assets/weeks'
os.makedirs(WEEKS_DIR, exist_ok=True)

def write_file(filename, content):
    filepath = os.path.join(WEEKS_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content.strip())
    print(f"Generated {filename}")

# ==========================================
# 1. Daily Study Routines (7 files)
# ==========================================
routines = {
    "page-hetfo-uj-elmelet.md": """# Hétfő — Új elmélet

Minden sikeres tanulási hét alapja a hétfői nap, amikor az új elméleti anyaggal és koncepciókkal ismerkedünk meg. Ezen a napon nem a rohamtempójú kódolás a cél, hanem a megértés és a stabil alapok lerakása.

## 📅 Napi Beosztás (Javasolt)
* **30 perc olvasás:** Tanulmányozd a heti elméletet, a kapcsolódó fogalmakat és a hivatalos dokumentációt.
* **60 perc kódpélda:** Írd be kézzel a leckében található példakódokat. Ne másold, hanem gépeld, mert így rögzül a szintaxis.
* **30 perc jegyzet:** Írd le a saját szavaiddal a tanultakat, különös tekintettel a nehezebb részekre és a feltett kérdéserre.

## 💡 Tippek a Hatékony Tanuláshoz
> [!TIP]
> * **Kapcsold ki a zavaró tényezőket:** A mobiltelefonodat és a közösségi médiát tedd félre a fókuszált tanulási idő alatt.
> * **Ne csak másolj:** Ha egy kódpéldát beírsz, próbáld megváltoztatni a változók értékét, nézd meg, mi történik, ha szándékosan hibát ejtesz.
> * **Használd a hivatalos doksit:** A Flutter és Dart hivatalos dokumentációja rendkívül részletes és pontos. Szokj hozzá a használatához már az első naptól kezdve!

---

> [!NOTE]
> A hétfői nap megalapozza az egész heti haladásodat. Ha itt alapos vagy, a keddi gyakorlás és a szerdai mini projekt sokkal könnyebben fog menni!
""",
    "page-kedd-gyakorlas-es-melyites.md": """# Kedd — Gyakorlás és mélyítés

A keddi nap a hétfőn tanult elmélet elmélyítéséről szól. Ezen a napon kisebb gyakorlófeladatokon keresztül sajátítjuk el a szintaxist és a widgetek működését, valamint finomítjuk a megírt kódokat.

## 📅 Napi Beosztás (Javasolt)
* **60-90 perc kódolás:** Oldj meg 3-5 kisebb, fókuszált programozási feladatot a hétfői témakörben.
* **20 perc refaktorálás:** Nézd át a megírt kódjaidat, és próbáld meg szebbé, olvashatóbbá tenni őket.
* **10 perc Git commit:** Commitold a napi előrehaladásodat a verziókövetőbe megfelelő commit üzenetekkel.

## 🛠️ Gyakorlati Irányelvek
> [!IMPORTANT]
> * **Törekedj a tiszta kódra:** Figyelj a helyes elnevezésekre, a formázásra és a felesleges ismétlések elkerülésére.
> * **Kísérletezz:** Próbálj ki alternatív megvalósításokat is ugyanarra a feladatra.
> * **Kérdezz:** Ha elakadsz, nézz utána a hibakódnak vagy kérj segítséget a közösségtől.

---

> [!TIP]
> **Profi tipp:** Használd a `dart format .` parancsot a kódod automatikus formázásához, így a kódod mindig professzionális megjelenésű lesz.
""",
    "page-szerda-sajat-mini-projekt.md": """# Szerda — Saját mini projekt

A szerdai napon egy önálló, működőképes mini funkciót vagy alkalmazást készítünk el a hét elméleti anyaga alapján. Ez segít összekötni a különálló ismereteket egy nagyobb egésszé.

## 📅 Napi Beosztás (Javasolt)
* **15 perc tervezés:** Határozd meg a mini projekt funkcióit és rajzold le az UI vázlatát.
* **75 perc fejlesztés:** Írd meg a logikát és építsd fel a felületet.
* **30 perc hibakezelés:** Teszteld le a szélsőséges eseteket (pl. üres bemenet, nagy számok) és kezeld a lehetséges hibákat.

## ✨ Elvárt Elemek a Mini Projektben
* **Tiszta UI állapotok:** Legyen felkészítve a felület a betöltésre, az üres állapotra és a hibaállapotra is.
* **Megfelelő modularitás:** Ne ömleszd a teljes kódot egyetlen fájlla, válaszd szét a komponenseket.
* **Git dokumentáció:** Hozz létre egy rövid leírást a projekt mappájában.

---

> [!NOTE]
> Egy működő mini projekt a hét közepén hatalmas motivációs löketet ad a folytatáshoz!
""",
    "page-csutortok-kodolvasas-es-refaktoralas.md": """# Csütörtök — Kódolvasás és refaktorálás

A csütörtöki napot a kódminőség javításának, a tesztelésnek és mások kódjának olvasásának szenteljük. Ez a nap segít abban, hogy a kódod ne csak működjön, de karbantartható is legyen.

## 📅 Napi Beosztás (Javasolt)
* **30 perc kódolvasás:** Keress nyílt forrású Flutter projekteket GitHubon, és nézd meg, mások hogyan oldották meg a heti feladatot.
* **60 perc refaktorálás és kódminőség:** Javítsd ki a linter figyelmeztetéseket, formázd a kódot, és egyszerűsítsd a túl bonyolult metódusokat.
* **30 perc tesztelés:** Írj alapvető unit és widget teszteket a hét során írt kódjaidhoz.

## 🔍 Ellenőrzőlista refaktoráláshoz
1. **Nincsenek figyelmeztetések:** A `flutter analyze` parancs nem adhat hibát vagy figyelmeztetést.
2. **Nincs kódduplikáció:** A többször leírt kódokat szervezd ki reusable widgetekbe vagy helper függvényekbe.
3. **Megfelelő elnevezések:** A változók és metódusok nevei egyértelműen tükrözik a feladatukat.

---

> [!IMPORTANT]
> A jó programozó nemcsak kódot írni tud, hanem mások kódját olvasni és a meglévő kódot tisztítani is!
""",
    "page-pentek-hetvegi-projekt-elokeszitese.md": """# Péntek — Hétvégi projekt előkészítése

A pénteki napon felkészülünk a hétvégi nagyobb lélegzetvételű projektmunkára. Megtervezzük a projekt architektúráját, tisztázzuk a követelményeket és elindítjuk a fejlesztést.

## 📅 Napi Beosztás (Javasolt)
* **20 perc specifikáció:** Írd le pontról pontra, mit fog tudni a hétvégi alkalmazás.
* **30 perc UI tervezés:** Rajzold le a képernyőket és a navigációs folyamatokat papíron vagy tervezőprogramban (pl. Figma).
* **70 perc kezdeti fejlesztés:** Hozd létre a projektet, állítsd be a Git adattárat, telepítsd a függőségeket és készítsd el az alap elrendezést.

## 🚀 Kezdőlépések Péntekre
> [!TIP]
> * **Git branch:** Hozz létre egy új branch-et a hétvégi projektnek (pl. `feature/weekend-project`).
> * **Mappa struktúra:** Alakítsd ki a tiszta mappaszerkezetet (`lib/models`, `lib/screens`, `lib/widgets` stb.) már a legelején.
> * **Készíts vázlatot:** Kódold le a legfőbb képernyők üres Scaffold vázát, hogy szombaton már csak a tartalommal kelljen foglalkoznod.

---

> [!NOTE]
> A jó előkészület fél siker. Egy jól átgondolt pénteki specifikáció megkímél a hétvégi felesleges újratervezéstől!
""",
    "page-szombat-projekt-nap.md": """# Szombat — Projekt nap

A szombat a hét legintenzívebb napja. Ezen a napon egy komplex, önálló portfólió-értékű alkalmazást építünk fel a hét során tanult összes ismeret ötvözésével.

## 📅 Napi Beosztás (Javasolt)
* **Délelőtt (2-3 óra):** Az alkalmazás magjának fejlesztése, üzleti logika megírása, képernyők felépítése.
* **Délután (2 óra):** Integráció, navigáció finomítása, stílusok és témák finomhangolása.
* **Késő délután (1 óra):** Tesztelés valódi eszközön, hibajavítás, README írása és végső verzió commitolása GitHubra.

## 🎯 Záró projekt elvárások
* **Gördülékeny működés:** Ne legyenek összeomlások, a görgetés legyen sima.
* **Dizájn:** Használj konzisztens színpalettát, árnyékokat és megfelelő térközöket.
* **Bemutatás:** Készíts screenshotokat és írd le a README-ben, hogyan kell futtatni az alkalmazást.

---

> [!IMPORTANT]
> A szombati projekt a te egyéni névjegyed. Ezzel bizonyítod, hogy az elméletet képes vagy valós alkalmazássá formálni!
""",
    "page-vasarnap-piheno-vagy-konnyu-otleteles.md": """# Vasárnap — Pihenő vagy könnyű ötletelés

A vasárnap a pihenésé és a feltöltődésé. Emellett szánhatsz egy kevés időt inspirálódásra, új alkalmazásötletek gyűjtésére vagy a következő hét céljainak kitűzésére.

## 📅 Napi Program (Javasolt)
* **Teljes kikapcsolódás:** Pihend ki a hét fáradalmait, hogy frissen kezdd a következő hetet.
* **Inspiráció gyűjtés (opcionális):** Nézegess dizájnokat Dribbble-en vagy Behance-en, próbálj ki sikeres mobilappokat a piacról.
* **Tervezés:** Vess egy pillantást a következő hét tananyagára, hogy tudd, mire kell készülnöd.

## 💡 Hogyan kerüld el a kiégést?
> [!TIP]
> * **Ne kódolj vasárnap:** Adj időt az agyadnak, hogy feldolgozza a héten tanult hatalmas mennyiségű információt.
> * **Menj a szabadba:** A mozgás és a friss levegő segít tisztázni a gondolatokat.
> * **Ötletelj stressz nélkül:** Írd fel egy füzetbe az eszedbe jutó alkalmazásötleteket, de ne kezdd el azonnal lefejleszteni őket.

---

> [!NOTE]
> A pihenés ugyanolyan fontos része a tanulási folyamatnak, mint a kódolás. A regenerálódott elme sokkal gyorsabban tanul!
"""
}

# ==========================================
# 2. Skill Map Levels (3 files)
# ==========================================
skills = {
    "page-junior-szint.md": """# Junior szint

A Junior szint a fejlesztői karrier kezdete. Ezen a szinten a legfőbb cél, hogy képes legyél önállóan, egyértelmű specifikáció alapján egyszerűbb Flutter alkalmazásokat elkészíteni és azokat alap szinten karbantartani.

## 🛠️ Elvárt Technikai Tudás
* **Dart alapok:** Változók, típusok, alapvető gyűjtemények (List, Map), OOP alapok, Null Safety magabiztos kezelése.
* **UI fejlesztés:** Alapvető widgetek (Column, Row, Container, Stack, ListView) ismerete és reszponzív elrendezések készítése.
* **Navigáció:** Képernyők közötti navigáció megvalósítása Navigator 1.0-val és egyszerű argumentumátadás.
* **Adatbevitel:** Formok készítése, beviteli mezők validálása és hibaüzenetek kezelése.
* **Hálózati kommunikáció:** HTTP kérések (GET, POST) indítása, JSON válaszok parszolása és modellekké alakítása.
* **Állapotkezelés:** A `setState` használata és az állapotkezelés elméleti alapjainak ismerete.

## 📂 Junior Portfólió Elvárások
1. **Todo / Teendőkezelő alkalmazás:** Helyi állapottal, szűréssel és szép dizájnnal.
2. **Időjárás előrejelző app:** API használatával, keresési lehetőséggel és loading/error állapotokkal.
3. **Receptkönyv alkalmazás:** Többképernyős navigációval, receptrészletezővel és kedvencnek jelölési opcióval.

---

> [!IMPORTANT]
> Junior szinten a legfontosabb erény a tanulási vágy, a visszajelzések elfogadása és a tiszta, linter-hibáktól mentes kód írása.
""",
    "page-medior-szint.md": """# Medior szint

A Medior szinten már elvárás a strukturált, skálázható alkalmazások tervezése és fejlesztése. Képesnek kell lenned összetettebb architektúrákban gondolkodni, state management rendszereket használni és teszteket írni.

## 🛠️ Elvárt Technikai Tudás
* **Architektúra:** Feature-alapú mappaszerkezet kialakítása, Clean Code elvek és a Repository Pattern alkalmazása.
* **State Management:** Riverpod vagy BLoC rendszerek mély, készségszintű ismerete és alkalmazása.
* **Biztonság és Autentikáció:** Token-alapú bejelentkezés (JWT), secure storage használata, interceptorok beállítása.
* **Adattárolás:** Helyi adatbázisok (pl. Isar, Hive, Drift) integrálása, cache stratégiák megvalósítása.
* **Tesztelés:** Egységtesztek (Unit Test) és widget tesztek írása mock adatok segítségével.
* **Kódminőség:** Git workflow (Git Flow, Commit konvenciók) és szigorú lint szabályok betartása.

## 📂 Medior Portfólió Elvárások
1. **Adminisztrációs mobilalkalmazás:** Valós tokenes autentikációval, Dio interceptorral és szerepkör-alapú UI elemekkel.
2. **Offline Jegyzetelő app:** Teljes körű helyi adatbázis kezeléssel, szinkronizációs képességekkel és kereséssel.
3. **Térképes szolgáltatáskereső:** GPS koordináták lekérésével, Google Maps integrációval és jogosultságkezeléssel.

---

> [!TIP]
> **Profi tipp:** Medior szinten törekedj arra, hogy a UI réteged teljesen független legyen az üzleti logikától, így a kódod könnyen tesztelhetővé válik.
""",
    "page-senior-profi-szint.md": """# Senior/profi szint

A Senior szinten a fejlesztő már technológiai döntéshozó, mentor és az alkalmazás architektúrájának legfőbb felelőse. Képes nagy terhelésű, biztonságos, offline-first rendszereket tervezni és a publikálási folyamatokat teljesen automatizálni.

## 🛠️ Elvárt Technikai Tudás
* **Haladó Architektúra:** Clean Architecture szigorú betartása rétegek közötti határokkal.
* **DevOps / CI/CD:** GitHub Actions pipeline-ok építése, automatizált tesztelés, linting és build generálás.
* **Offline-first szinkronizáció:** Komplex helyi adatbázis szinkronizáció távoli szerverrel, konfliktuskezelési stratégiák megvalósítása.
* **Natív Integráció:** Platform Csatornák (MethodChannel) írása natív Kotlin (Android) és Swift (iOS) kódok eléréséhez.
* **Teljesítmény Optimalizálás:** DevTools profilozás, memóriaszivárgások detektálása, Isolate-ok használata nehéz számításokhoz.
* **Publikálás:** Google Play Store és Apple App Store publikálási folyamatok kezelése, staged rollout, ProGuard beállítások.

## 📂 Senior Portfólió Elvárások
1. **Raktárkezelő / ERP mobil app:** Vonalkódolvasással, háttér szinkronizációval és offline írási sorral (Sync Queue).
2. **Okosotthon Vezérlő app:** Valós idejű MQTT/Websocket kommunikációval, push értesítésekkel és widgetekkel.
3. **Komplex Oktatási Platform (LMS) app:** Letölthető offline tartalmakkal, titkosított adattárolással és teljes tesztlefedettséggel.

---

> [!NOTE]
> A Senior szint nemcsak a kódolásról szól, hanem a skálázható csapatmunka kialakításáról és a technológiai kockázatok minimalizálásáról is.
"""
}

# ==========================================
# 3. Recommended Packages (10 files)
# ==========================================
packages = {
    "page-routing.md": """# Routing

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
""",
    "page-state-management.md": """# State management

Az állapotkezelés határozza meg, hogyan áramlik az adat az alkalmazásodban, és mikor épülnek újra a felhasználói felület elemei.

## 📦 Ajánlott Csomagok:
1. **`flutter_riverpod` (Modern / Ajánlott):** Tiszta, típusbiztos, nem függ a BuildContext-től, kiválóan tesztelhető és támogatja a Dependency Injection-t.
2. **`flutter_bloc` / `bloc` (Enterprise):** Esemény-vezérelt (Event-State) architektúra, szigorúan strukturált, nagy csapatok számára ideális.
3. **`provider` (Egyszerűbb appokhoz):** A klasszikus állapotkezelő, jó a ChangeNotifier alapú mintákhoz.

### Riverpod Példa:
```dart
// Állapot definiálása
final counterProvider = StateProvider<int>((ref) => 0);

// Widgetben használat
class CounterWidget extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final count = ref.watch(counterProvider);
    return ElevatedButton(
      onPressed: () => ref.read(counterProvider.notifier).state++,
      child: Text('Számláló: $count'),
    );
  }
}
```
""",
    "page-http-api.md": """# HTTP/API

A külső backend szerverekkel való kommunikáció a mobilalkalmazások többségének alapfeltétele.

## 📦 Ajánlott Csomagok:
* **`dio`:** Rendkívül robusztus HTTP kliens, amely támogatja az interceptorokat, globális konfigurációkat, fájl feltöltést, timeout kezelést és kérések megszakítását.
* **`pretty_dio_logger`:** Fejlesztés során gyönyörűen formázva naplózza a konzolra a kéréseket és válaszokat.

### Dio interceptor példa:
```dart
final dio = Dio();
dio.interceptors.add(InterceptorsWrapper(
  onRequest: (options, handler) {
    // Token hozzáadása minden kéréshez
    options.headers['Authorization'] = 'Bearer $token';
    return handler.next(options);
  },
));
```
""",
    "page-modellezes.md": """# Modellezés

A Dart nyelvben az immutable (módosíthatatlan) adatstruktúrák és a típusbiztosság kiemelt fontosságúak. A kézzel írt JSON szerializáció viszont sok hibalehetőséget rejt.

## 📦 Ajánlott Csomagok:
* **`freezed`:** Kódgenerátor immutable osztályokhoz, amely automatikusan elkészíti a `copyWith`, `toString`, `operator ==` metódusokat és támogatja a union típusokat.
* **`json_serializable`:** Létrehozza a `fromJson` és `toJson` konverziós függvényeket.

### Freezed Példa:
```dart
@freezed
class User with _$User {
  const factory User({
    required String id,
    required String name,
    required String email,
    @Default(false) bool isAdmin,
  }) = _User;

  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
}
```
""",
    "page-lokalis-adattarolas.md": """# Lokális adattárolás

Az adatok helyi mentése szükséges beállítások, offline működés és gyorsabb betöltési idők eléréséhez.

## 📦 Ajánlott Csomagok:
* **`shared_preferences`:** Egyszerű kulcs-érték párok tárolása (pl. sötét mód beállítása).
* **`flutter_secure_storage`:** Érzékeny adatok (pl. JWT tokenek) titkosított tárolása az eszköz biztonságos hardverében.
* **`isar` vagy `hive`:** Ultragyors NoSQL objektum-adatbázisok lokális adathalmazok tárolására.
* **`drift` (sqflite wrapper):** Relációs SQL adatbázis Dart nyelven, típusbiztos lekérdezésekkel.

### Döntési táblázat:
| Adat Típusa | Ajánlott Megoldás |
|---|---|
| Beállítások, flag-ek | `shared_preferences` |
| API Tokenek, jelszavak | `flutter_secure_storage` |
| Offline adatok, listák | `isar` vagy `hive` |
| Komplex relációk | `drift` |
""",
    "page-ui.md": """# UI

A modern felhasználói élményhez elengedhetetlenek a szép grafikák, ikonok, animációk és a gyors képbetöltés.

## 📦 Ajánlott Csomagok:
* **`flutter_svg`:** SVG formátumú vektoros grafikák renderelése minőségromlás nélkül.
* **`cached_network_image`:** Képek letöltése távoli URL-ről, automatikus helyi cache-eléssel és betöltési animációk (shimmer) támogatásával.
* **`shimmer`:** Modern betöltési animáció a tartalom megjelenése előtt (skeleton screen).
* **`lottie`:** Adobe After Effects-ben készített interaktív animációk lejátszása json fájlokból.
""",
    "page-eszkozfunkciok.md": """# Eszközfunkciók

A mobiltelefon beépített képességeinek elérése és a jogosultságok helyes kezelése.

## 📦 Ajánlott Csomagok:
* **`permission_handler`:** Egységes jogosultságkérő felület Androidon és iOS-en (kamera, GPS, értesítések).
* **`image_picker`:** Képek vagy videók készítése kamerával, illetve kiválasztása a galériából.
* **`geolocator`:** Az eszköz aktuális GPS koordinátáinak lekérése.
* **`connectivity_plus`:** A hálózari kapcsolat állapotának (Wifi, Mobilnet, Offline) valós idejű figyelése.
""",
    "page-firebase.md": """# Firebase

A Google Firebase platformja számtalan kész megoldást kínál szerveroldali infrastruktúra kiépítése nélkül.

## 📦 Ajánlott Csomagok:
* **`firebase_core`:** A Firebase SDK inicializálása az alkalmazásban.
* **`firebase_auth`:** Felhasználói fiókok kezelése, email/jelszó bejelentkezés, közösségi bejelentkezések (Google, Apple).
* **`cloud_firestore`:** Valós idejű, felhőalapú NoSQL adatbázis.
* **`firebase_messaging`:** Push értesítések fogadása.
* **`firebase_crashlytics`:** Automatikus hibajelentések küldése fejlesztés és éles működés során.
""",
    "page-teszt.md": """# Teszt

A minőségi kódbázis ismérve a megfelelő tesztlefedettség, amely megvéd a meglévő funkciók elromlásától (regresszió).

## 📦 Ajánlott Csomagok:
* **`mocktail`:** Rendkívül tiszta, null-safety kompatibilis mocking könyvtár, amellyel szimulálhatjuk a repositoryk vagy API kliensek működését.
* **`integration_test`:** A Flutter beépített csomagja, amellyel teljes E2E (End-to-End) folyamatokat futtathatunk emulátoron vagy fizikai eszközön.
""",
    "page-minoseg.md": """# Minőség

Az egységes kódolási stílus és a linter szabályok betartása elengedhetetlen a csapatmunkához és a hosszú távú karbantarthatósághoz.

## 📦 Ajánlott Csomagok:
* **`flutter_lints`:** A Flutter csapat által javasolt alapvető linter szabálygyűjtemény.
* **`very_good_analysis`:** Szigorúbb, professzionális linter szabályok az egységes kódstílusért.
"""
}

# ==========================================
# 4. Project Ideas (4 files)
# ==========================================
projects = {
    "page-6-1-sephir-erp-mobil-app.md": """# 6.1 Sephir ERP mobil app

A Sephir ERP mobil companion alkalmazása egy professzionális, éles piaci igényekre szabott üzleti alkalmazás. Célja, hogy a kkv-k munkatársai a raktárban vagy a terepen is elérjék az ERP rendszer legfontosabb adatait.

## 🎯 Fő Funkciók
* **Workspace választás:** Támogatja a több telephelyes vagy több céges struktúrák közötti egyszerű váltást.
* **Termék- és Partnerlista:** Gyors keresés, szűrés, kategóriák és valós idejű készletinformációk.
* **Rendelés felvitel:** Új értékesítési rendelések összeállítása és beküldése közvetlenül a vevőnél.
* **Raktárkezelés és Vonalkódolvasás:** Beépített kamera vagy hardveres olvasó segítségével történő leltározás és árukiadás.
* **Offline-first működés:** Hálózati kapcsolat hiányában is rögzíthetők a bizonylatok, amelyek a kapcsolat visszatérésekor automatikusan szinkronizálódnak.

## 🏗️ Architektúra és Technológiák
* **Állapotkezelés:** Riverpod az aszinkron adatok és a kosár állapotának menedzselésére.
* **Helyi Adatbázis:** Isar az offline adatok gyors és relációs tárolására.
* **Hálózat:** Dio interceptorokkal a JWT tokenek automatikus frissítésére és a kérések naplózására.
""",
    "page-6-2-oktatasi-app-prstart-hu-hoz.md": """# 6.2 Oktatási app prstart.hu-hoz

Ez az alkalmazás a prstart.hu e-learning és LMS platformjához kapcsolódó mobil kliens. Célja, hogy a tanulók bárhol, akár utazás közben, offline is hozzáférjenek a kurzusaikhoz és elvégezhessék a leckéket.

## 🎯 Fő Funkciók
* **Kurzusok és Tantárgyak:** A felvett kurzusok listája, tematikus modulok és leckék fája.
* **Offline Lecke mentés:** Videók és szöveges tananyagok letöltése helyi tárhelyre offline tanuláshoz.
* **Interaktív Kvízek:** Leckék utáni feleletválasztós és párosítós tesztek kitöltése azonnali kiértékeléssel.
* **Fejlődési Statisztikák:** Vizuális statisztika a haladásról, napi célok kitűzése és jelvények (gamifikáció).
* **Gyerekbarát UI:** Letisztult, nagy kontrasztú, modern dizájn mikro-animációkkal.

## 🏗️ Architektúra és Technológiák
* **Navigáció:** GoRouter nested navigation (ShellRoute) a tabos alsó menürendszerhez.
* **UI elemek:** Lottie animációk a sikeres kvízek ünneplésére, Shimmer a betöltési állapotokhoz.
* **Adattárolás:** SQLite/Drift a tanulói eredmények és leckestátuszok helyi vezetésére.
""",
    "page-6-3-okosotthon-mobil-app.md": """# 6.3 Okosotthon mobil app

Az okosotthon alkalmazás egy modern, valós idejű IoT (Internet of Things) vezérlőfelület. Lehetővé teszi a lakásban található eszközök (lámpák, termosztátok, kamerák) megtekintését és vezérlését.

## 🎯 Fő Funkciók
* **Szobák és Csoportok:** Eszközök csoportosítása helyiségek (Nappali, Konyha stb.) szerint.
* **Valós idejű Kapcsolók:** Eszközök státuszának azonnali módosítása és visszajelzése.
* **Fogyasztási Statisztikák:** Dinamikus grafikonok a ház energia- és vízfelhasználásáról.
* **Biztonsági Kamerák:** IP kamerák RTSP streamjének alacsony késleltetésű megjelenítése.
* **MQTT / WebSocket integráció:** Kétirányú, valós idejű adatkapcsolat az otthoni szerverrel.

## 🏗️ Architektúra és Technológiák
* **Állapotkezelés:** BLoC minta az eseményalapú állapotváltások (pl. lámpa felkapcsolás gombnyomásra) precíz modellezésére.
* **Hálózat:** Native WebSocket és MQTT kliensek integrálása a Flutter eseményfolyamokba (Streams).
* **UI:** CustomPainter az egyedi termosztát szabályozó tárcsa megrajzolásához.
""",
    "page-6-4-raktarkezelo-vonalkodos-app.md": """# 6.4 Raktárkezelő / vonalkódos app

A raktárkezelő mobilapp egy célirányos ipari célszoftver, amely a raktárosok napi munkáját (bevételezés, kiszedés, áthelyezés) támogatja vonalkód- és QR-kód olvasással.

## 🎯 Fő Funkciók
* **Termékkeresés:** Villámgyors keresés cikkszám, név vagy vonalkód alapján.
* **Vonalkód-olvasás:** A kamera képének folyamatos elemzése és a leolvasott kód azonnali feldolgozása.
* **Készletmódosítás:** Mennyiségek korrekciója, sérült termékek leírása közvetlenül a polcok mellett.
* **Offline írási sor (Sync Queue):** Hálózati hiba esetén a beolvasások lokálisan tárolódnak, majd a kapcsolat helyreállásakor szinkronizálódnak.
* **Raktáros Jogosultságok:** Egyszerűsített felület PIN-kódos vagy ujjlenyomatos gyors belépéssel.

## 🏗️ Architektúra és Technológiák
* **Olvasó:** `mobile_scanner` vagy Google ML Kit csomag a gyors kódleolvasáshoz.
* **Helyi adat:** Hive adatbázis a szupergyors íráshoz és az offline tranzakciós sor tárolásához.
* **Tesztelés:** Szigorú egységtesztek a szinkronizációs és konfliktuskezelési logika lefedésére.
"""
}

# ==========================================
# 5. Self-Assessment Exams (6 files)
# ==========================================
exams = {
    "page-1-szint-alap.md": """# 1. szint — Alap

Ezen a szinten azt ellenőrizzük, hogy sikerült-e elsajátítanod a Dart nyelv alapvető szintaxisát és a legegyszerűbb helyi perzisztens tárolást.

## 🎯 Vizsga Feladatok
Készíts egy egyképernyős Flutter alkalmazást, amely:
1. **Név bekérése:** Tartalmaz egy TextField-et, ahol a felhasználó megadhatja a nevét.
2. **Mentés lokálisan:** Egy 'Mentés' gomb megnyomására elmenti ezt a nevet helyben `shared_preferences` segítségével.
3. **Betöltés induláskor:** Az alkalmazás újraindítása után automatikusan beolvassa a mentett nevet és megjeleníti egy üdvözlő kártyán.
4. **Theme váltás:** Tartalmaz egy kapcsolót (Switch) a sötét és világos mód kézi váltásához.

## 🔍 Értékelési Szempontok
* A kód tiszta és mentes a `flutter analyze` figyelmeztetésektől.
* A név mentése és betöltése hibátlanul lefut üres értékek esetén is.
* A sötét mód azonnal érvényesül az egész felületen.
""",
    "page-2-szint-ui.md": """# 2. szint — UI

A vizsga célja annak bizonyítása, hogy képes vagy összetettebb, reszponzív és esztétikus felhasználói felületeket (UI) felépíteni statikus adatok alapján.

## 🎯 Vizsga Feladatok
Készíts egy termékkatalógus alkalmazást az alábbi két képernyővel:
1. **Katalógus oldal:**
   * Kategória választó chipek a lap tetején.
   * Termékek rácsos elrendezése (GridView) kép, név, ár és egy 'kedvenc' ikon megjelenítésével.
   * Keresősáv a termékek közötti gyors szűréshez.
2. **Részletező oldal:**
   * A termék nagy képe, leírása és kosárba helyezés gomb.
   * Gördülékeny átmenet a két képernyő között (Hero animáció használatával).

## 🔍 Értékelési Szempontok
* **Reszponzivitás:** A grid mobilon 2, míg széles kijelzőn 4 oszlopos legyen.
* **Overflow mentesség:** A szövegek nem lóghatnak ki a kártyákból, a billentyűzet felnyílása nem okozhat hibát.
* **Esztétika:** Használj kupacban spacinget, lekerekítéseket és színeket.
""",
    "page-3-szint-api.md": """# 3. szint — API

Ez a szint azt méri fel, hogyan tudsz összekötni egy mobilalkalmazást egy távoli REST API backenddel, és hogyan kezeled az aszinkron folyamatokat.

## 🎯 Vizsga Feladatok
Készíts egy alkalmazást, amely:
1. **Adatok lekérése:** Adatokat kér le egy szabadon választható publikus JSON API-ból (pl. JSONPlaceholder vagy saját backend).
2. **Három állapot kezelése:**
   * **Loading:** Amíg az adat töltődik, egy Shimmer vagy CircularProgressIndicator látható.
   * **Success:** Sikeres lekéréskor a lista elemei szépen megjelennek egy kártyás listában.
   * **Error:** Hálózati hiba vagy rossz válasz esetén egy hibaüzenet és egy 'Újrapróbálás' (Retry) gomb látható.
3. **Frissítés:** Swipe-to-refresh (RefreshIndicator) támogatása a lista frissítésére.

## 🔍 Értékelési Szempontok
* Az API kérés aszinkron (`async/await`) módon fut le és nem blokkolja az UI szálat.
* A hálózati hibák (pl. offline állapot) nem okoznak app-összeomlást.
""",
    "page-4-szint-auth.md": """# 4. szint — Auth

A vizsga fókuszában a felhasználói beléptetés, a tokenek biztonságos tárolása és a védett útvonalak (Protected Routes) kezelése áll.

## 🎯 Vizsga Feladatok
Valósítsd meg az alábbi biztonsági modult:
1. **Bejelentkező oldal:** Email és jelszó mezők validációval, hibaüzenetek megjelenítésével.
2. **Secure Token storage:** Sikeres bejelentkezés után a kapott JWT tokent mentsd el a `flutter_secure_storage` csomaggal.
3. **Protected Route:** Ha van mentett érvényes token, az app induláskor azonnal vigye a felhasználót a védett profil oldalra.
4. **Kijelentkezés:** Törölje a mentett tokent a storage-ból és vigye vissza a felhasználót a bejelentkező felületre.

## 🔍 Értékelési Szempontok
* A token soha nem kerül sima (nem titkosított) Shared Preferences-be.
* A nem hitelesített felhasználók semmilyen trükkel nem érhetik el a védett profil oldalt.
""",
    "page-5-szint-offline.md": """# 5. szint — Offline

A vizsga célja egy olyan offline-first alkalmazás létrehozása, amely hálózati kapcsolat nélkül is teljes értékűen használható adatbevitelre.

## 🎯 Vizsga Feladatok
Készíts egy offline jegyzetkezelő alkalmazást:
1. **Helyi Adatbázis:** A jegyzeteket tárold el egy helyi NoSQL vagy SQL adatbázisban (Isar, Hive vagy Drift).
2. **Offline CRUD:** Támogasd a jegyzetek létrehozását, szerkesztését és törlését hálózat nélkül is.
3. **Kapcsolat figyelés:** Figyeld a hálózati kapcsolatot (`connectivity_plus`). Kapcsolat visszatérésekor küldj egy szimulált szinkronizációt a szerverre és jeleníts meg egy sikeres szinkron státuszjelzőt.

## 🔍 Értékelési Szempontok
* Az adatok azonnal mentődnek a helyi adatbázisba, az alkalmazás bezárása után sem vesznek el.
* A szinkronizációs folyamat a háttérben fut le, nem zavarja az épp gépelő felhasználót.
""",
    "page-6-szint-profi.md": """# 6. szint — Profi

Ez a záróvizsga. Itt egy komplex, ipari szabványoknak megfelelő, teljesen letesztelt és kiadásra előkészített alkalmazást kell bemutatnod.

## 🎯 Záró projekt követelmények
* **Architektúra:** Clean Architecture szigorú betartása (UI, Domain, Data rétegek szétválasztása).
* **State Management:** Riverpod vagy BLoC használata tiszta Dependency Injection mintákkal.
* **Tesztlefedettség:** Legalább 30 unit és widget teszt, amelyek lefedik az üzleti logikát és a főbb felületeket.
* **CI/CD:** Beállított GitHub Actions pipeline, amely minden pull requestnél lefut (format, analyze, test).
* **Release:** Aláírt, kiadásra kész Android App Bundle (AAB) és debug banner mentes release build.
* **Dokumentáció:** Részletes README leírással, képernyőképekkel és architektúra diagrammal.

## 🔍 Értékelési Szempontok
* A projekt struktúrája professzionális, könnyen átlátható külső fejlesztők számára is.
* Nincsenek figyelmen kívül hagyott teszthibák vagy analyze warningok.
"""
}

# ==========================================
# 6. Command Cheatsheets (8 files)
# ==========================================
commands = {
    "page-projekt.md": """# Projekt

A Flutter projektek indításának és tesztkörnyezetben való futtatásának legalapvetőbb parancsai.

## 🛠️ Parancsok:
* **Projekt generálása:**
  ```bash
  flutter create --org hu.prstart my_app
  ```
  A `--org` paraméter határozza meg a csomagnevet (package name), ami a Play Áruházban egyedi azonosító lesz (pl. `hu.prstart.my_app`).

* **Alkalmazás indítása:**
  ```bash
  flutter run
  ```
  Elindítja az alkalmazást a kiválasztott emulátoron vagy telefonon debug módban, támogatva a Hot Reload funkciót.

* **Futtatás adott eszközön:**
  ```bash
  flutter run -d <device_id>
  ```
""",
    "page-csomag-hozzaadasa.md": """# Csomag hozzáadása

A Flutter projektünkhöz a pub.dev-en található külső csomagokat a pub parancsokkal tudjuk hozzáadni.

## 🛠️ Parancsok:
* **Csomag hozzáadása:**
  ```bash
  flutter pub add dio
  ```
  Ez a parancs automatikusan beírja a legfrissebb kompatibilis verziót a `pubspec.yaml` fájl `dependencies` szekciójába, és le is tölti azt.

* **Függőségek letöltése manuálisan:**
  ```bash
  flutter pub get
  ```
  Használd ezt a parancsot, ha a `pubspec.yaml` fájlt kézzel szerkesztetted vagy frissen húztad le a projektet Git-ről.
""",
    "page-dev-dependency.md": """# Dev dependency

A fejlesztési függőségek olyan eszközök, amelyekre csak a kód írásakor, generálásakor vagy tesztelésekor van szükség, az elkészült éles appba (build) nem kerülnek bele.

## 🛠️ Parancsok:
* **Fejlesztési csomag hozzáadása:**
  ```bash
  flutter pub add --dev build_runner
  ```
  Beírja a csomagot a `pubspec.yaml` fájl `dev_dependencies` szekciójába.

* **Tipikus dev függőségek:**
  * `build_runner` (kódgeneráláshoz)
  * `freezed` és `json_serializable` (modellezéshez)
  * `mocktail` (teszteléshez)
""",
    "page-kodgeneralas.md": """# Kódgenerálás

Sok Flutter csomag (pl. freezed, drift, retrofit) kódgenerálást használ a típusbiztos kód automatikus előállításához.

## 🛠️ Parancsok:
* **Egyszeri kódgenerálás:**
  ```bash
  dart run build_runner build --delete-conflicting-outputs
  ```
  Lefuttatja a generálást, és felülírja a korábbi konfliktusos fájlokat.

* **Folyamatos figyelés és generálás:**
  ```bash
  dart run build_runner watch --delete-conflicting-outputs
  ```
  A háttérben futva figyeli a fájlok változását, és mentéskor azonnal újraírja a generált fájlokat.
""",
    "page-elemzes.md": """# Elemzés

A kódminőség fenntartásának legfontosabb eszközei, amelyek biztosítják az egységes stílust és kiszűrik a potenciális hibákat.

## 🛠️ Parancsok:
* **Kód automatikus formázása:**
  ```bash
  dart format .
  ```
  A Dart hivatalos irányelvei alapján rendezi a behúzásokat, töréseket és vesszőket a teljes projektben.

* **Statikus elemző futtatása:**
  ```bash
  flutter analyze
  ```
  Átvizsgálja a kódot szintaktikai hibák, elavult (deprecated) api-k és linter szabályszegések után kutatva.
""",
    "page-teszt.md": """# Teszt

Az automatizált tesztek futtatása biztosítja, hogy a kód módosítása során ne rontsuk el a meglévő funkciókat.

## 🛠️ Parancsok:
* **Összes teszt futtatása:**
  ```bash
  flutter test
  ```
  Lefuttatja a `test/` mappában található összes unit és widget tesztet.

* **Tesztlefedettség (Coverage) mérése:**
  ```bash
  flutter test --coverage
  ```
  Létrehoz egy `coverage/lcov.info` fájlt, amely megmutatja, a sorok hány százalékát fedik le tesztek.
""",
    "page-build.md": """# Build

Az alkalmazás kiadásra (Google Play Áruházba való feltöltésre) való előkészítése és lefordítása.

## 🛠️ Parancsok:
* **Android App Bundle (AAB) készítése (Ajánlott):**
  ```bash
  flutter build appbundle --release
  ```
  Ez a hivatalos formátum a Play Áruházba való feltöltéshez. Kisebb méretet eredményez a felhasználók eszközein.

* **Hagyományos APK build:**
  ```bash
  flutter build apk --release
  ```
  Létrehoz egy telepíthető APK fájlt, amit közvetlenül is átküldhetsz tesztelésre.
""",
    "page-takaritas.md": """# Takarítás

Néha a Flutter cache-e megsérülhet, vagy verzióváltás után beragadhatnak régi build fájlok. Ilyenkor érdemes kitakarítani a projektet.

## 🛠️ Parancsok:
* **Build és cache fájlok törlése:**
  ```bash
  flutter clean
  ```
  Kitörli a `build/` mappát és az ideiglenes Dart cache fájlokat.

* **Függőségek friss letöltése:**
  ```bash
  flutter pub get
  ```
  A takarítás után mindig le kell futtatni, hogy újraépüljön a csomagtár.
"""
}

# ==========================================
# 7. Git Workflow (3 files)
# ==========================================
git_workflow = {
    "page-alap-branch-modell.md": """# Alap branch modell

A Git verziókövető strukturált használata elengedhetetlen a biztonságos kódfejlesztéshez és a csapatmunkához.

## 🌲 Ág Szerkezet (Branches):
* **`main`:** A stabil, éles ág. Csak alaposan letesztelt, kiadásra kész kód kerülhet ide.
* **`dev` / `development`:** A fejlesztési főág. A fejlesztők ide integrálják az elkészült funkciókat.
* **`feature/*`:** Új funkciók fejlesztésére szolgáló ideiglenes ágak (pl. `feature/login-screen`).
* **`fix/*` / `bugfix/*`:** Hibajavító ágak (pl. `fix/empty-list-crash`).

## 🔄 Fejlesztési Folyamat:
1. Hozz létre egy új ágat a dev ágból: `git checkout -b feature/my-feature dev`
2. Kódolj, majd commitolj rendszeresen.
3. Küldd be a kódot és nyiss egy Pull Request-et (PR) a dev ágra a kód felülvizsgálatához (Code Review).
""",
    "page-commit-pelda.md": """# Commit példa

Hogyan készítsünk tiszta, visszakövethető commitokat fejlesztés közben.

## 🛠️ Példa munkafolyamat:
```bash
# Változások ellenőrzése
git status

# Fájlok hozzáadása a stage-re
git add .

# Commit készítése beszédes üzenettel
git commit -m "feat: add secure token storage using flutter_secure_storage"

# Változások feltöltése a szerverre
git push origin feature/auth-module
```

> [!IMPORTANT]
> Ne csinálj hatalmas, több napos munkát lefedő commitokat. Törekedj a kis, logikailag egy összetartozó módosítást tartalmazó commitok írására!
""",
    "page-jo-commit-tipusok.md": """# Jó commit típusok

A szemantikus commit üzenetek segítenek abban, hogy a projekt története könnyen olvasható és automatizálható legyen.

## 🏷️ Commit prefixes minták:
* **`feat:`** Új funkció bevezetése (pl. `feat: implement user registration form`).
* **`fix:`** Hibajavítás (pl. `fix: resolve keyboard overflow on login screen`).
* **`refactor:`** Kód átrendezése a működés megváltoztatása nélkül (pl. `refactor: split main.dart into feature subfolders`).
* **`test:`** Tesztek hozzáadása vagy javítása (pl. `test: add unit tests for cart calculation`).
* **`docs:`** Dokumentáció bővítése vagy javítása (pl. `docs: update README with environment setup guide`).
* **`chore:`** Karbantartási munkák, verzióváltások, konfigurációs módosítások (pl. `chore: bump dio version to 5.4.0`).
"""
}

# ==========================================
# 8. First 30 Days (30 files)
# ==========================================
days_data = [
    {
        "num": 1,
        "title": "Flutter telepítés és környezet beállítása",
        "description": "A mai nap célja a Flutter fejlesztői környezet teljes körű beállítása. Telepítjük a Flutter SDK-t, beállítjuk a környezeti változókat (PATH), és ellenőrizzük a rendszert a flutter doctor segítségével. Ezt követően konfiguráljuk a VS Code vagy Android Studio szerkesztőket a Dart és Flutter pluginekkel, majd elindítunk egy emulátort vagy fizikai eszközt.",
        "code": "# Telepítés ellenőrzése\nflutter doctor -v\n\n# Elérhető eszközök listázása\nflutter devices",
        "exercise": "Futtasd le sikeresen a `flutter doctor` parancsot. Javíts ki minden hibát (Android toolchain licenc, VS Code kiterjesztés stb.), amíg minden lényeges pont zöld nem lesz."
    },
    {
        "num": 2,
        "title": "Dart változók, típusok és alap műveletek",
        "description": "Megismerkedünk a Dart nyelv alapvető szintaxisával, változók deklarálásával (var, final, const) és az alapvető adattípusokkal (int, double, String, bool). Különös figyelmet fordítunk a fordítási időben (const) és futási időben (final) állandó értékek közötti különbségre.",
        "code": "void main() {\n  var name = 'Flutter Tanuló';\n  final double price = 1990.90;\n  const int taxPercent = 27;\n  \n  print('Termék: $name, Bruttó: ${price * (1 + taxPercent / 100)} Ft');\n}",
        "exercise": "Írj egy konzolos Dart programot, amely bekér és kiszámol egy téglalap területét és kerületét adott oldalhosszak mellett."
    },
    {
        "num": 3,
        "title": "Dart függvények, osztályok és OOP alapok",
        "description": "A mai nap a függvények és az objektumorientált programozás (OOP) alapjairól szól Dartban. Megtanuljuk a pozicionális, opcionális és nevesített (named) paraméterek használatát, az osztályok, konstruktorok írását, valamint az adattagok elérését.",
        "code": "class Product {\n  final String name;\n  final double price;\n  final int stock;\n\n  Product({\n    required this.name,\n    required this.price,\n    this.stock = 0,\n  });\n\n  bool get isAvailable => stock > 0;\n}\n\nvoid main() {\n  final p = Product(name: 'Kávé', price: 990, stock: 15);\n  print('${p.name} elérhető? ${p.isAvailable}');\n}",
        "exercise": "Készíts egy `User` osztályt, amely tartalmazza a felhasználó nevét, emailjét és opcionálisan a korát. Írj egy metódust, amely ellenőrzi, hogy a felhasználó felnőttkorú-e."
    },
    {
        "num": 4,
        "title": "Dart Null Safety és gyűjtemények",
        "description": "A Dart Sound Null Safety koncepciója megvéd a null-pointer hibáktól. Megtanuljuk a nullable típusok (?, !), a null-aware operátorok (??, ?. ) és a legfontosabb gyűjteménytípusok (List, Map, Set) használatát.",
        "code": "void main() {\n  String? nickname = null;\n  print(nickname ?? 'Vendég'); // Ha null, Vendég jelenik meg\n  \n  List<String> fruits = ['alma', 'eper', 'banán'];\n  var capitalized = fruits.map((f) => f.toUpperCase()).toList();\n  print(capitalized);\n}",
        "exercise": "Hozz létre egy termékeket (Map) tartalmazó listát. Szűrd ki azokat, amelyek ára meghaladja az 5000 Ft-ot, és mentsd el a nevüket egy új listába."
    },
    {
        "num": 5,
        "title": "Első saját Flutter képernyő",
        "description": "A mai napon létrehozzuk az első minimális Flutter alkalmazásunkat. Megértjük a `runApp` függvény, a MaterialApp és a Scaffold widgetek feladatát. Létrehozunk egy egyszerű AppBar-t és egy Text widgettel ellátott törzset.",
        "code": "import 'package:flutter/material.dart';\n\nvoid main() {\n  runApp(\n    const MaterialApp(\n      home: Scaffold(\n        body: Center(\n          child: Text('Üdvözöl a Flutter!'),\n        ),\n      ),\n    ),\n  );\n}",
        "exercise": "Hozd létre a fenti kódot, és egészítsd ki a Scaffold-ot egy AppBar-ral, amelynek a címe 'Első Alkalmazásom'."
    },
    {
        "num": 6,
        "title": "Column, Row és Container widgetek",
        "description": "Megtanuljuk a legalapvetőbb elrendezési (layout) widgetek használatát. A Column függőlegesen, a Row vízszintesen helyezi el a gyerekeket. A Container dekorálható, méretezhető, margókkal és paddinggel látható el.",
        "code": "Container(\n  padding: const EdgeInsets.all(16.0),\n  margin: const EdgeInsets.all(8.0),\n  decoration: BoxDecoration(\n    color: Colors.blue.shade100,\n    borderRadius: BorderRadius.circular(12),\n  ),\n  child: const Column(\n    mainAxisSize: MainAxisSize.min,\n    children: [\n      Text('Főcím', style: TextStyle(fontWeight: FontWeight.bold)),\n      Row(\n        mainAxisAlignment: MainAxisAlignment.spaceBetween,\n        children: [\n          Text('Bal oldal'),\n          Text('Jobb oldal'),\n        ],\n      ),\n    ],\n  ),\n)",
        "exercise": "Készíts egy profil kártyát, ahol bal oldalon egy színes ikon látható, tőle jobbra pedig egymás alatt a felhasználó neve és munkaköre."
    },
    {
        "num": 7,
        "title": "Heti ismétlés és Git verziókezelés",
        "description": "A mai nap az ismétlésé. Áttekintjük a Dart alapokat és az első widgeteket. Emellett beállítunk egy helyi Git verziókövetőt a projektünknek, elvégezzük az első commitokat és megismerjük a `.gitignore` fájl fontosságát.",
        "code": "git init\ngit add .\ngit commit -m \"feat: initialize flutter demo app with basic layout\"\ngit status",
        "exercise": "Hozz létre egy új privát vagy publikus GitHub adattárat, és töltsd fel rá az első hét során elkészített mini projektjeidet."
    },
    {
        "num": 8,
        "title": "StatelessWidget vs StatefulWidget",
        "description": "A Flutterben a widgetek két fő típusra oszthatók. Megismerjük, mikor érdemes Stateless (állapotmentes) és mikor Stateful (állapottal rendelkező) widgetet választani. Megismerjük a `setState` működését és az UI újraépülését.",
        "code": "class MyButton extends StatelessWidget {\n  const MyButton({super.key});\n  @override\n  Widget build(BuildContext context) {\n    return const ElevatedButton(onPressed: null, child: Text('Kattints'));\n  }\n}",
        "exercise": "Készíts egy StatefulWidget alapú oldalt, ahol egy gomb megnyomásával változtatni tudod a képernyő háttérszínét két szín között."
    },
    {
        "num": 9,
        "title": "Számláló alkalmazás bővítése",
        "description": "A klasszikus Flutter sablon számlálót fogjuk kibővíteni és átírni. Megértjük a state életciklusát, a változók kezelését StatefulWidgeten belül, és finomhangoljuk az UI-t.",
        "code": "class CounterWidget extends StatefulWidget {\n  const CounterWidget({super.key});\n  @override\n  State<CounterWidget> createState() => _CounterWidgetState();\n}\n\nclass _CounterWidgetState extends State<CounterWidget> {\n  int _count = 0;\n  @override\n  Widget build(BuildContext context) {\n    return Column(\n      children: [\n        Text('Érték: $_count'),\n        ElevatedButton(\n          onPressed: () => setState(() => _count++),\n          child: const Text('Növel'),\n        ),\n      ],\n    );\n  }\n}",
        "exercise": "Egészítsd ki a számlálót egy 'Csökkent' gombbal, és egy 'Nullázó' gombbal. Biztosítsd, hogy a számláló értéke sose essen nulla alá."
    },
    {
        "num": 10,
        "title": "TextField, beviteli mezők és gombok",
        "description": "Megtanuljuk a felhasználói bevitelek kezelését. Használjuk a TextField widgetet, a `TextEditingController` osztályt a bevitt érték kiolvasására és törlésére, valamint stílust adunk a beviteli mezőnek.",
        "code": "final controller = TextEditingController();\n// A widgetben:\nTextField(\n  controller: controller,\n  decoration: const InputDecoration(\n    labelText: 'Írj be valamit',\n    border: OutlineInputBorder(),\n  ),\n)",
        "exercise": "Készíts egy képernyőt, ahol a felhasználó beírhatja a nevét, és a gomb megnyomására egy stílusos üdvözlő üzenet jelenik meg a beviteli mező alatt."
    },
    {
        "num": 11,
        "title": "Bevásárlólista alkalmazás",
        "description": "A mai napon összerakunk egy interaktív bevásárlólista oldalt. A listaelemeket egy tömbben tároljuk a State-ben, és dinamikusan tudunk elemet hozzáadni vagy törölni belőle.",
        "code": "List<String> items = [];\n// setState hívással módosítjuk a listát:\nsetState(() {\n  items.add(newText);\n});",
        "exercise": "Valósítsd meg a bevásárlólistát egy szövegbevitellel és egy hozzáadó gombbal. Mindegyik elem mellett szerepeljen egy törlés ikon, amire kattintva az elem kikerül a listából."
    },
    {
        "num": 12,
        "title": "ListView és Card widgetek",
        "description": "A nagy mennyiségű elem görgethető megjelenítésére a ListView és annak builder változata szolgál. Megismerkedünk a teljesítménybeli előnyeivel, a ListTile és a Card widgetekkel.",
        "code": "ListView.builder(\n  itemCount: items.length,\n  itemBuilder: (context, index) {\n    return Card(\n      child: ListTile(\n        title: Text(items[index]),\n        leading: const Icon(Icons.shopping_bag),\n      ),\n    );\n  },\n)",
        "exercise": "Alakítsd át a tegnapi bevásárlólistádat úgy, hogy a listaelemek Card widgetbe ágyazott ListTile-okként jelenjenek meg."
    },
    {
        "num": 13,
        "title": "Todo alkalmazás alapjai",
        "description": "Elkezdjük egy robusztusabb, többfunkciós teendőkezelő (Todo) alkalmazás fejlesztését. Hozzáadunk egy Todo modellt külön id-val, címmel és elkészültségi állapottal.",
        "code": "class Todo {\n  final String id;\n  final String title;\n  bool isCompleted;\n  Todo({required this.id, required this.title, this.isCompleted = false});\n}",
        "exercise": "Definiáld a Todo osztályt és készíts belőle egy kezdeti listát statikus tesztadatokkal. Jelenítsd meg őket egy ListView-ban."
    },
    {
        "num": 14,
        "title": "Todo alkalmazás befejezése",
        "description": "Befejezzük a teendőkezelőt. Képessé tesszük az appot a teendők kipipálására, a befejezett elemek szűrésére és az üres lista állapot (Empty State) szép grafikus kezelésére.",
        "code": "bool showOnlyActive = false;\nvar visibleTodos = todos.where((t) => !showOnlyActive || !t.isCompleted).toList();",
        "exercise": "Implementálj egy szűrősávot (pl. FilterChips használatával), amellyel a felhasználó válthat az 'Összes', 'Aktív' és 'Befejezett' teendők nézet között."
    },
    {
        "num": 15,
        "title": "Layout mélyítés és reszponzivitás",
        "description": "Megtanulunk profi módon bánni a méret- és elhelyezési korlátokkal. Megismerjük az Expanded, Flexible, Spacer widgeteket, és megértjük, hogyan kerüljük el a rettegett sárga-fekete csíkos overflow hibákat.",
        "code": "Row(\n  children: [\n    const Icon(Icons.star),\n    Expanded(\n      child: Text('Nagyon hosszú szöveg ami egyébként overflow-t okozna...'),\n    ),\n  ],\n)",
        "exercise": "Készíts egy reszponzív layoutot, amely egyaránt jól mutat függőleges és vízszintes elrendezésben is."
    },
    {
        "num": 16,
        "title": "Login UI tervezése",
        "description": "Egy modern, esztétikus bejelentkező felületet építünk fel. Használunk lekerekítéseket, árnyékokat, egyedi színpalettát és validálható form mezőket.",
        "code": "Form(\n  key: _formKey,\n  child: Column(\n    children: [\n      TextFormField(\n        validator: (v) => v!.isEmpty ? 'Töltsd ki!' : null,\n      ),\n    ],\n  ),\n)",
        "exercise": "Tervezd meg a login képernyő felületét, amely tartalmazzon egy logó helyőrzőt, email és jelszó mezőket, valamint egy 'Bejelentkezés' és 'Elfelejtett jelszó' gombot."
    },
    {
        "num": 17,
        "title": "Termékkártya UI és grid elrendezés",
        "description": "Készítünk egy webshop stílusú termékkártyát. Megtanuljuk a GridView.builder widget használatát, hogy az elemeket rácsban jeleníthessük meg, ügyelve a képarányokra.",
        "code": "GridView.builder(\n  gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(\n    crossAxisCount: 2,\n    childAspectRatio: 0.7,\n  ),\n  itemBuilder: (context, index) => ProductCard(),\n)",
        "exercise": "Készíts egy egyedi termékkártya komponenst képpel, terméknévvel, árral és egy kis kosár gombbal a jobb alsó sarokban."
    },
    {
        "num": 18,
        "title": "Responsive layout - LayoutBuilder",
        "description": "A LayoutBuilder segítségével a szülő widget fizikai méretétől függően tudunk eltérő elrendezéseket renderelni. Így ugyanaz a kód mobilon egyoszlopos, tableten kétoszlopos nézetet ad.",
        "code": "LayoutBuilder(\n  builder: (context, constraints) {\n    if (constraints.maxWidth > 600) {\n      return _buildTabletLayout();\n    } else {\n      return _buildMobileLayout();\n    }\n  },\n)",
        "exercise": "Alakítsd át a termékkatalógus gridet úgy, hogy keskeny képernyőn 2, míg széles (pl. landscape vagy tablet) kijelzőn automatikusan 4 oszlopos legyen."
    },
    {
        "num": 19,
        "title": "Webshop katalógus UI",
        "description": "Összeállítjuk a webáruház főoldalát. Vízszintesen görgethető kategória chipeket, akciós bannereket és függőlegesen görgethető termékrácsot integrálunk egyetlen lapba.",
        "code": "SingleChildScrollView(\n  child: Column(\n    children: [\n      _buildBannerSlider(),\n      _buildCategoryChips(),\n      _buildProductGrid(),\n    ],\n  ),\n)",
        "exercise": "Implementálj egy keresősávot az AppBar alá, amely gépelésre (egyelőre statikusan) vizuálisan kiemeli a keresési találatokat."
    },
    {
        "num": 20,
        "title": "Webshop részletező UI",
        "description": "Létrehozzuk a termék részletes leíró oldalát. Nagy felbontású kép, részletes leírás, árcédula és egy lebegő kosárba helyező akciógomb fogja alkotni a felületet.",
        "code": "Scaffold(\n  body: CustomScrollView(\n    slivers: [\n      SliverAppBar(expandedHeight: 300, flexibleSpace: FlexibleSpaceBar(background: Image.network(...))),\n      SliverFillRemaining(child: ProductDetails()),\n    ],\n  ),\n)",
        "exercise": "Készítsd el a termékrészletező oldalt, ahol a kosárba gomb megnyomására egy Snackbar jelzi a sikeres műveletet."
    },
    {
        "num": 21,
        "title": "Refaktor és dokumentáció",
        "description": "A tiszta kód érdekében kiszervezzük a widgeteket külön fájlokba, strukturáljuk a mappaszerkezetet, és megírjuk a projekt GitHub README.md dokumentációját.",
        "code": "lib/\n  models/\n    product.dart\n  widgets/\n    product_card.dart\n  screens/\n    catalog_screen.dart\n    details_screen.dart",
        "exercise": "Bontsd szét a webshop katalógus kódját a fenti könyvtárstruktúra szerint, ügyelve az importok helyes használatára."
    },
    {
        "num": 22,
        "title": "Navigator alapok",
        "description": "A képernyők közötti navigációt a Navigator kezeli. Megismerjük a push és pop műveleteket, valamint a MaterialPageRoute-ot, amellyel új képernyőt tolhatunk a navigációs stócba.",
        "code": "Navigator.push(\n  context,\n  MaterialPageRoute(builder: (context) => const DetailsScreen()),\n);",
        "exercise": "Köss össze két külön oldalt navigációval: a kezdőoldalról egy gombbal lépj át a beállítások oldalra, ahonnan egy vissza gombbal térhetsz vissza."
    },
    {
        "num": 23,
        "title": "Route argumentumok átadása",
        "description": "Navigáció során gyakran kell adatot (pl. egy termékazonosítót) átadni az új képernyőnek. Megtanuljuk a paraméterek átadását az új widget konstruktorán keresztül.",
        "code": "Navigator.push(\n  context,\n  MaterialPageRoute(\n    builder: (context) => DetailsScreen(product: currentProduct),\n  ),\n);",
        "exercise": "Módosítsd a katalógus oldaladat úgy, hogy a termékkártyára kattintva a Navigator átadja az adott termék objektumát a részletező oldalnak, ami azt jeleníti meg."
    },
    {
        "num": 24,
        "title": "Bottom Navigation",
        "description": "A modern mobilalkalmazások alapja az alsó navigációs sáv. Megismerjük a BottomNavigationBar és a NavigationBar widgeteket, és megtanuljuk kezelni az indexek váltását.",
        "code": "int _currentIndex = 0;\n// A Scaffoldban:\nbottomNavigationBar: BottomNavigationBar(\n  currentIndex: _currentIndex,\n  onTap: (index) => setState(() => _currentIndex = index),\n  items: const [ ... ],\n)",
        "exercise": "Készíts egy 3 fülből álló navigációs keretet (Főoldal, Keresés, Profil), ahol a fülek között kattintva változik a megjelenő tartalom."
    },
    {
        "num": 25,
        "title": "Theme alapok és ThemeData",
        "description": "Megtanuljuk az alkalmazás színeit, betűtípusait és formáit globálisan konfigurálni a ThemeData segítségével. Így az egész app arculatát egyetlen helyről vezérelhetjük.",
        "code": "MaterialApp(\n  theme: ThemeData(\n    primarySwatch: Colors.deepPurple,\n    scaffoldBackgroundColor: Colors.grey.shade50,\n    textTheme: const TextTheme(bodyLarge: TextStyle(fontSize: 18)),\n  ),\n)",
        "exercise": "Definiálj egy saját stílust a gombokra és a beviteli mezőkre globálisan az appod témájában, és figyeld meg a változást az összes képernyőn."
    },
    {
        "num": 26,
        "title": "Sötét és világos mód",
        "description": "A mai napon beállítjuk a sötét témát is. Megértjük, hogyan választ a Flutter a rendszerszintű beállítások alapján a világos és a sötét stílus között.",
        "code": "MaterialApp(\n  theme: ThemeData.light(),\n  darkTheme: ThemeData.dark(),\n  themeMode: ThemeMode.system, // Rendszerszintű beállítást követ\n)",
        "exercise": "Készíts egy beállítások képernyőt, ahol a felhasználó megváltoztathatja a sötét, világos, vagy rendszer által választott témát."
    },
    {
        "num": 27,
        "title": "Assetek és képek",
        "description": "A helyi statikus képeket, logókat, ikonokat és egyedi betűtípusokat regisztrálni kell a `pubspec.yaml` fájlban. Megtanuljuk a helyes formázást és az Image.asset használatát.",
        "code": "# pubspec.yaml-ben:\nflutter:\n  assets:\n    - assets/images/logo.png",
        "exercise": "Hozz létre egy `assets/images` mappát, helyezz el benne egy képet, regisztráld a pubspec.yaml-ben, majd jelenítsd meg az alkalmazásod fejlécében."
    },
    {
        "num": 28,
        "title": "UI kit komponensek",
        "description": "Megtervezzük a saját újrahasználható UI kitünket. Készítünk egyedi gombot (`PrimaryButton`), egyedi beviteli mezőt (`AppTextField`) és státuszjelző kártyákat.",
        "code": "class PrimaryButton extends StatelessWidget {\n  final String text;\n  final VoidCallback onPressed;\n  const PrimaryButton({super.key, required this.text, required this.onPressed});\n  @override\n  Widget build(BuildContext context) { ... }\n}",
        "exercise": "Szervezd ki az alkalmazásodban használt egyedi dizájnú gombokat és beviteli mezőket önálló, paraméterezhető osztályokba."
    },
    {
        "num": 29,
        "title": "Mini projekt összerakása",
        "description": "A mai napon elkezdjük egybefogni az eddig tanultakat. Létrehozunk egy teljes, integrált alkalmazást bejelentkező képernyővel, főoldali termékkatalógussal, részletezővel és profil oldallal.",
        "code": "// Navigáció bejelentkezés után:\nNavigator.pushReplacement(\n  context,\n  MaterialPageRoute(builder: (context) => const MainNavigationScreen()),\n);",
        "exercise": "Köss össze minden eddig elkészített képernyőt egy egységes logikai folyamattá, ahol a sikeres login a bottom navigációs főoldalra visz."
    },
    {
        "num": 30,
        "title": "Kód tisztítás, screenshotok, GitHub",
        "description": "A 30 napos alapozás zárásaként lefuttatjuk a statikus elemzőt, formázzuk a teljes kódbázist, készítünk látványos screenshotokat a működésről és véglegesítjük a GitHub repónkat.",
        "code": "# Végső ellenőrző parancsok\ndart format .\nflutter analyze",
        "exercise": "Futtasd le a formázót és az elemzőt. Javítsd az összes figyelmeztetést. Készíts egy README-t képernyőképekkel, és commitold a végső állapotot."
    }
]

days_template = """# {title}

{description}

---

## 📖 Elméleti Háttér és Koncepció
A mai napon a legfontosabb cél a témakör gyakorlati megvalósítása és elméleti tisztázása. A mobilfejlesztésben elengedhetetlen a tiszta szintaxis, a hatékony memóriakezelés és a platform-specifikus minták betartása.

### Kulcsfontosságú szempontok:
* **Strukturáltság:** Mindig válaszd szét a felületeket a logikától.
* **Tiszta kód:** Dart nyelven törekedj a deklaratív és könnyen olvasható elnevezésekre.
* **Hibamegelőzés:** Használj statikus elemzőket és kövesd a Flutter linter ajánlásait.

---

## 💻 Mintakód
Az alábbi kód bemutatja a mai nap legfőbb technológiai fókuszát. Másold be a projektedbe, és vizsgáld meg a működését!

```dart
{code}
```

---

## 🛠️ Napi Gyakorlat
> [!IMPORTANT]
> A programozást nem lehet elméletben megtanulni. A mai gyakorlati feladatod a következő:
>
> **Feladat:** {exercise}

---

> [!TIP]
> **Profi tipp:** Futtasd rendszeresen a `dart format .` parancsot a terminálból, hogy a kódod elrendezése mindig megfeleljen a Dart hivatalos irányelveinek.
"""

for day in days_data:
    filename = f"page-{day['num']}-nap.md"
    content = days_template.format(
        title=f"{day['num']}. nap — {day['title']}",
        description=day['description'],
        code=day['code'],
        exercise=day['exercise']
    )
    write_file(filename, content)

# Generate other dictionaries
for filename, content in routines.items():
    write_file(filename, content)

for filename, content in skills.items():
    write_file(filename, content)

for filename, content in packages.items():
    write_file(filename, content)

for filename, content in projects.items():
    write_file(filename, content)

for filename, content in exams.items():
    write_file(filename, content)

for filename, content in commands.items():
    write_file(filename, content)

for filename, content in git_workflow.items():
    write_file(filename, content)

print("ALL 71 CURRICULUM FILES GENERATED SUCCESSFULLY!")
