# A nagy Flutter State Management vita: Bloc vagy Riverpod?

**Szerző:** PRSTART Blog  
**Dátum:** 2026-06-20  
**Téma:** Állapotkezelés (State Management)  

---

A Flutter fejlesztők körében nincs még egy olyan téma, amely annyi vitát váltana ki, mint az állapotkezelés. Bár számos csomag létezik (Provider, GetX, MobX stb.), 2026-ra két fő irányzat maradt domináns a professzionális alkalmazásokban: a **Bloc (Business Logic Component)** és a **Riverpod**. Ebben a bejegyzésben összehasonlítjuk őket, hogy segítsünk kiválasztani a projektedhez leginkább illőt.

---

## 1. BLoC (Business Logic Component) — A vállalati standard

A Bloc a legrégebbi és legelterjedtebb professzionális állapotkezelő minta Flutterben. Szigorú, eseményvezérelt (Event-driven) architektúrát követ:
- **Event (Esemény):** A felhasználó interakciója (pl. gombnyomás).
- **Bloc (Üzleti Logika):** Fogadja az eseményeket, feldolgozza őket, majd új állapotot bocsát ki.
- **State (Állapot):** A felületen kirajzolódó pillanatnyi státusz (pl. Loading, Success, Error).

### Cubit: A Bloc könnyebb verziója
Ha nincs szükségünk eseményfolyamok transzformálására (pl. debounce, throttle), a Bloc csomag része a **Cubit**, amely események helyett egyszerű függvényhívásokkal módosítja az állapotot.

```dart
// Cubit példa
class CounterCubit extends Cubit<int> {
  CounterCubit() : super(0);
  void increment() => emit(state + 1);
}
```

### Miért jó a Bloc?
- **Szigorú struktúra:** Nagy csapatokban mindenki pontosan ugyanúgy írja a kódot. A logikai rétegek határozottan elválnak egymástól.
- **Kiváló tesztelhetőség:** A `bloc_test` csomag segítségével rendkívül egyszerűen tesztelhetőek a bemenő eseményekre adott kimenő állapotváltozások.
- **Függetlenség:** Az üzleti logika teljesen független a Flutter UI rétegétől (nem igényel BuildContext-et a tesztek alatt).

---

## 2. Riverpod — A rugalmas és típusbiztos alternatíva

A Riverpod-ot a népszerű Provider csomag szerzője, Remi Rousselet hozta létre, kifejezetten a Provider strukturális hibáinak kijavítására. A Riverpod egy globális deklaratív állapotkezelési rendszer.

### Fő jellemzői:
- **Nincs BuildContext függőség:** Bárhonnan elérhetjük a providereket (pl. egy külső szervizosztályból vagy tesztből is).
- **Compile-time Safe:** Nem kaphatunk futásidőben `ProviderNotFoundException`-t, mint a régi Providernél.
- **Auto-dispose támogatás:** A providerek automatikusan megsemmisülnek, ha a képernyőt bezárja a felhasználó, így elkerülhetőek a memóriaszivárgások.

```dart
// Riverpod Notifier példa
final counterProvider = NotifierProvider<CounterNotifier, int>(CounterNotifier.new);

class CounterNotifier extends Notifier<int> {
  @override
  int build() => 0;
  
  void increment() => state++;
}
```

---

## 3. Összehasonlítás

| Szempont | Bloc / Cubit | Riverpod |
| :--- | :--- | :--- |
| **Boilerplate kód** | Magas (sok osztály, esemény és állapot kell) | Alacsony/Közepes (tömör megvalósítás) |
| **BuildContext igény** | UI-ban igen (`BlocProvider.of`) | Nem (ConsumerWidget és WidgetRef kell) |
| **Tanulási görbe** | Meredek (szigorú fogalmak) | Közepes (könnyű elkezdeni) |
| **Tervezési minta** | Unidirectional Data Flow / Redux-szerű | Reaktiv Dependency Injection |
| **Kódgenerálás** | Opcionális | Ajánlott (`@riverpod` annotációk) |

---

## 4. Mit válassz a projektedhez?

### Válassz a BLoC-ot, ha:
1. **Nagyvállalati (Enterprise) projekten dolgozol:** Ahol a szigorú struktúra és a minták kényszerítése fontosabb, mint a gyorsaság.
2. **Nagy a csapat:** Ahol több fejlesztő dolgozik egyszerre, és minimalizálni kell az egyéni kódolási stílusból eredő káoszt.
3. **Komplex reaktív folyamataid vannak:** Pl. valós idejű chat üzenetek szűrése, pufferezése vagy keresési javaslatok késleltetése (debounce).

### Válassz a Riverpod-ot, ha:
1. **Startup vagy egyéni (Solo) fejlesztő vagy:** Ahol a fejlesztési sebesség és a rugalmasság a legfontosabb.
2. **Sok aszinkron adatod van:** A Riverpod `FutureProvider` és `StreamProvider` megoldásai zseniálisan kezelik a betöltési és hibaállapotokat automatikusan.
3. **Tiszta és tömör kódot szeretnél:** Kevesebb fájllal és kevesebb felesleges kóddal szeretnél azonos működést elérni.

---

## Végszó

Nincs abszolút győztes. Mindkét eszköz professzionális és alkalmas éles alkalmazások kiszolgálására. Ha a szigorú struktúra híve vagy, a Bloc lesz a barátod, ha a modern, reaktív és tömör kódolást szereted, adj egy esélyt a Riverpodnak.
