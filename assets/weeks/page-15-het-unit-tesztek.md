# 15. hét — Unit tesztek

## Cél
A lecke célja, hogy elsajátítsd a Flutter és Dart alkalmazások üzleti logikájának automatizált tesztelését. Megtanulod, hogyan építsd fel a tesztjeidet az Arrange-Act-Assert (AAA) minta alapján, hogyan válaszd le a külső függőségeket (API-k, adatbázisok) a `mocktail` csomag segítségével, és hogyan írj tiszta, karbantartható, robusztus unit teszteket az alkalmazásod különböző rétegeire (Use Case, Validator, Formatter, Repository).

---

## Elmélet

### Mi az a unit tesztelés és miért fontos?
A unit tesztelés (egységtesztelés) az alkalmazás legkisebb tesztelhető egységeinek – jellemzően függvényeknek, metódusoknak vagy osztályoknak – az izolált ellenőrzését jelenti. A unit tesztek gyorsak (pár ezredmásodperc alatt lefutnak), nem igényelnek grafikus felületet, emulátort vagy fizikai eszközt, és azonnali visszajelzést adnak a kód helyességéről.

A unit tesztelés előnyei:
- **Biztonságos refaktorálás:** Ha megváltoztatod a belső logikát, a tesztek azonnal jelzik, ha elrontottál valamit (regresszió).
- **Dokumentáció:** A jól megírt tesztek leírják, hogyan kellene a kódnak viselkednie különböző bemenetek esetén.
- **Tiszta kód:** A nehezen tesztelhető kód általában rosszul strukturált kód. A tesztelhetőség rákényszerít a Dependency Injection (függőség-befecskendezés) használatára és a Clean Architecture elveinek betartására.

### Az Arrange-Act-Assert (AAA) minta
Minden jó egységteszt három jól elkülöníthető lépésre osztható fel:
1. **Arrange (Előkészítés):** Létrehozzuk a tesztelni kívánt osztályt, beállítjuk a bemeneti adatokat, és konfiguráljuk a mock függőségeket.
2. **Act (Végrehajtás):** Meghívjuk a tesztelni kívánt metódust vagy függvényt.
3. **Assert (Ellenőrzés):** Ellenőrizzük, hogy a kapott eredmény megegyezik-e a várt eredménnyel, illetve a függőségek a várt módon lettek-e meghívva.

### Mit tesztelünk unit teszttel?
- **Use Case-ek:** Az üzleti folyamatokat leíró osztályok logikáját.
- **Validatorok:** Beviteli mezők (e-mail, jelszó, telefonszám) ellenőrzési szabályait.
- **Formatterek:** Adatok megjelenítési formátumát (pl. pénznem formázó, dátum átalakító).
- **Repository-ok:** Hogy a hálózati kliens vagy adatbázis hibája esetén a megfelelő egyedi Exception-t dobják-e tovább.
- **Entity szabályok:** Az üzleti modellek belső logikáját (pl. egy kosár végösszeg-számítása).

### A mockolás elve és a mocktail csomag
Amikor egy egységet tesztelünk, el kell szigetelnünk azt a külvilágtól (hálózat, adatbázis, fájlrendszer). Ha a `GetProductUseCase` osztály lekérdezi a terméket az adatbázisból, nem akarunk valódi adatbázist indítani a teszt alatt. Ehelyett létrehozunk egy "Mock" (utánzat) objektumot, ami leutánozza a valódi adatbázis-kapcsolatot megvalósító osztály interfészét.

A Dart ökoszisztémában a `mocktail` egy kódgenerálás nélküli, típusbiztos mockoló csomag, ami rendívül megkönnyíti a stubolást (az előre megírt válaszok konfigurálását) és a verifikálást (annak ellenőrzését, hogy az adott metódus lefutott-e).

> [!NOTE]
> A hagyományos `mockito` csomaggal szemben a `mocktail` nem igényel `build_runner` kódgenerálást, így a tesztek írása és futtatása sokkal gyorsabb és egyszerűbb.

---

## Kódpéldák

Az alábbiakban egy teljes, működő és compilable példát láthatsz egy `mocktail`-lal megvalósított unit tesztre. Bemutatjuk a modelleket, a repository interfészt, a Use Case-t, majd a hozzájuk tartozó teszteket.

### A tesztelendő kód (`lib/domain/product.dart` és `lib/domain/get_product_use_case.dart`)

```dart
// lib/domain/product.dart
class Product {
  final String id;
  final String name;
  final double price;

  const Product({
    required this.id,
    required this.name,
    required this.price,
  });
}

// lib/domain/product_repository.dart
abstract class ProductRepository {
  Future<Product> getProductById(String id);
}

// lib/domain/get_product_use_case.dart
class ProductNotFoundException implements Exception {
  final String message;
  ProductNotFoundException(this.message);
}

class GetProductUseCase {
  final ProductRepository repository;

  GetProductUseCase({required this.repository});

  Future<Product> execute(String id) async {
    if (id.trim().isEmpty) {
      throw ArgumentError('Az ID nem lehet üres!');
    }
    try {
      return await repository.getProductById(id);
    } catch (e) {
      throw ProductNotFoundException('A keresett termék nem található: $id');
    }
  }
}
```

### A teszt kód (`test/get_product_use_case_test.dart`)

```dart
// test/get_product_use_case_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

// A tesztben definiáljuk a Mock osztályt
class MockProductRepository extends Mock implements ProductRepository {}

void main() {
  // Létrehozzuk a tesztben használt változókat
  late MockProductRepository mockRepository;
  late GetProductUseCase useCase;

  // Minden egyes teszteset előtt lefutó inicializálás
  setUp(() {
    mockRepository = MockProductRepository();
    useCase = GetProductUseCase(repository: mockRepository);
  });

  group('GetProductUseCase - egységtesztek', () {
    const tProductId = 'prod-123';
    const tProduct = Product(
      id: tProductId,
      name: 'Teszt Laptop',
      price: 299990.0,
    );

    test(
      'sikeres lekérdezés esetén vissza kell adnia a megfelelő Product objektumot',
      () async {
        // Arrange (Stubolás: megmondjuk a mock-nak, mit válaszoljon)
        when(() => mockRepository.getProductById(tProductId))
            .thenAnswer((_) async => tProduct);

        // Act
        final result = await useCase.execute(tProductId);

        // Assert
        expect(result, isNotNull);
        expect(result.id, equals(tProductId));
        expect(result.name, equals('Teszt Laptop'));
        expect(result.price, equals(299990.0));

        // Verifikáljuk, hogy a repository metódusa pontosan egyszer lett meghívva a megadott ID-val
        verify(() => mockRepository.getProductById(tProductId)).called(1);
        verifyNoMoreInteractions(mockRepository);
      },
    );

    test(
      'ha az ID üres string, ArgumentError kivételt kell dobnia anélkül, hogy a repository-t meghívná',
      () async {
        // Arrange - nincs szükség repository stubolásra, mert el sem jut odáig a kód

        // Act & Assert
        expect(
          () => useCase.execute('   '),
          throwsA(isA<ArgumentError>()),
        );

        // Verifikáljuk, hogy a repository-hoz nem érkezett hívás
        verifyZeroInteractions(mockRepository);
      },
    );

    test(
      'ha a repository hibát dob, a UseCase-nek át kell alakítania ProductNotFoundException kivétellé',
      () async {
        // Arrange (Stubolás hiba dobásra)
        when(() => mockRepository.getProductById(tProductId))
            .thenThrow(Exception('Database error'));

        // Act & Assert
        expect(
          () => useCase.execute(tProductId),
          throwsA(isA<ProductNotFoundException>()),
        );

        // Ellenőrizzük a hívást
        verify(() => mockRepository.getProductById(tProductId)).called(1);
      },
    );
  });
}
```

---

## Gyakorlófeladatok & Megoldások

### 1. feladat: Kosár végösszeg számító tesztelése
Készíts egy `Cart` osztályt, ami `CartItem` listát tárol. A kosárnak rendelkeznie kell egy `calculateTotal()` metódussal.
Szabályok:
- Ha a részösszeg meghaladja a 10 000 Ft-ot, 10% kedvezmény jár a végösszegből.
- Ha van megadva fix értékű kuponkód kedvezmény (pl. 2000 Ft), azt a százalékos kedvezmény *után* kell levonni. A végösszeg sosem mehet 0 Ft alá.

#### Megoldás kódja (`lib/cart_calculator.dart`)
```dart
class CartItem {
  final String name;
  final double price;
  final int quantity;

  const CartItem({
    required this.name,
    required this.price,
    required this.quantity,
  });

  double get subtotal => price * quantity;
}

class Cart {
  final List<CartItem> items;
  final double couponDiscount;

  const Cart({
    required this.items,
    this.couponDiscount = 0.0,
  });

  double calculateTotal() {
    double subtotal = items.fold(0.0, (sum, item) => sum + item.subtotal);
    
    // Százalékos kedvezmény levonása
    if (subtotal > 10000.0) {
      subtotal = subtotal * 0.9;
    }

    // Fix kupon levonása
    double finalTotal = subtotal - couponDiscount;
    return finalTotal < 0 ? 0.0 : finalTotal;
  }
}
```

#### Teszt kódja (`test/cart_calculator_test.dart`)
```dart
import 'package:flutter_test/flutter_test.dart';
// Feltételezzük, hogy a fenti osztályokat importáljuk

void main() {
  group('Cart - calculateTotal tesztek', () {
    test('üres kosár esetén a végösszeg 0 Ft', () {
      const cart = Cart(items: []);
      expect(cart.calculateTotal(), equals(0.0));
    });

    test('10 000 Ft alatti kosárérték esetén nincs százalékos kedvezmény', () {
      const cart = Cart(items: [
        CartItem(name: 'Zokni', price: 1500.0, quantity: 2), // 3000 Ft
        CartItem(name: 'Póló', price: 4000.0, quantity: 1), // 4000 Ft
      ]);
      expect(cart.calculateTotal(), equals(7000.0));
    });

    test('10 000 Ft feletti kosárérték esetén 10% kedvezmény jár', () {
      const cart = Cart(items: [
        CartItem(name: 'Cipő', price: 12000.0, quantity: 1), // 12000 Ft
      ]);
      // 12000 * 0.9 = 10800 Ft
      expect(cart.calculateTotal(), equals(10800.0));
    });

    test('kuponkedvezmény helyes levonása a százalékos kedvezmény után', () {
      const cart = Cart(
        items: [
          CartItem(name: 'Cipő', price: 12000.0, quantity: 1), // 12000 Ft
        ],
        couponDiscount: 2000.0,
      );
      // (12000 * 0.9) - 2000 = 8800 Ft
      expect(cart.calculateTotal(), equals(8800.0));
    });

    test('a végösszeg nem mehet nullánál lejjebb nagy kupon esetén sem', () {
      const cart = Cart(
        items: [
          CartItem(name: 'Póló', price: 3000.0, quantity: 1),
        ],
        couponDiscount: 5000.0,
      );
      expect(cart.calculateTotal(), equals(0.0));
    });
  });
}
```

---

### 2. feladat: Form validator tesztelése
Írj teszteket egy `FormValidator` osztályra, aminek két metódusa van:
- `validateEmail(String? email)`: Visszaadja, hogy "Az email megadása kötelező" ha null vagy üres, "Érvénytelen formátum" ha nem tartalmaz `@` és `.` karaktereket a megfelelő helyen, egyébként `null` (sikeres).
- `validatePassword(String? password)`: Visszaadja, hogy "A jelszó legalább 8 karakter hosszú legyen", "A jelszónak tartalmaznia kell számot" ha nincs benne digit, egyébként `null`.

#### Megoldás kódja (`lib/form_validator.dart`)
```dart
class FormValidator {
  static String? validateEmail(String? email) {
    if (email == null || email.trim().isEmpty) {
      return 'Az email megadása kötelező';
    }
    final emailRegex = RegExp(r'^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$');
    if (!emailRegex.hasMatch(email)) {
      return 'Érvénytelen formátum';
    }
    return null;
  }

  static String? validatePassword(String? password) {
    if (password == null || password.length < 8) {
      return 'A jelszó legalább 8 karakter hosszú legyen';
    }
    if (!password.contains(RegExp(r'[0-9]'))) {
      return 'A jelszónak tartalmaznia kell számot';
    }
    return null;
  }
}
```

#### Teszt kódja (`test/form_validator_test.dart`)
```dart
import 'package:flutter_test/flutter_test.dart';

void main() {
  group('FormValidator - Email tesztek', () {
    test('null vagy üres email hibaüzenetet ad', () {
      expect(FormValidator.validateEmail(null), equals('Az email megadása kötelező'));
      expect(FormValidator.validateEmail(''), equals('Az email megadása kötelező'));
      expect(FormValidator.validateEmail('   '), equals('Az email megadása kötelező'));
    });

    test('rossz formátumú email hibát dob', () {
      expect(FormValidator.validateEmail('teszt'), equals('Érvénytelen formátum'));
      expect(FormValidator.validateEmail('teszt@com'), equals('Érvénytelen formátum'));
      expect(FormValidator.validateEmail('teszt.hu'), equals('Érvénytelen formátum'));
    });

    test('helyes email esetén null-t ad vissza', () {
      expect(FormValidator.validateEmail('info@prstart.hu'), isNull);
    });
  });

  group('FormValidator - Jelszó tesztek', () {
    test('túl rövid jelszó hibaüzenetet ad', () {
      expect(FormValidator.validatePassword('Abc1'), equals('A jelszó legalább 8 karakter hosszú legyen'));
    });

    test('jelszó szám nélkül hibaüzenetet ad', () {
      expect(FormValidator.validatePassword('Abcdefghij'), equals('A jelszónak tartalmaznia kell számot'));
    });

    test('helyes jelszó esetén null-t ad vissza', () {
      expect(FormValidator.validatePassword('Biztonsagos123'), isNull);
    });
  });
}
```

---

## Heti Mini Projekt: Tesztelt domain layer

A heti projekt feladat egy e-learning vagy e-commerce backend szinkronizációért felelős domain réteg elkészítése és teljes körű lefedése unit tesztekkel. A rendszernek a következő elemekből kell állnia:

1. `Order` entitás (id, items, status).
2. `OrderRepository` interfész, amely eléri az API-t.
3. `CheckoutUseCase` osztály, amely a kosár feldolgozását, az árak kalkulációját és az API hívást koordinálja.

### Implementáció (`lib/features/checkout/checkout_use_case.dart`)

```dart
// Rendelés entitás
class Order {
  final String id;
  final double totalAmount;
  final String status;

  const Order({
    required this.id,
    required this.totalAmount,
    required this.status,
  });
}

// Interfész a külső adathoz
abstract class OrderRepository {
  Future<Order> createOrder(List<Map<String, dynamic>> items, double total);
}

// Egyedi kivétel
class CheckoutException implements Exception {
  final String message;
  CheckoutException(this.message);
}

// Üzleti logika
class CheckoutUseCase {
  final OrderRepository repository;

  CheckoutUseCase({required this.repository});

  Future<Order> execute(List<Map<String, dynamic>> items) async {
    if (items.isEmpty) {
      throw CheckoutException('A kosár nem lehet üres!');
    }

    double total = 0.0;
    for (var item in items) {
      final price = item['price'] as double?;
      final qty = item['quantity'] as int?;
      
      if (price == null || qty == null || price <= 0 || qty <= 0) {
        throw CheckoutException('Érvénytelen termékadatok a kosárban.');
      }
      total += price * qty;
    }

    try {
      return await repository.createOrder(items, total);
    } catch (e) {
      throw CheckoutException('A rendelés leadása sikertelen: ${e.toString()}');
    }
  }
}
```

### Tesztelési lefedettség (`test/features/checkout/checkout_use_case_test.dart`)

Ebben a tesztben szimulálunk minden lehetséges sikeres és hibás ágat, biztosítva a lefedettséget ezen az üzleti logikán.

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

// Mock osztály definiálása
class MockOrderRepository extends Mock implements OrderRepository {}

void main() {
  late MockOrderRepository mockRepository;
  late CheckoutUseCase useCase;

  setUp(() {
    mockRepository = MockOrderRepository();
    useCase = CheckoutUseCase(repository: mockRepository);
  });

  group('CheckoutUseCase tesztcsomag (Mini Projekt)', () {
    final tValidItems = [
      {'name': 'Könyv', 'price': 3500.0, 'quantity': 2}, // 7000.0
      {'name': 'Toll', 'price': 500.0, 'quantity': 1},   // 500.0
    ];
    const tTotal = 7500.0;
    const tOrder = Order(id: 'order-999', totalAmount: tTotal, status: 'pending');

    test(
      'sikeres rendelés leadása esetén a kalkulált összeggel hívja meg a repository-t',
      () async {
        // Arrange
        when(() => mockRepository.createOrder(tValidItems, tTotal))
            .thenAnswer((_) async => tOrder);

        // Act
        final result = await useCase.execute(tValidItems);

        // Assert
        expect(result, equals(tOrder));
        expect(result.totalAmount, equals(tTotal));
        
        verify(() => mockRepository.createOrder(tValidItems, tTotal)).called(1);
        verifyNoMoreInteractions(mockRepository);
      },
    );

    test(
      'ha üres a terméklista, CheckoutException-t dob, és nem hívja a repository-t',
      () async {
        // Act & Assert
        expect(
          () => useCase.execute([]),
          throwsA(
            isA<CheckoutException>().having(
              (e) => e.message,
              'üzenet',
              contains('A kosár nem lehet üres'),
            ),
          ),
        );

        verifyZeroInteractions(mockRepository);
      },
    );

    test(
      'ha a termék ára negatív vagy nulla, hibát dob',
      () async {
        final invalidItems = [
          {'name': 'Hibás', 'price': -100.0, 'quantity': 1}
        ];

        expect(
          () => useCase.execute(invalidItems),
          throwsA(isA<CheckoutException>()),
        );
        verifyZeroInteractions(mockRepository);
      },
    );

    test(
      'ha a repository hibát dob (pl. hálózati hiba), a UseCase CheckoutException-t dob',
      () async {
        // Arrange
        when(() => mockRepository.createOrder(any(), any()))
            .thenThrow(Exception('Server unreachable'));

        // Act & Assert
        expect(
          () => useCase.execute(tValidItems),
          throwsA(isA<CheckoutException>()),
        );

        verify(() => mockRepository.createOrder(tValidItems, tTotal)).called(1);
      },
    );
  });
}
```

---

## Heti Ellenőrző Kérdések

### 1. Miért nem futtathatunk valós HTTP hívást vagy adatbázis lekérdezést unit tesztben?
A hálózati hívások és az adatbázis-hozzáférések külső tényezőktől függenek (internetkapcsolat, szerver elérhetősége, lokális fájlrendszer állapota). Ha valós hívást végeznénk:
1. A tesztek lassúak lennének.
2. A tesztek instabillá válnának (flaky tests) – elbukhatnának úgy is, hogy a kódunk egyébként tökéletes, csak épp elment az internet.
3. Megváltoztathatnák a teszt- vagy éles adatbázis tartalmát.
Ezért ezeket a rétegeket mindig mockolni kell unit tesztben.

### 2. Mi a különbség a mock, stub és fake fogalmak között?
- **Stub:** Egy olyan minimális implementáció vagy objektum, ami előre rögzített válaszokat ad vissza a hívásokra (pl. "ha ezt a metódust hívják ezen paraméterrel, adj vissza egy üres listát").
- **Mock:** Olyan objektum, aminél nemcsak a visszatérési értéket tudjuk beállítani, hanem azt is ellenőrizni tudjuk (verifikáció), hogy milyen paraméterekkel, hányszor lett meghívva a futás során.
- **Fake:** Egy valódi, de egyszerűsített működéssel rendelkező osztály, ami nem produkciós környezetre való (pl. egy `InMemoryDatabaseRepository`, ami egy sima Dart Map-ben tárolja a memóriában a rekordokat a valódi SQLite helyett).

### 3. Hogyan tesztelhetünk olyan metódusokat, amik aszinkron Future-t vagy Stream-et adnak vissza?
- **Future:** A teszt kódjában az `async` kulcsszót használjuk, és az `await` kulcsszóval megvárjuk a metódus lefutását, vagy az `expect` kifejezésben a `completion` vagy `throwsA` matcheket használjuk.
- **Stream:** A `test` csomag tartalmazza az `emits`, `emitsInOrder` vagy `emitsError` matcheket, amelyekkel ellenőrizhető, hogy a Stream a várt eseményeket küldi-e ki egymás után.

### 4. Mire szolgál a setUp és tearDown függvény a tesztcsomagban?
- **setUp:** Minden egyes `test()` blokk futása előtt végrehajtódik. Célja a tiszta tesztkörnyezet (új mockok, új Use Case példányok) felállítása, hogy a tesztek ne tudják egymás állapotát elrontani.
- **tearDown:** Minden egyes `test()` blokk futása után hajtódik végre. Főleg erőforrások lezárására (pl. StreamController, adatbázis kapcsolat bontása) használatos.

### 5. Miért fontos a registerFallbackValue a mocktail használatakor?
Amikor a `mocktail` csomagban az `any()` paraméter-matchert használjuk nem primitív típusok (pl. egyedi osztályok) esetén, a Dart típusrendszere miatt regisztrálnunk kell egy alapértelmezett értéket. Ha ezt elmulasztjuk, a teszt futása `TypeError`-ral elszáll. Ezt a `registerFallbackValue(DummyObject())` hívással tehetjük meg a `setUpAll()` vagy `main()` függvény elején.
