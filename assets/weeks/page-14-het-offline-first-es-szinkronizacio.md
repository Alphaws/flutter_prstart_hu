# 14. hét — Offline-first és szinkronizáció

## Cél
A lecke célja, hogy elsajátítsd az **Offline-First** alkalmazásfejlesztés elméletét és gyakorlatát Flutterben. Megtanulod, hogyan készíts olyan mobilalkalmazást, amely korlátozott vagy teljesen hiányzó internetkapcsolat mellett is zökkenőmentesen és gyorsan működik. Képes leszel megvalósítani egy SQLite alapú **szinkronizációs sort (Sync Queue)**, figyelni a hálózat állapotát (`connectivity_plus` segítségével), alkalmazni az **optimista UI frissítést (Optimistic Update)**, valamint felépíteni egy automatikus szinkronizációs motort (Sync Engine) a szerver és a kliens közötti adatkonfliktusok feloldásával.

---

## Elmélet

### 1. Az Offline-First filozófia
A hagyományos online alkalmazások minden UI interakció előtt megvárják az API választ (pl. gombnyomás -> töltőképernyő -> API válasz -> UI frissítés). Ha nincs internet vagy lassú a szerver, az alkalmazás használhatatlanná válik.
Az **Offline-First** megközelítés lényege:
1.  A felhasználói felület **mindig a lokális adatbázisból (cache) épül fel**.
2.  Minden adatbevitel vagy módosítás **azonnal a lokális adatbázisba íródik**, így a UI azonnal reagál.
3.  A háttérben az alkalmazás elmenti a végrehajtott műveletet egy **szinkronizációs várólistába (Sync Queue)**.
4.  Amikor az eszköz online állapotba kerül, a **Szinkronizációs Motor (Sync Engine)** feldolgozza a várólistát és beküldi a módosításokat a backendnek.

### 2. A Szinkronizációs Sor (Sync Queue) működése (Outbox Pattern)
A szinkronizációs sor egy lokális adatbázis-tábla, amely leírja, hogy milyen műveleteket (Insert, Update, Delete) kell végrehajtani a szerveren, ha visszatér az internet.
Egy tipikus `sync_queue` rekord sémája:
*   `id`: Egyedi lokális azonosító (UUID vagy Auto-Increment).
*   `table_name`: Melyik entitás-táblát érinti a változás (pl. `products`, `todos`).
*   `record_id`: Az érintett lokális rekord azonosítója.
*   `operation`: A művelet típusa (`CREATE`, `UPDATE`, `DELETE`).
*   `payload`: A küldendő adatok JSON formátumban.
*   `created_at`: Létrehozás ideje.
*   `retry_count`: Hányszor próbálta megküldeni a motor (segít kiszűrni a hibás, ún. poison-pill kéréseket).

### 3. Optimista UI Frissítés (Optimistic Update)
Az optimista frissítés során az alkalmazás feltételezi, hogy a hálózati kérés sikeres lesz. Például egy Like gomb megnyomásakor a szív ikon azonnal pirosra vált, és a számláló növekszik a képernyőn, miközben az API kérés csak ezután indul el a háttérben.
*   **Előny:** Rendkívül gyors, azonnali visszajelzést ad a felhasználónak.
*   **Kihívás (Rollback):** Ha a háttérben futó kérés elbukik (pl. lejárt a token, vagy szerver hiba lép fel), a lokális adatbázist és a felhasználói felületet vissza kell állítani (rollback) az eredeti állapotra, és értesíteni kell a felhasználót a hibáról.

### 4. Konfliktusfeloldási stratégiák
Ha ugyanazt az adatot az offline időszak alatt a szerveren és a kliensen is módosították, dönteni kell, melyik adat érvényes:
1.  **Client Wins (Ügyfél nyer):** A kliens által offline végzett módosítás felülírja a szerveren lévőt.
2.  **Server Wins (Szerver nyer):** A kliens eldobja az offline módosításait, és felülírja azokat a szerverről letöltött friss adatokkal.
3.  **Last-Write-Wins (LWW - Legutolsó írás nyer):** Az időbélyeg alapján a legfrissebb módosítás marad meg.
4.  **Merge (Összefésülés):** Ha különböző mezőket módosítottak, az adatokat összefésüljük.

---

## Kódpéldák

### 1. Hálózati állapot figyelő szerviz (`connectivity_plus`)

Ez a szerviz figyelmeztetést ad a hálózati kapcsolat megváltozásáról egy Stream-en keresztül.

```dart
// lib/core/network/network_info.dart
import 'dart:async';
import 'package:connectivity_plus/connectivity_plus.dart';

class NetworkInfo {
  final Connectivity _connectivity;

  NetworkInfo(this._connectivity);

  // Visszaadja, hogy jelenleg online vagyunk-e
  Future<bool> get isConnected async {
    final result = await _connectivity.checkConnectivity();
    return _isOnline(result);
  }

  // Stream, amely figyeli a hálózat változásait
  Stream<bool> get onConnectionChanged {
    return _connectivity.onConnectivityChanged.map((result) => _isOnline(result));
  }

  bool _isOnline(List<ConnectivityResult> results) {
    // connectivity_plus 6.x-től kezdve egy listát ad vissza, mert több adapter is aktív lehet
    if (results.isEmpty) return false;
    return results.any((result) =>
        result == ConnectivityResult.mobile ||
        result == ConnectivityResult.wifi ||
        result == ConnectivityResult.ethernet);
  }
}
```

### 2. SQLite Szinkronizációs Sor sémája és segédosztálya

```dart
// lib/core/database/sync_queue_helper.dart
import 'dart:convert';
import 'package:sqflite/sqflite.dart';
import 'database_helper.dart'; // a 11. héten megírt DatabaseHelper

class SyncItem {
  final int? id;
  final String tableName;
  final String recordId;
  final String operation; // 'CREATE', 'UPDATE', 'DELETE'
  final Map<String, dynamic> payload;
  final int retryCount;

  SyncItem({
    this.id,
    required this.tableName,
    required this.recordId,
    required this.operation,
    required this.payload,
    this.retryCount = 0,
  });

  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'table_name': tableName,
      'record_id': recordId,
      'operation': operation,
      'payload': json.encode(payload),
      'retry_count': retryCount,
    };
  }

  factory SyncItem.fromMap(Map<String, dynamic> map) {
    return SyncItem(
      id: map['id'] as int?,
      tableName: map['table_name'] as String,
      recordId: map['record_id'] as String,
      operation: map['operation'] as String,
      payload: json.decode(map['payload'] as String) as Map<String, dynamic>,
      retryCount: map['retry_count'] as int,
    );
  }
}
```

### 3. Szinkronizációs Motor (Sync Engine) megvalósítása

Ez a háttérben futó motor felelős a várólista elemeinek beküldéséért az API-ra.

```dart
// lib/core/network/sync_engine.dart
import 'package:dio/dio.dart';
import '../database/sync_queue_helper.dart';
import 'database_helper.dart';
import 'network_info.dart';

class SyncEngine {
  final Dio dio;
  final NetworkInfo networkInfo;

  SyncEngine({required this.dio, required this.networkInfo});

  bool _isSyncing = false;
  bool get isSyncing => _isSyncing;

  // Elindítja a szinkronizációt
  Future<void> syncOutbox() async {
    // Ha már fut a szinkron vagy nincs net, azonnal lépjünk ki
    if (_isSyncing || !(await networkInfo.isConnected)) return;

    _isSyncing = true;
    final db = await DatabaseHelper.instance.database;

    try {
      // 1. Lekérjük a függőben lévő elemeket a sorból (leggrégebbit először)
      final List<Map<String, dynamic>> maps = await db.query(
        'sync_queue',
        orderBy: 'id ASC',
      );

      final List<SyncItem> queue = maps.map((e) => SyncItem.fromMap(e)).toList();

      for (var item in queue) {
        // Ha egy tétel túl sokszor elbukott, hagyjuk ki ( poison pill elkerülése )
        if (item.retryCount >= 5) continue;

        bool success = false;

        try {
          // 2. Művelet végrehajtása az API-n
          if (item.operation == 'CREATE') {
            await dio.post('/${item.tableName}/', data: item.payload);
            success = true;
          } else if (item.operation == 'UPDATE') {
            await dio.put('/${item.tableName}/${item.recordId}/', data: item.payload);
            success = true;
          } else if (item.operation == 'DELETE') {
            await dio.delete('/${item.tableName}/${item.recordId}/');
            success = true;
          }
        } on DioException catch (e) {
          // Hálózati szakadás vagy szerver hiba esetén
          if (e.response != null && e.response!.statusCode! >= 400 && e.response!.statusCode! < 500) {
            // Kliens hiba (pl. 400 Bad Request vagy 422 Validáció) - ezt nem érdemes újrapróbálni,
            // valószínűleg rossz a payload. Jelöljük meg vagy töröljük, hogy ne blokkolja a sort.
            success = false;
          } else {
            // Szerver hiba (pl. 500 vagy nincs net) - álljunk meg, később újrapróbáljuk
            break;
          }
        }

        if (success) {
          // 3. Ha sikeres volt az API hívás, töröljük a tételt a szinkronizációs sorból
          await db.delete('sync_queue', where: 'id = ?', whereArgs: [item.id]);
        } else {
          // 4. Sikertelenség esetén növeljük az újrapróbálkozások számát
          await db.update(
            'sync_queue',
            {'retry_count': item.retryCount + 1},
            where: 'id = ?',
            whereArgs: [item.id],
          );
        }
      }
    } catch (_) {
      // Globális hiba kezelése
    } finally {
      _isSyncing = false;
    }
  }
}
```

---

## Gyakorlófeladatok & Megoldások

### Gyakorlófeladat
Írj egy olyan szinkronizációs tábla sémát és egy Dart függvényt, amely biztosítja, hogy ha egy objektumot offline módban többször is módosítottak (pl. a jegyzet címét 3-szor is átírták), ne keletkezzen 3 különálló `UPDATE` rekord a szinkronizációs sorban, hanem a meglévő rekord frissüljön (sor optimalizálás).

### Megoldás

A sor optimalizálását a beszúrás előtt kell elvégezni. Ha már létezik egy függőben lévő `UPDATE` vagy `CREATE` kérés ugyanarra a rekordra, akkor a meglévőt írjuk felül az új adatokkal.

```dart
// lib/core/database/sync_queue_helper.dart kiegészítése

Future<void> queueSyncItem({
  required String tableName,
  required String recordId,
  required String operation,
  required Map<String, dynamic> payload,
}) async {
  final db = await DatabaseHelper.instance.database;

  // Ellenőrizzük, hogy van-e már függőben lévő művelet ugyanehhez a rekordhoz
  final List<Map<String, dynamic>> existing = await db.query(
    'sync_queue',
    where: 'table_name = ? AND record_id = ?',
    whereArgs: [tableName, recordId],
  );

  if (existing.isNotEmpty) {
    final existingItem = SyncItem.fromMap(existing.first);
    
    if (existingItem.operation == 'CREATE' && operation == 'UPDATE') {
      // Ha még létre sincs hozva a szerveren, de már frissítettük offline, 
      // egyszerűen frissítsük a CREATE payload-ját a legújabb adatokkal
      await db.update(
        'sync_queue',
        {
          'payload': json.encode(payload),
          'retry_count': 0, // Reseteljük az újrapróbálást
        },
        where: 'id = ?',
        whereArgs: [existingItem.id],
      );
    } else if (existingItem.operation == 'UPDATE' && operation == 'UPDATE') {
      // Ha már van egy függő frissítés, írjuk felül a payload-ot a legfrissebbel
      await db.update(
        'sync_queue',
        {
          'payload': json.encode(payload),
          'retry_count': 0,
        },
        where: 'id = ?',
        whereArgs: [existingItem.id],
      );
    }
    // Ha DELETE jön egy meglévő CREATE-re, törölhetjük a teljes sort, mert meg sem kell születnie élesben!
  } else {
    // Ha nincs még függő művelet, simán beszúrjuk az újat
    final newItem = SyncItem(
      tableName: tableName,
      recordId: recordId,
      operation: operation,
      payload: payload,
    );
    await db.insert('sync_queue', newItem.toMap());
  }
}
```

---

## Heti Mini Projekt: Offline Raktárkészlet App

**Projekt leírása:**
Készíts egy olyan offline raktárkészlet nyilvántartó alkalmazást, ahol a termékek darabszámát lehet növelni és csökkenteni.
1.  **Működés:** A módosítások azonnal lefutnak a lokális SQLite adatbázisban, és a UI frissül. A háttérben bejegyzés kerül a `sync_queue` táblába.
2.  **Hálózatkezelés:** Az alkalmazás figyeli a hálózatot. Amikor a telefon visszakapcsolódik az internetre, automatikusan lefut a szinkronizáció.
3.  **UI jelzések:** A termékek mellett jelenjen meg egy státusz ikon:
    *   Felhő ikon zöld pipával: szinkronizálva.
    *   Homokóra ikon: szinkronizálásra vár (offline módosítás).
    *   Figyelmeztető ikon: a szinkronizáció hibára futott.

### Teljes, működőképes kód

```dart
// lib/main.dart
import 'dart:async';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:sqflite/sqflite.dart';
import 'package:path/path.dart' as p;
import 'package:connectivity_plus/connectivity_plus.dart';
import 'package:dio/dio.dart';

// --- MOCK API INTERCEPTOR ---
// Szimulálja a távoli backendet
class MockStockAdapter extends HttpClientAdapter {
  final Map<String, int> _serverStock = {
    'prod-1': 10,
    'prod-2': 25,
    'prod-3': 5,
  };

  @override
  Future<ResponseBody> fetch(
    RequestOptions options,
    Stream<void>? requestStream,
    Future<void>? cancelFuture,
  ) async {
    final path = options.path;
    final method = options.method;

    // PUT /stock/{id}/ - Készlet frissítés
    if (path.contains('/stock/') && method == 'PUT') {
      final segments = path.split('/');
      final id = segments[segments.length - 2];
      final body = json.decode(options.data.toString()) as Map<String, dynamic>;
      final int newQuantity = body['quantity'] as int;
      
      _serverStock[id] = newQuantity;

      return ResponseBody.fromString(
        '{"id": "$id", "quantity": $newQuantity, "status": "updated"}',
        200,
        headers: {Headers.contentTypeHeader: [Headers.jsonContentType]},
      );
    }
    return ResponseBody.fromString('{"error": "Not Found"}', 404);
  }

  @override
  void close({bool force = false}) {}
}

// --- DATABASE HELPER ---
class AppDatabase {
  static final AppDatabase instance = AppDatabase._init();
  static Database? _database;

  AppDatabase._init();

  Future<Database> get database async {
    if (_database != null) return _database!;
    _database = await _initDB('stock_app.db');
    return _database!;
  }

  Future<Database> _initDB(String filePath) async {
    final dbPath = await getDatabasesPath();
    final path = p.join(dbPath, filePath);

    return await openDatabase(path, version: 1, onCreate: _createDB);
  }

  Future<void> _createDB(Database db, int version) async {
    // Termékek tábla
    await db.execute('''
      CREATE TABLE products (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        sync_status TEXT NOT NULL -- 'synced', 'pending', 'error'
      )
    ''');

    // Szinkronizációs sor tábla
    await db.execute('''
      CREATE TABLE sync_queue (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        table_name TEXT NOT NULL,
        record_id TEXT NOT NULL,
        operation TEXT NOT NULL,
        payload TEXT NOT NULL,
        retry_count INTEGER NOT NULL
      )
    ''');

    // Alap adatok feltöltése
    await db.insert('products', {'id': 'prod-1', 'name': 'Laptop állvány', 'quantity': 10, 'sync_status': 'synced'});
    await db.insert('products', {'id': 'prod-2', 'name': 'Vezeték nélküli egér', 'quantity': 25, 'sync_status': 'synced'});
    await db.insert('products', {'id': 'prod-3', 'name': 'Mechanikus billentyűzet', 'quantity': 5, 'sync_status': 'synced'});
  }
}

// --- NETWORK STATE WATCHER ---
class ConnectivityService {
  final _connectivity = Connectivity();

  Stream<bool> get onConnectionChanged {
    return _connectivity.onConnectivityChanged.map((results) {
      if (results.isEmpty) return false;
      return results.any((r) => r != ConnectivityResult.none);
    });
  }

  Future<bool> get isOnline async {
    final result = await _connectivity.checkConnectivity();
    if (result.isEmpty) return false;
    return result.any((r) => r != ConnectivityResult.none);
  }
}

// --- PROVIDER / APP LOGIC ---
class StockProvider extends ChangeNotifier {
  final ConnectivityService _connectivityService = ConnectivityService();
  final Dio _dio = Dio()..httpClientAdapter = MockStockAdapter();
  
  List<Map<String, dynamic>> _products = [];
  List<Map<String, dynamic>> get products => _products;

  bool _isOnline = true;
  bool get isOnline => _isOnline;

  bool _isSyncing = false;
  bool get isSyncing => _isSyncing;

  StreamSubscription? _connectivitySubscription;

  StockProvider() {
    _init();
  }

  void _init() async {
    await loadLocalProducts();
    _isOnline = await _connectivityService.isOnline;
    notifyListeners();

    // Figyeljük az internet változásait, és ha online-ok leszünk, indítsuk el a szinkronizációt
    _connectivitySubscription = _connectivityService.onConnectionChanged.listen((online) async {
      _isOnline = online;
      notifyListeners();
      if (online) {
        await syncQueue();
      }
    });
  }

  @override
  void dispose() {
    _connectivitySubscription?.cancel();
    super.dispose();
  }

  Future<void> loadLocalProducts() async {
    final db = await AppDatabase.instance.database;
    _products = await db.query('products');
    notifyListeners();
  }

  // Készlet frissítés offline-first módon
  Future<void> updateStock(String productId, int newQuantity) async {
    final db = await AppDatabase.instance.database;

    // 1. Lokális adatbázis frissítése azonnal a UI zökkenőmentes futásához
    await db.update(
      'products',
      {
        'quantity': newQuantity,
        'sync_status': 'pending', // Jelöljük meg szinkronizálásra váróként
      },
      where: 'id = ?',
      whereArgs: [productId],
    );

    // 2. Szinkronizációs elem hozzáadása a sorhoz
    final payload = {'quantity': newQuantity};
    
    // Optimalizálás: ha már van függő módosítás ugyanerre a termékre, írjuk felül
    final List<Map<String, dynamic>> existing = await db.query(
      'sync_queue',
      where: 'record_id = ?',
      whereArgs: [productId],
    );

    if (existing.isNotEmpty) {
      await db.update(
        'sync_queue',
        {'payload': json.encode(payload), 'retry_count': 0},
        where: 'id = ?',
        whereArgs: [existing.first['id']],
      );
    } else {
      await db.insert('sync_queue', {
        'table_name': 'stock',
        'record_id': productId,
        'operation': 'UPDATE',
        'payload': json.encode(payload),
        'retry_count': 0,
      });
    }

    await loadLocalProducts();

    // 3. Megpróbáljuk elindítani a szinkront, ha éppen online vagyunk
    if (_isOnline) {
      await syncQueue();
    }
  }

  // Szinkronizációs motor
  Future<void> syncQueue() async {
    if (_isSyncing) return;
    _isSyncing = true;
    notifyListeners();

    final db = await AppDatabase.instance.database;
    final List<Map<String, dynamic>> queueMaps = await db.query('sync_queue', orderBy: 'id ASC');

    for (var row in queueMaps) {
      final id = row['id'] as int;
      final productId = row['record_id'] as String;
      final payload = json.decode(row['payload'] as String) as Map<String, dynamic>;
      final retryCount = row['retry_count'] as int;

      if (retryCount >= 3) {
        // Poison-pill: ha 3-szor is elbukott, jelöljük meg a terméket hibás státusszal
        await db.update('products', {'sync_status': 'error'}, where: 'id = ?', whereArgs: [productId]);
        continue;
      }

      bool success = false;

      try {
        // API hívás szimulálása
        final response = await _dio.put('/stock/$productId/', data: payload);
        if (response.statusCode == 200) {
          success = true;
        }
      } catch (_) {
        success = false;
      }

      if (success) {
        // Törlés a szinkron sorból
        await db.delete('sync_queue', where: 'id = ?', whereArgs: [id]);
        // Átállítás szinkronizáltra a termék táblában
        await db.update('products', {'sync_status': 'synced'}, where: 'id = ?', whereArgs: [productId]);
      } else {
        // Újrapróbálási számláló növelése
        await db.update('sync_queue', {'retry_count': retryCount + 1}, where: 'id = ?', whereArgs: [id]);
      }
    }

    await loadLocalProducts();
    _isSyncing = false;
    notifyListeners();
  }
}

// --- UI SCREENS ---
void main() {
  runApp(
    ChangeNotifierProvider(
      create: (_) => StockProvider(),
      child: const MaterialApp(
        home: StockListScreen(),
      ),
    ),
  );
}

class StockListScreen extends StatelessWidget {
  const StockListScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final provider = context.watch<StockProvider>();

    return Scaffold(
      appBar: AppBar(
        title: const Text('Raktár Készlet (Offline-First)'),
        backgroundColor: provider.isOnline ? Colors.green : Colors.orange,
        actions: [
          Padding(
            padding: const EdgeInsets.only(right: 16.0),
            child: Center(
              child: Text(
                provider.isOnline ? 'ONLINE' : 'OFFLINE',
                style: const TextStyle(fontWeight: FontWeight.bold),
              ),
            ),
          )
        ],
      ),
      body: provider.products.isEmpty
          ? const Center(child: CircularProgressIndicator())
          : ListView.builder(
              itemCount: provider.products.length,
              itemBuilder: (context, index) {
                final product = provider.products[index];
                final String id = product['id'] as String;
                final int qty = product['quantity'] as int;
                final String status = product['sync_status'] as String;

                Widget statusIcon;
                if (status == 'synced') {
                  statusIcon = const Icon(Icons.cloud_done, color: Colors.green);
                } else if (status == 'pending') {
                  statusIcon = const Icon(Icons.hourglass_empty, color: Colors.orange);
                } else {
                  statusIcon = const Icon(Icons.cloud_off, color: Colors.red);
                }

                return Card(
                  margin: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                  child: ListTile(
                    title: Text(product['name'] as String, style: const TextStyle(fontWeight: FontWeight.bold)),
                    subtitle: Text('Készlet: $qty db'),
                    leading: statusIcon,
                    trailing: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        IconButton(
                          icon: const Icon(Icons.remove_circle_outline, color: Colors.red),
                          onPressed: qty > 0 ? () => provider.updateStock(id, qty - 1) : null,
                        ),
                        IconButton(
                          icon: const Icon(Icons.add_circle_outline, color: Colors.green),
                          onPressed: () => provider.updateStock(id, qty + 1),
                        ),
                      ],
                    ),
                  ),
                );
              },
            ),
    );
  }
}
```

---

## Heti Ellenőrző Kérdések

1.  **Miért hívjuk az Offline-First architektúrát "Single Source of Truth" (Egyetlen Igazságforrás) mintának a lokális adatbázis szempontjából?**
    *   *Válasz:* Mert az Offline-First modellben a felhasználói felület (UI) soha nem rajzol adatot közvetlenül az API válaszból. A UI kizárólag a helyi adatbázisból (pl. SQLite) táplálkozik. Minden hálózati szinkronizáció a háttérben történik, és a letöltött adatok először a helyi adatbázisba kerülnek mentésre, ami automatikusan frissíti a felületet. Így nincs esély arra, hogy a UI és a lokális tároló eltérő állapotot mutasson.
2.  **Mit jelent a "Poison Pill" (Mérgezett pirula) jelenség a szinkronizációs sorban, és hogyan védekezünk ellene?**
    *   *Válasz:* A Poison Pill egy olyan hibás rekord a szinkronizációs sorban, amelyet a backend szerver valamilyen validációs vagy logikai hiba miatt soha nem fog elfogadni (pl. negatív ár, vagy hiányzó kötelező mező). Ha nem védekezünk ellene, ez a hibás elem a sor elején ragad, és a szinkronizációs motor végtelen ciklusban próbálja újra és újra elküldeni, teljesen leblokkolva a sorban mögötte álló többi, egyébként helyes kérés feldolgozását. Védekezésként bevezetünk egy újrapróbálkozási számlálót (`retry_count`). Ha egy elem pl. 3 sikertelen kísérlet után sem megy át, kivesszük a sorból, és megjelöljük hibásként, így a sor többi része fel tud dolgozódni.
3.  **Hogyan működik az optimista UI frissítés visszavonása (Rollback) hiba esetén?**
    *   *Válasz:* Amikor elvégezzük a módosítást (pl. termék darabszámának növelése), a módosítás előtt el kell mentenünk az eredeti állapotot a memóriában vagy egy ideiglenes változóban. Ha a háttérben futó API kérés vagy a szinkronizáció véglegesen elbukik, egy visszaállító (Rollback) tranzakciót kell indítanunk: a mentett régi értékeket visszaírjuk a lokális adatbázisba, és meghívjuk a UI értesítőt (`notifyListeners()`), így a képernyőn visszaugrik a korábbi érték, miközben hibaüzenetet mutatunk a felhasználónak.
4.  **Mi a különbség a Last-Write-Wins (LWW) és a manuális konfliktusfeloldás között?**
    *   *Válasz:* A **Last-Write-Wins** egy automatikus feloldási technika, amely az adatok módosításának pontos időbélyegét (timestamp) használja. Amelyik módosítás később történt (akár a kliensen offline, akár a szerveren), az írja felül a korábbit. Ez egyszerű, de pontatlan lehet az eszközök óráinak eltérése miatt. A **manuális konfliktusfeloldás** során a rendszer észleli az ütközést, megállítja a folyamatot, és a felhasználó elé tárja a két verziót (pl. "Szerveren tárolt: XYZ" vs "Telefonodon szerkesztett: ABC"), és a felhasználónak kell kiválasztania, melyik verziót kívánja megtartani.
5.  **Hogyan segít a `connectivity_plus` csomag az akkumulátor élettartamának megőrzésében offline appoknál?**
    *   *Válasz:* Ha a connectivity_plus nélkül folyamatosan próbálnánk szinkronizálni (pl. egy háttérben futó 5 másodperces timerrel lekérdezni az API-t), a telefon rádióantennája folyamatosan ébren lenne, ami rendkívül gyorsan lemerítené az akkumulátort és elpazarolná a felhasználó adatkeretét. A connectivity_plus segítségével az alkalmazás passzív módban van: feliratkozik a rendszer szintű hálózati változás eseményre, és a szinkronizációs motort kizárólag akkor indítja el, amikor a telefon operációs rendszere jelzi, hogy újra elérhető az internetkapcsolat.
