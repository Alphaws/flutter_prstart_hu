# 4. nap — Dart Null Safety és gyűjtemények

A Dart Sound Null Safety koncepciója megvéd a null-pointer hibáktól. Megtanuljuk a nullable típusok (?, !), a null-aware operátorok (??, ?. ) és a legfontosabb gyűjteménytípusok (List, Map, Set) használatát.

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
  String? nickname = null;
  print(nickname ?? 'Vendég'); // Ha null, Vendég jelenik meg
  
  List<String> fruits = ['alma', 'eper', 'banán'];
  var capitalized = fruits.map((f) => f.toUpperCase()).toList();
  print(capitalized);
}
```

---

## 🛠️ Napi Gyakorlat
> [!IMPORTANT]
> A programozást nem lehet elméletben megtanulni. A mai gyakorlati feladatod a következő:
>
> **Feladat:** Hozz létre egy termékeket (Map) tartalmazó listát. Szűrd ki azokat, amelyek ára meghaladja az 5000 Ft-ot, és mentsd el a nevüket egy új listába.

---

> [!TIP]
> **Profi tipp:** Futtasd rendszeresen a `dart format .` parancsot a terminálból, hogy a kódod elrendezése mindig megfeleljen a Dart hivatalos irányelveinek.