# 7. hét — Async, Future, Stream, API

## Cél
A lecke célja, hogy elsajátítsd a Dart aszinkron programozási koncepcióit (Future, Stream, async/await), és megtanulj külső REST API-kkal kommunikálni. Megérted a Dart egy szálas (Single-Threaded) Event Loop modelljét, megtanulsz JSON adatokat modellezni, és elsajátítod a `http` és a `dio` csomagok használatát, beleértve a hibakezelést, a timeoutokat és a hálózati interceptorokat.

---

## Elmélet

### 1. A Dart Event Loop és az aszinkronitás
A Dart egy **egyszálú** programozási nyelv. Ez azt jelenti, hogy egyszerre csak egy műveletet tud végrehajtani. Hogyan lehetséges mégis, hogy egy hálózati kérés futása közben az UI nem fagy le, és a felhasználó továbbra is tud görgetni?

A válasz az **Event Loop (Eseményhurok)**.
A Dart háttérben két sort (Queue) tart fenn:
1.  **Microtask Queue:** Nagyon rövid, belső rendszerfeladatoknak (ritkán használjuk közvetlenül).
2.  **Event Queue:** Külső események (felhasználói kattintás, I/O művelet, hálózati válasz megérkezése, timer lefutása).

Amikor egy aszinkron műveletet indítunk (pl. HTTP kérés), a Dart átadja a feladatot az operációs rendszernek (vagy egy háttérszálnak natív szinten). Amikor a válasz megérkezik, a Dart elhelyez egy eseményt az Event Queue végén. Amikor a főszál felszabadul, az Event Loop kiveszi ezt az eseményt és végrehajtja a hozzá tartozó Dart kódot.

### 2. A Future fogalma és az async/await
A `Future` egy olyan objektum, amely egy jövőben elkészülő értéket (vagy hibát) reprezentál. Három állapota lehet:
*   **Uncompleted (Befejezetlen):** A háttérművelet még fut, az érték nem érhető el.
*   **Completed with value (Sikeresen befejezett):** A művelet lefutott, megkaptuk az eredményt.
*   **Completed with error (Hibával befejezett):** A művelet meghiúsult (pl. hálózati hiba, rossz URL).

Az `async` és `await` kulcsszavak segítségével az aszinkron kódunkat úgy írhatjuk meg, mintha szinkron (sorról sorra végrehajtódó) kód lenne, ami drasztikusan javítja az olvashatóságot a hagyományos callbackekkel (`.then()`, `.catchError()`) szemben.

### 3. A Stream fogalma
Míg a `Future` egyetlen egy jövőbeli értéket ad vissza (kérés-válasz modell), addig a `Stream` **értékek sorozatát** képes biztosítani az idő múlásával.
*   *Példa Future-re:* Egy HTTP GET kérés a termékek listájára.
*   *Példa Stream-re:* Egy chat alkalmazás üzenetei (Firebase Firestore-on keresztül), a telefon GPS koordinátáinak folyamatos változása, vagy egy letöltés százalékos állapota.

### 4. HTTP csomag vs. Dio csomag
Flutterben a hálózati kommunikációra két fő megoldást használunk:

| Funkció | `http` csomag | `dio` csomag |
|---|---|---|
| **Fejlesztő** | Dart csapat (hivatalos) | Közösségi (nagyon népszerű) |
| **Bonyolultság** | Egyszerű, minimalista | Haladó, funkciógazdag |
| **Timeout kezelés** | Manuálisan kell írni | Beépített paraméter |
| **Interceptorok** | Nincs alapból (burkolni kell) | Beépített támogatás |
| **Fájl feltöltés** | Bonyolultabb (MultipartRequest) | Egyszerű (FormData) |
| **Global Config** | Korlátozott | Nagyon erős (BaseOptions) |

### 5. JSON modellezés Dartban
A szerverről érkező válasz szinte mindig JSON formátumú. Mivel a Dart típusbiztos nyelv, a nyers `Map<String, dynamic>` típusú adatot célszerű egy egyedi Dart osztállyá (**Model**) alakítani.
Ezt manuálisan egy `factory` konstruktorral oldjuk meg:
```dart
factory Product.fromJson(Map<String, dynamic> json)
```
Nagyobb projektekben kódgenerátorokat (`json_serializable`, `freezed`) használunk, de az alapok megértéséhez elengedhetetlen a manuális parsing ismerete.

---

## Kódpéldák

### 1. Aszinkron függvény és késleltetés (`Future.delayed`)
Így szimulálunk egy aszinkron folyamatot, például egy adatbázis-lekérdezést.

```dart
Future<String> fetchUserNickname(String userId) async {
  print('Adatlekérés indul a háttérben...');
  // 2 másodpercre megállítjuk a végrehajtást ezen a szálon, de a UI nem fagy le
  await Future.delayed(const Duration(seconds: 2));
  
  if (userId == '123') {
    return 'FlutterMaster';
  } else {
    throw Exception('A felhasználó nem található!');
  }
}
```

### 2. UI kirajzolás `FutureBuilder` segítségével
A `FutureBuilder` egy olyan widget, amely automatikusan figyeli a `Future` állapotváltozásait, és annak megfelelően építi újra magát.

```dart
import 'package:flutter/material.dart';

class UserProfileWidget extends StatelessWidget {
  final String userId;

  const UserProfileWidget({super.key, required this.userId});

  // Fontos: a jövőbeli metódust célszerűbb StatefulWidget initState-ben tárolni,
  // de ha StatelessWidget-ben vagyunk, közvetlenül is hívható (bár vigyázni kell a rebuild-ekkel).
  Future<String> _fetchData() => fetchUserNickname(userId);

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<String>(
      future: _fetchData(),
      builder: (context, snapshot) {
        // 1. Állapot: Betöltés alatt (Waiting)
        if (snapshot.connectionState == ConnectionState.waiting) {
          return const Center(child: CircularProgressIndicator());
        }
        
        // 2. Állapot: Hiba történt (Error)
        if (snapshot.hasError) {
          return Center(
            child: Text(
              'Hiba: ${snapshot.error}',
              style: const TextStyle(color: Colors.red),
            ),
          );
        }

        // 3. Állapot: Sikerült megkapni az adatot (Data)
        if (snapshot.hasData) {
          final nickname = snapshot.data!;
          return Center(
            child: Text(
              'Felhasználónév: $nickname',
              style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
          );
        }

        return const Center(child: Text('Nincs adat.'));
      },
    );
  }
}
```

### 3. API lekérdezés a beépített `http` csomaggal (GET & POST)
Először adjuk hozzá a csomagot: `flutter pub add http`

```dart
import 'dart:convert';
import 'package:http/http.dart' as http;

class ProductService {
  static const String _baseUrl = 'https://jsonplaceholder.typicode.com';

  // GET kérés lefutása hibakezeléssel
  Future<List<dynamic>> fetchPosts() async {
    final url = Uri.parse('$_baseUrl/posts');
    
    try {
      final response = await http.get(
        url,
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
      ).timeout(const Duration(seconds: 10)); // Timeout kezelése

      if (response.statusCode == 200) {
        // UTF-8 dekódolás a magyar ékezetes karakterek miatt!
        final decodedData = jsonDecode(utf8.decode(response.bodyBytes));
        return decodedData as List<dynamic>;
      } else {
        throw Exception('Szerver hiba: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Hálózati hiba történt: $e');
    }
  }

  // POST kérés küldése JSON body-val
  Future<Map<String, dynamic>> createPost(String title, String body, int userId) async {
    final url = Uri.parse('$_baseUrl/posts');
    
    try {
      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json; charset=UTF-8'},
        body: jsonEncode({
          'title': title,
          'body': body,
          'userId': userId,
        }),
      );

      if (response.statusCode == 201) {
        return jsonDecode(response.body) as Map<String, dynamic>;
      } else {
        throw Exception('Nem sikerült létrehozni a bejegyzést: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Hiba a küldés során: $e');
    }
  }
}
```

### 4. JSON manuális modellezése (`fromJson`)
A kapott JSON objektumból biztonságos Dart objektum készítése.

```dart
class Post {
  final int id;
  final int userId;
  final String title;
  final String body;

  Post({
    required this.id,
    required this.userId,
    required this.title,
    required this.body,
  });

  // Factory konstruktor JSON mapből történő példányosításhoz
  factory Post.fromJson(Map<String, dynamic> json) {
    return Post(
      id: json['id'] as int,
      userId: json['userId'] as int,
      title: json['title'] as String? ?? 'Nincs cím',
      body: json['body'] as String? ?? '',
    );
  }

  // Dart objektum konvertálása vissza Map-pé (pl. POST kéréshez)
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'userId': userId,
      'title': title,
      'body': body,
    };
  }
}
```

### 5. Dio alapú lekérdezés Interceptor-ral
A `dio` csomag használata (`flutter pub add dio`). Az Interceptor segítségével minden kérés elé automatikusan beilleszthetjük pl. az Authorization headert (JWT tokent), és logolhatjuk a hibákat.

```dart
import 'package:dio/dio.dart';

class ApiClient {
  late final Dio _dio;

  ApiClient() {
    _dio = Dio(
      BaseOptions(
        baseUrl: 'https://jsonplaceholder.typicode.com',
        connectTimeout: const Duration(seconds: 5),
        receiveTimeout: const Duration(seconds: 5),
        headers: {'Accept': 'application/json'},
      ),
    );

    // Interceptorok hozzáadása
    _dio.interceptors.add(
      InterceptorsWrapper(
        onRequest: (options, handler) {
          // Itt fűzhetünk hozzá dinamikusan tokent secure storage-ból
          const mockToken = 'Bearer xyz123_my_secret_token';
          options.headers['Authorization'] = mockToken;
          
          print('--- KÉRÉS INDUL: ${options.method} ${options.path}');
          return handler.next(options); // Folytatja a kérést
        },
        onResponse: (response, handler) {
          print('--- VÁLASZ ÉRKEZETT: ${response.statusCode}');
          return handler.next(response);
        },
        onError: (DioException e, handler) {
          print('--- HIBA TÖRTÉNT: ${e.message}');
          // Itt lehet globálisan kezelni pl. a 401-es hiba kódokat (lejárt session)
          return handler.next(e);
        },
      ),
    );
  }

  Future<List<Post>> getPosts() async {
    try {
      final response = await _dio.get('/posts');
      final data = response.data as List;
      return data.map((json) => Post.fromJson(json as Map<String, dynamic>)).toList();
    } on DioException catch (e) {
      // Speciális Dio hibakezelés
      if (e.type == DioExceptionType.connectionTimeout) {
        throw Exception('Kapcsolódási időtúllépés!');
      }
      throw Exception('API hiba: ${e.response?.statusCode ?? "Ismeretlen hiba"}');
    }
  }
}
```

---

## Gyakorlófeladatok & Megoldások

### 1. Feladat: JSONPlaceholder felhasználók lekérése
Írj egy konzolban vagy egyszerű UI-on futtatható Dart kódot, ami a `https://jsonplaceholder.typicode.com/users` végpontról lekéri a felhasználókat, és kiírja a konzolra a neveiket és a várost, ahol laknak.

#### Megoldás:
```dart
import 'dart:convert';
import 'package:http/http.dart' as http;

Future<void> printUsers() async {
  final url = Uri.parse('https://jsonplaceholder.typicode.com/users');
  try {
    final response = await http.get(url);
    if (response.statusCode == 200) {
      final List<dynamic> users = jsonDecode(response.body);
      for (var user in users) {
        final name = user['name'];
        final city = user['address']['city'];
        print('Név: $name, Város: $city');
      }
    } else {
      print('Szerver hiba: ${response.statusCode}');
    }
  } catch (e) {
    print('Hálózati hiba: $e');
  }
}
```

### 2. Feladat: User Model osztály elkészítése
Készíts egy robusztus `User` modellt a fenti API-hoz. Tartalmazza a következő mezőket: `id`, `name`, `email`, és egy beágyazott `Address` modellt, amiben a `city` mező található.

#### Megoldás:
```dart
class Address {
  final String city;

  Address({required this.city});

  factory Address.fromJson(Map<String, dynamic> json) {
    return Address(
      city: json['city'] as String? ?? 'Nincs megadva',
    );
  }
}

class User {
  final int id;
  final String name;
  final String email;
  final Address address;

  User({
    required this.id,
    required this.name,
    required this.email,
    required this.address,
  });

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'] as int,
      name: json['name'] as String? ?? 'Névtelen',
      email: json['email'] as String? ?? '',
      address: Address.fromJson(json['address'] as Map<String, dynamic>),
    );
  }
}
```

### 3. Feladat: Spinner megjelenítése betöltés közben
Készíts egy StatefulWidget alapú oldalt, ami indításakor lekéri a felhasználók listáját. Amíg az adat nem érkezik meg, jeleníts meg egy `CircularProgressIndicator`-t a képernyő közepén!

#### Megoldás:
```dart
import 'package:flutter/material.dart';
// Feltételezzük a fenti User és Address modellek meglétét

class UserListLoaderPage extends StatefulWidget {
  const UserListLoaderPage({super.key});

  @override
  State<UserListLoaderPage> createState() => _UserListLoaderPageState();
}

class _UserListLoaderPageState extends State<UserListLoaderPage> {
  late Future<List<User>> _usersFuture;

  Future<List<User>> _fetchUsers() async {
    // Szimulált lassú hálózat kedvéért
    await Future.delayed(const Duration(seconds: 2));
    
    final response = await http.get(Uri.parse('https://jsonplaceholder.typicode.com/users'));
    if (response.statusCode == 200) {
      final List<dynamic> data = jsonDecode(response.body);
      return data.map((json) => User.fromJson(json)).toList();
    } else {
      throw Exception('Nem sikerült betölteni a felhasználókat');
    }
  }

  @override
  void initState() {
    super.initState();
    // A Future-t az initState-ben indítjuk el, így widget rebuild esetén nem fut le újra feleslegesen!
    _usersFuture = _fetchUsers();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Felhasználók')),
      body: FutureBuilder<List<User>>(
        future: _usersFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          if (snapshot.hasError) {
            return Center(child: Text('Hiba: ${snapshot.error}'));
          }
          if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return const Center(child: Text('Nincsenek felhasználók.'));
          }

          final users = snapshot.data!;
          return ListView.builder(
            itemCount: users.length,
            itemBuilder: (context, index) {
              final user = users[index];
              return ListTile(
                title: Text(user.name),
                subtitle: Text('${user.email} | ${user.address.city}'),
              );
            },
          );
        },
      ),
    );
  }
}
```

### 4. Feladat: Felhasználóbarát hibaüzenet
Módosítsd a fenti kódot úgy, hogy ha a hálózati kérés elbukik (pl. lekapcsolt internetnél), akkor ne a nyers Dart hibaüzenetet írja ki a felhasználónak, hanem egy szép piros kártyát egy hálózati ikonnal és a következő szöveggel: "Sikertelen kapcsolódás. Ellenőrizd az internetkapcsolatodat!".

#### Megoldás:
```dart
Widget _buildErrorWidget(Object? error) {
  return Center(
    padding: const EdgeInsets.all(20.0),
    child: Card(
      color: Colors.red.shade50,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Icon(Icons.wifi_off, size: 48, color: Colors.red),
            const SizedBox(height: 16),
            const Text(
              'Kapcsolódási hiba',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.red),
            ),
            const SizedBox(height: 8),
            const Text(
              'Nem sikerült elérni a szervert. Kérjük, ellenőrizd az internetkapcsolatodat és próbáld újra!',
              textAlign: TextAlign.center,
              style: TextStyle(color: Colors.black87),
            ),
          ],
        ),
      ),
    ),
  );
}
```

### 5. Feladat: Újrapróbálkozás (Retry) gomb megvalósítása
Egészítsd ki a fenti hiba-megjelenítő kártyát egy "Újra" (Retry) gombbal. Ha a felhasználó rákattint, az alkalmazás próbálja meg újra letölteni az adatokat a szerverről.

#### Megoldás:
```dart
// A hiba widgetet kiegészítjük egy callback-kel:
Widget _buildErrorWidget(Object? error, VoidCallback onRetry) {
  return Center(
    child: Card(
      margin: const EdgeInsets.all(20),
      color: Colors.red.shade50,
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Icon(Icons.refresh, size: 48, color: Colors.red),
            const SizedBox(height: 16),
            const Text('Hiba történt a letöltés során!'),
            const SizedBox(height: 16),
            ElevatedButton.icon(
              onPressed: onRetry,
              icon: const Icon(Icons.replay_outlined),
              label: const Text('Újrapróbálkozás'),
            ),
          ],
        ),
      ),
    ),
  );
}

// Az UI-ban a meghívás:
// builder: (context, snapshot) {
//   ...
//   if (snapshot.hasError) {
//     return _buildErrorWidget(snapshot.error, () {
//       setState(() {
//         // Újraindítjuk a Future-t, ami kiváltja a reloadot!
//         _usersFuture = _fetchUsers();
//       });
//     });
//   }
//   ...
// }
```

---

## Heti Mini Projekt: Hírolvasó API-ról

Ez a mini projekt egy teljes, működő hírolvasó (Post olvasó) alkalmazás, amely a JSONPlaceholder API-ból dolgozik, támogatja a lokális keresést, a lehúzással történő frissítést (Pull-to-refresh) és a részletes nézetet.

### Fájl: `main.dart`
```dart
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

void main() {
  runApp(const NewsApp());
}

class NewsApp extends StatelessWidget {
  const NewsApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'PrStart Hírolvasó',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.teal),
        useMaterial3: true,
      ),
      home: const NewsListScreen(),
    );
  }
}

// 1. Model osztály
class Article {
  final int id;
  final String title;
  final String body;

  Article({required this.id, required this.title, required this.body});

  factory Article.fromJson(Map<String, dynamic> json) {
    return Article(
      id: json['id'] as int,
      title: json['title'] as String? ?? '',
      body: json['body'] as String? ?? '',
    );
  }
}

// 2. Főképernyő
class NewsListScreen extends StatefulWidget {
  const NewsListScreen({super.key});

  @override
  State<NewsListScreen> createState() => _NewsListScreenState();
}

class _NewsListScreenState extends State<NewsListScreen> {
  List<Article> _allArticles = [];
  List<Article> _filteredArticles = [];
  bool _isLoading = false;
  String _errorMessage = '';
  final _searchController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _loadArticles();
    _searchController.addListener(_filterArticles);
  }

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  // Adat betöltése az API-ról
  Future<void> _loadArticles() async {
    setState(() {
      _isLoading = true;
      _errorMessage = '';
    });

    try {
      final response = await http
          .get(Uri.parse('https://jsonplaceholder.typicode.com/posts'))
          .timeout(const Duration(seconds: 8));

      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(utf8.decode(response.bodyBytes));
        final articles = data.map((json) => Article.fromJson(json)).toList();
        setState(() {
          _allArticles = articles;
          _filteredArticles = articles;
          _isLoading = false;
        });
      } else {
        setState(() {
          _errorMessage = 'Hiba történt a szerver oldalon: ${response.statusCode}';
          _isLoading = false;
        });
      }
    } catch (e) {
      setState(() {
        _errorMessage = 'Nem sikerült betölteni a híreket. Ellenőrizd a kapcsolatot!';
        _isLoading = false;
      });
    }
  }

  // Lokális szűrés a keresősáv alapján
  void _filterArticles() {
    final query = _searchController.text.toLowerCase();
    setState(() {
      _filteredArticles = _allArticles.where((article) {
        return article.title.toLowerCase().contains(query) ||
            article.body.toLowerCase().contains(query);
      }).toList();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('PrStart Hírek'),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
      ),
      body: Column(
        children: [
          // Keresősáv
          Padding(
            padding: const EdgeInsets.all(10.0),
            child: TextField(
              controller: _searchController,
              decoration: InputDecoration(
                labelText: 'Keresés a hírek között...',
                prefixIcon: const Icon(Icons.search),
                suffixIcon: _searchController.text.isNotEmpty
                    ? IconButton(
                        icon: const Icon(Icons.clear),
                        onPressed: () => _searchController.clear(),
                      )
                    : null,
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(10),
                ),
              ),
            ),
          ),
          // Hírek listája
          Expanded(
            child: _isLoading
                ? const Center(child: CircularProgressIndicator())
                : _errorMessage.isNotEmpty
                    ? Center(
                        child: Padding(
                          padding: const EdgeInsets.all(20.0),
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Text(_errorMessage, style: const TextStyle(color: Colors.red, fontSize: 16), textAlign: TextAlign.center),
                              const SizedBox(height: 10),
                              ElevatedButton(
                                onPressed: _loadArticles,
                                child: const Text('Újra'),
                              )
                            ],
                          ),
                        ),
                      )
                    : _filteredArticles.isEmpty
                        ? const Center(child: Text('Nincs a keresésnek megfelelő hír.'))
                        : RefreshIndicator(
                            onRefresh: _loadArticles,
                            child: ListView.builder(
                              itemCount: _filteredArticles.length,
                              itemBuilder: (context, index) {
                                final article = _filteredArticles[index];
                                return Card(
                                  margin: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                                  child: ListTile(
                                    title: Text(
                                      article.title,
                                      style: const TextStyle(fontWeight: FontWeight.bold),
                                      maxLines: 1,
                                      overflow: TextOverflow.ellipsis,
                                    ),
                                    subtitle: Text(
                                      article.body,
                                      maxLines: 2,
                                      overflow: TextOverflow.ellipsis,
                                    ),
                                    trailing: const Icon(Icons.arrow_forward_ios, size: 16),
                                    onPressed: () {
                                      Navigator.push(
                                        context,
                                        MaterialPageRoute(
                                          builder: (context) => ArticleDetailScreen(article: article),
                                        ),
                                      );
                                    },
                                  ),
                                );
                              },
                            ),
                          ),
          ),
        ],
      ),
    );
  }
}

// 3. Részletező képernyő
class ArticleDetailScreen extends StatelessWidget {
  final Article article;

  const ArticleDetailScreen({super.key, required this.article});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Hír részletei'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              article.title,
              style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: Colors.teal),
            ),
            const Divider(height: 30, thickness: 1.5),
            Expanded(
              child: SingleChildScrollView(
                child: Text(
                  article.body,
                  style: const TextStyle(fontSize: 16, height: 1.5),
                ),
              ),
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

### 1. Mi az az Event Loop és hogyan kezeli a Dart az aszinkron feladatokat egyetlen szálon?
Az **Event Loop** a Dart futtatókörnyezet azon belső mechanizmusa, amely koordinálja az aszinkron események (I/O, időzítők, hálózati válaszok) végrehajtását. Bár a Dart egyszálú, a nehéz I/O műveleteket az operációs rendszer végzi a háttérben. Amikor a háttérművelet elkészül, egy esemény kerül az Event Queue-ba. Az Event Loop folyamatosan figyeli a sorokat, és amikor a fő programkód lefutott (a szál üres), egymás után kiveszi és futtatja a sorban álló eseményeket.

### 2. Mi a különbség a Future és a Stream között?
A **Future** egy egyszeri aszinkron művelet eredményét reprezentálja: vagy egyetlen értéket ad vissza a jövőben, vagy egy hibát (pl. hálózati kérés lefutása). A **Stream** egy aszinkron adatfolyam, amely az idő múlásával több értéket is képes egymás után kiadni (pl. folyamatosan frissülő szenzoradatok, websocket kapcsolat vagy fájl olvasásakor érkező adatcsomagok).

### 3. Miért nem javasolt közvetlenül a Widget build metódusában meghívni egy Future-t elindító függvényt a FutureBuilder-nél?
Ha a `FutureBuilder` `future` paraméterében közvetlenül hívjuk meg a lekérdező függvényt (pl. `future: apiService.getData()`), akkor valahányszor a widget újraépül (pl. egy billentyűzet felnyílása, szülő rebuild vagy lokális állapotszóró miatt), a `getData()` újra és újra lefut. Ez felesleges hálózati terhelést és folyamatos villódzó betöltőképernyőt eredményez. A helyes megoldás, ha a Future-t egy `StatefulWidget` `initState` metódusában indítjuk el, és egy változóban tárolva adjuk át a `FutureBuilder`-nek.

### 4. Mit jelent az interceptor a Dio csomagban és mikor használjuk?
Az **interceptor** egy olyan köztes szoftver (middleware), amely képes elkapni és módosítani a kimenő HTTP kéréseket (onRequest), a bejövő válaszokat (onResponse) vagy a hibákat (onError) még azelőtt, hogy azok elérnék a hívó kódot. Tipikus felhasználási területei: globális hitelesítő tokenek hozzáadása a fejlécben, kérések automatikus naplózása (logging), hálózati hibák központi kezelése (pl. 401 Unauthorized esetén automatikus kijelentkeztetés vagy token refresh indítása).

### 5. Hogyan érdemes kezelni a hibákat (pl. 404, 500, Timeout) egy HTTP repository szinten?
A repository rétegben a hálózati hívásokat `try-catch` blokkba kell zárni. Vizsgálni kell a válasz HTTP státuszkódját: a 200-as (vagy 2xx) kódok jelentik a sikert, minden más (pl. 400 rossz kérés, 401 nincs jogosultság, 404 nem található, 500 belső szerverhiba) esetén egyedi, az alkalmazás által értelmezhető üzleti hibát (`Exception` vagy specifikus hibaosztály) kell dobni. Figyelni kell a kapcsolódási hibákra és az időtúllépésekre (timeout) is, hogy az UI réteg tiszta üzeneteket kapjon és barátságos felületet jeleníthessen meg a felhasználónak.
