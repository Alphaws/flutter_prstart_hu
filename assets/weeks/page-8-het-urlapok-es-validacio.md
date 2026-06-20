# 8. hét — Űrlapok és validáció

## Cél
A lecke célja, hogy elsajátítsd a professzionális felhasználói adatbevitel és validáció megvalósítását Flutterben. Megtanulod kezelni a billentyűzetet, fókuszpontokat váltani, reguláris kifejezésekkel (Regex) ellenőrizni az e-mail címeket és jelszavakat, valamint megismered a különböző beviteli típusokat (Checkbox, Dropdown, DatePicker, ImagePicker). A hét végére képes leszel biztonságos, akadálymentes és látványos űrlapokat építeni.

---

## Elmélet

### 1. Beviteli mezők és a memóriakezelés (`TextEditingController`)
A Flutterben a legegyszerűbb szövegbevitelre a `TextField`, űrlapokba ágyazva pedig a `TextFormField` widgetet használjuk. A mezőben lévő szöveg olvasására, írására és figyelésére a `TextEditingController` szolgál.

**FONTOS:** A `TextEditingController` natív erőforrásokat és listenereket regisztrál a háttérben. Ha a widget kikerül a widget-fából, de a kontrollert nem semmisítjük meg, az **Memory Leak-et (memóriaszivárgást)** okoz. Ezért a kontrollereket **mindig** meg kell semmisíteni a `StatefulWidget` `dispose()` metódusában:

```dart
@override
void dispose() {
  _myController.dispose(); // Kötelező lépés!
  super.dispose();
}
```

### 2. A `Form` és a `GlobalKey<FormState>`
Több mezőből álló űrlapok esetén nem érdemes minden egyes mezőt külön kontrollerrel vizsgálni a validációhoz. Ehelyett a mezőket egy `Form` widgetbe csomagoljuk.

A `Form` működését egy `GlobalKey<FormState>` segítségével vezéreljük az UI kódból. Ez a kulcs egyedi azonosítót biztosít az űrlap állapotához, így elérhetjük az alatta lévő összes `TextFormField` állapotát egyszerre:
*   `formKey.currentState!.validate()`: Lefuttatja az összes mezőhöz tartozó `validator` függvényt. Ha mindegyik `null`-t ad vissza, az űrlap érvényes (true), egyébként érvénytelen (false).
*   `formKey.currentState!.save()`: Lefuttatja az összes mezőhöz tartozó `onSaved` callbacket (hasznos az adatok egyben történő kimentéséhez).
*   `formKey.currentState!.reset()`: Alaphelyzetbe állítja az összes mezőt.

### 3. Validációs stratégiák (AutovalidateMode)
A Flutter háromféle módot kínál a validáció időzítésére az `AutovalidateMode` enumon keresztül:
1.  `disabled` (alapértelmezett): Csak akkor validál, ha a kódból explicit meghívjuk a `validate()` metódust (pl. gombnyomásra).
2.  `always`: Folyamatosan validál, már a képernyő megjelenésekor is (rossz UX, mert azonnal hibát jelez, mielőtt a felhasználó gépelni kezdene).
3.  `onUserInteraction`: Csak akkor kezdi el ellenőrizni a mezőt, miután a felhasználó már elkezdett gépelni benne. Ez nyújtja a legjobb felhasználói élményt (UX).

### 4. Akadálymentesítés és kód-UX (Fókusz és billentyűzet akciók)
Egy profi mobilalkalmazásban a felhasználónak nem kell manuálisan kattintgatnia a következő mezőre.
*   **TextInputAction:** Beállítható, hogy mi jelenjen meg a mobil billentyűzet sarkában (pl. `TextInputAction.next` a "Következő" gombhoz, vagy `TextInputAction.done` a "Kész"-hez).
*   **FocusScope:** A `FocusScope.of(context).nextFocus()` hívással a fókusz automatikusan átugrik a következő beviteli mezőre a képernyőn.

---

## Kódpéldák

### 1. Alapvető Form és GlobalKey deklaráció
Így épül fel egy minimális, működő űrlap struktúra:

```dart
import 'package:flutter/material.dart';

class SimpleFormPage extends StatefulWidget {
  const SimpleFormPage({super.key});

  @override
  State<SimpleFormPage> createState() => _SimpleFormPageState();
}

class _SimpleFormPageState extends State<SimpleFormPage> {
  // 1. Deklaráljuk a Form kulcsát
  final _formKey = GlobalKey<FormState>();
  String _userName = '';

  void _submitForm() {
    // 2. Ellenőrizzük a validációt gombnyomáskor
    if (_formKey.currentState!.validate()) {
      // 3. Ha sikeres, kimentjük az adatokat
      _formKey.currentState!.save();
      
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Sikeres mentés: $_userName')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Alap Form')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Form(
          key: _formKey, // 4. Hozzárendeljük a kulcsot
          child: Column(
            children: [
              TextFormField(
                decoration: const InputDecoration(labelText: 'Felhasználónév'),
                // Validátor logika
                validator: (value) {
                  if (value == null || value.trim().isEmpty) {
                    return 'A név nem lehet üres!';
                  }
                  return null; // Nincs hiba
                },
                onSaved: (value) {
                  _userName = value ?? '';
                },
              ),
              const SizedBox(height: 20),
              ElevatedButton(
                onPressed: _submitForm,
                child: const Text('Küldés'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
```

### 2. Komplex E-mail és Jelszó validátor reguláris kifejezéssel
A professzionális adatszűréshez reguláris kifejezéseket (Regex) használunk.

```dart
class Validators {
  // Hivatalos email regex minta
  static final RegExp _emailRegExp = RegExp(
    r"^[a-zA-Z0-9.a-zA-Z0-9.!#$%&'*+-/=?^_`{|}~]+@[a-zA-Z0-9]+\.[a-zA-Z]+",
  );

  static String? validateEmail(String? value) {
    if (value == null || value.trim().isEmpty) {
      return 'Az e-mail cím megadása kötelező!';
    }
    if (!_emailRegExp.hasMatch(value)) {
      return 'Kérjük, érvényes e-mail címet adj meg!';
    }
    return null;
  }

  static String? validatePassword(String? value) {
    if (value == null || value.isEmpty) {
      return 'A jelszó megadása kötelező!';
    }
    if (value.length < 8) {
      return 'A jelszónak legalább 8 karakterből kell állnia!';
    }
    if (!value.contains(RegExp(r'[A-Z]'))) {
      return 'Tartalmaznia kell legalább egy nagybetűt!';
    }
    if (!value.contains(RegExp(r'[0-9]'))) {
      return 'Tartalmaznia kell legalább egy számot!';
    }
    return null;
  }
}
```

### 3. Regisztrációs Form jelszó-megerősítéssel
Így hasonlítjuk össze a két jelszómezőt egymással. A megerősítő mező ellenőrzi a fő jelszómező kontrollerében tárolt értéket.

```dart
class RegisterFormWidget extends StatefulWidget {
  const RegisterFormWidget({super.key});

  @override
  State<RegisterFormWidget> createState() => _RegisterFormWidgetState();
}

class _RegisterFormWidgetState extends State<RegisterFormWidget> {
  final _formKey = GlobalKey<FormState>();
  final _passwordController = TextEditingController();
  final _confirmPasswordController = TextEditingController();

  @override
  void dispose() {
    _passwordController.dispose();
    _confirmPasswordController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Form(
      key: _formKey,
      autovalidateMode: AutovalidateMode.onUserInteraction,
      child: Column(
        children: [
          TextFormField(
            controller: _passwordController,
            decoration: const InputDecoration(labelText: 'Jelszó'),
            obscureText: true,
            validator: Validators.validatePassword,
          ),
          const SizedBox(height: 10),
          TextFormField(
            controller: _confirmPasswordController,
            decoration: const InputDecoration(labelText: 'Jelszó újra'),
            obscureText: true,
            validator: (value) {
              if (value == null || value.isEmpty) {
                return 'Kérjük, igazold vissza a jelszavadat!';
              }
              if (value != _passwordController.text) {
                return 'A két jelszó nem egyezik meg!';
              }
              return null;
            },
          ),
        ],
      ),
    );
  }
}
```

### 4. Checkbox és Dropdown elhelyezése Formon belül
A normál `Checkbox` és `DropdownButton` helyett formban érdemes a `FormField` változatukat használni, mert ezek rendelkeznek beépített validációval és hibaüzenet-megjelenítéssel.

```dart
// 1. Dropdown formon belül
DropdownButtonFormField<String>(
  decoration: const InputDecoration(labelText: 'Szakmai szint'),
  value: 'junior',
  items: const [
    DropdownMenuItem(value: 'junior', child: Text('Junior')),
    DropdownMenuItem(value: 'medior', child: Text('Medior')),
    DropdownMenuItem(value: 'senior', child: Text('Senior')),
  ],
  onChanged: (value) {
    print('Kiválasztva: $value');
  },
  validator: (value) {
    if (value == null) return 'Kérjük, válassz egy szintet!';
    return null;
  },
);

// 2. Checkbox FormField (ÁSZF elfogadáshoz, ahol kötelező a true érték)
FormField<bool>(
  initialValue: false,
  validator: (value) {
    if (value == null || value == false) {
      return 'A folytatáshoz el kell fogadnod az ÁSZF-et!';
    }
    return null;
  },
  builder: (formFieldState) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        CheckboxListTile(
          title: const Text('Elfogadom a felhasználási feltételeket'),
          value: formFieldState.value,
          onChanged: (newValue) {
            formFieldState.didChange(newValue); // Értesíti a FormField-et a változásról!
          },
          controlAffinity: ListTileControlAffinity.leading,
        ),
        if (formFieldState.hasError)
          Padding(
            padding: const EdgeInsets.only(left: 16.0, top: 4.0),
            child: Text(
              formFieldState.errorText!,
              style: const TextStyle(color: Colors.red, fontSize: 12),
            ),
          )
      ],
    );
  },
);
```

### 5. Profilkép feltöltés `image_picker` segítségével (Vázlat)
A csomag telepítése: `flutter pub add image_picker` (Androidon automatikusan működik, iOS esetén a `Info.plist`-be fel kell venni a kamerahasználati leírást!).

```dart
import 'dart:io';
import 'package:image_picker/image_picker.dart';

class ImageUploadHelper {
  final ImagePicker _picker = ImagePicker();

  Future<File?> pickImageFromGallery() async {
    try {
      final XFile? image = await _picker.pickImage(
        source: ImageSource.gallery,
        maxWidth: 800, // Méret optimalizálás
        imageQuality: 85, // Minőség csökkentése a sávszélesség miatt
      );

      if (image != null) {
        return File(image.path);
      }
      return null;
    } catch (e) {
      print('Hiba a képkiválasztás során: $e');
      return null;
    }
  }
}
```

---

## Gyakorlófeladatok & Megoldások

### 1. Feladat: Login Form validáció
Készíts egy bejelentkező űrlapot két mezővel (Email, Jelszó) és egy "Bejelentkezés" gombbal. Csak akkor engedélyezd a belépést, ha az e-mail formátuma helyes, és a jelszó legalább 6 karakter hosszú.

#### Megoldás:
```dart
import 'package:flutter/material.dart';

class SimpleLoginPage extends StatefulWidget {
  const SimpleLoginPage({super.key});

  @override
  State<SimpleLoginPage> createState() => _SimpleLoginPageState();
}

class _SimpleLoginPageState extends State<SimpleLoginPage> {
  final _formKey = GlobalKey<FormState>();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Bejelentkezés')),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Form(
          key: _formKey,
          child: Column(
            children: [
              TextFormField(
                decoration: const InputDecoration(labelText: 'E-mail cím'),
                keyboardType: TextInputType.emailAddress,
                validator: (value) {
                  if (value == null || !value.contains('@')) {
                    return 'Hibás e-mail cím formátum!';
                  }
                  return null;
                },
              ),
              TextFormField(
                decoration: const InputDecoration(labelText: 'Jelszó'),
                obscureText: true,
                validator: (value) {
                  if (value == null || value.length < 6) {
                    return 'A jelszónak legalább 6 karakteresnek kell lennie!';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 20),
              ElevatedButton(
                onPressed: () {
                  if (_formKey.currentState!.validate()) {
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(content: Text('Belépés folyamatban...')),
                    );
                  }
                },
                child: const Text('Bejelentkezés'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
```

### 2. Feladat: Regisztráció ÁSZF-el és Jelszó-ellenőrzéssel
Egészítsd ki a korábbi regisztrációs példát egy Checkbox-szal. A regisztrációs gomb megnyomásakor a program ellenőrizze, hogy a jelszavak megegyeznek-e, és a felhasználó bejelölte-e az ÁSZF-et.

#### Megoldás:
```dart
// A megoldást a lenti Heti Mini Projekt tartalmazza teljesen kifejtve.
```

### 3. Feladat: Profil szerkesztő "Módosult az adat" gomb aktiválással
Készíts egy profil szerkesztő oldalt (Név mezővel). A "Mentés" gomb legyen inaktív (szürke, nem kattintható) mindaddig, amíg a felhasználó meg nem változtatja a mező értékét az eredeti névhez képest!

#### Megoldás:
```dart
import 'package:flutter/material.dart';

class ProfileEditPage extends StatefulWidget {
  const ProfileEditPage({super.key});

  @override
  State<ProfileEditPage> createState() => _ProfileEditPageState();
}

class _ProfileEditPageState extends State<ProfileEditPage> {
  static const String _originalName = 'Kovács János';
  late final TextEditingController _nameController;
  bool _isModified = false;

  @override
  void initState() {
    super.initState();
    _nameController = TextEditingController(text: _originalName);
    _nameController.addListener(_checkModification);
  }

  void _checkModification() {
    setState(() {
      _isModified = _nameController.text != _originalName;
    });
  }

  @override
  void dispose() {
    _nameController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Profil szerkesztése')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextField(
              controller: _nameController,
              decoration: const InputDecoration(labelText: 'Felhasználó Név'),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: _isModified 
                  ? () {
                      ScaffoldMessenger.of(context).showSnackBar(
                        const SnackBar(content: Text('Változások mentve!')),
                      );
                      // Mentés után az új név lesz az alapértelmezett
                      FocusScope.of(context).unfocus();
                    }
                  : null, // Inaktív állapot
              child: const Text('Mentés'),
            ),
          ],
        ),
      ),
    );
  }
}
```

### 4. Feladat: Új termék létrehozó Form
Írj egy űrlapot új termék felvételéhez. Mezők: termék neve (kötelező), termék ára (csak szám lehet, nagyobb mint 0), és egy dropdown a kategóriáknak (Elektronika, Ruha, Élelmiszer).

#### Megoldás:
```dart
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class CreateProductPage extends StatefulWidget {
  const CreateProductPage({super.key});

  @override
  State<CreateProductPage> createState() => _CreateProductPageState();
}

class _CreateProductPageState extends State<CreateProductPage> {
  final _formKey = GlobalKey<FormState>();
  final List<String> _categories = ['Elektronika', 'Ruha', 'Élelmiszer'];
  String? _selectedCategory;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Új termék létrehozása')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: Column(
            children: [
              TextFormField(
                decoration: const InputDecoration(labelText: 'Termék neve'),
                validator: (val) => (val == null || val.isEmpty) ? 'A név kötelező!' : null,
              ),
              TextFormField(
                decoration: const InputDecoration(labelText: 'Ár (Ft)'),
                keyboardType: TextInputType.number,
                // Csak számjegyeket engedélyezünk beírni!
                inputFormatters: [FilteringTextInputFormatter.digitsOnly],
                validator: (val) {
                  if (val == null || val.isEmpty) return 'Az ár megadása kötelező!';
                  final price = int.tryParse(val);
                  if (price == null || price <= 0) return 'Az árnak nagyobbnak kell lennie mint 0!';
                  return null;
                },
              ),
              DropdownButtonFormField<String>(
                decoration: const InputDecoration(labelText: 'Kategória'),
                value: _selectedCategory,
                items: _categories.map((cat) => DropdownMenuItem(value: cat, child: Text(cat))).toList(),
                onChanged: (val) => setState(() => _selectedCategory = val),
                validator: (val) => val == null ? 'Válassz kategóriát!' : null,
              ),
              const SizedBox(height: 20),
              ElevatedButton(
                onPressed: () {
                  if (_formKey.currentState!.validate()) {
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(content: Text('Termék létrehozva!')),
                    );
                  }
                },
                child: const Text('Termék hozzáadása'),
              )
            ],
          ),
        ),
      ),
    );
  }
}
```

### 5. Feladat: Egységes és dekoratív hiba-megjelenítés
Készíts egy szép input dekorációs témát (`InputDecorationTheme`), amelyet globálisan beállíthatsz a `ThemeData`-ban, hogy minden beviteli mező lekerekített szegéllyel rendelkezzen, hiba esetén pedig piros háttérrel és vastag piros szegéllyel villanjon fel.

#### Megoldás:
```dart
final customInputDecorationTheme = InputDecorationTheme(
  filled: true,
  fillColor: Colors.grey.shade100,
  contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 16),
  border: OutlineInputBorder(
    borderRadius: BorderRadius.circular(12),
    borderSide: BorderSide(color: Colors.grey.shade400),
  ),
  enabledBorder: OutlineInputBorder(
    borderRadius: BorderRadius.circular(12),
    borderSide: BorderSide(color: Colors.grey.shade300),
  ),
  focusedBorder: OutlineInputBorder(
    borderRadius: BorderRadius.circular(12),
    borderSide: const BorderSide(color: Colors.blue, width: 2),
  ),
  errorBorder: OutlineInputBorder(
    borderRadius: BorderRadius.circular(12),
    borderSide: const BorderSide(color: Colors.red, width: 2),
  ),
  focusedErrorBorder: OutlineInputBorder(
    borderRadius: BorderRadius.circular(12),
    borderSide: const BorderSide(color: Colors.red, width: 2.5),
  ),
  errorStyle: const TextStyle(fontWeight: FontWeight.bold, color: Colors.red),
);
```

---

## Heti Mini Projekt: Regisztrációs folyamat

Ebben a mini projektben egy komplett, három lépésből álló regisztrációs űrlapot készítünk el. Támogatja a jelszavak láthatóságának beállítását, a fókuszok automatikus átadását, a formátumellenőrzést, az ÁSZF kötelező kipipálását, és egy látványos siker-képernyőt.

### A teljes forráskód (`main.dart`):

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const RegisterApp());
}

class RegisterApp extends StatelessWidget {
  const RegisterApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'PrStart Regisztráció',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.indigo),
        useMaterial3: true,
        // Alkalmazzuk az egységes dizájnt a mezőkre
        inputDecorationTheme: InputDecorationTheme(
          filled: true,
          fillColor: Colors.indigo.shade50.withOpacity(0.3),
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(12),
          ),
        ),
      ),
      home: const RegisterScreen(),
    );
  }
}

class RegisterScreen extends StatefulWidget {
  const RegisterScreen({super.key});

  @override
  State<RegisterScreen> createState() => _RegisterScreenState();
}

class _RegisterScreenState extends State<RegisterScreen> {
  final _formKey = GlobalKey<FormState>();
  
  // Kontrollerek
  final _nameController = TextEditingController();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  final _confirmPasswordController = TextEditingController();

  // Fókusz csomópontok a zökkenőmentes navigációhoz
  final _nameFocus = FocusNode();
  final _emailFocus = FocusNode();
  final _passwordFocus = FocusNode();
  final _confirmPasswordFocus = FocusNode();

  // Állapotváltozók
  bool _obscurePassword = true;
  bool _obscureConfirmPassword = true;
  String? _selectedAgeGroup;
  bool _acceptTerms = false;

  final List<String> _ageGroups = ['18-25', '26-35', '36-50', '50 felett'];

  @override
  void dispose() {
    _nameController.dispose();
    _emailController.dispose();
    _passwordController.dispose();
    _confirmPasswordController.dispose();
    _nameFocus.dispose();
    _emailFocus.dispose();
    _passwordFocus.dispose();
    _confirmPasswordFocus.dispose();
    super.dispose();
  }

  void _submitRegistration() {
    if (_formKey.currentState!.validate()) {
      // Sikeres regisztráció -> Átirányítás a siker oldalra
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(
          builder: (context) => SuccessScreen(userName: _nameController.text),
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('PrStart Regisztráció'),
        centerTitle: true,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20.0),
        child: Form(
          key: _formKey,
          autovalidateMode: AutovalidateMode.onUserInteraction,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const Text(
                'Csatlakozz a fejlesztői kurzushoz!',
                style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 25),
              
              // 1. Teljes név mező
              TextFormField(
                controller: _nameController,
                focusNode: _nameFocus,
                textInputAction: TextInputAction.next,
                decoration: const InputDecoration(
                  labelText: 'Teljes név',
                  prefixIcon: Icon(Icons.person),
                ),
                validator: (val) => (val == null || val.trim().isEmpty) ? 'Kérjük, add meg a neved!' : null,
                onFieldSubmitted: (_) => FocusScope.of(context).requestFocus(_emailFocus),
              ),
              const SizedBox(height: 16),

              // 2. E-mail mező
              TextFormField(
                controller: _emailController,
                focusNode: _emailFocus,
                keyboardType: TextInputType.emailAddress,
                textInputAction: TextInputAction.next,
                decoration: const InputDecoration(
                  labelText: 'E-mail cím',
                  prefixIcon: Icon(Icons.email),
                ),
                validator: (val) {
                  if (val == null || val.trim().isEmpty) return 'Az e-mail kötelező!';
                  if (!val.contains('@') || !val.contains('.')) return 'Érvénytelen e-mail formátum!';
                  return null;
                },
                onFieldSubmitted: (_) => FocusScope.of(context).requestFocus(_passwordFocus),
              ),
              const SizedBox(height: 16),

              // 3. Jelszó mező szem ikonnal
              TextFormField(
                controller: _passwordController,
                focusNode: _passwordFocus,
                obscureText: _obscurePassword,
                textInputAction: TextInputAction.next,
                decoration: InputDecoration(
                  labelText: 'Jelszó',
                  prefixIcon: const Icon(Icons.lock),
                  suffixIcon: IconButton(
                    icon: Icon(_obscurePassword ? Icons.visibility_off : Icons.visibility),
                    onPressed: () => setState(() => _obscurePassword = !_obscurePassword),
                  ),
                ),
                validator: (val) {
                  if (val == null || val.isEmpty) return 'A jelszó kötelező!';
                  if (val.length < 8) return 'Legalább 8 karakter hosszúságú legyen!';
                  return null;
                },
                onFieldSubmitted: (_) => FocusScope.of(context).requestFocus(_confirmPasswordFocus),
              ),
              const SizedBox(height: 16),

              // 4. Jelszó megerősítés mező
              TextFormField(
                controller: _confirmPasswordController,
                focusNode: _confirmPasswordFocus,
                obscureText: _obscureConfirmPassword,
                textInputAction: TextInputAction.done,
                decoration: InputDecoration(
                  labelText: 'Jelszó megerősítése',
                  prefixIcon: const Icon(Icons.lock_outline),
                  suffixIcon: IconButton(
                    icon: Icon(_obscureConfirmPassword ? Icons.visibility_off : Icons.visibility),
                    onPressed: () => setState(() => _obscureConfirmPassword = !_obscureConfirmPassword),
                  ),
                ),
                validator: (val) {
                  if (val == null || val.isEmpty) return 'Kérjük, igazold vissza a jelszót!';
                  if (val != _passwordController.text) return 'A beírt jelszavak nem egyeznek!';
                  return null;
                },
              ),
              const SizedBox(height: 16),

              // 5. Korcsoport választó (Dropdown)
              DropdownButtonFormField<String>(
                decoration: const InputDecoration(
                  labelText: 'Korosztály',
                  prefixIcon: Icon(Icons.calendar_today),
                ),
                value: _selectedAgeGroup,
                items: _ageGroups.map((group) {
                  return DropdownMenuItem(value: group, child: Text(group));
                }).toList(),
                onChanged: (val) => setState(() => _selectedAgeGroup = val),
                validator: (val) => val == null ? 'Kérjük, válaszd ki a korosztályodat!' : null,
              ),
              const SizedBox(height: 16),

              // 6. ÁSZF elfogadás (Checkbox)
              FormField<bool>(
                initialValue: false,
                validator: (val) => (val == null || val == false) ? 'A regisztrációhoz el kell fogadnod a szabályzatot!' : null,
                builder: (fieldState) {
                  return Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      CheckboxListTile(
                        contentPadding: EdgeInsets.zero,
                        title: const Text('Elfogadom az Adatvédelmi Nyilatkozatot és az ÁSZF-et'),
                        value: _acceptTerms,
                        onChanged: (val) {
                          setState(() => _acceptTerms = val ?? false);
                          fieldState.didChange(val);
                        },
                        controlAffinity: ListTileControlAffinity.leading,
                      ),
                      if (fieldState.hasError)
                        Text(
                          fieldState.errorText!,
                          style: const TextStyle(color: Colors.red, fontSize: 12, fontWeight: FontWeight.bold),
                        ),
                    ],
                  );
                },
              ),
              const SizedBox(height: 25),

              // Regisztrációs gomb
              ElevatedButton(
                style: ElevatedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: 16),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                  backgroundColor: Colors.indigo,
                  foregroundColor: Colors.white,
                ),
                onPressed: _submitRegistration,
                child: const Text('Regisztráció véglegesítése', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

// 7. Sikeres regisztráció képernyő
class SuccessScreen extends StatelessWidget {
  final String userName;

  const SuccessScreen({super.key, required this.userName});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Icon(Icons.check_circle_outline, size: 100, color: Colors.green),
              const SizedBox(height: 24),
              const Text(
                'Sikeres regisztráció!',
                style: TextStyle(fontSize: 26, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 12),
              Text(
                'Kedves $userName, fiókod sikeresen elkészült. Üdvözlünk a PrStart közösségében!',
                textAlign: TextAlign.center,
                style: const TextStyle(fontSize: 16, color: Colors.black54),
              ),
              const SizedBox(height: 30),
              ElevatedButton(
                onPressed: () {
                  Navigator.pushReplacement(
                    context,
                    MaterialPageRoute(builder: (context) => const RegisterScreen()),
                  );
                },
                child: const Text('Vissza a kezdőlapra'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
```

---

## Heti Ellenőrző Kérdések

### 1. Miért kötelező meghívni a `dispose()` metódust a `TextEditingController` esetében?
A `TextEditingController` egy erőforrás-igényes objektum, ami belső csatornákat és eseményfigyelőket (listener) regisztrál a Flutter keretrendszer natív szintjén. Ha a hozzá tartozó StatefulWidget megsemmisül, de a kontrollert nem engedjük el a `dispose()` hívással, a szemétgyűjtő (Garbage Collector) nem tudja felszabadítani a hozzá tartozó memóriaterületet, ami **memóriaszivárgást** (Memory Leak) okoz. Emiatt az alkalmazás idővel lelassulhat és összeomolhat.

### 2. Mi a szerepe a `GlobalKey<FormState>`-nek az űrlapkezelésben?
A `GlobalKey<FormState>` egy globálisan egyedi azonosító, amely közvetlen hozzáférést biztosít a `Form` widget mögöttes állapotához (`FormState`). Ezen a kulcson keresztül tudjuk egyetlen utasítással lekérdezni és validálni az összes benne lévő `TextFormField` állapotát (`currentState!.validate()`), elmenteni az adatokat a mezőkhöz csatolt `onSaved` metódusok meghívásával, vagy teljesen alaphelyzetbe állítani a beviteli mezőket (`currentState!.reset()`).

### 3. Mi a különbség az `AutovalidateMode.always` és az `AutovalidateMode.onUserInteraction` között?
Az `AutovalidateMode.always` folyamatosan validálja az űrlap mezőit, beleértve azt a pillanatot is, amikor az űrlap először kirajzolódik a képernyőn. Ez nagyon rossz felhasználói élményt okoz, mert a felhasználó azonnal piros hibaüzeneteket lát a még üres mezőknél.
Az `AutovalidateMode.onUserInteraction` ezzel szemben csak akkor kezdi meg a validációt egy adott mezőn, miután a felhasználó már megérintette azt és elkezdett gépelni. Így a mező üresen hagyása nem jelez hibát azonnal, csak a gépelést követő interakciók során.

### 4. Hogyan tudjuk a billentyűzet "Keresés" vagy "Küldés" gombját beállítani az input mezőben (TextInputAction)?
A billentyűzet akciógombját a beviteli mező `textInputAction` paraméterével lehet szabályozni. Ha például a `TextInputAction.next` értéket adjuk meg, a billentyűzeten egy jobbra mutató nyíl vagy "Következő" felirat jelenik meg. Ha a `TextInputAction.search` értéket használjuk, akkor nagyító ikon jelenik meg. A kód lefutásakor a billentyűzet ezen gombjának megnyomására az `onFieldSubmitted` callback-ben reagálhatunk.

### 5. Hogyan lehet megvalósítani, hogy a fókusz automatikusan átugorjon a következő beviteli mezőre (FocusScope)?
Ahhoz, hogy a fókusz automatikusan átugorjon, minden érintett mezőhöz létre kell hozni egy egyedi `FocusNode` objektumot. A szövegmező `onFieldSubmitted` metódusában (ami akkor fut le, ha a felhasználó a billentyűzet akciógombjára nyom) a `FocusScope.of(context).requestFocus(nextFocusNode)` utasítással tudjuk expliciten átadni a fókuszt a következő mezőnek. Így a billentyűzet nyitva marad, és a kurzor automatikusan a következő mezőbe ugrik.
