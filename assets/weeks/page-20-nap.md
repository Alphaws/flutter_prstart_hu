# 20. nap — Webshop részletező UI

Létrehozzuk a termék részletes leíró oldalát. Nagy felbontású kép, részletes leírás, árcédula és egy lebegő kosárba helyező akciógomb fogja alkotni a felületet.

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
Scaffold(
  body: CustomScrollView(
    slivers: [
      SliverAppBar(expandedHeight: 300, flexibleSpace: FlexibleSpaceBar(background: Image.network(...))),
      SliverFillRemaining(child: ProductDetails()),
    ],
  ),
)
```

---

## 🛠️ Napi Gyakorlat
> [!IMPORTANT]
> A programozást nem lehet elméletben megtanulni. A mai gyakorlati feladatod a következő:
>
> **Feladat:** Készítsd el a termékrészletező oldalt, ahol a kosárba gomb megnyomására egy Snackbar jelzi a sikeres műveletet.

---

> [!TIP]
> **Profi tipp:** Futtasd rendszeresen a `dart format .` parancsot a terminálból, hogy a kódod elrendezése mindig megfeleljen a Dart hivatalos irányelveinek.