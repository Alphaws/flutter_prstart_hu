# 6. hét — State management alapok

## Cél
A lecke célja, hogy mélyen megértsd a Flutter állapotkezelésének (State Management) elméletét és gyakorlatát. Megtanuljuk megkülönböztetni a helyi (ephemeral) és a globális (app-szintű) állapotokat, megismerjük a `setState` korlátait, és elsajátítjuk a `ChangeNotifier`, `ValueNotifier` és a `Provider` használatát. A hét végére képes leszel több képernyő között hatékonyan, tiszta architektúrával megosztani az alkalmazás állapotát.

---

## Elmélet

### 1. Mi az az állapot (State)?
A Flutter deklaratív UI keretrendszer. Ez azt jelenti, hogy a felhasználói felület (UI) az aktuális állapot (State) tükröződése. A képlet egyszerű:
$$UI = f(State)$$
Ahol az $f$ a widget-fa `build` metódusait reprezentálja. Minden, ami a képernyőn megjelenik, és a felhasználó interakciója vagy háttérfolyamatok hatására megváltozhat, az **állapot**.

**Példák az állapotra:**
*   **Felhasználói profil:** A bejelentkezett felhasználó neve, email címe, jogosultságai.
*   **Bevásárlókosár:** A kiválasztott termékek listája, mennyiségük és a végösszeg.
*   **UI beállítások:** Kiválasztott téma (Light/Dark mode), nyelv (HU/EN), aktuális lap indexe.
*   **Hálózati státusz:** Az éppen futó API kérés állapota (töltődik, sikeresen lefutott, hibára futott).
*   **Űrlapok:** Beviteli mezők szövege, validációs hibák megléte vagy hiánya.

### 2. A helyi (Ephemeral) és a globális (App) állapot különbsége

#### A. Ephemeral State (Helyi / Ideiglenes állapot)
Olyan állapot, amely csak egyetlen widgeten belül fontos, és nem befolyásolja az alkalmazás többi részét. Nem szükséges külső állapottároló, a Flutter beépített `StatefulWidget`-je és a `setState` tökéletesen elegendő hozzá.
*   *Példa:* Egy `Switch` be- és kikapcsolt állapota, egy `TextField` fókuszállapota, egy `PageView` aktuális oldalszáma, vagy egy egyszerű lokális animáció fázisa.

#### B. App State (Globális / Megosztott állapot)
Olyan állapot, amelyet az alkalmazás több, egymástól távol eső része is olvas vagy módosít.
*   *Példa:* A kosár tartalma (a terméklistánál látni kell a Badge-en a darabszámot, a kosár oldalon részletezve van, a fizetési oldalon pedig a végösszeget használjuk).
*   *Példa:* Autentikációs állapot (ha a felhasználó kijelentkezik, a profil oldalnak, a főoldalnak és a navigációnak is azonnal reagálnia kell).

### 3. Miért nem elég a `setState` egy nagyobb alkalmazásban?
Bár a `setState` a legegyszerűbb módja a változtatások kijelzésének, nagyobb projektekben komoly problémákat okoz:
1.  **Prop Drilling (Adatok átpréselése a widget-fán):** Ha egy alsó szintű widgetnek szüksége van a felső szinten lévő adatra, azt minden köztes widget konstruktorán át kell adnunk, még akkor is, ha a köztes widgetek nem használják azt.
2.  **Widget Rebuild teljesítményprobléma:** A `setState` meghívásakor az adott `StatefulWidget` teljes al-fája újraépül (`build` lefut). Ha túl magasan hívjuk meg a fában, feleslegesen rajzolunk újra rengeteg statikus komponenst.
3.  **Kódszervezés hiánya:** Az üzleti logika (pl. kosár összeg számítása, API hívások kezelése) belekeveredik a UI rétegbe (a Widget osztályba), ami tesztelhetetlenné és karbantarthatatlanná teszi a kódot.

### 4. Az állapotkezelés evolúciója Flutterben
Hogy elkerüljük az UI és a logika keveredését, a következő szinteken lépkedhetünk végig:
1.  `setState`: Csak lokális UI állapotokhoz.
2.  `ValueNotifier` / `ValueListenableBuilder`: Egyszerű, reaktív primitív értékekhez (pl. egy sötét mód kapcsolóhoz) anélkül, hogy a teljes widgetet `StatefulWidget`-re kellene alakítani.
3.  `ChangeNotifier`: Bonyolultabb üzleti logikát tömörítő osztály, amely képes értesíteni a hallgatóit (`notifyListeners()`).
4.  `Provider`: Dependency Injection (DI) és állapottároló wrapper a `ChangeNotifier` fölé, amely a `BuildContext`-en keresztül teszi elérhetővé az állapotot a fa tetszőleges pontján.

---

## Kódpéldák

### 1. Lokális kosár állapot `setState`-tel (Egy képernyőn belül)
Az alábbi példa bemutatja, hogyan kezeljük az állapotot lokálisan. Ez a megközelítés csak akkor jó, ha a kosár funkció nem nyúlik át más képernyőkre.

```dart
import 'package:flutter/material.dart';

class LocalCartPage extends StatefulWidget {
  const LocalCartPage({super.key});

  @override
  State<LocalCartPage> createState() => _LocalCartPageState();
}

class _LocalCartPageState extends State<LocalCartPage> {
  // Lokális állapot
  final List<Map<String, dynamic>> _products = [
    {'name': 'Flutter póló', 'price': 5900, 'quantity': 1},
    {'name': 'Dart bögre', 'price': 3200, 'quantity': 2},
  ];

  void _incrementQuantity(int index) {
    setState(() {
      _products[index]['quantity']++;
    });
  }

  void _decrementQuantity(int index) {
    setState(() {
      if (_products[index]['quantity'] > 1) {
        _products[index]['quantity']--;
      }
    });
  }

  int _calculateTotal() {
    return _products.fold(0, (sum, item) => sum + (item['price'] as int) * (item['quantity'] as int));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Lokális Kosár')),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              itemCount: _products.length,
              itemBuilder: (context, index) {
                final item = _products[index];
                return ListTile(
                  title: Text(item['name']),
                  subtitle: Text('${item['price']} Ft'),
                  trailing: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      IconButton(
                        icon: const Icon(Icons.remove),
                        onPressed: () => _decrementQuantity(index),
                      ),
                      Text('${item['quantity']}'),
                      IconButton(
                        icon: const Icon(Icons.add),
                        onPressed: () => _incrementQuantity(index),
                      ),
                    ],
                  ),
                );
              },
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: Text(
              'Összesen: ${_calculateTotal()} Ft',
              style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
          ),
        ],
      ),
    );
  }
}
```

### 2. Kosár állapot `ChangeNotifier`-rel és `Provider`-rel (Megosztott állapot)
Ehhez először vegyük fel a `provider` csomagot a `pubspec.yaml`-be. 
A `ChangeNotifier` különválasztja a logikát az UI-tól.

```dart
// lib/features/cart/cart_notifier.dart
import 'package:flutter/foundation.dart';

class CartItem {
  final String id;
  final String name;
  final int price;
  int quantity;

  CartItem({
    required this.id,
    required this.name,
    required this.price,
    this.quantity = 1,
  });
}

class CartNotifier extends ChangeNotifier {
  final Map<String, CartItem> _items = {};

  List<CartItem> get items => _items.values.toList();

  int get totalAmount {
    var total = 0;
    _items.forEach((key, cartItem) {
      total += cartItem.price * cartItem.quantity;
    });
    return total;
  }

  int get itemCount => _items.length;

  void addItem(String productId, String name, int price) {
    if (_items.containsKey(productId)) {
      _items[productId]!.quantity++;
    } else {
      _items[productId] = CartItem(id: productId, name: name, price: price);
    }
    // Fontos: ezzel értesítjük az UI-t a változásról!
    notifyListeners();
  }

  void removeItem(String productId) {
    _items.remove(productId);
    notifyListeners();
  }

  void updateQuantity(String productId, int newQuantity) {
    if (_items.containsKey(productId) && newQuantity > 0) {
      _items[productId]!.quantity = newQuantity;
      notifyListeners();
    }
  }
}
```

### 3. Theme váltás `Provider`-rel
A globális alkalmazás szintjén tárolt témaállapot és annak injektálása a `main.dart`-ban.

```dart
// lib/core/theme_notifier.dart
import 'package:flutter/material.dart';

class ThemeNotifier extends ChangeNotifier {
  bool _isDarkMode = false;
  bool get isDarkMode => _isDarkMode;

  ThemeMode get currentTheme => _isDarkMode ? ThemeMode.dark : ThemeMode.light;

  void toggleTheme() {
    _isDarkMode = !_isDarkMode;
    notifyListeners();
  }
}
```

Így konfiguráljuk az alkalmazás belépési pontján (`main.dart`):

```dart
// lib/main.dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'core/theme_notifier.dart';
import 'features/cart/cart_notifier.dart';

void main() {
  runApp(
    // MultiProvider használata több globális állapot esetén
    MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => ThemeNotifier()),
        ChangeNotifierProvider(create: (_) => CartNotifier()),
      ],
      child: const MyApp(),
    ),
  );
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    // Figyeljük a ThemeNotifier változását
    final themeNotifier = context.watch<ThemeNotifier>();

    return MaterialApp(
      title: 'State Management App',
      themeMode: themeNotifier.currentTheme,
      theme: ThemeData.light(useMaterial3: true),
      darkTheme: ThemeData.dark(useMaterial3: true),
      home: const HomeScreen(),
    );
  }
}

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final cartNotifier = context.watch<CartNotifier>();
    final themeNotifier = context.read<ThemeNotifier>(); // Csak olvasunk, nem figyelünk változást híváskor

    return Scaffold(
      appBar: AppBar(
        title: const Text('Főoldal'),
        actions: [
          IconButton(
            icon: Icon(themeNotifier.isDarkMode ? Icons.light_mode : Icons.dark_mode),
            onPressed: () => themeNotifier.toggleTheme(),
          ),
          Stack(
            alignment: Alignment.center,
            children: [
              IconButton(
                icon: const Icon(Icons.shopping_cart),
                onPressed: () {
                  // Navigáció a kosár oldalra
                },
              ),
              if (cartNotifier.itemCount > 0)
                Positioned(
                  right: 8,
                  top: 8,
                  child: CircleAvatar(
                    radius: 8,
                    backgroundColor: Colors.red,
                    child: Text(
                      '${cartNotifier.itemCount}',
                      style: const TextStyle(fontSize: 10, color: Colors.white),
                    ),
                  ),
                ),
            ],
          )
        ],
      ),
      body: Center(
        child: ElevatedButton(
          onPressed: () {
            context.read<CartNotifier>().addItem('p1', 'Flutter póló', 5900);
          },
          child: const Text('Póló kosárba'),
        ),
      ),
    );
  }
}
```

### 4. Felhasználói autentikáció (`AuthNotifier`) modellezése

```dart
import 'package:flutter/material.dart';

class UserProfile {
  final String email;
  final String name;

  UserProfile({required this.email, required this.name});
}

class AuthNotifier extends ChangeNotifier {
  UserProfile? _user;
  bool _isLoading = false;

  UserProfile? get user => _user;
  bool get isAuthenticated => _user != null;
  bool get isLoading => _isLoading;

  Future<bool> login(String email, String password) async {
    _isLoading = true;
    notifyListeners();

    // Szimulált hálózati késleltetés
    await Future.delayed(const Duration(seconds: 2));

    if (email == 'teszt@prstart.hu' && password == 'titok123') {
      _user = UserProfile(email: email, name: 'PrStart Diák');
      _isLoading = false;
      notifyListeners();
      return true;
    }

    _isLoading = false;
    notifyListeners();
    return false;
  }

  void logout() {
    _user = null;
    notifyListeners();
  }
}
```

### 5. Aszinkron állapotok modellezése Dart 3+ Sealed osztályokkal
Ahelyett, hogy boolean változókat (`isLoading`, `hasError`) halmoznánk fel, a modern Dart lehetővé teszi, hogy az állapotot kizáró típusokként (`sealed class`) modellezzük.

```dart
// lib/core/result_state.dart
sealed class ResultState<T> {
  const ResultState();
}

class Initial<T> extends ResultState<T> {
  const Initial();
}

class Loading<T> extends ResultState<T> {
  const Loading();
}

class Success<T> extends ResultState<T> {
  final T data;
  const Success(this.data);
}

class Failure<T> extends ResultState<T> {
  final String error;
  const Failure(this.error);
}

// UI használat minta pattern matchinggel:
Widget buildStateWidget(ResultState<String> state) {
  return switch (state) {
    Initial() => const Text('Indításra kész'),
    Loading() => const CircularProgressIndicator(),
    Success(data: final content) => Text('Siker! Adat: $content'),
    Failure(error: final msg) => Text('Hiba történt: $msg', style: const TextStyle(color: Colors.red)),
  };
}
```

---

## Gyakorlófeladatok & Megoldások

### 1. Feladat: Egyszerű számláló `ValueNotifier` használatával
Készíts egy oldalt, ahol egy számot tudunk növelni és csökkenteni. A fő widget legyen `StatelessWidget`, és az érték változását `ValueNotifier` valamint `ValueListenableBuilder` segítségével kezeld!

#### Megoldás:
```dart
import 'package:flutter/material.dart';

class ValueNotifierCounterPage extends StatelessWidget {
  ValueNotifierCounterPage({super.key});

  // A notifier tárolja az állapotot
  final ValueNotifier<int> _counter = ValueNotifier<int>(0);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('ValueNotifier Számláló')),
      body: Center(
        child: ValueListenableBuilder<int>(
          valueListenable: _counter,
          builder: (context, value, child) {
            // Csak ez a Text widget fog újraépülni változáskor!
            return Text(
              'Számláló értéke: $value',
              style: const TextStyle(fontSize: 24),
            );
          },
        ),
      ),
      floatingActionButton: Row(
        mainAxisAlignment: MainAxisSize.end,
        children: [
          FloatingActionButton(
            heroTag: 'dec',
            onPressed: () => _counter.value--,
            child: const Icon(Icons.remove),
          ),
          const SizedBox(width: 10),
          FloatingActionButton(
            heroTag: 'inc',
            onPressed: () => _counter.value++,
            child: const Icon(Icons.add),
          ),
        ],
      ),
    );
  }
}
```

### 2. Feladat: Kedvenc termékek (`FavoritesNotifier`) állapotkezelés
Hozd létre a `FavoritesNotifier` osztályt, ami `ChangeNotifier`-t terjeszt ki, és alkalmas termék ID-k kedvencként való elmentésére vagy törlésére (`toggleFavorite`). Injektáld a Provider-be és kösd össze egy gombbal!

#### Megoldás:
```dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class FavoritesNotifier extends ChangeNotifier {
  final Set<String> _favoriteIds = {};

  Set<String> get favoriteIds => _favoriteIds;

  bool isFavorite(String id) => _favoriteIds.contains(id);

  void toggleFavorite(String id) {
    if (_favoriteIds.contains(id)) {
      _favoriteIds.remove(id);
    } else {
      _favoriteIds.add(id);
    }
    notifyListeners();
  }
}

class ProductItemWidget extends StatelessWidget {
  final String productId;
  final String productName;

  const ProductItemWidget({
    super.key,
    required this.productId,
    required this.productName,
  });

  @override
  Widget build(BuildContext context) {
    // Kiválasztjuk az állapotot a watch segítségével
    final favoritesNotifier = context.watch<FavoritesNotifier>();
    final isFav = favoritesNotifier.isFavorite(productId);

    return ListTile(
      title: Text(productName),
      trailing: IconButton(
        icon: Icon(
          isFav ? Icons.favorite : Icons.favorite_border,
          color: isFav ? Colors.red : null,
        ),
        onPressed: () {
          // Itt a read használata ajánlott, mert csak eseményt indítunk
          context.read<FavoritesNotifier>().toggleFavorite(productId);
        },
      ),
    );
  }
}
```

### 3. Feladat: Háromszínű téma választó
Hozz létre egy `ThemeNotifier`-t, amely nemcsak dark és light módok között vált, hanem három konkrét háttérszínt (Kék, Zöld, Narancs) képes kezelni. Az UI-ról lehessen kiválasztani a színt, ami azonnal megváltoztatja az app fő témájának `primaryColor`-ját.

#### Megoldás:
```dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

enum CustomThemeColor { blue, green, orange }

class CustomThemeNotifier extends ChangeNotifier {
  CustomThemeColor _themeColor = CustomThemeColor.blue;

  CustomThemeColor get themeColor => _themeColor;

  ThemeData get currentTheme {
    return switch (_themeColor) {
      CustomThemeColor.blue => ThemeData(primaryColor: Colors.blue, scaffoldBackgroundColor: Colors.blue.shade50),
      CustomThemeColor.green => ThemeData(primaryColor: Colors.green, scaffoldBackgroundColor: Colors.green.shade50),
      CustomThemeColor.orange => ThemeData(primaryColor: Colors.orange, scaffoldBackgroundColor: Colors.orange.shade50),
    };
  }

  void setThemeColor(CustomThemeColor color) {
    _themeColor = color;
    notifyListeners();
  }
}
```

### 4. Feladat: Login folyamat hiba és sikeres állapotkezelés
Készíts egy bejelentkező oldalt, ahol az `AuthNotifier` által nyújtott `login` függvény fut le. Ha a bejelentkezés sikertelen, piros hibaüzenet jelenjen meg a képernyőn. Ha sikeres, írja ki, hogy "Üdvözlünk, [név]!".

#### Megoldás:
```dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

// Az AuthNotifier megegyezik a Kódpéldák 4. pontjában leírttal.

class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  String? _errorMessage;

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final auth = context.watch<AuthNotifier>();

    if (auth.isAuthenticated) {
      return Scaffold(
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text('Üdvözlünk, ${auth.user?.name}!'),
              ElevatedButton(
                onPressed: () => auth.logout(),
                child: const Text('Kijelentkezés'),
              )
            ],
          ),
        ),
      );
    }

    return Scaffold(
      appBar: AppBar(title: const Text('Bejelentkezés')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextField(
              controller: _emailController,
              decoration: const InputDecoration(labelText: 'Email (teszt@prstart.hu)'),
            ),
            TextField(
              controller: _passwordController,
              decoration: const InputDecoration(labelText: 'Jelszó (titok123)'),
              obscureText: true,
            ),
            const SizedBox(height: 10),
            if (_errorMessage != null)
              Text(_errorMessage!, style: const TextStyle(color: Colors.red)),
            const SizedBox(height: 20),
            auth.isLoading
                ? const CircularProgressIndicator()
                : ElevatedButton(
                    onPressed: () async {
                      final success = await auth.login(
                        _emailController.text,
                        _passwordController.text,
                      );
                      if (!success) {
                        setState(() {
                          _errorMessage = 'Hibás felhasználónév vagy jelszó!';
                        });
                      } else {
                        setState(() {
                          _errorMessage = null;
                        });
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
```

### 5. Feladat: API állapot szimuláció Sealed osztályokkal
Készíts egy widgetet, amely egy `ResultState<List<String>>` állapotot jelenít meg. A felhasználó egy gomb megnyomásával szimulálhat egy API hívást (2 másodperc betöltés után vagy sikerül, vagy hiba történik véletlenszerűen).

#### Megoldás:
```dart
import 'dart:math';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

// Tegyük fel, hogy a ResultState sealed osztály be van töltve (Kódpéldák 5.)

class ApiSimulationNotifier extends ChangeNotifier {
  ResultState<List<String>> _state = const Initial();

  ResultState<List<String>> get state => _state;

  Future<void> fetchData() async {
    _state = const Loading();
    notifyListeners();

    await Future.delayed(const Duration(seconds: 2));

    final random = Random().nextBool();
    if (random) {
      _state = const Success(['Alma', 'Körte', 'Barack']);
    } else {
      _state = const Failure('Szerverhiba történt (500).');
    }
    notifyListeners();
  }
}
```

---

## Heti Mini Projekt: Kosár app state managementtel

Ez a projekt egy teljes, két képernyőből álló Flutter alkalmazás, amely bemutatja a `ChangeNotifier` és a `Provider` együttes használatát.

### Projektstruktúra
```text
lib/
  main.dart
  cart_notifier.dart
  screens/
    catalog_screen.dart
    cart_screen.dart
```

### 1. Fájl: `cart_notifier.dart` (Állapottároló osztály)
```dart
import 'package:flutter/material.dart';

class Product {
  final String id;
  final String name;
  final int price;

  Product({required this.id, required this.name, required this.price});
}

class CartItem {
  final Product product;
  int quantity;

  CartItem({required this.product, this.quantity = 1});
}

class CartNotifier extends ChangeNotifier {
  final Map<String, CartItem> _items = {};

  List<CartItem> get items => _items.values.toList();

  int get totalAmount {
    return _items.values.fold(0, (sum, item) => sum + item.product.price * item.quantity);
  }

  int get totalItemCount {
    return _items.values.fold(0, (sum, item) => sum + item.quantity);
  }

  void addToCart(Product product) {
    if (_items.containsKey(product.id)) {
      _items[product.id]!.quantity++;
    } else {
      _items[product.id] = CartItem(product: product);
    }
    notifyListeners();
  }

  void removeOneFromCart(Product product) {
    if (!_items.containsKey(product.id)) return;

    if (_items[product.id]!.quantity > 1) {
      _items[product.id]!.quantity--;
    } else {
      _items.remove(product.id);
    }
    notifyListeners();
  }

  void clearCart() {
    _items.clear();
    notifyListeners();
  }
}
```

### 2. Fájl: `screens/catalog_screen.dart` (Katalógus nézet)
```dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../cart_notifier.dart';
import 'cart_screen.dart';

class CatalogScreen extends StatelessWidget {
  const CatalogScreen({super.key});

  static final List<Product> _products = [
    Product(id: '1', name: 'Flutter Fejlesztő Kurzus', price: 29900),
    Product(id: '2', name: 'Dart Kezdő Könyv', price: 4900),
    Product(id: '3', name: 'Szakmai Mentorálás (1 óra)', price: 15000),
    Product(id: '4', name: 'UI/UX Tervezősablonok', price: 9900),
  ];

  @override
  Widget build(BuildContext context) {
    final cart = context.watch<CartNotifier>();

    return Scaffold(
      appBar: AppBar(
        title: const Text('PrStart Kurzuskatalógus'),
        actions: [
          Stack(
            alignment: Alignment.center,
            children: [
              IconButton(
                icon: const Icon(Icons.shopping_cart),
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) => const CartScreen()),
                  );
                },
              ),
              if (cart.totalItemCount > 0)
                Positioned(
                  right: 4,
                  top: 4,
                  child: CircleAvatar(
                    radius: 9,
                    backgroundColor: Colors.red,
                    child: Text(
                      '${cart.totalItemCount}',
                      style: const TextStyle(fontSize: 10, color: Colors.white, fontWeight: FontWeight.bold),
                    ),
                  ),
                )
            ],
          )
        ],
      ),
      body: ListView.builder(
        itemCount: _products.length,
        itemBuilder: (context, index) {
          final product = _products[index];
          return Card(
            margin: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
            child: ListTile(
              title: Text(product.name, style: const TextStyle(fontWeight: FontWeight.bold)),
              subtitle: Text('${product.price} Ft'),
              trailing: ElevatedButton(
                onPressed: () {
                  context.read<CartNotifier>().addToCart(product);
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(
                      content: Text('${product.name} kosárba téve!'),
                      duration: const Duration(milliseconds: 800),
                    ),
                  );
                },
                child: const Text('Kosárba'),
              ),
            ),
          );
        },
      ),
    );
  }
}
```

### 3. Fájl: `screens/cart_screen.dart` (Kosár nézet)
```dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../cart_notifier.dart';

class CartScreen extends StatelessWidget {
  const CartScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final cart = context.watch<CartNotifier>();

    return Scaffold(
      appBar: AppBar(
        title: const Text('Kosár tartalma'),
        actions: [
          if (cart.items.isNotEmpty)
            IconButton(
              icon: const Icon(Icons.delete_sweep),
              onPressed: () => cart.clearCart(),
            ),
        ],
      ),
      body: cart.items.isEmpty
          ? const Center(
              child: Text('A kosarad jelenleg üres!', style: TextStyle(fontSize: 18)),
            )
          : Column(
              children: [
                Expanded(
                  child: ListView.builder(
                    itemCount: cart.items.length,
                    itemBuilder: (context, index) {
                      final item = cart.items[index];
                      return ListTile(
                        title: Text(item.product.name),
                        subtitle: Text('${item.product.price} Ft x ${item.quantity}'),
                        trailing: Row(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            IconButton(
                              icon: const Icon(Icons.remove_circle_outline),
                              onPressed: () => cart.removeOneFromCart(item.product),
                            ),
                            Text('${item.quantity}', style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                            IconButton(
                              icon: const Icon(Icons.add_circle_outline),
                              onPressed: () => cart.addToCart(item.product),
                            ),
                          ],
                        ),
                      );
                    },
                  ),
                ),
                Container(
                  padding: const EdgeInsets.all(20.0),
                  decoration: BoxDecoration(
                    color: Theme.of(context).cardColor,
                    boxShadow: const [BoxShadow(color: Colors.black12, blurRadius: 10)],
                  ),
                  child: Column(
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          const Text('Fizetendő végösszeg:', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                          Text('${cart.totalAmount} Ft', style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: Colors.blue)),
                        ],
                      ),
                      const SizedBox(height: 15),
                      SizedBox(
                        width: double.infinity,
                        child: ElevatedButton(
                          style: ElevatedButton.styleFrom(
                            padding: const EdgeInsets.symmetric(vertical: 15),
                            backgroundColor: Colors.blue,
                            foregroundColor: Colors.white,
                          ),
                          onPressed: () {
                            ScaffoldMessenger.of(context).showSnackBar(
                              const SnackBar(content: Text('Rendelés elküldve!')),
                            );
                            cart.clearCart();
                            Navigator.pop(context);
                          },
                          child: const Text('Megrendelés és fizetés', style: TextStyle(fontSize: 16)),
                        ),
                      )
                    ],
                  ),
                ),
              ],
            ),
    );
  }
}
```

### 4. Fájl: `main.dart` (Alkalmazás gyökér)
```dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'cart_notifier.dart';
import 'screens/catalog_screen.dart';

void main() {
  runApp(
    ChangeNotifierProvider(
      create: (context) => CartNotifier(),
      child: const MaterialApp(
        debugShowCheckedModeBanner: false,
        home: CatalogScreen(),
      ),
    ),
  );
}
```

---

## Heti Ellenőrző Kérdések

### 1. Mi a különbség a lokális (ephemeral) és a globális (app) state között?
A **lokális (ephemeral) állapot** egyetlen widget belső, elszigetelt adata, amelyre más widgeteknek nincs rálátása és nincs rá hatásuk (pl. egy checkbox kipipált állapota vagy az aktuálisan beírt szöveg egy mezőben). Ezt bátran és hatékonyan lehet `setState`-tel kezelni.
A **globális (app) állapot** ezzel szemben az alkalmazás több pontján, akár különböző képernyőkön is felhasznált és módosított adatot jelent (pl. a bejelentkezett felhasználó adatai vagy a kosár tartalma). Ennek átadásához és kezeléséhez strukturált állapotkezelőt (pl. `Provider`-t, `Riverpod`-ot) használunk.

### 2. Mi a gond a setState-tel, ha mélyen fészkelt widgetfában akarunk adatot továbbítani?
Ha a state a widget-fa tetején van, és a fa alján lévő widgetnek van rá szüksége, akkor minden köztes widgetnek át kell adni az adatot (és a callback metódusokat) a konstruktorán keresztül. Ezt a jelenséget **prop drillingnek** nevezzük. Ez felesleges boilerplate kódot generál, rontja a karbantarthatóságot, és a köztes widgetek szükségtelenül újraépülnek a szülő `setState` hívásakor.

### 3. Mi az a prop drilling és hogyan oldja meg a Provider/ChangeNotifier?
A **prop drilling** az adatok konstruktorokon keresztüli mély átadása a widget-fában. A `Provider` ezt úgy oldja meg, hogy az InheritedWidget technológiát használva közvetlenül a `BuildContext`-en keresztül elérhetővé teszi az adatokat a fa bármely pontján. Bármelyik widget lekérheti a tárolót a `context.read<Notifier>()` vagy `context.watch<Notifier>()` hívásokkal, kihagyva az összes köztes szintet.

### 4. Hogyan értesíti a ChangeNotifier a hallgatóit a változásokról?
A `ChangeNotifier` a megfigyelő (Observer) tervezési mintát implementálja. Amikor az osztályban egy belső változó értéke megváltozik, meg kell hívni a `notifyListeners()` metódust. Ez a metódus végigmegy az összes feliratkozott widgeten (akik pl. `context.watch<T>()`-on keresztül hallgatják) és jelzi nekik, hogy az állapot megváltozott, ami kiváltja a widgetek `build` metódusának újbóli lefutását.

### 5. Miért érdemes szelektíven figyelni a változásokat (watch vs read)?
A `context.watch<T>()` feliratkozik az állapot változásaira: ha a notifier meghívja a `notifyListeners()`-t, a widget újraépül. Ezt csak a `build` metódusban szabad használni, ahol konkrétan meg akarjuk jeleníteni az adatot.
A `context.read<T>()` csak lekéri a notifier példányát, de nem iratkozik fel rá. Nem vált ki újraépülést a változáskor. Ezt tipikusan eseménykezelőkben (pl. egy gomb `onPressed` callbackjében) használjuk metódusok meghívására, így megóvjuk az UI-t a felesleges rebuild-ektől, javítva a teljesítményt.
