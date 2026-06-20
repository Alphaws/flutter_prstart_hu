# 22. hét — Teljesítmény és optimalizálás

## Cél
A lecke célja, hogy a tanuló elsajátítsa a Flutter alkalmazások sebességének és erőforrás-kihasználásának mérését, a lassulások (Jank) okainak felderítését és az optimális kódolási mintákat. Megismerjük a szükségtelen renderelések (Rebuild) megelőzését, a `RepaintBoundary` használatát, az Isolate-ekkel végzett háttérszámításokat, a memóriakezelést és a DevTools használatát.

---

## Elmélet

### 1. A Flutter három fája és a renderelés folyamata
Ahhoz, hogy megértsük az optimalizálást, ismernünk kell, hogyan rajzol a Flutter:
1. **Widget Tree (Widget fa):** Konfigurációs réteg. Rendkívül könnyű objektumok alkotják, amelyeket a Flutter nagyon gyorsan hoz létre és dob el.
2. **Element Tree (Elem fa):** Strukturális réteg. Összeköti a Widgetet a fizikai renderelt objektummal. Kezeli a widgetek életciklusát, az állapotot (State) és megőrzi az identitást.
3. **RenderObject Tree (Megjelenítő fa):** A tényleges elrendezésért (Layout) és rajzolásért (Painting) felelős réteg. Ezek nehéz objektumok, amelyek közvetlenül számolják a méreteket és rajzolnak a Skia vagy Impeller grafikus motor segítségével.

Ha megváltoztatunk egy változót, a Widget fa újraépül. A Flutter zsenialitása, hogy az Element fa segítségével összehasonlítja a változásokat, és a RenderObject fában csak azt az elemet rajzolja újra, amelyik valóban módosult.

```text
Widget Tree             Element Tree            RenderObject Tree
[ Container ]  <---->  [ ComponentElement ] <---->  [ RenderPadding ]
     |                      |                            |
  [ Text ]     <---->  [ LeafElement ]      <---->  [ RenderParagraph ]
```

### 2. UI Thread vs GPU (Raster) Thread és a Jank fogalma
A mobiltelefonok általában 60 Hz-en (vagy a modern eszközök 90/120 Hz-en) frissítik a képernyőt. 60 FPS esetén a Flutternek pontosan **16.6 milliseconds** áll rendelkezésére, hogy kiszámolja és kirajzolja a következő képkockát.
A munka két fő szálon (Thread) oszlik meg:
- **UI Thread (Dart VM):** Itt fut az összes Dart kódunk, az elrendezés kiszámítása (Layout), az állapotváltozások kezelése és a widgetek felépítése.
- **Raster Thread (GPU Thread):** Ez a szál veszi át a Dart szál által előkészített rajzolási utasításokat, és alakítja azokat fizikai pixelekké a képernyőn (rasterization).

Ha a UI szálon egy nehéz számítást (pl. 5 MB JSON parsolást) végzünk, az lefoglalja a szálat pl. 100 ms-ra. Ekkor a rendszer nem tud időben új képkockát adni a Raster szálnak. Ezt a megakadást nevezzük **Jank**-nek (akadozás, döccenés).

### 3. Felesleges Rebuild-ek elkerülése
A legegyszerűbb optimalizálás a szükségtelen build hívások csökkentése:
- **`const` widgetek:** Ha egy widgetet `const` kulcsszóval hozunk létre, a Flutter tudja, hogy annak tartalma soha nem változik. Emiatt a szülő widget újraépülésekor a `const` gyermek widget build metódusát a Flutter teljesen kihagyja (átugorja).
- **Lokális state:** Ne tartsuk az állapotot túl magasan a widgetfában, ha az csak egy kis részt érint. Például egy villogó kurzor miatt ne építsük újra az egész bejelentkező képernyőt.
- **Provider / Riverpod szelektálás:** Használjuk a `.select()` metódust a provider-eknél, hogy a widget csak akkor épüljön újra, ha a modell egy konkrét mezője megváltozik, ne a teljes objektum változásakor.

### 4. RepaintBoundary
Ha egy widget sűrűn változik (pl. egy folyamatosan forgó töltő ikon vagy egy részecske-animáció), a Flutter alapértelmezetten a teljes képernyőt (vagy a szülő renderelési rétegét) újrafestheti.
A **`RepaintBoundary`** segítségével létrehozhatunk egy különálló rajzolási réteget. Így az animáló widget rajzolási műveletei nem érintik a statikus hátteret, drasztikusan csökkentve a GPU terhelését.

### 5. Memóriaoptimalizálás és Kép Cache
A képek a mobilalkalmazások legnagyobb memóriafogyasztói. Ha egy 4000x3000 pixeles (12 megapixeles, kb. 15 MB kiterített méretű) képet egy 100x100-as avatar boxban jelenítünk meg optimalizálatlanul, az app hamar Out of Memory (OOM) hibával leállhat.
Megoldás:
- Használjuk a `cacheWidth` és `cacheHeight` tulajdonságokat az `Image.network` vagy `Image.asset` hívásoknál, így a Flutter már az átméretezett képet tartja a memóriában.
- Használjunk lazy loading-ot a listáknál (`ListView.builder`), ami csak a képernyőn látható elemeket rendereli le.

---

## Kódpéldák

### 1. JSON parsolás háttér Isolate-ben
Ha egy nagy méretű JSON sztringet kapunk a szerverről, annak parsolása lefoglalhatja a UI szálat. Az `Isolate.run` segítségével ezt könnyen kiszervezhetjük egy másik CPU magra.

```dart
import 'dart:convert';
import 'package:flutter/foundation.dart';

class OptimizedDataParser {
  /// Nehéz JSON sztring parsolása háttér Isolate-ben.
  /// Nem blokkolja a UI-t, a görgetés folyamatos marad.
  Future<List<Map<String, dynamic>>> parseHeavyJson(String jsonString) async {
    // Az Isolate.run automatikusan létrehoz egy isolate-et, 
    // lefuttatja a függvényt, átadja az eredményt és leáll.
    return await compute(_decodeAndCast, jsonString);
  }

  // Megjegyzés: top-level vagy static függvénynek kell lennie
  static List<Map<String, dynamic>> _decodeAndCast(String data) {
    final decoded = jsonDecode(data);
    if (decoded is List) {
      return decoded.cast<Map<String, dynamic>>();
    }
    return [];
  }
}
```

### 2. Dart Benchmark loop példa
A következő kód egy egyszerű teljesítménymérést mutat be `Stopwatch` segítségével, demonstrálva a blokkoló futás idejét.

```dart
class PerformanceBenchmark {
  /// Nehéz számítás benchmark mérése.
  /// Visszaadja a futási időt milliszekundumban.
  static double runMathComputation() {
    final stopwatch = Stopwatch()..start();
    
    int sum = 0;
    // Blokkoló loop
    for (int i = 0; i < 100000000; i++) {
      sum += (i % 3 == 0) ? i : -i;
    }
    
    stopwatch.stop();
    print("Számítás eredménye: $sum");
    return stopwatch.elapsedMicroseconds / 1000.0; // ms
  }
}
```

### 3. Végtelen görgetés (Infinite Scroll / Pagination) sablon
Lista lapozásának lekezelése `ScrollController` segítségével.

```dart
import 'package:flutter/material.dart';

class PaginatedListTemplate extends StatefulWidget {
  const PaginatedListTemplate({super.key});

  @override
  State<PaginatedListTemplate> createState() => _PaginatedListTemplateState();
}

class _PaginatedListTemplateState extends State<PaginatedListTemplate> {
  final ScrollController _scrollController = ScrollController();
  final List<String> _items = [];
  bool _isLoading = false;
  int _currentPage = 1;

  @override
  void initState() {
    super.initState();
    _loadMoreData();
    _scrollController.addListener(_scrollListener);
  }

  void _scrollListener() {
    // Ellenőrizzük, hogy elértük-e a lista alját (90%-os gördítésnél már indítjuk)
    if (_scrollController.position.pixels >= _scrollController.position.maxScrollExtent * 0.9) {
      if (!_isLoading) {
        _loadMoreData();
      }
    }
  }

  Future<void> _loadMoreData() async {
    setState(() {
      _isLoading = true;
    });

    // API hívás szimulálása
    await Future.delayed(const Duration(seconds: 1));
    
    final newItems = List.generate(20, (index) => 'Elem #${((_currentPage - 1) * 20) + index + 1}');
    
    setState(() {
      _items.addAll(newItems);
      _currentPage++;
      _isLoading = false;
    });
  }

  @override
  void dispose() {
    _scrollController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Optimalizált Lapozás')),
      body: ListView.builder(
        controller: _scrollController,
        itemCount: _items.length + 1, // +1 a betöltő indikátornak
        itemBuilder: (context, index) {
          if (index == _items.length) {
            return _isLoading 
                ? const Padding(
                    padding: EdgeInsets.all(16.0),
                    child: Center(child: CircularProgressIndicator()),
                  )
                : const SizedBox.shrink();
          }
          return ListTile(
            title: Text(_items[index]),
          );
        },
      ),
    );
  }
}
```

### 4. Optimalizált Képletöltés méretkorlátozással
Hálózati kép optimalizálása, megadva a cache maximális fizikai méretét a memóriában.

```dart
import 'package:flutter/material.dart';

class OptimizedImageWidget extends StatelessWidget {
  final String imageUrl;

  const OptimizedImageWidget({super.key, required this.imageUrl});

  @override
  Widget build(BuildContext context) {
    return ClipRRect(
      borderRadius: BorderRadius.circular(8),
      child: Image.network(
        imageUrl,
        width: 150,
        height: 150,
        fit: BoxFit.cover,
        // Korlátozzuk a memóriában tárolt kép méretét pixelben
        cacheWidth: 300, // 2x felbontás a retina/magas DPI kijelzők miatt
        cacheHeight: 300,
        // Betöltési állapot kezelése
        loadingBuilder: (context, child, loadingProgress) {
          if (loadingProgress == null) return child;
          return Container(
            width: 150,
            height: 150,
            color: Colors.grey[900],
            child: const Center(child: CircularProgressIndicator(strokeWidth: 2)),
          );
        },
        // Hiba kezelése (nem omlik össze az app, ha hibás a URL)
        errorBuilder: (context, error, stackTrace) {
          return Container(
            width: 150,
            height: 150,
            color: Colors.red[900],
            child: const Icon(Icons.broken_image, color: Colors.white),
          );
        },
      ),
    );
  }
}
```

---

## Gyakorlófeladatok & Megoldások

### 1. Feladat: Prímszám-generátor háttér Isolate-ben
Készíts egy alkalmazást egy gombbal és egy számlálóval. A gomb megnyomására számolj ki prímszámokat 1-től 2.000.000-ig. Ha simán a fő szálon futtatod, a UI teljesen megfagy (próbáld ki). Ezután írd meg a megoldást `compute` vagy `Isolate.run` segítségével, hogy a számláló és a UI animációk teljesen simák maradjanak a számítás alatt is.

#### Megoldás:
```dart
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';

class IsolateExercisePage extends StatefulWidget {
  const IsolateExercisePage({super.key});

  @override
  State<IsolateExercisePage> createState() => _IsolateExercisePageState();
}

class _IsolateExercisePageState extends State<IsolateExercisePage> {
  int _counter = 0;
  String _status = 'Inaktív';
  bool _isCalculating = false;

  // 1. Prímszám számító nehéz algoritmus (top-level/static kell legyen az Isolate-hez)
  static int _calculatePrimes(int limit) {
    int count = 0;
    for (int i = 2; i <= limit; i++) {
      bool isPrime = true;
      for (int j = 2; j * j <= i; j++) {
        if (i % j == 0) {
          isPrime = false;
          break;
        }
      }
      if (isPrime) count++;
    }
    return count;
  }

  // 2. Számítás indítása Isolate-ben
  Future<void> _startComputation() async {
    setState(() {
      _isCalculating = true;
      _status = 'Számítás folyamatban (háttér Isolate-ben)...';
    });

    // Kiszervezzük a munkát a fő szálról
    final int primeCount = await compute(_calculatePrimes, 2000000);

    setState(() {
      _status = 'Befejezve: $primeCount db prímszámot találtam.';
      _isCalculating = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Isolate Gyakorlat')),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(20.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              // Ez a számláló bizonyítja, hogy a UI nem fagy le számítás közben!
              Text('UI Teszt számláló: $_counter', style: const TextStyle(fontSize: 22)),
              const SizedBox(height: 10),
              ElevatedButton(
                onPressed: () => setState(() => _counter++),
                child: const Text('Számláló növelése (UI Teszt)'),
              ),
              const Divider(height: 50),
              Text(
                _status,
                textAlign: TextAlign.center,
                style: const TextStyle(fontSize: 16, color: Colors.amber),
              ),
              const SizedBox(height: 20),
              ElevatedButton(
                onPressed: _isCalculating ? null : _startComputation,
                style: ElevatedButton.styleFrom(backgroundColor: Colors.teal),
                child: const Text('Nehéz Számítás Indítása'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
```

### 2. Feladat: Lapozás (Pagination) megvalósítása mock adatokkal
Készíts egy listát, amely kezdetben 15 elemet mutat. Ha a felhasználó a lista aljára görget, tölts be automatikusan újabb 15 elemet egy 800 ms-os késleltetés után (szimulált hálózati késleltetés).

#### Megoldás:
Lásd a fentebb bemutatott **`PaginatedListTemplate`** kódpéldát, amely pontos és teljes megoldást nyújt a `ScrollController` és a betöltési állapot kezelésére.

### 3. Feladat: Widget újraépülés optimalizálása (Rebuild Counter)
Készíts egy képernyőt, amely tartalmaz egy statikus részt (szöveg és ikon) és egy dinamikus részt (egy másodpercenként frissülő órát/számlálót). Mutasd be, hogy az óra frissülésekor hogyan tudod megakadályozni a statikus rész újraépülését a `const` kulcsszó és a widgetek megfelelő szétszedésével.

#### Megoldás:
```dart
import 'dart:async';
import 'package:flutter/material.dart';

class RebuildOptimalPage extends StatefulWidget {
  const RebuildOptimalPage({super.key});

  @override
  State<RebuildOptimalPage> createState() => _RebuildOptimalPageState();
}

class _RebuildOptimalPageState extends State<RebuildOptimalPage> {
  @override
  Widget build(BuildContext context) {
    print('--> FŐ KÉPERNYŐ (RebuildOptimalPage) UJRAEPUL!');
    return Scaffold(
      appBar: AppBar(title: const Text('Rebuild Optimalizálás')),
      body: const Column(
        mainAxisAlignment: MainAxisAlignment.center,
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          // Statikus rész: const kulcsszó miatt sosem épül újra az óra ketyegésekor!
          StaticWidget(),
          SizedBox(height: 40),
          // Dinamikus rész: ez a saját belső állapotát frissíti, lokálisan
          ClockWidget(),
        ],
      ),
    );
  }
}

class StaticWidget extends StatelessWidget {
  const StaticWidget({super.key});

  @override
  Widget build(BuildContext context) {
    print('StaticWidget build lefutott (nem kellene sűrűn lefutnia!)');
    return const Card(
      margin: EdgeInsets.all(16),
      color: Colors.blueGrey,
      child: Padding(
        padding: EdgeInsets.all(20.0),
        child: Column(
          children: [
            Icon(Icons.info, size: 40, color: Colors.white),
            SizedBox(height: 10),
            Text(
              'Ez egy statikus kártya.\nA const kulcsszónak köszönhetően a build metódusa csak egyszer fut le az app életében!',
              textAlign: TextAlign.center,
              style: TextStyle(color: Colors.white),
            ),
          ],
        ),
      ),
    );
  }
}

class ClockWidget extends StatefulWidget {
  const ClockWidget({super.key});

  @override
  State<ClockWidget> createState() => _ClockWidgetState();
}

class _ClockWidgetState extends State<ClockWidget> {
  late Timer _timer;
  DateTime _currentTime = DateTime.now();

  @override
  void initState() {
    super.initState();
    _timer = Timer.periodic(const Duration(seconds: 1), (timer) {
      setState(() {
        _currentTime = DateTime.now();
      });
    });
  }

  @override
  void dispose() {
    _timer.cancel(); // Nagyon fontos a memory leak elkerüléséhez!
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    print('ClockWidget build lefutott (másodpercenként egyszer)');
    return Center(
      child: Text(
        'Pontos idő: ${_currentTime.hour.toString().padLeft(2, '0')}:${_currentTime.minute.toString().padLeft(2, '0')}:${_currentTime.second.toString().padLeft(2, '0')}',
        style: const TextStyle(fontSize: 28, fontWeight: FontWeight.bold, color: Colors.tealAccent),
      ),
    );
  }
}
```

### 4. Feladat: Memóriaszivárgás (Memory Leak) megelőzése
Írj egy olyan widgetet, amely egy `StreamSubscription`-re iratkozik fel (pl. másodperces Timer stream). Mutasd be a helyes megvalósítást, ahol az előfizetést (Subscription) lezárod az életciklus megfelelő szakaszában, megelőzve az alkalmazás háttérben történő lassú memóriafogyasztását.

#### Megoldás:
Mindig a `dispose()` metódusban kell meghívni a `.cancel()` függvényt a stream feliratkozásokon:
```dart
import 'dart:async';
import 'package:flutter/material.dart';

class LeakFreeWidget extends StatefulWidget {
  const LeakFreeWidget({super.key});

  @override
  State<LeakFreeWidget> createState() => _LeakFreeWidgetState();
}

class _LeakFreeWidgetState extends State<LeakFreeWidget> {
  StreamSubscription<int>? _subscription;
  int _counter = 0;

  @override
  void initState() {
    super.initState();
    // Feliratkozás egy végtelen streamre
    _subscription = Stream.periodic(const Duration(seconds: 1), (count) => count)
        .listen((value) {
      setState(() {
        _counter = value;
      });
    });
  }

  @override
  void dispose() {
    // KÖTELEZŐ: Megszüntetjük az előfizetést, ha a widget megsemmisül.
    // Ha ezt kihagynánk, a stream a widget bezárása után is futna a memóriában!
    _subscription?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Memory Leak Megelőzés')),
      body: Center(
        child: Text('Érték: $_counter', style: const TextStyle(fontSize: 24)),
      ),
    );
  }
}
```

### 5. Feladat: RepaintBoundary alkalmazása
Készíts egy felületet, amelynek hátterében egy sűrűn mozgó/animáló komponens fut, előtte pedig egy statikus gomb található. Helyezd el a `RepaintBoundary` widgetet úgy, hogy a gomb és a többi statikus elem rajzolási művelete külön rétegre kerüljön az animációtól.

#### Megoldás:
```dart
import 'dart:math';
import 'package:flutter/material.dart';

class RepaintBoundaryExercise extends StatefulWidget {
  const RepaintBoundaryExercise({super.key});

  @override
  State<RepaintBoundaryExercise> createState() => _RepaintBoundaryExerciseState();
}

class _RepaintBoundaryExerciseState extends State<RepaintBoundaryExercise> with SingleTickerProviderStateMixin {
  late AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 2),
    )..repeat();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('RepaintBoundary Teszt')),
      body: Stack(
        children: [
          // 1. Sűrűn animáló háttér: RepaintBoundary-ba csomagolva elszigeteljük a rajzolást!
          RepaintBoundary(
            child: AnimatedBuilder(
              animation: _controller,
              builder: (context, child) {
                return CustomPaint(
                  painter: RadarPainter(_controller.value),
                  child: Container(),
                );
              },
            ),
          ),
          // 2. Statikus tartalom: Külön rétegen van, nem rajzolódik újra a radar mozgásakor
          const RepaintBoundary(
            child: Center(
              child: Card(
                elevation: 8,
                color: Color(0xDD1E293B),
                child: Padding(
                  padding: EdgeInsets.all(24.0),
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Text(
                        'Statikus panel',
                        style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                      ),
                      SizedBox(height: 10),
                      Text('Ez a kártya és a gombok nincsenek újrarajzolva a háttér miatt.'),
                    ],
                  ),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class RadarPainter extends CustomPainter {
  final double progress;
  RadarPainter(this.progress);

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = Colors.teal.withOpacity(1.0 - progress)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 3.0;

    final center = Offset(size.width / 2, size.height / 2);
    final maxRadius = min(size.width, size.height) * 0.4;
    
    // Rajzolunk 3 koncentrikus táguló kört
    canvas.drawCircle(center, maxRadius * progress, paint);
    canvas.drawCircle(center, maxRadius * ((progress + 0.33) % 1.0), paint);
    canvas.drawCircle(center, maxRadius * ((progress + 0.66) % 1.0), paint);
  }

  @override
  bool shouldRepaint(covariant RadarPainter oldDelegate) {
    return oldDelegate.progress != progress;
  }
}
```

---

## Heti Mini Projekt: Nagy termékkatalógus app (SuperCatalog)

### Leírás és Funkciók
A heti mini projekt egy **Nagy termékkatalógus app (SuperCatalog)**. A cél 1000+ szimulált webáruházi termék zökkenőmentes listázása és keresése. 
A projekt bemutatja az alábbi optimalizálási technikákat valós működés közben:
1. **Lazy Loading:** `ListView.builder` használata.
2. **Háttér Isolate szűrés:** A keresősávba írt szöveg alapján a termékek szűrését egy háttér Isolate végzi (compute), így a billentyűzet és a felület egyetlen képkockát sem dob el (no frame drop).
3. **Memóriabarát képek:** Szimulált kép-placeholder-ek fix cache méretezéssel.

### A projekt teljes kódja (`lib/main.dart`)
Add hozzá a `pubspec.yaml`-hez:
```yaml
dependencies:
  flutter:
    sdk: flutter
```

```dart
import 'dart:async';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';

void main() {
  runApp(const SuperCatalogApp());
}

class SuperCatalogApp extends StatelessWidget {
  const SuperCatalogApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'SuperCatalog',
      theme: ThemeData(
        brightness: Brightness.dark,
        primaryColor: Colors.amber,
        scaffoldBackgroundColor: const Color(0xFF0F172A),
        useMaterial3: true,
      ),
      home: const CatalogPage(),
    );
  }
}

/// Termék adatmodell
class Product {
  final int id;
  final String title;
  final String category;
  final double price;

  const Product({
    required this.id,
    required this.title,
    required this.category,
    required this.price,
  });
}

/// Szűrési paraméterek az Isolate számára
class FilterParams {
  final List<Product> rawProducts;
  final String query;

  const FilterParams(this.rawProducts, this.query);
}

class CatalogPage extends StatefulWidget {
  const CatalogPage({super.key});

  @override
  State<CatalogPage> createState() => _CatalogPageState();
}

class _CatalogPageState extends State<CatalogPage> {
  // Generálunk 5000 terméket a memóriában
  late final List<Product> _allProducts;
  List<Product> _filteredProducts = [];
  
  final _searchController = TextEditingController();
  Timer? _debounce;
  bool _isSearching = false;

  @override
  void initState() {
    super.initState();
    // 5000 elem generálása
    _allProducts = List.generate(5000, (index) {
      final categories = ['Elektronika', 'Ruházat', 'Könyvek', 'Otthon', 'Sport'];
      return Product(
        id: index + 1,
        title: 'Termék #${index + 1} - ${index % 2 == 0 ? 'Prémium' : 'Standard'} eszköz',
        category: categories[index % categories.length],
        price: (index * 13 % 990) + 9.9,
      );
    });
    _filteredProducts = _allProducts;
  }

  // 1. Isolate-ben futó szűrési feladat (static)
  static List<Product> _filterTask(FilterParams params) {
    if (params.query.isEmpty) return params.rawProducts;
    
    // Lineáris keresés 5000 elemen (Isolate-en belül történik!)
    return params.rawProducts.where((product) {
      final titleMatch = product.title.toLowerCase().contains(params.query.toLowerCase());
      final categoryMatch = product.category.toLowerCase().contains(params.query.toLowerCase());
      return titleMatch || categoryMatch;
    }).toList();
  }

  // 2. Debounce és Isolate hívás indítása
  void _onSearchChanged(String query) {
    if (_debounce?.isActive ?? false) _debounce?.cancel();
    
    setState(() {
      _isSearching = true;
    });

    _debounce = Timer(const Duration(milliseconds: 300), () async {
      // Meghívjuk az Isolate-et a compute függvénnyel
      final filtered = await compute(
        _filterTask,
        FilterParams(_allProducts, query),
      );

      if (mounted) {
        setState(() {
          _filteredProducts = filtered;
          _isSearching = false;
        });
      }
    });
  }

  @override
  void dispose() {
    _debounce?.cancel();
    _searchController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('SuperCatalog (5000+ Termék)'),
        backgroundColor: Colors.amber[800],
        foregroundColor: Colors.black,
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(12.0),
            child: TextField(
              controller: _searchController,
              onChanged: _onSearchChanged,
              decoration: InputDecoration(
                labelText: 'Keresés termékek között...',
                border: const OutlineInputBorder(),
                prefixIcon: const Icon(Icons.search),
                suffixIcon: _isSearching
                    ? const Padding(
                        padding: EdgeInsets.all(12.0),
                        child: CircularProgressIndicator(strokeWidth: 2),
                      )
                    : null,
              ),
            ),
          ),
          Expanded(
            child: _filteredProducts.isEmpty
                ? const Center(child: Text('Nincs találat.'))
                : ListView.builder(
                    itemCount: _filteredProducts.length,
                    itemExtent: 85.0, // FIX magasság megadásával a ListView renderelése sokkal gyorsabb!
                    itemBuilder: (context, index) {
                      final product = _filteredProducts[index];
                      return Card(
                        margin: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                        color: const Color(0xFF1E293B),
                        child: ListTile(
                          // Csatolunk egy optimalizált memóriájú ikont/képet
                          leading: const RepaintBoundary(
                            child: CircleAvatar(
                              backgroundColor: Colors.amber,
                              child: Icon(Icons.shopping_bag, color: Colors.black),
                            ),
                          ),
                          title: Text(
                            product.title,
                            style: const TextStyle(fontWeight: FontWeight.bold),
                          ),
                          subtitle: Text(product.category),
                          trailing: Text(
                            '${product.price.toStringAsFixed(2)} Ft',
                            style: const TextStyle(color: Colors.amberAccent, fontWeight: FontWeight.bold),
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

## Heti Ellenőrző Kérdések

### 1. Kérdés: Miért gyorsítja meg a listák kirajzolását a `ListView.builder`-nél a `itemExtent` vagy `prototypeItem` paraméter megadása?
**Válasz:**
Alapértelmezetten, amikor a `ListView` görgetés közben új elemeket jelenít meg, a Flutternek le kell futtatnia az elrendezés (Layout) fázist minden egyes elemnél, hogy kiszámolja annak pontos fizikai magasságát, és ez alapján helyezze el a következőt. Ez nagy terhelést jelent.
Ha megadjuk az `itemExtent` paramétert (pl. `itemExtent: 85.0`), a Flutternek nem kell mérnie a widgeteket; előre tudja, hogy minden elem pontosan 85 pixel magas. Így azonnal ki tudja számolni a görgetési tartományt és a viewportban lévő elemek pozícióját mérési fázis nélkül, ami drasztikus sebességnövekedést eredményez.

### 2. Kérdés: Mi az a Shader Compilation Jank, és hogyan javítja ezt a Flutter új Impeller grafikus motorja?
**Válasz:**
A Skia motor használatakor az alkalmazás első futtatásakor (amikor egy új animáció vagy effekt először jelenik meg) a grafikus kártya (GPU) számára le kell fordítani a megfelelő árnyékoló programokat (Shader). Ez a fordítás a futási időben történik, és 100-200 ms-ig is eltarthat, ami azonnali, látványos megakadást (Jank) okoz.
Az új **Impeller** grafikus motor (amely iOS-en már alapértelmezett, Androidon pedig folyamatosan bevezetés alatt áll) az összes shadert az alkalmazás fordításakor (AOT - Ahead-Of-Time build alatt) előre lefordítja. Így futási időben már csak be kell tölteni a kész binárisokat, teljesen megszüntetve a Shader Compilation okozta döccenéseket.

### 3. Kérdés: Hogyan azonosíthatunk memóriaszivárgást (Memory Leak) az alkalmazásunkban a Flutter DevTools segítségével?
**Válasz:**
A Flutter DevTools **Memory** fülén az alábbi lépésekkel kereshetünk szivárgást:
1. Indítsuk el az alkalmazást Profile módban (`flutter run --profile`).
2. Nyissuk meg a Memory profiler-t, és készítsünk egy kezdő pillanatképet (Heap Snapshot).
3. Végezzük el a gyanús műveletet az appban többször (pl. nyissunk meg egy képernyőt, majd zárjuk be 10-szer).
4. Készítsünk egy újabb Heap Snapshot-ot.
5. Hasonlítsuk össze a két snapshotot. Ha a megsemmisített képernyő widgetjei, controller-ei vagy stream feliratkozásai továbbra is a memóriában maradtak (növekszik a példányszámuk és nem szabadulnak fel), akkor memóriaszivárgásunk van. Leggyakoribb ok a le nem zárt stream vagy controller a `dispose()`-ban.

### 4. Kérdés: Miért nem szabad a `setState` hívást a `build` metódus belsejében közvetlenül meghívni?
**Válasz:**
A `build` metódus feladata kizárólag a widgetfa leírása. Ha a `build` futása közben meghívjuk a `setState`-et, az jelzi a Flutternek, hogy a widget állapota megváltozott, és azonnal újra kell építeni a widgetet. Ez egy végtelen ciklust (Infinite Rebuild Loop) indít el: `build` -> `setState` -> `build` -> `setState`..., ami lefagyasztja az alkalmazást és azonnali hibaüzenetet dob a konzolra.

### 5. Kérdés: Mikor kötelező saját Isolate-et indítani a `compute` függvénnyel, és mikor elegendő a sima `async / await` használata?
**Válasz:**
A sima `async/await` nem hoz létre új szálat, a kód továbbra is a UI (Dart) szálon fut, csak várakozik (pl. hálózati válaszra vagy fájl írásra).
- **async/await elegendő:** I/O műveleteknél (HTTP kérések, adatbázis lekérdezések, fájl betöltése), mert ezeket a háttérben az operációs rendszer végzi, és a Dart szál addig szabad.
- **Saját Isolate kötelező:** CPU-intenzív feladatoknál (nagy JSON feldolgozása, képfeldolgozás, titkosítás, bonyolult matematikai keresések/szűrések), mert ezeket a számításokat a Dart VM végzi. Ha nem szervezzük ki Isolate-be, a UI szálat teljesen lefoglalja a processzor munka, és megakad a felület.
