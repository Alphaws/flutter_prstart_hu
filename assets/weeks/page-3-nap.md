# 3. nap — Dart függvények, osztályok és OOP alapok

A mai nap a függvények és az objektumorientált programozás (OOP) alapjairól szól Dartban. Megtanuljuk a pozicionális, opcionális és nevesített (named) paraméterek használatát, az osztályok, konstruktorok írását, valamint az adattagok elérését.

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
class Product {
  final String name;
  final double price;
  final int stock;

  Product({
    required this.name,
    required this.price,
    this.stock = 0,
  });

  bool get isAvailable => stock > 0;
}

void main() {
  final p = Product(name: 'Kávé', price: 990, stock: 15);
  print('${p.name} elérhető? ${p.isAvailable}');
}
```

---

## 🛠️ Napi Gyakorlat
> [!IMPORTANT]
> A programozást nem lehet elméletben megtanulni. A mai gyakorlati feladatod a következő:
>
> **Feladat:** Készíts egy `User` osztályt, amely tartalmazza a felhasználó nevét, emailjét és opcionálisan a korát. Írj egy metódust, amely ellenőrzi, hogy a felhasználó felnőttkorú-e.

---

> [!TIP]
> **Profi tipp:** Futtasd rendszeresen a `dart format .` parancsot a terminálból, hogy a kódod elrendezése mindig megfeleljen a Dart hivatalos irányelveinek.