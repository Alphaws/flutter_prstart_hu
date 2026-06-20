# 28. nap — UI kit komponensek

Megtervezzük a saját újrahasználható UI kitünket. Készítünk egyedi gombot (`PrimaryButton`), egyedi beviteli mezőt (`AppTextField`) és státuszjelző kártyákat.

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
class PrimaryButton extends StatelessWidget {
  final String text;
  final VoidCallback onPressed;
  const PrimaryButton({super.key, required this.text, required this.onPressed});
  @override
  Widget build(BuildContext context) { ... }
}
```

---

## 🛠️ Napi Gyakorlat
> [!IMPORTANT]
> A programozást nem lehet elméletben megtanulni. A mai gyakorlati feladatod a következő:
>
> **Feladat:** Szervezd ki az alkalmazásodban használt egyedi dizájnú gombokat és beviteli mezőket önálló, paraméterezhető osztályokba.

---

> [!TIP]
> **Profi tipp:** Futtasd rendszeresen a `dart format .` parancsot a terminálból, hogy a kódod elrendezése mindig megfeleljen a Dart hivatalos irányelveinek.