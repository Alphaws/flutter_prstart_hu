# 2. nap — Dart változók, típusok és alap műveletek

Megismerkedünk a Dart nyelv alapvető szintaxisával, változók deklarálásával (var, final, const) és az alapvető adattípusokkal (int, double, String, bool). Különös figyelmet fordítunk a fordítási időben (const) és futási időben (final) állandó értékek közötti különbségre.

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
void main() {
  var name = 'Flutter Tanuló';
  final double price = 1990.90;
  const int taxPercent = 27;
  
  print('Termék: $name, Bruttó: ${price * (1 + taxPercent / 100)} Ft');
}
```

---

## 🛠️ Napi Gyakorlat
> [!IMPORTANT]
> A programozást nem lehet elméletben megtanulni. A mai gyakorlati feladatod a következő:
>
> **Feladat:** Írj egy konzolos Dart programot, amely bekér és kiszámol egy téglalap területét és kerületét adott oldalhosszak mellett.

---

> [!TIP]
> **Profi tipp:** Futtasd rendszeresen a `dart format .` parancsot a terminálból, hogy a kódod elrendezése mindig megfeleljen a Dart hivatalos irányelveinek.