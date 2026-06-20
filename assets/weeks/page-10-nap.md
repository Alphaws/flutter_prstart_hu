# 10. nap — TextField, beviteli mezők és gombok

Megtanuljuk a felhasználói bevitelek kezelését. Használjuk a TextField widgetet, a `TextEditingController` osztályt a bevitt érték kiolvasására és törlésére, valamint stílust adunk a beviteli mezőnek.

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
final controller = TextEditingController();
// A widgetben:
TextField(
  controller: controller,
  decoration: const InputDecoration(
    labelText: 'Írj be valamit',
    border: OutlineInputBorder(),
  ),
)
```

---

## 🛠️ Napi Gyakorlat
> [!IMPORTANT]
> A programozást nem lehet elméletben megtanulni. A mai gyakorlati feladatod a következő:
>
> **Feladat:** Készíts egy képernyőt, ahol a felhasználó beírhatja a nevét, és a gomb megnyomására egy stílusos üdvözlő üzenet jelenik meg a beviteli mező alatt.

---

> [!TIP]
> **Profi tipp:** Futtasd rendszeresen a `dart format .` parancsot a terminálból, hogy a kódod elrendezése mindig megfeleljen a Dart hivatalos irányelveinek.