# 1. hét — Fejlesztői környezet és Dart alapok

Üdvözöllek az első héten! Ebben a fejezetben lefektetjük a mobilfejlesztés technikai alapjait. Megértjük, mi az a Flutter és a Dart, telepítjük a szükséges fejlesztőeszközöket, teszteljük a környezetünket, és elmerülünk a Dart programozási nyelv alapjaiban. A fejezet végén egy teljesen működőképes, konzolos Kosár Kalkulátor mini-projektet fogunk megírni.

---

## 📘 1.1 Flutter és Dart fogalmak

Mielőtt kódot írnánk, tisztázzuk a technológiai stóc elemeit és a legfontosabb fogalmakat.

* **Flutter SDK:** A Google által fejlesztett nyílt forrású szoftverfejlesztő készlet (UI Software Development Kit). Nem egy különálló programozási nyelv, hanem egy keretrendszer (framework) és eszköztár, amely lehetővé teszi, hogy egyetlen kódbázisból fordítsunk natív gépi kódot Android, iOS, Web, macOS, Windows és Linux platformokra.
* **Dart SDK:** A Google által kifejlesztett, kliensoldali fejlesztésre optimalizált, típusbiztos programozási nyelv. A Flutter a Dart nyelvet használja az alkalmazások üzleti logikájának és felületének megírásához. A Dart SDK tartalmazza a fordítót, a virtuális gépet (VM) és a futtatókörnyezetet.
* **Widget:** A Flutterben a UI (felhasználói felület) építőkövei. Flutterben **minden egy widget**: a gombok, a szövegek, a beviteli mezők, de még az elrendezést szabályozó elemek (mint a margók, igazítások, rácsok) is widgetek formájában jelennek meg. A widgetek egy hierarchikus fát alkotnak.
* **Hot Reload vs. Hot Restart:** 
  * **Hot Reload:** A módosított kód másodpercek töredéke alatt betöltődik a futó Dart virtuális gépbe anélkül, hogy az alkalmazás elveszítené az aktuális állapotát (pl. beírt adatok, megnyitott menük megmaradnak).
  * **Hot Restart:** Újraindítja a teljes alkalmazást és törli az állapotot, visszaállítva a kezdőképernyőt, de még mindig sokkal gyorsabb, mint egy teljes újrafordítás.
* **Material Design és Cupertino widgetek:** A Flutter beépített widget-csomagjai. A Material Design a Google vizuális formanyelve, míg a Cupertino az Apple iOS stílusú vizuális elemeit adja a kezünkbe.
* **pub.dev:** A Dart és Flutter hivatalos csomagkezelő portálja, ahonnan mások által írt külső könyvtárakat (pl. adatbázis-kezelő, hálózati kliens, animációs csomagok) tudunk letölteni a saját projektünkhöz.

---

## 🛠️ 1.2 A fejlesztői környezet kialakítása

A fejlesztés megkezdéséhez az alábbi szoftverek telepítése szükséges.

### 💻 Szükséges eszközök és lépések
1. **Flutter SDK:** Töltsd le a hivatalos oldalkról a rendszerednek megfelelő verziót. Csomagold ki egy stabil helyre (pl. Windows-on `C:\src\flutter`, macOS/Linux-on pedig a home mappád alá). Add hozzá a `flutter/bin` mappát a rendszered elérési útjához (**PATH** környezeti változó).
2. **Git:** Szükséges a verziókezeléshez és a Flutter belső működéséhez.
3. **Android Studio és Android SDK:** Telepítsd az Android Studio-t. A telepítő varázslón keresztül töltsd le az Android SDK-t, SDK command-line tools-t és az emulátor eszközöket.
4. **Java Development Kit (JDK):** Az Android Studio beépítve tartalmazza, de érdemes megbizonyosodni róla, hogy a Java környezet helyesen van beállítva.
5. **Kódszerkesztő (IDE):** Használhatod a **VS Code**-ot (könnyebb, gyorsabb) vagy az **Android Studio**-t. Mindkét esetben telepítsd a **Flutter** és **Dart** bővítményeket (plugins).

---

## 🔍 1.3 Környezet ellenőrzése és első projekt

A terminálban az alábbi parancsokkal tudod ellenőrizni, hogy minden sikeresen települt-e:

```bash
# Részletes diagnosztikai jelentés futtatása
flutter doctor
```
*Ha a `flutter doctor` valahol hibát vagy hiányosságot jelez (pl. nem fogadott Android licencek), kövesd a terminálban kiírt instrukciókat (pl. `flutter doctor --android-licenses`).*

További hasznos parancsok:
```bash
# Flutter és Dart verzió lekérdezése
flutter --version
dart --version

# Elérhető futtatóeszközök (emulátorok, csatlakoztatott telefonok) listázása
flutter devices
```

### 🚀 Az első projekt létrehozása és futtatása
Navigálj abba a mappába, ahol a projektjeidet tárolod, majd futtasd a következő parancsokat a terminálban:

```bash
# Új Flutter projekt létrehozása
flutter create hello_flutter

# Belépés a projekt mappájába
cd hello_flutter

# Alkalmazás indítása a kiválasztott eszközön
flutter run
```

---

## 💻 1.4 Dart nyelv mély elmélete és alapjai

A Dart egy modern, objektumorientált nyelv, amely nagyban hasonlít a Java-ra, a C#-ra és a TypeScript-re. Vegyük sorra a nyelv építőelemeit.

### 📌 1. Változók és Konstansok (`var`, `final`, `const`)
A Dart statikusan típusos nyelv, de képes a típus kikövetkeztetésére (`type inference`).

```dart
// 1. var: A Dart kitalálja a típust (itt String), de a típus utána már nem módosítható.
var nev = 'Péter'; 
// nev = 42; // HIBÁS! Nem változtatható a típusa egész számmá.

// Explicit típusmegadás:
String varos = 'Budapest';
int kor = 28;

// 2. final: Futásidőben meghatározott konstans. Egyszer kaphat értéket, utána nem módosítható.
final mostaniIdo = DateTime.now(); // Csak futás közben derül ki a pontos idő.

// 3. const: Fordítási időben meghatározott konstans. Az értéke már a kód fordításakor ismert kell legyen.
const pi = 3.14159;
// const mikor = DateTime.now(); // HIBÁS! Mert a DateTime.now() futásidejű érték.
```

### 🔢 2. Primitív Típusok
* **`int`**: Egész számok (pl. `1`, `42`, `-10`).
* **`double`**: Lebegőpontos tizedes törtek (pl. `3.14`, `-0.5`).
* **`num`**: A számok közös őse. Tárolhat egész és tizedes számot is.
* **`String`**: Karakterlánc (pl. `'Szia'`, `"Dart"`). Támogatja a string interpolációt: `'$kor éves vagyok'` vagy `'Összeg: ${a + b}'`.
* **`bool`**: Logikai érték (`true` vagy `false`).

### 📦 3. Kollekciók (`List`, `Map`, `Set`)
* **`List` (Lista):** Rendezett gyűjtemény, amely engedélyezi a duplikációkat.
  ```dart
  List<String> nevek = ['Anna', 'Béla', 'Anna'];
  nevek.add('Dávid');
  print(nevek[0]); // Anna
  ```
* **`Set` (Halmaz):** Rendezetlen, egyedi elemekből álló gyűjtemény. Nem tartalmazhat duplikált elemet.
  ```dart
  Set<int> szamok = {1, 2, 3, 1}; // A duplikált '1' automatikusan kiszűrődik.
  print(szamok.length); // 3
  ```
* **`Map` (Szótár / Kulcs-Érték pár):** Kulcsok és értékek összerendelése. A kulcsok egyediek.
  ```dart
  Map<String, double> arak = {
    'alma': 350.0,
    'banan': 480.0,
  };
  print(arak['alma']); // 350.0
  ```

### ⚙️ 4. Függvények és Paraméterezés
Dartban a függvények visszatérési típussal rendelkeznek. Támogatják a normál pozicionális, valamint az opcionális és nevesített paramétereket.

```dart
// 1. Pozicionális paraméterek
int osszead(int a, int b) {
  return a + b;
}

// Arrow syntax (nyíl szintaxis) rövid függvényekhez:
int kivon(int a, int b) => a - b;

// 2. Opcionális pozicionális paraméterek (szögletes zárójelben, alapértelmezett értékkel)
String koszont(String nev, [String titulus = '']) {
  return 'Üdvözlöm $titulus $nev';
}

// 3. Nevesített paraméterek (kapcsos zárójelben)
// A 'required' kulcsszó kötelezővé teszi a paraméter átadását.
void beallitasok({required String tema, bool ertesitesek = true}) {
  print('Téma: $tema, Értesítések: $ertesitesek');
}

// Hívása:
// beallitasok(tema: 'Sötét', ertesitesek: false);
```

### 🔒 5. Null Safety (Nullabiztonság)
A Dart nyelv **Sound Null Safety** rendszert használ. Alapértelmezetten minden típus nem-nullázható (`non-nullable`), azaz nem tartalmazhat `null` értéket, hacsak azt külön nem jelezzük.

```dart
int kor = 30; // Nem lehet null.
// kor = null; // HIBÁS!

int? opcionalisKor; // A típus utáni kérdőjel (?) jelzi, hogy lehet null az értéke.
opcionalisKor = null; // Helyes.

// Null-aware operátorok:
// 1. ?. (Null-feltételes elérés): Ha a változó null, nullt ad vissza ahelyett, hogy elszállna.
print(opcionalisKor?.toString()); 

// 2. ?? (Null-koaleszkáló / Alapértelmezett érték): Ha a bal oldal null, a jobb oldali érték érvényesül.
int felhasznaltKor = opcionalisKor ?? 18; 

// 3. ! (Null assertion / kényszerítés): Megígérjük a fordítónak, hogy az érték biztosan nem null. Óvatosan használd!
int biztosNemNull = opcionalisKor!; 

// 4. late kulcsszó: Későbbi inicializáció ígérete.
late String bejelentkezettUser;
void login() {
  bejelentkezettUser = 'Gábor';
}
```

### 🏢 6. Objektumorientált Programozás (OOP)
A Dart osztályalapú nyelv. Kiválóan támogatja az encapsulation, inheritance és polymorphism elveit.

```dart
class Auto {
  // Mezők (tulajdonságok)
  final String marka;
  final String modell;
  int _kilometerora = 0; // A név eleji aláhúzás (_) privát láthatóságot jelent a fájlon kívül.

  // 1. Alapértelmezett konstruktor (szintaktikai cukorka)
  Auto(this.marka, this.modell);

  // 2. Nevesített konstruktor (Named Constructor)
  Auto.elektromos(String marka) : this(marka, 'EV-Pro');

  // Inicializációs lista (kód futtatása a konstruktortest előtt)
  Auto.hasznalt(this.marka, this.modell, int km) : assert(km >= 0) {
    _kilometerora = km;
  }

  // Getter
  int get futottKm => _kilometerora;

  // Metódus
  void utazik(int tavolsag) {
    if (tavolsag > 0) {
      _kilometerora += tavolsag;
    }
  }
}
```

#### Konstruktor fajták összefoglalása:
* **Generative Constructor:** Létrehozza a példányt és inicializálja a mezőket (`Auto(this.marka, this.modell)`).
* **Named Constructor:** Lehetővé teszi, hogy egy osztálynak több, különböző nevű konstruktora legyen (`Auto.elektromos(...)`).
* **Redirecting Constructor:** Egy konstruktor átirányítja a hívást az osztály egy másik konstruktorára.
* **Const Constructor:** Ha az osztály minden mezője `final`, a konstruktor elé írható a `const` szó. Így fordítási időben optimalizált, azonos memóriacímen osztozó objektumok hozhatók létre.
* **Factory Constructor:** A `factory` kulcsszóval ellátott konstruktor nem feltétlenül hoz létre új példányt. Visszaadhat egy már meglévő példányt a memóriából (Cache) vagy egy alosztály példányát is.

### 🏷️ 7. Enums (Felsorolás típusok)
A Dart támogatja az alapvető és az úgynevezett továbbfejlesztett (**Enhanced Enums**) típusokat is, amelyekhez saját mezők, metódusok és konstruktorok rendelhetők.

```dart
// Enhanced Enum példa
enum FizetesiMod {
  keszpenz('Készpénz', 0),
  bankkartya('Bankkártya', 1.5),
  utalás('Banki Utalás', 0.5);

  final String nev;
  final double tranzakciosDijSzazalek;

  // Konstruktor az enumnak
  const FizetesiMod(this.nev, this.tranzakciosDijSzazalek);

  // Metódus az enumban
  double tranzakciosDij(double vegosszeg) {
    return vegosszeg * (tranzakciosDijSzazalek / 100);
  }
}
```

### 📄 8. Records (Dart 3+)
A **Record** egy név nélküli, könnyűsúlyú kollekció típus, amellyel egyszerre több értéket is visszaadhatunk egy függvényből anélkül, hogy külön osztályt kellene létrehoznunk.

```dart
// Record létrehozása pozicionális és nevesített mezőkkel:
var user = ('János', age: 32, aktiv: true);

// Értékek elérése:
print(user.$1); // János (első pozicionális elem)
print(user.age); // 32 (nevesített elem)

// Visszatérési értékként függvényből:
(double, double) getKoordinatak() {
  return (47.4979, 19.0402);
}
```

### 🧩 9. Pattern Matching és Destructuring (Dart 3+)
A minták segítségével kényelmesen le tudjuk kérdezni és szét tudjuk bontani (destrukturálni) a bonyolultabb adatszerkezeteket.

```dart
// Destrukturálás (Értékek kicsomagolása egyből változókba)
final (szelesseg, hosszusag) = getKoordinatak();
print('Szélesség: $szelesseg, Hosszúság: $hosszusag');

// Pattern Matching Switch-ben
void ellenorizAllapot(Object adat) {
  switch (adat) {
    case [int a, int b]:
      print('Ez egy két egész számból álló lista: $a és $b');
      break;
    case (String nev, age: int kor):
      print('Ez egy felhasználó rekord. Név: $nev, Kor: $kor');
      break;
    default:
      print('Ismeretlen struktúra');
  }
}
```

---

## 📝 1.5 Gyakorlófeladatok és Megoldások

Az alábbiakban a fejezet gyakorlófeladatait és azok részletes, magyarázatokkal ellátott megoldásait láthatod.

### 1. Feladat: Kosár végösszeg kiszámítása
**Feladat:** Írj egy Dart programot, amely kiszámolja egy kosár végösszegét.
```dart
void main() {
  // Termékek és áraik listája
  List<double> kosarArak = [1200.0, 4500.0, 890.0, 3100.0];
  
  double vegosszeg = 0.0;
  for (var ar in kosarArak) {
    vegosszeg += ar;
  }
  
  print('A kosár végösszege: $vegosszeg Ft');
}
```

### 2. Feladat: `Product` osztály létrehozása
**Feladat:** Készíts `Product` osztályt névvel, árral és készlettel.
```dart
class Product {
  final String nev;
  final double ar;
  int keszlet;

  Product({
    required this.nev,
    required this.ar,
    required this.keszlet,
  });

  // Segédmetódus a kiíratáshoz
  void printInfo() {
    print('Termék: $nev | Ár: $ar Ft | Készleten: $keszlet db');
  }
}

void main() {
  var termek = Product(nev: 'Tej', ar: 450.0, keszlet: 12);
  termek.printInfo();
}
```

### 3. Feladat: `User` osztály opcionális telefonszámmal
**Feladat:** Készíts `User` osztályt opcionális telefonszámmal (Null Safety).
```dart
class User {
  final String nev;
  final String email;
  final String? telefonszam; // Lehet null az értéke

  User({
    required this.nev,
    required this.email,
    this.telefonszam, // Opcionális, nem kell required
  });

  void printUserDetail() {
    print('Név: $nev | Email: $email');
    if (telefonszam != null) {
      print('Telefonszám: $telefonszam');
    } else {
      print('Telefonszám: Nincs megadva');
    }
  }
}

void main() {
  var user1 = User(nev: 'Gábor', email: 'gabor@example.com');
  var user2 = User(nev: 'Kata', email: 'kata@example.com', telefonszam: '+36301234567');

  user1.printUserDetail();
  print('---');
  user2.printUserDetail();
}
```

### 4. Feladat: Termékek szűrése ár alapján
**Feladat:** Készíts listát termékekből, majd szűrd azokat, amelyek ára nagyobb mint 5000 Ft.
```dart
void main() {
  List<Product> termekek = [
    Product(nev: 'Fejhallgató', ar: 12000.0, keszlet: 5),
    Product(nev: 'Egérpad', ar: 2500.0, keszlet: 10),
    Product(nev: 'Billentyűzet', ar: 18500.0, keszlet: 3),
    Product(nev: 'USB Kábel', ar: 1500.0, keszlet: 20),
  ];

  // Szűrés a .where() metódus és lambda segítségével
  List<Product> dragaTermekek = termekek.where((t) => t.ar > 5000.0).toList();

  print('5000 Ft-nál drágább termékek:');
  for (var t in dragaTermekek) {
    print('- ${t.nev}: ${t.ar} Ft');
  }
}
```

### 5. Feladat: Kedvezményt számoló függvény
**Feladat:** Készíts függvényt, amely kedvezményt számol.
```dart
// A függvény elfogadja a végösszeget és a kedvezmény mértékét százalékban (alapértelmezetten 10%).
double kedvezmenySzamolo(double vegosszeg, {double szazalek = 10.0}) {
  if (vegosszeg < 0 || szazalek < 0 || szazalek > 100) {
    return vegosszeg; // Érvénytelen adatok esetén nincs kedvezmény
  }
  double kedvezmenyErteke = vegosszeg * (szazalek / 100);
  return vegosszeg - kedvezmenyErteke;
}

void main() {
  double eredetiAr = 10000.0;
  double akciotAr = kedvezmenySzamolo(eredetiAr, szazalek: 15.0);
  
  print('Eredeti ár: $eredetiAr Ft | Akciós ár: $akciotAr Ft');
}
```

---

## 🚀 1.6 Mini Projekt — Kosár kalkulátor konzolos Dartban

Most pedig mindezt összerakjuk egy teljesen működő, interaktív, konzolos Dart alkalmazásba. A program termékeket listáz, engedi a kosárba tételt, kezeli a mennyiségeket, alkalmazza a kedvezmény-kuponokat, kiszámítja az ÁFA-t (27%), és kezeli az érvénytelen bemeneteket.

Hozd létre a fájlt a gépeden `kosar_kalkulator.dart` néven, majd futtasd a `dart run kosar_kalkulator.dart` paranccsal!

```dart
import 'dart:io';

// 1. Termék osztály az áruk reprezentálására
class Termek {
  final String id;
  final String nev;
  final double egysegAr;
  int keszlet;

  Termek({
    required this.id,
    required this.nev,
    required this.egysegAr,
    required this.keszlet,
  });
}

// 2. Kosár elem osztály, ami összeköti a terméket a kosárba helyezett darabszámmal
class KosarElem {
  final Termek termek;
  int darabszam;

  KosarElem({required this.termek, required this.darabszam});

  double get reszosszeg => termek.egysegAr * darabszam;
}

// 3. Kosár osztály az üzleti logika kezelésére
class Kosar {
  final List<KosarElem> _elemek = [];
  double _kedvezmenySzazalek = 0.0;
  String? _alkalmazottKupon;

  List<KosarElem> get elemek => List.unmodifiable(_elemek);

  // Termék hozzáadása a kosárhoz
  bool termekHozzaadas(Termek termek, int db) {
    if (db <= 0) {
      print('⚠️ Hiba: A darabszámnak nagyobbnak kell lennie nullánál!');
      return false;
    }
    if (termek.keszlet < db) {
      print('⚠️ Hiba: Nincs elegendő készlet! Elérhető: ${termek.keszlet} db.');
      return false;
    }

    // Készlet csökkentése
    termek.keszlet -= db;

    // Megnézzük, benne van-e már a kosárban
    for (var elem in _elemek) {
      if (elem.termek.id == termek.id) {
        elem.darabszam += db;
        return true;
      }
    }

    // Ha nincs benne, új elemet adunk hozzá
    _elemek.add(KosarElem(termek: termek, darabszam: db));
    return true;
  }

  // Kupon érvényesítése
  bool kuponAlkalmaz(String kuponKod) {
    final tisztaKod = kuponKod.trim().toUpperCase();
    if (tisztaKod == 'PROMO10') {
      _kedvezmenySzazalek = 10.0;
      _alkalmazottKupon = 'PROMO10';
      return true;
    } else if (tisztaKod == 'SUPER20') {
      _kedvezmenySzazalek = 20.0;
      _alkalmazottKupon = 'SUPER20';
      return true;
    }
    return false;
  }

  // Számítások
  double get nettoReszosszeg {
    double osszeg = 0.0;
    for (var elem in _elemek) {
      osszeg += elem.reszosszeg;
    }
    return osszeg;
  }

  double get kedvezmenyErtek => nettoReszosszeg * (_kedvezmenySzazalek / 100);

  double get kedvezmenyesNetto => nettoReszosszeg - kedvezmenyErtek;

  // 27%-os ÁFA tartalom
  double get afaErtek => kedvezmenyesNetto * 0.27;

  double get fizetendoVegosszeg => kedvezmenyesNetto + afaErtek;

  void kosarUrites() {
    // Visszatöltjük a készletet
    for (var elem in _elemek) {
      elem.termek.keszlet += elem.darabszam;
    }
    _elemek.clear();
    _kedvezmenySzazalek = 0.0;
    _alkalmazottKupon = null;
  }

  // Nyugta / Összegzés kiírása
  void nyugtaNyomtatas() {
    if (_elemek.isEmpty) {
      print('\nA kosarad üres.');
      return;
    }

    print('\n================== NYUGTA ==================');
    for (var elem in _elemek) {
      print('${elem.termek.nev.padRight(18)} ${elem.darabszam} db x ${elem.termek.egysegAr.toStringAsFixed(0)} Ft = ${elem.reszosszeg.toStringAsFixed(0)} Ft');
    }
    print('--------------------------------------------');
    print('Nettó részösszeg:         ${nettoReszosszeg.toStringAsFixed(0)} Ft');
    if (_kedvezmenySzazalek > 0) {
      print('Kedvezmény ($_alkalmazottKupon):      -${kedvezmenyErtek.toStringAsFixed(0)} Ft (${_kedvezmenySzazalek.toStringAsFixed(0)}%)');
      print('Kedvezményes nettó:       ${kedvezmenyesNetto.toStringAsFixed(0)} Ft');
    }
    print('ÁFA (27%):                 ${afaErtek.toStringAsFixed(0)} Ft');
    print('============================================');
    print('Fizetendő végösszeg:      ${fizetendoVegosszeg.toStringAsFixed(0)} Ft');
    print('============================================');
  }
}

void main() {
  // Statikus termékkínálat inicializálása
  List<Termek> boltKinalat = [
    Termek(id: '1', nev: 'Kávé (szemes)', egysegAr: 2490.0, keszlet: 15),
    Termek(id: '2', nev: 'Tej 2.8%', egysegAr: 420.0, keszlet: 50),
    Termek(id: '3', nev: 'Kenyér (kovászos)', egysegAr: 850.0, keszlet: 8),
    Termek(id: '4', nev: 'Étcsokoládé 70%', egysegAr: 690.0, keszlet: 30),
  ];

  final kosar = Kosar();
  bool fut = true;

  print('🛒 ÜDVÖZÖLLEK A PRSTART DART KOSÁR KALKULÁTORBAN! 🛒');

  while (fut) {
    print('\n--- MENÜ ---');
    print('1. Bolt kínálatának megtekintése');
    print('2. Termék kosárba tétele');
    print('3. Kosár megtekintése és nyugta');
    print('4. Kedvezmény kupon megadása');
    print('5. Kosár kiürítése');
    print('6. Fizetés és Kilépés');
    stdout.write('Kérem válasszon menüpontot (1-6): ');

    final bemenet = stdin.readLineSync();

    switch (bemenet) {
      case '1':
        print('\n--- BOLT KÍNÁLATA ---');
        for (var termek in boltKinalat) {
          print('[ID: ${termek.id}] ${termek.nev.padRight(20)} | Ár: ${termek.egysegAr.toStringAsFixed(0)} Ft | Készlet: ${termek.keszlet} db');
        }
        break;

      case '2':
        print('\n--- TERMÉK KOSÁRBA HELYEZÉSE ---');
        stdout.write('Adja meg a termék ID-ját: ');
        final idInput = stdin.readLineSync();
        
        // Keresés
        final termek = boltKinalat.firstWhere(
          (t) => t.id == idInput, 
          orElse: () => Termek(id: '0', nev: '', egysegAr: 0.0, keszlet: 0)
        );

        if (termek.id == '0') {
          print('⚠️ Hiba: Nincs ilyen termék ID!');
          break;
        }

        stdout.write('Adja meg a darabszámot: ');
        final dbInput = stdin.readLineSync();
        final db = int.tryParse(dbInput ?? '');

        if (db == null) {
          print('⚠️ Hiba: Kérjük, érvényes egész számot adjon meg!');
          break;
        }

        final siker = kosar.termekHozzaadas(termek, db);
        if (siker) {
          print('✅ A(z) ${termek.nev} (${db} db) sikeresen bekerült a kosárba.');
        }
        break;

      case '3':
        kosar.nyugtaNyomtatas();
        break;

      case '4':
        print('\n--- KUPON KÓD ALKALMAZÁSA ---');
        print('Elérhető kuponok teszteléshez: PROMO10 (10%), SUPER20 (20%)');
        stdout.write('Írja be a kuponkódot: ');
        final kuponKod = stdin.readLineSync();

        if (kuponKod == null || kuponKod.trim().isEmpty) {
          print('⚠️ Hiba: Nem adott meg kuponkódot!');
          break;
        }

        final kuponSiker = kosar.kuponAlkalmaz(kuponKod);
        if (kuponSiker) {
          print('✅ Kupon sikeresen elfogadva! Kedvezmény érvényesítve.');
        } else {
          print('⚠️ Hiba: Érvénytelen vagy lejárt kuponkód!');
        }
        break;

      case '5':
        kosar.kosarUrites();
        print('✅ A kosár teljesen kiürítve. Készletek visszaállítva.');
        break;

      case '6':
        if (kosar.elemek.isNotEmpty) {
          print('\nKöszönjük a vásárlást!');
          kosar.nyugtaNyomtatas();
        } else {
          print('\nKöszönjük az érdeklődést. Viszontlátásra!');
        }
        fut = false;
        break;

      default:
        print('⚠️ Érvénytelen menüpont! Kérjük, 1 és 6 közötti számot válasszon.');
    }
  }
}
```

---

## ❓ 1.7 Heti ellenőrző kérdések

### 1. Mi a különbség a `final` és a `const` között?
* **`final`**: Futásidőben meghatározott állandó (runtime constant). Értékét csak egyszer lehet megadni, de ez az érték kiszámítható a program futása során is (pl. a pontos idő leolvasása, vagy egy API-ból érkező adat).
* **`const`**: Fordítási időben meghatározott állandó (compile-time constant). Az értékének már a kód lefordításakor pontosan ismertnek kell lennie (pl. `const pi = 3.14`). A `const` objektumok memóriatakarékosak, mert a megegyező értékű konstansok ugyanazon a fizikai memóriacímen osztoznak.

### 2. Mit jelent a null safety?
A **Null Safety** (nullabiztonság) megvédi az alkalmazást a futás közben fellépő null-pointer hibáktól (amikor egy nem létező objektum metódusát vagy változóját próbáljuk elérni). Dartban alapértelmezetten minden típus nem-nullázható (`non-nullable`). Ha egy változónak engedélyezni akarjuk a `null` értéket, a típus után egy kérdőjelet kell tennünk (pl. `String? nev`). A fordítóprogram szigorúan ellenőrzi ezt, és nem engedi lefordítani a kódot, ha nem kezeltük biztonságosan a null-értékű eseteket.

### 3. Miért hasznosak a named (nevesített) paraméterek?
A nevesített paraméterek növelik a kód olvashatóságát és csökkentik a hibák lehetőségét, főleg sok paraméterrel rendelkező függvények és konstruktorok esetén. A hívó félnek nem kell emlékeznie a paraméterek pontos sorrendjére, mert név szerint hivatkozik rájuk (pl. `beallit(tema: 'Világos', hang: true)` ahelyett, hogy `beallit('Világos', true)`-t írna). Emellett tetszőlegesen elhagyhatóvá tehetők, vagy a `required` kulcsszóval kötelezővé tehetők.

### 4. Mikor használunk `List`, `Map`, `Set` típust?
* **`List`**: Ha az elemek **sorrendje** számít, és szeretnénk indexek alapján eléri őket (pl. `list[0]`), vagy ha előfordulhatnak duplikált elemek (pl. napi értékesítési tranzakciók árai).
* **`Set`**: Ha az elemek **egyedisége** a legfontosabb, és el akarjuk kerülni a duplikációkat, vagy gyorsan ellenőrizni akarjuk, hogy egy elem része-e a halmaznak (pl. egyedi felhasználói ID-k listája).
* **`Map`**: Ha az adatokat **párosítva** tároljuk (kulcs-érték), ahol egy egyedi kulcs alapján szeretnénk nagyon gyorsan megtalálni a hozzá tartozó értéket (pl. országkódok és országhatárok összerendelése).

### 5. Mi a különbség a hot reload és a hot restart között?
* **Hot Reload**: Feltölti a megváltozott kódcsomagot a futó alkalmazás VM-jébe (Virtual Machine), és újrarajzolja a widget fát. **Megtartja a jelenlegi állapotot** (`state`), így rendkívül gyors (~100-300 ms), és ideális UI finomhangolásra.
* **Hot Restart**: Feltölti a kódot, de **megsemmisíti az alkalmazás belső állapotát**, majd elölről indítja a teljes programot és a `main()` függvényt. Ezt akkor kell használni, ha globális változókat, inicializációs logikát vagy a konstruktorokat módosítottuk.
