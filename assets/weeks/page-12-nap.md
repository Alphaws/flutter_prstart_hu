# 12. nap — ListView és Card widgetek

A nagy mennyiségű elem görgethető megjelenítésére a ListView és annak builder változata szolgál. Megismerkedünk a teljesítménybeli előnyeivel, a ListTile és a Card widgetekkel.

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
ListView.builder(
  itemCount: items.length,
  itemBuilder: (context, index) {
    return Card(
      child: ListTile(
        title: Text(items[index]),
        leading: const Icon(Icons.shopping_bag),
      ),
    );
  },
)
```

---

## 🛠️ Napi Gyakorlat
> [!IMPORTANT]
> A programozást nem lehet elméletben megtanulni. A mai gyakorlati feladatod a következő:
>
> **Feladat:** Alakítsd át a tegnapi bevásárlólistádat úgy, hogy a listaelemek Card widgetbe ágyazott ListTile-okként jelenjenek meg.

---

> [!TIP]
> **Profi tipp:** Futtasd rendszeresen a `dart format .` parancsot a terminálból, hogy a kódod elrendezése mindig megfeleljen a Dart hivatalos irányelveinek.