# Dart 3.0: Rekordok, minták és az új osztálymódosítók korszak

**Szerző:** PRSTART Blog  
**Dátum:** 2026-06-20  
**Téma:** Dart nyelvi újdonságok  

---

A Google a Dart 3-as verziójával a nyelv történetének egyik legnagyobb frissítését szállította le. A 100%-os Sound Null Safety kötelezővé tétele mellett bevezetésre kerültek olyan funkciók, mint a **Records** (rekordok), a **Pattern Matching** (mintailesztés) és az új **osztálymódosítók** (class modifiers). Ebből a bejegyzésből megtudhatod, hogyan tehetik ezek hatékonyabbá és tisztábbá a Flutter kódodat.

---

## 1. 100% Sound Null Safety — Nincs visszaút

A Dart 3-tól kezdve a nyelv **kizárólag** null-safe módban fut. A régi, nem null-safe kódok támogatása teljesen megszűnt. 
Ez azt jelenti, hogy a fordító garantálja: ha egy változó típusa nem nullable (nincs ott a `?` végén), akkor az soha, semmilyen körülmények között nem vehet fel `null` értéket futásidőben. Ez drasztikusan csökkenti a hírhedt *NullPointerException* hibák számát és hatékonyabbá teszi a futtatókörnyezet (AOT compiler) optimalizációját is.

---

## 2. Records (Rekordok) — Egyszerű és gyors adatcsoportosítás

Gyakran előfordul, hogy egy függvényből több értéket szeretnénk visszaadni. Eddig ehhez vagy egy egyedi osztályt kellett létrehoznunk, vagy egy listával/mappel kellett trükköznünk. A rekordok erre nyújtanak beépített, típusbiztos megoldást.

A rekordok névtelen, nem módosítható (immutable) kollekciók, amelyek pozicionális vagy nevesített mezőket tartalmazhatnak.

### Példa pozicionális mezőkre:
```dart
(double, double) getLatLng() {
  return (47.4979, 19.0402); // Budapest koordinátái
}

void main() {
  final coordinates = getLatLng();
  print("Szélesség: ${coordinates.$1}"); // 47.4979
  print("Hosszúság: ${coordinates.$2}"); // 19.0402
}
```

### Példa nevesített mezőkre:
```dart
({String name, int age}) getUserInfo() {
  return (name: "Marci", age: 24);
}

void main() {
  final user = getUserInfo();
  print("Név: ${user.name}, Kor: ${user.age}");
}
```

---

## 3. Pattern Matching (Mintailesztés) — A switch-case újjászületése

A mintailesztés lehetővé teszi, hogy strukturált adatok szerkezetét ellenőrizzük és egyetlen lépésben kicsomagoljuk (destructuring) azokat. Ez rendkívül erős kifejezéssé teszi a `switch` kulcsszót.

### Destructuring (Adatok kibontása):
```dart
void printCoordinates((double, double) point) {
  // A rekord mezőit azonnal lokális változókba bontjuk ki:
  final (lat, lng) = point;
  print("Lat: $lat, Lng: $lng");
}
```

### Switch Kifejezések (Switch Expressions):
A Dart 3-ban a switch-nek van kifejezés formája is, amely értéket ad vissza:
```dart
String getButtonColor(ButtonStatus status) {
  return switch (status) {
    ButtonStatus.active => 'blue',
    ButtonStatus.disabled => 'grey',
    ButtonStatus.loading => 'light-blue',
  };
}
```

### Összetett logikai minták:
```dart
String describeScore(int score) {
  return switch (score) {
    >= 90 => "Kiváló (A)",
    >= 80 && < 90 => "Jó (B)",
    >= 50 => "Átment (C)",
    _ => "Elégtelen (F)", // Default eset (wildcard)
  };
}
```

---

## 4. Új Osztálymódosítók (Class Modifiers)

A Dart 3 szigorúbb ellenőrzést tesz lehetővé a könyvtárak (library-k) határain átnyúló osztályöröklődés felett. Az új módosítók:

*   **`sealed`**: A lezárt osztályok. Csak az adott fájlban örökölhetőek. A fordító switch esetében ellenőrzi a teljességet (exhaustiveness checking) – ha nem fedtük le az összes alosztályt, fordítási hibát kapunk!
*   **`final`**: Az osztály örökölhető a saját fájljában, de kívülről nem származtatható le és nem implementálható.
*   **`interface`**: Az osztály kívülről csak implementálható (`implements`), de nem örökölhető (`extends`).
*   **`base`**: Az osztály csak kiterjeszthető (`extends`), de nem implementálható.

### A `sealed` osztályok és a switch kombinációja:
```dart
sealed class NetworkState {}
class Loading extends NetworkState {}
class Success extends NetworkState { final String data; Success(this.data); }
class Failure extends NetworkState { final String error; Failure(this.error); }

Widget buildState(NetworkState state) {
  // A fordító ellenőrzi, hogy mind a három ágat lefedtük-e!
  return switch (state) {
    Loading() => const CircularProgressIndicator(),
    Success(data: var content) => Text("Adat: $content"),
    Failure(error: var msg) => Text("Hiba: $msg"),
  };
}
```

---

## Összegzés

A Dart 3.0 nem csupán egy ráncfelvarrás, hanem egy komoly szintlépés, amely a modern funkcionális programozási nyelvek szintjére emeli a Dartot. A rekordok és a mintailesztés segítségével sokkal kevesebb "boilerplate" kódot kell írnunk, a sealed osztályok pedig biztonságosabbá és tisztábbá teszik az állapotkezelésünket a Flutter alkalmazásokban.

> [!TIP]
> Kezdd el használni a switch kifejezéseket és a rekordokat a következő mini projektedben! Meg fogsz lepődni, mennyivel tömörebb és olvashatóbb será a kódod.
