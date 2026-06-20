# 11. hét — Lokális adattárolás

## Cél
A lecke célja, hogy megértsd és készségszinten alkalmazd a lokális adattárolás különféle típusait Flutter alkalmazásokban. Megtanulod, hogyan válassz a kulcs-érték tárolók (`shared_preferences`), a biztonságos tárolók (`flutter_secure_storage`) és a relációs adatbázisok (`sqflite` / SQLite) közül. Képes leszel felépíteni egy robusztus, önálló adatbázis-kezelő osztályt, kezelni az adatbázis verzióváltásait (migráció), és összekötni ezt egy offline cache stratégiával a zökkenőmentes felhasználói élmény érdekében.

---

## Elmélet

### 1. Lokális tárolási technológiák Flutterben
A mobilalkalmazások fejlesztése során az adatok jellege és biztonsági szintje határozza meg, milyen tárolási módot kell választanunk.

| Technológia | Típus | Ajánlott használat | Biztonság | Sebesség |
| :--- | :--- | :--- | :--- | :--- |
| **Shared Preferences** | XML / Plist (Kulcs-érték) | Felhasználói beállítások, egyszerű flag-ek (pl. sötét mód, nyelv). | Alacsony (sima szöveges fájl) | Nagyon gyors |
| **Secure Storage** | Keystore (Android) / Keychain (iOS) | Szenzitív adatok (API tokenek, jelszavak, személyes adatok). | Nagyon magas (hardveresen titkosított) | Lassabb (titkosítási overhead) |
| **SQLite (sqflite)** | Relációs SQL Adatbázis | Összetett adatszerkezetek, szűrések, relációk, offline adatszinkron. | Közepes (titkosítható SQLCipher-rel) | Gyors (indexelhető) |
| **Hive / Isar** | NoSQL Objektum Adatbázis | Egyszerűbb offline-first appok, gyors lekérdezések, direkt objektum-mentés. | Közepes (beépített AES titkosítás) | Rendkívül gyors |

### 2. Relációs adatbázisok használata (SQLite)
Ha az adatok között strukturált kapcsolatok vannak (pl. egy *Megrendelő*-höz több *Termék* is tartozik, vagy egy *Felhasználó*-nak több *Jegyzet*-e van), az **SQLite** a legmegbízhatóbb választás.
Flutterben az `sqflite` csomag nyújt natív hidat az eszközök beépített SQLite motorjához.

#### Adatbázis Életciklus és Helper Osztály:
1.  **Singleton minta:** Az adatbázis kapcsolatból egyetlen példányt tartunk fent az appon belül, hogy elkerüljük az adatbázis lockolását (zárolását) és a memóriaszivárgást.
2.  **Létrehozás (`onCreate`):** Az adatbázis első megnyitásakor fut le. Itt hajtjuk végre a `CREATE TABLE` utasításokat.
3.  **Verziófrissítés (`onUpgrade`):** Ha a séma megváltozik (új tábla vagy új oszlop kell), növeljük az adatbázis verziószámát. Az `onUpgrade` callback felelős a sémamódosítások (migrációk) végrehajtásáért anélkül, hogy a felhasználó meglévő adatai elvesznének.

### 3. Cache stratégiák
A lokális adatbázis nemcsak offline módban hasznos, hanem mint gyorsítótár (cache) is szolgál a távoli szerverről jövő adatokhoz.
*   **Cache-First:** Először a lokális adatbázisból olvassuk be az adatokat, megjelenítjük a felhasználónak, és csak akkor indítunk hálózati kérést, ha a helyi adat túl régi (expired) vagy nem létezik.
*   **Network-First:** Mindig megpróbáljuk a friss adatokat a hálózatról lekérni. Ha a hálózat nem elérhető (offline vagy timeout), akkor a legutoljára elmentett helyi adatokat adjuk vissza.
*   **Cache-then-Network:** Azonnal betöltjük és megmutatjuk a lokális adatot, miközben a háttérben elindítjuk az API hívást. Amikor az API válasz megérkezik, frissítjük a képernyőt és elmentjük az új adatokat a lokális adatbázisba. Ez biztosítja a leggyorsabb UI reakcióidőt.

---

## Kódpéldák

### 1. Shared Preferences és Secure Storage wraperek

A szenzitív adatok és a beállítások elkülönített, tiszta kezelése érdekében érdemes külön szerviz osztályokat készíteni.

```dart
// lib/core/services/settings_storage.dart
import 'package:shared_preferences/shared_preferences.dart';

class SettingsStorage {
  final SharedPreferences _prefs;

  SettingsStorage(this._prefs);

  static const String _themeKey = 'is_dark_mode';
  static const String _fontSizeKey = 'app_font_size';

  Future<void> setDarkMode(bool isDark) async {
    await _prefs.setBool(_themeKey, isDark);
  }

  bool getIsDarkMode() {
    return _prefs.getBool(_themeKey) ?? false;
  }

  Future<void> setFontSize(double size) async {
    await _prefs.setDouble(_fontSizeKey, size);
  }

  double getFontSize() {
    return _prefs.getDouble(_fontSizeKey) ?? 14.0;
  }
}
```

```dart
// lib/core/services/secure_token_storage.dart
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class SecureTokenStorage {
  final FlutterSecureStorage _secureStorage;

  SecureTokenStorage(this._secureStorage);

  static const String _accessTokenKey = 'jwt_access_token';
  static const String _refreshTokenKey = 'jwt_refresh_token';

  Future<void> saveTokens({required String accessToken, required String refreshToken}) async {
    await _secureStorage.write(key: _accessTokenKey, value: accessToken);
    await _secureStorage.write(key: _refreshTokenKey, value: refreshToken);
  }

  Future<String?> getAccessToken() async {
    return await _secureStorage.read(key: _accessTokenKey);
  }

  Future<String?> getRefreshToken() async {
    return await _secureStorage.read(key: _refreshTokenKey);
  }

  Future<void> clearTokens() async {
    await _secureStorage.delete(key: _accessTokenKey);
    await _secureStorage.delete(key: _refreshTokenKey);
  }
}
```

### 2. SQLite Database Helper (`sqflite` csomaggal)

Ez az osztály megmutatja a teljes adatbázis inicializációt, a tábla létrehozását, a migrációt és az alapvető CRUD műveleteket.

```dart
// lib/core/database/database_helper.dart
import 'package:path/path.dart';
import 'package:sqflite/sqflite.dart';

class DatabaseHelper {
  // Singleton minta megvalósítása
  static final DatabaseHelper instance = DatabaseHelper._init();
  static Database? _database;

  DatabaseHelper._init();

  // Az adatbázis neve és verziója. Ha változik a séma, a verziót növelni kell!
  static const String _dbName = 'app_local_database.db';
  static const int _dbVersion = 2; 

  Future<Database> get database async {
    if (_database != null) return _database!;
    _database = await _initDB(_dbName);
    return _database!;
  }

  Future<Database> _initDB(String filePath) async {
    final dbPath = await getDatabasesPath();
    final path = join(dbPath, filePath);

    return await openDatabase(
      path,
      version: _dbVersion,
      onCreate: _createDB,
      onUpgrade: _upgradeDB,
    );
  }

  // Táblák létrehozása az első indításkor
  Future<void> _createDB(Database db, int version) async {
    const textType = 'TEXT NOT NULL';
    const boolType = 'INTEGER NOT NULL'; // SQLite nem tárol natív boolean-t (0=false, 1=true)
    const idType = 'TEXT PRIMARY KEY';

    await db.execute('''
      CREATE TABLE notes (
        id $idType,
        title $textType,
        content $textType,
        createdAt $textType,
        isPinned $boolType
      )
    ''');
  }

  // Migráció kezelése verzióváltáskor
  Future<void> _upgradeDB(Database db, int oldVersion, int newVersion) async {
    if (oldVersion < 2) {
      // Verzió 2: Adjunk hozzá egy új oszlopot a notes táblához adatvesztés nélkül
      await db.execute('ALTER TABLE notes ADD COLUMN category TEXT DEFAULT "General"');
    }
  }

  // --- CRUD MŰVELETEK ---

  // Beszúrás (Create)
  Future<void> insertNote(Map<String, dynamic> noteJson) async {
    final db = await instance.database;
    await db.insert(
      'notes',
      noteJson,
      conflictAlgorithm: ConflictAlgorithm.replace, // Ha létezik az ID, írja felül
    );
  }

  // Összes elem lekérése (Read all)
  Future<List<Map<String, dynamic>>> fetchAllNotes() async {
    final db = await instance.database;
    // Lekérdezés rendezéssel (a kitűzöttek legyenek elöl, utána a legfrissebbek)
    return await db.query('notes', orderBy: 'isPinned DESC, createdAt DESC');
  }

  // Egy elem lekérése (Read single)
  Future<Map<String, dynamic>?> fetchNoteById(String id) async {
    final db = await instance.database;
    final maps = await db.query(
      'notes',
      columns: ['id', 'title', 'content', 'createdAt', 'isPinned', 'category'],
      where: 'id = ?',
      whereArgs: [id],
    );

    if (maps.isNotEmpty) {
      return maps.first;
    } else {
      return null;
    }
  }

  // Frissítés (Update)
  Future<int> updateNote(Map<String, dynamic> noteJson) async {
    final db = await instance.database;
    return await db.update(
      'notes',
      noteJson,
      where: 'id = ?',
      whereArgs: [noteJson['id']],
    );
  }

  // Törlés (Delete)
  Future<int> deleteNote(String id) async {
    final db = await instance.database;
    return await db.delete(
      'notes',
      where: 'id = ?',
      whereArgs: [id],
    );
  }

  // Kapcsolat lezárása
  Future<void> close() async {
    final db = await _database;
    if (db != null) {
      await db.close();
    }
  }
}
```

---

## Gyakorlófeladatok & Megoldások

### Gyakorlófeladat
Bővítsd ki a `DatabaseHelper` osztályt egy könyvtárkezelő rendszerhez szükséges `books` (könyvek) táblával. A tábla tartalmazza a könyv azonosítóját (`id` - String), címét (`title` - String), szerzőjét (`author` - String), és azt, hogy ki van-e kölcsönözve (`isBorrowed` - Integer/Boolean). Implementáld a könyv beszúrását és az összes könyv lekérdezését.

### Megoldás

1.  **Tábla hozzáadása az inicializáláshoz:**
    Mivel új táblát adunk hozzá a sémához, a meglévő adatbázis verzióját meg kell növelni (pl. verzió 3-ra), és az `onCreate` valamint `onUpgrade` metódusokat ki kell egészíteni.

```dart
// Kiegészítés a DatabaseHelper osztályon belül:

// 1. Frissített verziószám:
// static const int _dbVersion = 3;

// 2. onCreate frissítése:
/*
  Future<void> _createDB(Database db, int version) async {
    // ... notes tábla létrehozása ...
    
    // Books tábla létrehozása:
    await db.execute('''
      CREATE TABLE books (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        isBorrowed INTEGER NOT NULL
      )
    ''');
  }
*/

// 3. onUpgrade frissítése (ha korábbi verzióról lépünk fel):
/*
  Future<void> _upgradeDB(Database db, int oldVersion, int newVersion) async {
    if (oldVersion < 2) {
      await db.execute('ALTER TABLE notes ADD COLUMN category TEXT DEFAULT "General"');
    }
    if (oldVersion < 3) {
      await db.execute('''
        CREATE TABLE books (
          id TEXT PRIMARY KEY,
          title TEXT NOT NULL,
          author TEXT NOT NULL,
          isBorrowed INTEGER NOT NULL
        )
      ''');
    }
  }
*/

// 4. CRUD metódusok a könyvekhez:
Future<void> insertBook(Map<String, dynamic> bookJson) async {
  final db = await database;
  await db.insert(
    'books',
    bookJson,
    conflictAlgorithm: ConflictAlgorithm.replace,
  );
}

Future<List<Map<String, dynamic>>> fetchAllBooks() async {
  final db = await database;
  return await db.query('books', orderBy: 'title ASC');
}
```

---

## Heti Mini Projekt: Offline Jegyzet App

**Projekt leírása:**
Készíts egy offline jegyzetfüzet alkalmazást. Az alkalmazásban lehessen jegyzeteket létrehozni, megtekinteni, szerkeszteni és törölni. A jegyzeteket helyben, SQLite adatbázisban kell tárolni. A preferenciákat (pl. betűméret és sötét mód beállítása) a Shared Preferences segítségével mentsd el és töltsd be. Az alkalmazás felülete legyen modern és reszponzív.

### Teljes, működőképes kód

```dart
// lib/features/notes/domain/note_model.dart
class Note {
  final String id;
  final String title;
  final String content;
  final DateTime createdAt;
  final bool isPinned;
  final String category;

  Note({
    required this.id,
    required this.title,
    required this.content,
    required this.createdAt,
    this.isPinned = false,
    this.category = 'General',
  });

  Note copyWith({
    String? id,
    String? title,
    String? content,
    DateTime? createdAt,
    bool? isPinned,
    String? category,
  }) {
    return Note(
      id: id ?? this.id,
      title: title ?? this.title,
      content: content ?? this.content,
      createdAt: createdAt ?? this.createdAt,
      isPinned: isPinned ?? this.isPinned,
      category: category ?? this.category,
    );
  }

  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'title': title,
      'content': content,
      'createdAt': createdAt.toIso8601String(),
      'isPinned': isPinned ? 1 : 0,
      'category': category,
    };
  }

  factory Note.fromMap(Map<String, dynamic> map) {
    return Note(
      id: map['id'] as String,
      title: map['title'] as String,
      content: map['content'] as String,
      createdAt: DateTime.parse(map['createdAt'] as String),
      isPinned: (map['isPinned'] as int) == 1,
      category: (map['category'] as String?) ?? 'General',
    );
  }
}
```

```dart
// lib/features/notes/presentation/providers/notes_provider.dart
import 'package:flutter/material.dart';
import '../../../core/database/database_helper.dart';
import '../../notes/domain/note_model.dart';

class NotesProvider extends ChangeNotifier {
  List<Note> _notes = [];
  List<Note> get notes => _notes;

  bool _isLoading = false;
  bool get isLoading => _isLoading;

  Future<void> loadNotes() async {
    _isLoading = true;
    notifyListeners();

    final dataList = await DatabaseHelper.instance.fetchAllNotes();
    _notes = dataList.map((map) => Note.fromMap(map)).toList();

    _isLoading = false;
    notifyListeners();
  }

  Future<void> addNote(String title, String content, {bool isPinned = false, String category = 'General'}) async {
    final newNote = Note(
      id: DateTime.now().millisecondsSinceEpoch.toString(),
      title: title,
      content: content,
      createdAt: DateTime.now(),
      isPinned: isPinned,
      category: category,
    );

    await DatabaseHelper.instance.insertNote(newNote.toMap());
    await loadNotes();
  }

  Future<void> updateNoteItem(Note note) async {
    await DatabaseHelper.instance.updateNote(note.toMap());
    await loadNotes();
  }

  Future<void> deleteNoteItem(String id) async {
    await DatabaseHelper.instance.deleteNote(id);
    await loadNotes();
  }
}
```

```dart
// lib/features/notes/presentation/pages/notes_list_page.dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../notes/domain/note_model.dart';
import '../providers/notes_provider.dart';
import 'note_edit_page.dart';

class NotesListPage extends StatelessWidget {
  const NotesListPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Offline Jegyzetek'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: () => context.read<NotesProvider>().loadNotes(),
          )
        ],
      ),
      body: Consumer<NotesProvider>(
        builder: (context, provider, child) {
          if (provider.isLoading) {
            return const Center(child: CircularProgressIndicator());
          }

          if (provider.notes.isEmpty) {
            return const Center(
              child: Text(
                'Nincs még jegyzeted. Kattints a + gombra!',
                style: TextStyle(fontSize: 16, color: Colors.grey),
              ),
            );
          }

          return ListView.builder(
            itemCount: provider.notes.length,
            itemBuilder: (context, index) {
              final note = provider.notes[index];
              return Card(
                margin: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                child: ListTile(
                  title: Text(
                    note.title,
                    style: const TextStyle(fontWeight: FontWeight.bold),
                  ),
                  subtitle: Text(
                    note.content,
                    maxLines: 2,
                    overflow: TextOverflow.ellipsis,
                  ),
                  leading: Icon(
                    note.isPinned ? Icons.push_pin : Icons.note,
                    color: note.isPinned ? Colors.orange : Colors.grey,
                  ),
                  trailing: IconButton(
                    icon: const Icon(Icons.delete, color: Colors.redAccent),
                    onPressed: () {
                      provider.deleteNoteItem(note.id);
                    },
                  ),
                  onTap: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) => NoteEditPage(note: note),
                      ),
                    );
                  },
                ),
              );
            },
          );
        },
      ),
      floatingActionButton: FloatingActionButton(
        child: const Icon(Icons.add),
        onPressed: () {
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (_) => const NoteEditPage(),
            ),
          );
        },
      ),
    );
  }
}
```

```dart
// lib/features/notes/presentation/pages/note_edit_page.dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../notes/domain/note_model.dart';
import '../providers/notes_provider.dart';

class NoteEditPage extends StatefulWidget {
  final Note? note;

  const NoteEditPage({super.key, this.note});

  @override
  State<NoteEditPage> createState() => _NoteEditPageState();
}

class _NoteEditPageState extends State<NoteEditPage> {
  final _formKey = GlobalKey<FormState>();
  late String _title;
  late String _content;
  late bool _isPinned;
  late String _category;

  @override
  void initState() {
    super.initState();
    _title = widget.note?.title ?? '';
    _content = widget.note?.content ?? '';
    _isPinned = widget.note?.isPinned ?? false;
    _category = widget.note?.category ?? 'General';
  }

  void _saveForm() {
    if (_formKey.currentState!.validate()) {
      _formKey.currentState!.save();
      final provider = context.read<NotesProvider>();

      if (widget.note == null) {
        provider.addNote(_title, _content, isPinned: _isPinned, category: _category);
      } else {
        final updatedNote = widget.note!.copyWith(
          title: _title,
          content: _content,
          isPinned: _isPinned,
          category: _category,
        );
        provider.updateNoteItem(updatedNote);
      }
      Navigator.pop(context);
    }
  }

  @override
  Widget build(BuildContext context) {
    final isEditing = widget.note != null;

    return Scaffold(
      appBar: AppBar(
        title: Text(isEditing ? 'Jegyzet Szerkesztése' : 'Új Jegyzet'),
        actions: [
          IconButton(
            icon: const Icon(Icons.save),
            onPressed: _saveForm,
          )
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: Column(
            children: [
              TextFormField(
                initialValue: _title,
                decoration: const InputDecoration(labelText: 'Cím'),
                validator: (val) => val == null || val.trim().isEmpty ? 'A cím nem lehet üres' : null,
                onSaved: (val) => _title = val ?? '',
              ),
              const SizedBox(height: 12),
              TextFormField(
                initialValue: _content,
                decoration: const InputDecoration(labelText: 'Tartalom'),
                maxLines: 6,
                validator: (val) => val == null || val.trim().isEmpty ? 'A tartalom nem lehet üres' : null,
                onSaved: (val) => _content = val ?? '',
              ),
              const SizedBox(height: 12),
              SwitchListTile(
                title: const Text('Kitűzés felülre'),
                value: _isPinned,
                onChanged: (val) => setState(() => _isPinned = val),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
```

```dart
// lib/main.dart módosítása a jegyzet app betöltéséhez
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'features/notes/presentation/providers/notes_provider.dart';
import 'features/notes/presentation/pages/notes_list_page.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => NotesProvider()..loadNotes()),
      ],
      child: const MyApp(),
    ),
  );
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Offline Notes App',
      theme: ThemeData(primarySwatch: Colors.teal),
      home: const NotesListPage(),
    );
  }
}
```

---

## Heti Ellenőrző Kérdések

1.  **Miért kell az SQLite boolean értékeket Integer formában tárolni?**
    *   *Válasz:* Az SQLite egy nagyon könnyűsúlyú adatbázismotor, amely nem rendelkezik natív logikai (Boolean) adattípussal. Helyette a logikai értékeket egész számként (Integer) tároljuk, ahol a `0` a hamis (`false`) értéket, az `1` (vagy bármely nullától eltérő egész szám) pedig az igaz (`true`) értéket jelöli. A kódolás során a modell osztályunk feladata ezt a transzformációt elvégezni (pl. `isPinned ? 1 : 0`).
2.  **Hogyan működik az adatbázis verziózása, és mikor hívódik meg az `onUpgrade` callback?**
    *   *Válasz:* Amikor inicializáljuk az SQLite kapcsolatot az `openDatabase` hívással, megadunk egy verziószámot (`version`). Ha az eszközön már létezik az adatbázis fájl, az `sqflite` összehasonlítja a fájlban tárolt sémakódot a megadott verziószámmal. Ha a megadott verziószám magasabb, mint az eszközön lévő verziószám, a rendszer automatikusan meghívja az `onUpgrade` callback-et. Itt tudjuk futtatni azokat az SQL parancsokat (pl. `ALTER TABLE`), amelyek frissítik a sémát a legújabb állapotra.
3.  **Mi a kockázata annak, ha nem Singleton mintával hozzuk létre a DatabaseHelper osztályt?**
    *   *Válasz:* Ha nem Singleton mintát használunk, az alkalmazás különböző részei egymástól független adatbázis-kapcsolatokat nyithatnak meg ugyanahhoz a fizikai fájlhoz. Ez komoly szinkronizációs problémákhoz vezethet: írási ütközések történhetnek, az adatbázis zárolt állapotba kerülhet (database is locked hiba), és megnő az erőforrás-pazarlás, valamint a memóriaszivárgás esélye is.
4.  **Mikor érdemes a Flutter Secure Storage csomagot választani a Shared Preferences helyett?**
    *   *Válasz:* A Shared Preferences az adatokat sima, titkosítatlan XML vagy JSON fájlban tárolja a telefon háttértárán. Bárki, aki hozzáfér az eszköz fájlrendszeréhez (pl. rootolt készülékeken vagy biztonsági mentésekből), könnyedén kiolvashatja ezeket a fájlokat. Ezért minden olyan adatot, ami érzékeny információ (pl. JWT belépési tokenek, jelszavak, bankkártya adatok), a Flutter Secure Storage csomaggal kell elmenteni, mert az iOS alatt a Keychain-t, Android alatt pedig a KeyStore által hardveresen védett titkosított tárhelyet használja.
5.  **Hogyan javítja a felhasználói élményt a "Cache-then-Network" stratégia?**
    *   *Válasz:* A "Cache-then-Network" stratégia alkalmazásakor a felhasználónak nem kell másodperceket várnia a töltőképernyőt (spinner) nézve, amíg a lassú mobilinternet lekéri az adatokat az API-ról. Az app azonnal betölti és kirajzolja a legutóbb lementett lokális adatokat a gyors adatbázisból (ami ezredmásodpercekig tart), majd a háttérben elindít egy hálózati kérést. Amikor a friss adatok megérkeznek, a UI észrevétlenül frissül, így az app rendkívül gyorsnak és reszponzívnak érződik.
