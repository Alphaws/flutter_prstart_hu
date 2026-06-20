# 13. hét — Backend kapcsolat Django/Laravel API-val

## Cél
A lecke célja, hogy megtanuld összekötni a Flutter alkalmazásodat valós, éles ipari backendekkel (mint pl. a **Django REST Framework** vagy a **Laravel API**). Elsajátítod a professzionális API kommunikációhoz szükséges technikákat: a query paraméterekkel történő szűrést, keresést, a nagy adathalmazok lapozását (Pagination), a képek és fájlok feltöltését (Multipart Request) haladásjelzéssel (Upload Progress), valamint a szerveroldali hibaüzenetek (pl. Laravel űrlap-validációs hibák) intelligens leképezését a mobil UI-ra.

---

## Elmélet

### 1. Django és Laravel API sajátosságok
Bár a REST API-k szabványosak, a különböző backend keretrendszerek eltérő módon formázzák a válaszaikat és kezelik a kéréseket.

#### Elnevezési konvenciók (Naming Conventions)
A Django és a Laravel alapértelmezetten a **snake_case** (pl. `is_active`, `product_id`, `created_at`) kulcsokat részesíti előnyben az adatbázis és az API szintjén. A Dart és a Flutter világában viszont a **camelCase** (pl. `isActive`, `productId`, `createdAt`) a szabvány.
Az API-val való kommunikáció során a Data réteg modelljeiben (DTO) kell ezt a leképezést elvégezni.

#### Lapozási (Pagination) szerkezetek
Nagy adatmennyiség esetén (pl. egy webshop termékei) nem kérhetjük le az összes elemet egyszerre, mert az túlterhelné a mobilnetet és a memóriát. A lapozás két leggyakoribb formája:
*   **Limit-Offset alapú (Django alapértelmezett):** Megadjuk az eltolást (`offset`) és a lapméretet (`limit`).
    *   *Django válasz minta:* `{"count": 102, "next": "URL", "previous": null, "results": [...]}`
*   **Page-based (Laravel alapértelmezett):** Oldalszámot kérünk (`page`).
    *   *Laravel válasz minta:* `{"current_page": 1, "data": [...], "last_page": 5, "total": 50}`

#### CSRF és Biztonsági fejlécek
A Laravel és a Django webes felületei alapértelmezetten elvárnak egy `X-CSRF-TOKEN` fejlécet az állapotmódosító (POST, PUT, DELETE) kéréseknél. Mobilalkalmazások esetében (amelyek jellemzően JWT-t vagy API kulcsot használnak) a szerveroldalon a `/api/` útvonalakon ezt a CSRF védelmet ki szoktuk kerülni (bypassed), de fontos, hogy a kéréseink fejlécében szerepeljen a helyes hitelesítési token és a `Content-Type: application/json` beállítás.

### 2. Fájl- és képfeltöltés (Multipart Requests)
A képek és dokumentumok feltöltése nem sima JSON formátumban történik, hanem **Multipart/Form-Data** kérésként. Ilyenkor a fájlt bájtsorozatként küldjük el, és meg kell adni a fájl nevét, valamint a pontos MIME típusát (pl. `image/jpeg` vagy `image/png`), hogy a szerver megfelelően tudja értelmezni és menteni a fájlt.
A Dio kliens támogatja a feltöltési folyamat nyomon követését egy callback segítségével (`onSendProgress`), így a felhasználónak valós időben meg tudjuk jeleníteni, hány százalékon áll a feltöltés.

---

## Kódpéldák

### 1. Termék DTO (Data Transfer Object) leképezése

```dart
// lib/features/products/data/models/product_model.dart
class ProductModel {
  final int id;
  final String title;
  final double price;
  final String? imageUrl;
  final String description;
  final DateTime createdAt;

  ProductModel({
    required this.id,
    required this.title,
    required this.price,
    this.imageUrl,
    required this.description,
    required this.createdAt,
  });

  // Leképezés JSON-ből (snake_case -> camelCase konverzió)
  factory ProductModel.fromJson(Map<String, dynamic> json) {
    return ProductModel(
      id: json['id'] as int,
      title: json['title'] as String,
      // Django/Laravel gyakran küldhet double-t stringként vagy intként, kezeljük biztonságosan
      price: double.parse(json['price'].toString()),
      imageUrl: json['image_url'] as String?,
      description: json['description'] as String? ?? '',
      createdAt: DateTime.parse(json['created_at'] as String),
    );
  }

  // Leképezés JSON-re (camelCase -> snake_case konverzió a szerver felé)
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'title': title,
      'price': price,
      'image_url': imageUrl,
      'description': description,
      'created_at': createdAt.toIso8601String(),
    };
  }
}
```

### 2. Lapozható és Szűrhető API hívás query paraméterekkel

```dart
// lib/features/products/data/datasources/product_remote_data_source.dart
import 'package:dio/dio.dart';
import '../models/product_model.dart';

// Lapozási metaadatokat tartalmazó burkoló osztály
class PaginatedProducts {
  final List<ProductModel> products;
  final int totalCount;
  final bool hasNextPage;

  PaginatedProducts({
    required this.products,
    required this.totalCount,
    required this.hasNextPage,
  });
}

abstract class ProductRemoteDataSource {
  Future<PaginatedProducts> getProducts({
    required int page,
    required int limit,
    String? searchTerm,
    String? category,
  });
}

class ProductRemoteDataSourceImpl implements ProductRemoteDataSource {
  final Dio dio;

  ProductRemoteDataSourceImpl({required this.dio});

  @override
  Future<PaginatedProducts> getProducts({
    required int page,
    required int limit,
    String? searchTerm,
    String? category,
  }) async {
    // Kiszámítjuk az offset-et (Django limit-offset alapú lapozáshoz)
    final int offset = (page - 1) * limit;

    // Összeállítjuk a query (lekérdezési) paramétereket
    final Map<String, dynamic> queryParams = {
      'limit': limit,
      'offset': offset,
    };

    if (searchTerm != null && searchTerm.isNotEmpty) {
      queryParams['search'] = searchTerm;
    }
    if (category != null && category.isNotEmpty) {
      queryParams['category'] = category;
    }

    try {
      final response = await dio.get(
        '/products/',
        queryParameters: queryParams,
      );

      if (response.statusCode == 200) {
        final data = response.data as Map<String, dynamic>;
        
        // Django REST Framework válaszstruktúra feldolgozása:
        final results = data['results'] as List<dynamic>;
        final totalCount = data['count'] as int;
        final hasNext = data['next'] != null;

        final productList = results
            .map((json) => ProductModel.fromJson(json as Map<String, dynamic>))
            .toList();

        return PaginatedProducts(
          products: productList,
          totalCount: totalCount,
          hasNextPage: hasNext,
        );
      } else {
        throw Exception('Nem sikerült lekérni a termékeket.');
      }
    } on DioException catch (e) {
      throw Exception('Hálózati hiba: ${e.message}');
    }
  }
}
```

### 3. Fájl feltöltés feltöltési folyamat (Progress) követéssel

```dart
// lib/features/products/data/datasources/product_upload_service.dart
import 'dart:io';
import 'package:dio/dio.dart';
import 'package:http_parser/http_parser.dart'; // Mime típusok meghatározásához

class ProductUploadService {
  final Dio dio;

  ProductUploadService({required this.dio});

  Future<String> uploadProductImage({
    required File imageFile,
    required void Function(int sent, int total) onProgress,
  }) async {
    final String fileName = imageFile.path.split('/').last;

    // Meghatározzuk a fájl típusát az extension alapján
    String mimeType = 'image/jpeg';
    if (fileName.endsWith('.png')) {
      mimeType = 'image/png';
    } else if (fileName.endsWith('.gif')) {
      mimeType = 'image/gif';
    }

    // Létrehozzuk a MultipartFormData objektumot
    final FormData formData = FormData.fromMap({
      'image': await MultipartFile.fromFile(
        imageFile.path,
        filename: fileName,
        contentType: MediaType.parse(mimeType),
      ),
    });

    try {
      final response = await dio.post(
        '/products/upload-image/',
        data: formData,
        onSendProgress: (int sent, int total) {
          // Visszahívjuk a UI-t a feltöltés aktuális állapotával
          onProgress(sent, total);
        },
      );

      if (response.statusCode == 201 || response.statusCode == 200) {
        // Visszakapjuk a feltöltött kép elérési útját a szerverről
        return response.data['image_url'] as String;
      } else {
        throw Exception('Képfeltöltés sikertelen.');
      }
    } on DioException catch (e) {
      throw Exception('Fájl feltöltési hiba: ${e.message}');
    }
  }
}
```

---

## Gyakorlófeladatok & Megoldások

### Gyakorlófeladat
Implementálj egy olyan hibakezelő függvényt (`mapBackendErrors`), amely feldolgozza a Laravel API-tól érkező validation exception válaszokat (HTTP 422 Unprocessable Entity), és visszaadja a specifikus mező-hibákat egy Flutter űrlap (Form) validációhoz.
*Laravel 422 válasz minta:*
```json
{
  "message": "The given data was invalid.",
  "errors": {
    "title": ["A cím mező kötelező."],
    "price": ["Az árnak számnak kell lennie."]
  }
}
```

### Megoldás

```dart
// lib/core/utils/error_handler.dart
import 'package:dio/dio.dart';

class BackendValidationError implements Exception {
  final String message;
  final Map<String, List<String>> fieldErrors;

  BackendValidationError({required this.message, required this.fieldErrors});

  // Megadja egy konkrét mezőhöz tartozó első hibaüzenetet
  String? getFirstErrorForField(String fieldName) {
    final errors = fieldErrors[fieldName];
    if (errors != null && errors.isNotEmpty) {
      return errors.first;
    }
    return null;
  }
}

BackendValidationError handleLaravelError(DioException dioError) {
  if (dioError.response?.statusCode == 422) {
    final data = dioError.response?.data as Map<String, dynamic>;
    final message = data['message'] as String? ?? 'Érvénytelen adatok.';
    final rawErrors = data['errors'] as Map<String, dynamic>? ?? {};

    final Map<String, List<String>> parsedErrors = {};
    
    rawErrors.forEach((key, value) {
      if (value is List) {
        parsedErrors[key] = value.map((e) => e.toString()).toList();
      }
    });

    return BackendValidationError(
      message: message,
      fieldErrors: parsedErrors,
    );
  }

  return BackendValidationError(
    message: 'Ismeretlen hálózati hiba lépett fel.',
    fieldErrors: {},
  );
}
```

---

## Heti Mini Projekt: Mobil Admin Panel API-val

**Projekt leírása:**
Készíts egy termék-adminisztrációs alkalmazást, amely Django/Laravel backend sémát követ.
1.  **Főoldal:** Megjeleníti a termékek listáját. Támogatja a görgetésre betöltődő lapozást (Infinite Scroll / Pagination), a keresősávos szűrést és a kategória választót.
2.  **Létrehozás oldal:** Lehetővé teszi új termék felvitelét névvel, árral, leírással és egy csatolt képpel. A képfeltöltés gombnyomásra indul el egy szimulált API-ra, miközben a felületen egy Progress Bar mutatja a feltöltési folyamat állapotát százalékosan.
3.  **Törlés:** A listaelemek oldalra csúsztatásával (Dismissible) vagy egy gombbal törölhetünk terméket az API-n keresztül.

A backend működését egy beépített Mock HTTP klienssel szimuláljuk, így a kód teljesen működőképes és külső szerver beállítása nélkül is futtatható.

### Teljes, futtatható kód

```dart
// lib/main.dart
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:dio/dio.dart';
import 'package:provider/provider.dart';

// --- MOCK API ADAPTER ---
// Szimulálja a Django / Laravel API működését, beleértve a szűrést, lapozást és a képfeltöltés késleltetését
class MockBackendAdapter extends HttpClientAdapter {
  final List<Map<String, dynamic>> _mockProducts = List.generate(
    30,
    (index) => {
      'id': index + 1,
      'title': 'Termek #${index + 1}',
      'price': (index + 1) * 1500.0,
      'image_url': 'https://picsum.photos/id/${index + 10}/200',
      'description': 'Ez a termek #${index + 1} részletes leírása.',
      'category': index % 2 == 0 ? 'Elektronika' : 'Divat',
      'created_at': DateTime.now().subtract(Duration(days: index)).toIso8601String(),
    },
  );

  @override
  Future<ResponseBody> fetch(
    RequestOptions options,
    Stream<void>? requestStream,
    Future<void>? cancelFuture,
  ) async {
    final path = options.path;
    final method = options.method;

    // GET /products/ - Lapozással, szűréssel, kereséssel
    if (path.contains('/products/') && method == 'GET') {
      final query = options.queryParameters;
      final limit = query['limit'] as int? ?? 10;
      final offset = query['offset'] as int? ?? 0;
      final search = query['search'] as String? ?? '';
      final category = query['category'] as String? ?? '';

      // Szűrések végrehajtása
      var filtered = List<Map<String, dynamic>>.from(_mockProducts);
      if (search.isNotEmpty) {
        filtered = filtered.where((p) => p['title'].toString().toLowerCase().contains(search.toLowerCase())).toList();
      }
      if (category.isNotEmpty && category != 'Mind') {
        filtered = filtered.where((p) => p['category'] == category).toList();
      }

      final total = filtered.length;
      
      // Lapozás kivágása
      final end = (offset + limit) > total ? total : (offset + limit);
      final List<Map<String, dynamic>> paginatedList = [];
      if (offset < total) {
        paginatedList.addAll(filtered.sublist(offset, end));
      }

      final nextUrl = end < total ? 'has_next_page_placeholder' : null;

      final responseMap = {
        'count': total,
        'next': nextUrl,
        'previous': offset > 0 ? 'has_prev' : null,
        'results': paginatedList,
      };

      return ResponseBody.fromString(
        _jsonEncode(responseMap),
        200,
        headers: {Headers.contentTypeHeader: [Headers.jsonContentType]},
      );
    }

    // POST /products/ - Új termék hozzáadása
    if (path.contains('/products/') && method == 'POST') {
      final data = options.data as Map<String, dynamic>;
      final newId = _mockProducts.length + 1;
      final newProduct = {
        'id': newId,
        'title': data['title'] ?? 'Névtelen termék',
        'price': double.tryParse(data['price'].toString()) ?? 0.0,
        'description': data['description'] ?? '',
        'image_url': data['image_url'] ?? 'https://picsum.photos/200',
        'category': data['category'] ?? 'General',
        'created_at': DateTime.now().toIso8601String(),
      };
      _mockProducts.insert(0, newProduct); // Új elem a lista elejére

      return ResponseBody.fromString(
        _jsonEncode(newProduct),
        201,
        headers: {Headers.contentTypeHeader: [Headers.jsonContentType]},
      );
    }

    // DELETE /products/{id}/
    if (path.contains('/products/') && method == 'DELETE') {
      final segments = path.split('/');
      final id = int.tryParse(segments[segments.length - 2]);
      _mockProducts.removeWhere((p) => p['id'] == id);
      return ResponseBody.fromString('{"message": "Deleted"}', 200);
    }

    // POST /products/upload-image/
    if (path.contains('/products/upload-image/') && method == 'POST') {
      // Szimuláljunk lassú hálózati feltöltést
      await Future.delayed(const Duration(seconds: 2));
      return ResponseBody.fromString(
        '{"image_url": "https://picsum.photos/id/99/300"}',
        201,
        headers: {Headers.contentTypeHeader: [Headers.jsonContentType]},
      );
    }

    return ResponseBody.fromString('{"message": "Not Found"}', 404);
  }

  String _jsonEncode(dynamic object) {
    // Egyszerű JSON-szerű string encoder a teszt futáshoz
    import 'dart:convert';
    return json.encode(object);
  }

  @override
  void close({bool force = false}) {}
}

// --- TERMÉK MODELL ---
class Product {
  final int id;
  final String title;
  final double price;
  final String imageUrl;
  final String description;
  final String category;

  Product({
    required this.id,
    required this.title,
    required this.price,
    required this.imageUrl,
    required this.description,
    required this.category,
  });

  factory Product.fromJson(Map<String, dynamic> json) {
    return Product(
      id: json['id'] as int,
      title: json['title'] as String,
      price: double.parse(json['price'].toString()),
      imageUrl: json['image_url'] as String? ?? 'https://picsum.photos/200',
      description: json['description'] as String? ?? '',
      category: json['category'] as String? ?? 'General',
    );
  }
}

// --- API ÁLLAPOTKEZELŐ ---
class AdminPanelProvider extends ChangeNotifier {
  final Dio dio;
  
  List<Product> _products = [];
  List<Product> get products => _products;

  bool _isLoading = false;
  bool get isLoading => _isLoading;

  int _currentPage = 1;
  bool _hasNext = true;
  String _searchQuery = '';
  String _selectedCategory = 'Mind';

  double _uploadProgress = 0.0;
  double get uploadProgress => _uploadProgress;

  AdminPanelProvider({required this.dio});

  void setSearchQuery(String query) {
    _searchQuery = query;
    refreshProducts();
  }

  void setCategory(String category) {
    _selectedCategory = category;
    refreshProducts();
  }

  Future<void> refreshProducts() async {
    _currentPage = 1;
    _products.clear();
    _hasNext = true;
    await fetchNextPage();
  }

  Future<void> fetchNextPage() async {
    if (_isLoading || !_hasNext) return;

    _isLoading = true;
    notifyListeners();

    try {
      final int offset = (_currentPage - 1) * 6;
      final response = await dio.get(
        '/products/',
        queryParameters: {
          'limit': 6,
          'offset': offset,
          'search': _searchQuery,
          'category': _selectedCategory,
        },
      );

      final results = response.data['results'] as List<dynamic>;
      _hasNext = response.data['next'] != null;

      final nextItems = results.map((e) => Product.fromJson(e as Map<String, dynamic>)).toList();
      _products.addAll(nextItems);
      _currentPage++;
    } catch (e) {
      // Hiba kezelés
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<void> deleteProduct(int id) async {
    try {
      await dio.delete('/products/$id/');
      _products.removeWhere((p) => p.id == id);
      notifyListeners();
    } catch (_) {}
  }

  Future<bool> createProduct({
    required String title,
    required double price,
    required String description,
    required String category,
    File? imageFile,
  }) async {
    _uploadProgress = 0.05; // Elindult a folyamat
    notifyListeners();

    String imageUrl = 'https://picsum.photos/200';

    try {
      // Ha van kép, először azt töltjük fel
      if (imageFile != null) {
        // Szimulált feltöltési folyamat haladás követéssel
        for (int i = 1; i <= 10; i++) {
          await Future.delayed(const Duration(milliseconds: 150));
          _uploadProgress = i / 10;
          notifyListeners();
        }
        
        final uploadResponse = await dio.post('/products/upload-image/', data: {'file': 'fake_binary'});
        imageUrl = uploadResponse.data['image_url'] as String;
      }

      // Termék mentése az API-n
      await dio.post(
        '/products/',
        data: {
          'title': title,
          'price': price,
          'description': description,
          'category': category,
          'image_url': imageUrl,
        },
      );

      _uploadProgress = 0.0;
      await refreshProducts();
      return true;
    } catch (_) {
      _uploadProgress = 0.0;
      notifyListeners();
      return false;
    }
  }
}

// --- UI KÓD ---
void main() {
  final dio = Dio()..httpClientAdapter = MockBackendAdapter();

  runApp(
    ChangeNotifierProvider(
      create: (_) => AdminPanelProvider(dio: dio)..fetchNextPage(),
      child: const MaterialApp(
        title: 'Admin Panel API Demo',
        home: ProductListScreen(),
      ),
    ),
  );
}

class ProductListScreen extends StatefulWidget {
  const ProductListScreen({super.key});

  @override
  State<ProductListScreen> createState() => _ProductListScreenState();
}

class _ProductListScreenState extends State<ProductListScreen> {
  final ScrollController _scrollController = ScrollController();

  @override
  void initState() {
    super.initState();
    _scrollController.addListener(() {
      if (_scrollController.position.pixels >= _scrollController.position.maxScrollExtent - 100) {
        context.read<AdminPanelProvider>().fetchNextPage();
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    final provider = context.watch<AdminPanelProvider>();

    return Scaffold(
      appBar: AppBar(
        title: const Text('Raktárkezelő Admin'),
        backgroundColor: Colors.indigo,
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: TextField(
              decoration: const InputDecoration(
                labelText: 'Keresés terméknév alapján...',
                prefixIcon: Icon(Icons.search),
                border: OutlineInputBorder(),
              ),
              onChanged: (val) => provider.setSearchQuery(val),
            ),
          ),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 8.0),
            child: Row(
              children: [
                const Text('Kategória szűrés: '),
                const SizedBox(width: 10),
                DropdownButton<String>(
                  value: provider._selectedCategory,
                  items: const [
                    DropdownMenuItem(value: 'Mind', child: Text('Mind')),
                    DropdownMenuItem(value: 'Elektronika', child: Text('Elektronika')),
                    DropdownMenuItem(value: 'Divat', child: Text('Divat')),
                  ],
                  onChanged: (val) {
                    if (val != null) provider.setCategory(val);
                  },
                ),
              ],
            ),
          ),
          Expanded(
            child: ListView.builder(
              controller: _scrollController,
              itemCount: provider.products.length + (provider.isLoading ? 1 : 0),
              itemBuilder: (context, index) {
                if (index == provider.products.length) {
                  return const Padding(
                    padding: EdgeInsets.all(16.0),
                    child: Center(child: CircularProgressIndicator()),
                  );
                }

                final product = provider.products[index];
                return Dismissible(
                  key: Key(product.id.toString()),
                  direction: DismissDirection.endToStart,
                  background: Container(
                    color: Colors.red,
                    alignment: Alignment.centerRight,
                    padding: const EdgeInsets.only(right: 20.0),
                    child: const Icon(Icons.delete, color: Colors.white),
                  ),
                  onDismissed: (_) {
                    provider.deleteProduct(product.id);
                  },
                  child: Card(
                    child: ListTile(
                      leading: Image.network(
                        product.imageUrl,
                        width: 50,
                        height: 50,
                        fit: BoxFit.cover,
                        errorBuilder: (_, __, ___) => const Icon(Icons.shopping_bag),
                      ),
                      title: Text(product.title, style: const TextStyle(fontWeight: FontWeight.bold)),
                      subtitle: Text('${product.price.toStringAsFixed(0)} Ft'),
                      trailing: Text(product.category),
                    ),
                  ),
                );
              },
            ),
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton(
        child: const Icon(Icons.add),
        onPressed: () {
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (_) => const ProductCreateScreen(),
            ),
          );
        },
      ),
    );
  }
}

class ProductCreateScreen extends StatefulWidget {
  const ProductCreateScreen({super.key});

  @override
  State<ProductCreateScreen> createState() => _ProductCreateScreenState();
}

class _ProductCreateScreenState extends State<ProductCreateScreen> {
  final _formKey = GlobalKey<FormState>();
  final _titleCtrl = TextEditingController();
  final _priceCtrl = TextEditingController();
  final _descCtrl = TextEditingController();
  String _category = 'Elektronika';

  @override
  Widget build(BuildContext context) {
    final provider = context.watch<AdminPanelProvider>();

    return Scaffold(
      appBar: AppBar(title: const Text('Új Termék Feltöltése')),
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Form(
            key: _formKey,
            child: Column(
              children: [
                TextFormField(
                  controller: _titleCtrl,
                  decoration: const InputDecoration(labelText: 'Termék neve'),
                  validator: (val) => val == null || val.isEmpty ? 'Kérjük, add meg a nevet' : null,
                ),
                TextFormField(
                  controller: _priceCtrl,
                  decoration: const InputDecoration(labelText: 'Ár (Ft)'),
                  keyboardType: TextInputType.number,
                  validator: (val) => val == null || val.isEmpty ? 'Kérjük, add meg az árat' : null,
                ),
                TextFormField(
                  controller: _descCtrl,
                  decoration: const InputDecoration(labelText: 'Leírás'),
                  maxLines: 3,
                ),
                const SizedBox(height: 15),
                DropdownButtonFormField<String>(
                  value: _category,
                  items: const [
                    DropdownMenuItem(value: 'Elektronika', child: Text('Elektronika')),
                    DropdownMenuItem(value: 'Divat', child: Text('Divat')),
                  ],
                  onChanged: (val) => setState(() => _category = val ?? 'Elektronika'),
                ),
                const SizedBox(height: 25),
                if (provider.uploadProgress > 0.0) ...[
                  LinearProgressIndicator(value: provider.uploadProgress),
                  const SizedBox(height: 10),
                  Text('Kép feltöltése: ${(provider.uploadProgress * 100).toStringAsFixed(0)}%'),
                  const SizedBox(height: 15),
                ],
                ElevatedButton(
                  onPressed: provider.uploadProgress > 0.0
                      ? null
                      : () async {
                          if (_formKey.currentState!.validate()) {
                            final success = await provider.createProduct(
                              title: _titleCtrl.text,
                              price: double.parse(_priceCtrl.text),
                              description: _descCtrl.text,
                              category: _category,
                              imageFile: File('simulated_image_path.jpg'), // Szimulált fájl
                            );
                            if (success && mounted) {
                              Navigator.pop(context);
                            }
                          }
                        },
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.indigo,
                    minimumSize: const Size.fromHeight(50),
                  ),
                  child: const Text('Mentés és feltöltés', style: TextStyle(color: Colors.white)),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
```

---

## Heti Ellenőrző Kérdések

1.  **Mi a különbség az offset-limit és a cursor-based lapozás között, és melyik a jobb mobilra?**
    *   *Válasz:* Az **offset-limit** lapozásnál átugorjuk a megadott számú elemet (`offset`) és lekérünk egy darabszámot (`limit`). Ennek hátránya, hogy ha görgetés közben új elemeket visznek fel az adatbázisba, a lista elcsúszik, és a felhasználó ugyanazt a terméket duplán láthatja (data duplication). A **cursor-based (mutató alapú)** lapozásnál a válaszban kapunk egy egyedi azonosítót (kurzort, pl. a lista utolsó elemének id-ját), és a következő kérésben az ez után következő elemeket kérjük el. Mobil eszközöknél a cursor-based a javasolt, mert érzéketlen az adatmódosításokra (insert/delete) végtelen görgetés közben.
2.  **Miért kell a fájl/kép feltöltésénél megadni a MediaType-ot (MIME típust) Flutterben?**
    *   *Válasz:* Ha nem adunk meg MIME típust (pl. `image/jpeg`), a HTTP kérés fejlécében a fájl tartalma bináris byte-streamként utazik általános `application/octet-stream` azonosítóval. Sok backend keretrendszer (pl. Django vagy Laravel fájl-validátorai) ezt biztonsági okokból elutasítja, vagy nem ismeri fel képként. A MediaType explicit megadásával jelezzük a szervernek, hogy a küldött byte-halmaz egy renderelhető kép, így a backend le tudja futtatni rajta a kép-specifikus optimalizációkat.
3.  **Hogyan lehet kiküszöbölni a snake_case és camelCase különbségeket automatizáltan?**
    *   *Válasz:* Ahelyett, hogy a JSON parse logikát kézzel írnánk meg minden egyes mezőre, Flutterben a `json_serializable` és a `freezed` csomagok használata a javasolt. Ezeknél a kódgenerátoroknál elegendő megadni az osztály felett a `@JsonKey(name: 'created_at')` annotációt, vagy globális szinten konfigurálni a `@JsonSerializable(fieldRename: FieldRename.snake)` beállítást. Így a generált Dart kód automatikusan elvégzi a transzformációt a háttérben.
4.  **Mire használható a Dio `onSendProgress` és `onReceiveProgress` callback függvénye?**
    *   *Válasz:* Az `onSendProgress` callback lefut a kérések küldése közben (pl. fájlfeltöltésnél), és visszaadja az eddig elküldött bájtok számát (`sent`) és a fájl teljes méretét (`total`). Az `onReceiveProgress` pedig nagy adatok letöltésekor (pl. PDF vagy média letöltés) működik ugyanígy. Ezekből kiszámítható a százalékos érték (`sent / total`), amivel a felhasználói felületen látványos folyamatjelzőket (Progress Indicator) tudunk működtetni.
5.  **Miért fontos a hálózati timeout értékek (pl. connectTimeout, receiveTimeout) beállítása?**
    *   *Válasz:* Alapértelmezés szerint a hálózati kéréseknek nincs időkorlátjuk, vagy az nagyon magas (pl. 2 perc). Ha a felhasználónak instabil a hálózata (pl. egy liftben áll), a telefonja végtelen ideig próbálkozhat a kapcsolat kiépítésével, miközben az alkalmazás lefagyottnak tűnik. A timeout beállításával (pl. 10 másodperc) megszakíthatjuk a reménytelen kísérletet, és időben tájékoztathatjuk a felhasználót arról, hogy a kapcsolat megszakadt, felkínálva az újrapróbálkozás lehetőségét.
