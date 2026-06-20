# 11. nap — Bevásárlólista alkalmazás

A mai napon összerakunk egy interaktív bevásárlólista oldalt. A listaelemeket egy tömbben tároljuk a State-ben, és dinamikusan tudunk elemet hozzáadni vagy törölni belőle.

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
List<String> items = [];
// setState hívással módosítjuk a listát:
setState(() {
  items.add(newText);
});
```

---

## 🛠️ Napi Gyakorlat
> [!IMPORTANT]
> A programozást nem lehet elméletben megtanulni. A mai gyakorlati feladatod a következő:
>
> **Feladat:** Valósítsd meg a bevásárlólistát egy szövegbevitellel és egy hozzáadó gombbal. Mindegyik elem mellett szerepeljen egy törlés ikon, amire kattintva az elem kikerül a listából.

---

> [!TIP]
> **Profi tipp:** Futtasd rendszeresen a `dart format .` parancsot a terminálból, hogy a kódod elrendezése mindig megfeleljen a Dart hivatalos irányelveinek.