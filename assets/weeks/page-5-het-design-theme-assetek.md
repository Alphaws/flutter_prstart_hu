# 5. hét — Design, theme, assetek

## Cél
A hét célja, hogy megtanuljuk, hogyan készíthetünk professzionális, egységes és modern megjelenésű mobilalkalmazásokat. Megértjük a `ThemeData` felépítését, beállítjuk az alkalmazás színsémáját, gombjait, beviteli mezőit, betűtípusait, és megvalósítjuk a dinamikus sötét/világos mód váltást. Kialakítunk egy saját design rendszert, kezeljük a média asseteket és egyedi betűtípusokat, végül összeállítunk egy saját UI Kit-et Flutterben.

---

## Elmélet

### 5.1 A ThemeData Rendszer és a Sötét/Világos Mód
A Flutter a Material Design irányelveire épülő téma-rendszert használ. A `ThemeData` osztályban határozhatjuk meg az alkalmazás teljes vizuális identitását. Ha a témát globálisan beállítjuk a `MaterialApp`-ban, minden widget automatikusan átveszi a megfelelő stílust (pl. a gombok a primary színt kapják, a hátterek a surface színt).

A legfontosabb téma-tulajdonságok:
*   **`ColorScheme`**: A színek logikai rendszere. Tartalmazza a legfontosabb színszerepeket (pl. `primary` a kiemelt elemeknek, `onPrimary` a rajta lévő szövegnek, `error` a hibaüzeneteknek stb.). Ezt a legcélszerűbb a `ColorScheme.fromSeed()` konstruktorral generáltatni egyetlen bázisszín alapján.
*   **`Typography` / `TextTheme`**: A betűtípusok és szövegméretek gyűjteménye (`displayLarge`, `titleMedium`, `bodyMedium` stb.).
*   **Komponens Témák**: Finomhangolhatjuk az egyes widgetek alapértelmezett megjelenését, például:
    *   `ElevatedButtonThemeData`: A gombok lekerekítése, magassága, színe.
    *   `InputDecorationTheme`: A beviteli mezők (`TextField`) keretének színe, fókusza, hibaállapotai.
    *   `CardTheme`: A kártyák árnyékolása, sarkainak lekerekítése.

#### Sötét és Világos Mód (Dark & Light Mode)
A `MaterialApp`-ban egyszerre adható meg világos (`theme`) és sötét (`darkTheme`) téma konfiguráció, valamint a rendszer alapértelmezett beállításához igazodó mód (`themeMode`):

```dart
MaterialApp(
  theme: ThemeData.light(useMaterial3: true),
  darkTheme: ThemeData.dark(useMaterial3: true),
  themeMode: ThemeMode.system, // A telefon rendszerbeállítása szerint vált
);
```

### 5.2 Assetek és Médiafájlok Kezelése
Az alkalmazáshoz tartozó nem-kód fájlokat (képek, ikonok, JSON-ök, betűtípusok, lokalizációs fájlok) asseteknek nevezzük.

1.  **Mappa létrehozása:** Hozz létre egy `assets/images/` vagy `assets/icons/` könyvtárat a projekt gyökerében.
2.  **Deklaráció a `pubspec.yaml`-ben:**
    ```yaml
    flutter:
      assets:
        - assets/images/logo.png
        - assets/images/ # A teljes mappa tartalmát beolvassa
    ```
3.  **Betöltés a kódban:**
    ```dart
    Image.asset('assets/images/logo.png')
    ```

### 5.3 Egyedi Betűtípusok (Custom Fonts)
Ha nem a rendszer alapértelmezett betűtípusát akarjuk használni (pl. Inter betűtípust szeretnénk):

1.  Töltsd le a `.ttf` vagy `.otf` fájlokat (pl. Google Fonts-ról).
2.  Helyezd el őket az `assets/fonts/` mappában.
3.  Regisztráld a `pubspec.yaml`-ben:
    ```yaml
    flutter:
      fonts:
        - family: Inter
          fonts:
            - asset: assets/fonts/Inter-Regular.ttf
            - asset: assets/fonts/Inter-Bold.ttf
              weight: 700
    ```
4.  Állítsd be alapértelmezettnek a témában:
    ```dart
    ThemeData(
      fontFamily: 'Inter',
    )
    ```

### 5.4 Design Rendszer felépítése Flutterben
Egy professzionális alkalmazás nem használ ad-hoc méreteket és színeket a fájlokban. Mindennek egy szigorú rendszerhez kell igazodnia:

*   **Színpaletta:** Konkrét jelentéssel bíró színszerepek használata a közvetlen hexakódok helyett (pl. `Theme.of(context).colorScheme.primary`).
*   **Spacing (Térköz) Rendszer:** A távolságok legyenek a 4 vagy 8 pixel többszörösei (`8.0`, `16.0`, `24.0`, `32.0`). Ez biztosítja az egyenletes ritmust és elrendezést.
*   **Állapotok Vizualizációja:**
    *   *Loading State:* Felhasználó visszajelzése (pl. `CircularProgressIndicator`).
    *   *Empty State:* Ha nincs adat (pl. üres lista), egyértelmű ikon és leírás.
    *   *Error State:* Ha hiba történt, jól olvasható piros doboz vagy felirat újrapróbálkozási gombbal.

---

## Kódpéldák

### Egyedi Téma és Dinamikus Mód Váltó (compilable kód)
Az alábbi kód bemutatja, hogyan építünk fel egy egyedi témát világos és sötét változattal, és hogyan váltjuk ezt dinamikusan egy `ValueNotifier` segítségével.

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

// Globális notifier a téma állapotának követésére (Light / Dark)
final ValueNotifier<ThemeMode> themeNotifier = ValueNotifier(ThemeMode.light);

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return ValueListenableBuilder<ThemeMode>(
      valueListenable: themeNotifier,
      builder: (_, currentMode, __) {
        return MaterialApp(
          title: 'Design és Theme',
          debugShowCheckedModeBanner: false,
          themeMode: currentMode,
          // Világos téma
          theme: ThemeData(
            useMaterial3: true,
            colorScheme: ColorScheme.fromSeed(
              seedColor: Colors.deepPurple,
              brightness: Brightness.light,
            ),
            cardTheme: CardTheme(
              elevation: 2,
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
            ),
            inputDecorationTheme: InputDecorationTheme(
              filled: true,
              fillColor: Colors.grey.shade100,
              border: OutlineInputBorder(
                borderRadius: BorderRadius.circular(12),
                borderSide: BorderSide.none,
              ),
              focusedBorder: OutlineInputBorder(
                borderRadius: BorderRadius.circular(12),
                borderSide: const BorderSide(color: Colors.deepPurple, width: 2),
              ),
            ),
          ),
          // Sötét téma
          darkTheme: ThemeData(
            useMaterial3: true,
            colorScheme: ColorScheme.fromSeed(
              seedColor: Colors.deepPurple,
              brightness: Brightness.dark,
            ),
            cardTheme: CardTheme(
              elevation: 4,
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
            ),
            inputDecorationTheme: InputDecorationTheme(
              filled: true,
              fillColor: Colors.grey.shade900,
              border: OutlineInputBorder(
                borderRadius: BorderRadius.circular(12),
                borderSide: BorderSide.none,
              ),
              focusedBorder: OutlineInputBorder(
                borderRadius: BorderRadius.circular(12),
                borderSide: const BorderSide(color: Colors.purpleAccent, width: 2),
              ),
            ),
          ),
          home: const ThemeGalleryScreen(),
        );
      },
    );
  }
}

class ThemeGalleryScreen extends StatelessWidget {
  const ThemeGalleryScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;

    return Scaffold(
      appBar: AppBar(
        title: const Text('UI & Design Rendszer'),
        actions: [
          IconButton(
            icon: Icon(isDark ? Icons.light_mode : Icons.dark_mode),
            onPressed: () {
              // Téma váltása dinamikusan
              themeNotifier.value = isDark ? ThemeMode.light : ThemeMode.dark;
            },
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Címsor a témából vett betűstílussal
            Text(
              'Globális Témahasználat',
              style: theme.textTheme.headlineMedium?.copyWith(
                    fontWeight: FontWeight.bold,
                    color: theme.colorScheme.primary,
                  ),
            ),
            const SizedBox(height: 8),
            Text(
              'Ez az oldal bemutatja, hogyan reagál a UI a Light/Dark váltásra a ThemeData-n keresztül.',
              style: theme.textTheme.bodyMedium,
            ),
            const SizedBox(height: 24),

            // Kártya a témából vett színekkel
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text('Téma Színséma', style: theme.textTheme.titleMedium),
                    const SizedBox(height: 12),
                    Row(
                      children: [
                        _ColorBox(label: 'Primary', color: theme.colorScheme.primary),
                        _ColorBox(label: 'Secondary', color: theme.colorScheme.secondary),
                        _ColorBox(label: 'Surface', color: theme.colorScheme.surfaceContainer),
                      ],
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 24),

            // Beviteli Mező a téma InputDecorationTheme-ével
            const TextField(
              decoration: InputDecoration(
                hintText: 'Írj be valamit...',
                prefixIcon: Icon(Icons.edit),
              ),
            ),
            const SizedBox(height: 16),

            // Különböző gombok a témának megfelelően
            ElevatedButton(
              onPressed: () {},
              child: const Text('Primary Elevated Button'),
            ),
            const SizedBox(height: 8),
            OutlinedButton(
              onPressed: () {},
              child: const Text('Secondary Outlined Button'),
            ),
          ],
        ),
      ),
    );
  }
}

class _ColorBox extends StatelessWidget {
  final String label;
  final Color color;

  const _ColorBox({required this.label, required this.color});

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: Container(
        margin: const EdgeInsets.symmetric(horizontal: 4.0),
        padding: const EdgeInsets.symmetric(vertical: 16.0),
        decoration: BoxDecoration(
          color: color,
          borderRadius: BorderRadius.circular(8),
          border: Border.all(color: Colors.grey.withOpacity(0.3)),
        ),
        child: Text(
          label,
          textAlign: TextAlign.center,
          style: TextStyle(
            fontSize: 12,
            fontWeight: FontWeight.bold,
            color: ThemeData.estimateBrightnessForColor(color) == Brightness.dark
                ? Colors.white
                : Colors.black,
          ),
        ),
      ),
    );
  }
}
```

---

## Gyakorlófeladatok & Megoldások

### 1. Feladat: Külső Téma Osztály Készítése
Készíts egy saját `AppTheme` nevű osztályt külső fájlként (vagy struktúraként), amely statikusan biztosítja a `lightTheme` és `darkTheme` konfigurációkat, hogy elkerüld a `main.dart` felduzzasztását.

#### Megoldás:
```dart
import 'package:flutter/material.dart';

class AppTheme {
  // Privát konstruktor, hogy ne lehessen példányosítani
  AppTheme._();

  static const Color primarySeedColor = Colors.teal;

  static ThemeData get lightTheme {
    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.light,
      colorScheme: ColorScheme.fromSeed(
        seedColor: primarySeedColor,
        brightness: Brightness.light,
      ),
      scaffoldBackgroundColor: Colors.teal.shade50 / 2,
      appBarTheme: const AppBarTheme(
        backgroundColor: Colors.teal,
        foregroundColor: Colors.white,
        elevation: 0,
      ),
    );
  }

  static ThemeData get darkTheme {
    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.dark,
      colorScheme: ColorScheme.fromSeed(
        seedColor: primarySeedColor,
        brightness: Brightness.dark,
      ),
      appBarTheme: AppBarTheme(
        backgroundColor: Colors.grey.shade900,
        foregroundColor: Colors.white,
      ),
    );
  }
}
```

### 2. Feladat: Újrahasználható `PrimaryButton` Widget
Hozz létre egy saját `PrimaryButton` widgetet, amely megkapja a gomb szövegét, az eseménykezelőt (`onPressed`), egy opcionális betöltési állapotot (`isLoading`) és egy opcionális színt. Ha betöltési állapotban van, a gomb szövege helyett egy kis `CircularProgressIndicator` pörögjön.

#### Megoldás:
```dart
import 'package:flutter/material.dart';

class PrimaryButton extends StatelessWidget {
  final String label;
  final VoidCallback? onPressed;
  final bool isLoading;
  final Color? backgroundColor;
  final Color? foregroundColor;

  const PrimaryButton({
    super.key,
    required this.label,
    required this.onPressed,
    this.isLoading = false,
    this.backgroundColor,
    this.foregroundColor,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    
    return ElevatedButton(
      onPressed: isLoading ? null : onPressed,
      style: ElevatedButton.styleFrom(
        backgroundColor: backgroundColor ?? theme.colorScheme.primary,
        foregroundColor: foregroundColor ?? theme.colorScheme.onPrimary,
        padding: const EdgeInsets.symmetric(vertical: 14, horizontal: 24),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
        disabledBackgroundColor: (backgroundColor ?? theme.colorScheme.primary).withOpacity(0.5),
      ),
      child: isLoading
          ? SizedBox(
              height: 20,
              width: 20,
              child: CircularProgressIndicator(
                strokeWidth: 2,
                color: foregroundColor ?? theme.colorScheme.onPrimary,
              ),
            )
          : Text(
              label,
              style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
            ),
    );
  }
}
```

### 3. Feladat: Újrahasználható `AppTextField` Formázással
Készíts egy egyedi `AppTextField` widgetet, ami kezeli a szövegbevitelt, tartalmaz egy címkét (`labelText`), beállítható ikont, jelszómaszkolást (`obscureText`), és szép egyedi fókuszkeretet ad.

#### Megoldás:
```dart
import 'package:flutter/material.dart';

class AppTextField extends StatelessWidget {
  final TextEditingController? controller;
  final String labelText;
  final String? hintText;
  final IconData? prefixIcon;
  final bool obscureText;
  final String? Function(String?)? validator;

  const AppTextField({
    super.key,
    this.controller,
    required this.labelText,
    this.hintText,
    this.prefixIcon,
    this.obscureText = false,
    this.validator,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return TextFormField(
      controller: controller,
      obscureText: obscureText,
      validator: validator,
      decoration: InputDecoration(
        labelText: labelText,
        hintText: hintText,
        prefixIcon: prefixIcon != null ? Icon(prefixIcon, color: theme.colorScheme.primary) : null,
        filled: true,
        fillColor: theme.brightness == Brightness.light ? Colors.grey.shade100 : Colors.grey.shade900,
        contentPadding: const EdgeInsets.symmetric(vertical: 16, horizontal: 16),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: BorderSide(color: Colors.grey.shade300),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: BorderSide(color: Colors.grey.withOpacity(0.2)),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: BorderSide(color: theme.colorScheme.primary, width: 2),
        ),
        errorBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: BorderSide(color: theme.colorScheme.error),
        ),
      ),
    );
  }
}
```

### 4. Feladat: Light/Dark Mód Váltás Switch-csel
Készíts egy beállító oldalt, amin egy `SwitchListTile` widgettel ki-be kapcsolható a sötét mód.

#### Megoldás:
```dart
import 'package:flutter/material.dart';

// Tegyük fel, hogy ugyanazt a themeNotifiert használjuk a main.dart-ból
// Valósítsuk meg a beállító panelt:
class SettingsToggleScreen extends StatelessWidget {
  const SettingsToggleScreen({super.key, required this.themeNotifier});

  final ValueNotifier<ThemeMode> themeNotifier;

  @override
  Widget build(BuildContext context) {
    final isDarkMode = themeNotifier.value == ThemeMode.dark;

    return Scaffold(
      appBar: AppBar(title: const Text('Megjelenés Beállítások')),
      body: ListView(
        children: [
          SwitchListTile(
            title: const Text('Sötét téma alkalmazása'),
            subtitle: const Text('Energiatakarékos és kíméli a szemet sötétben'),
            secondary: const Icon(Icons.dark_mode),
            value: isDarkMode,
            onChanged: (bool value) {
              themeNotifier.value = value ? ThemeMode.dark : ThemeMode.light;
            },
          ),
        ],
      ),
    );
  }
}
```

### 5. Feladat: Esztétikus Üres Állapot (Empty State) Komponens
Készíts egy újrahasználható `EmptyStateWidget` komponenst, amely kap egy ikont, egy címet, egy alcímet és egy opcionális gomb feliratot gomb eseménnyel. Ezt használhatjuk, ha pl. egy lista üres vagy nem érkezett adat.

#### Megoldás:
```dart
import 'package:flutter/material.dart';

class EmptyStateWidget extends StatelessWidget {
  final IconData icon;
  final String title;
  final String subtitle;
  final String? actionLabel;
  final VoidCallback? onActionPressed;

  const EmptyStateWidget({
    super.key,
    required this.icon,
    required this.title,
    required this.subtitle,
    this.actionLabel,
    this.onActionPressed,
  });

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              icon,
              size: 80,
              color: Colors.grey.shade400,
            ),
            const SizedBox(height: 16),
            Text(
              title,
              style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 8),
            Text(
              subtitle,
              style: TextStyle(fontSize: 14, color: Colors.grey.shade600),
              textAlign: TextAlign.center,
            ),
            if (actionLabel != null && onActionPressed != null) ...[
              const SizedBox(height: 24),
              ElevatedButton(
                onPressed: onActionPressed,
                child: Text(actionLabel!),
              ),
            ]
          ],
        ),
      ),
    );
  }
}
```

---

## Heti Mini Projekt

### Saját UI Kit Flutterben
Ez a projekt egy interaktív UI Galéria, amely felsorakoztatja a saját egyedi komponenseinket. Segítségével tesztelhető a világos/sötét téma konzisztenciája és a komponensek viselkedése.

#### Főbb modulok:
*   Egyedi `PrimaryButton` normál, inaktív és betöltő (loading) állapotban.
*   Egyedi `AppTextField` normál beviteli móddal és egy validációs hibaállapottal rendelkező mezővel.
*   `EmptyStateWidget` bemutatása.
*   Általános visszajelzők: Error Box (hibaüzenet) és sikeres Badge-ek.
*   Theme Switcher az AppBar-ban.

#### A Teljes Kód (`lib/main.dart`):

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const UIKitApp());
}

// Globális notifier
final ValueNotifier<ThemeMode> globalThemeNotifier = ValueNotifier(ThemeMode.light);

class UIKitApp extends StatelessWidget {
  const UIKitApp({super.key});

  @override
  Widget build(BuildContext context) {
    return ValueListenableBuilder<ThemeMode>(
      valueListenable: globalThemeNotifier,
      builder: (_, currentMode, __) {
        return MaterialApp(
          title: 'Saját UI Kit Galéria',
          debugShowCheckedModeBanner: false,
          themeMode: currentMode,
          // Világos téma
          theme: ThemeData(
            useMaterial3: true,
            colorScheme: ColorScheme.fromSeed(seedColor: Colors.teal),
          ),
          // Sötét téma
          darkTheme: ThemeData(
            useMaterial3: true,
            colorScheme: ColorScheme.fromSeed(seedColor: Colors.teal, brightness: Brightness.dark),
          ),
          home: const UIKitGalleryScreen(),
        );
      },
    );
  }
}

class UIKitGalleryScreen extends StatefulWidget {
  const UIKitGalleryScreen({super.key});

  @override
  State<UIKitGalleryScreen> createState() => _UIKitGalleryScreenState();
}

class _UIKitGalleryScreenState extends State<UIKitGalleryScreen> {
  bool _isBtnLoading = false;
  final _formKey = GlobalKey<FormState>();

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;

    return Scaffold(
      appBar: AppBar(
        title: const Text('UI Kit Bemutató'),
        actions: [
          IconButton(
            icon: Icon(isDark ? Icons.light_mode : Icons.dark_mode),
            onPressed: () {
              globalThemeNotifier.value = isDark ? ThemeMode.light : ThemeMode.dark;
            },
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // 1. Szekció: Gombok
              _buildSectionTitle('1. Egyedi Gombok (PrimaryButton)'),
              Row(
                children: [
                  Expanded(
                    child: PrimaryButton(
                      label: 'Aktív Gomb',
                      onPressed: () {
                        setState(() {
                          _isBtnLoading = true;
                        });
                        Future.delayed(const Duration(seconds: 2), () {
                          if (mounted) {
                            setState(() {
                              _isBtnLoading = false;
                            });
                          }
                        });
                      },
                      isLoading: _isBtnLoading,
                    ),
                  ),
                  const SizedBox(width: 8),
                  const Expanded(
                    child: PrimaryButton(
                      label: 'Inaktív Gomb',
                      onPressed: null,
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 24),

              // 2. Szekció: Beviteli mezők
              _buildSectionTitle('2. Egyedi Beviteli Mezők (AppTextField)'),
              const AppTextField(
                labelText: 'Felhasználónév',
                hintText: 'Pl. sandor123',
                prefixIcon: Icons.person,
              ),
              const SizedBox(height: 12),
              AppTextField(
                labelText: 'E-mail cím',
                hintText: 'Pelda@email.com',
                prefixIcon: Icons.email,
                validator: (val) {
                  if (val == null || !val.contains('@')) {
                    return 'Helytelen e-mail cím formátum!';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 8),
              ElevatedButton(
                onPressed: () {
                  _formKey.currentState?.validate();
                },
                child: const Text('Form Validálása'),
              ),
              const SizedBox(height: 24),

              // 3. Szekció: Hibaablak és Badge
              _buildSectionTitle('3. Státusz és Visszajelzők'),
              const ErrorBox(message: 'Sikertelen kapcsolódás a szerverhez. Ellenőrizd az internetkapcsolatot!'),
              const SizedBox(height: 12),
              const Row(
                children: [
                  StatusBadge(label: 'Aktív', color: Colors.green),
                  SizedBox(width: 8),
                  StatusBadge(label: 'Függőben', color: Colors.orange),
                  SizedBox(width: 8),
                  StatusBadge(label: 'Lejárt', color: Colors.red),
                ],
              ),
              const SizedBox(height: 24),

              // 4. Szekció: Üres Állapot
              _buildSectionTitle('4. Üres Állapot Komponens'),
              Card(
                child: Padding(
                  padding: const EdgeInsets.symmetric(vertical: 16.0),
                  child: EmptyStateWidget(
                    icon: Icons.hourglass_empty,
                    title: 'Nincs elmentett adat',
                    subtitle: 'Hozd létre az első elemet a gomb megnyomásával.',
                    actionLabel: 'Létrehozás',
                    onActionPressed: () {},
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildSectionTitle(String title) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12.0, top: 8.0),
      child: Text(
        title,
        style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.grey),
      ),
    );
  }
}

// === COMPONENT IMPLEMENTATIONS ===

// 1. Gomb
class PrimaryButton extends StatelessWidget {
  final String label;
  final VoidCallback? onPressed;
  final bool isLoading;

  const PrimaryButton({super.key, required this.label, required this.onPressed, this.isLoading = false});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return ElevatedButton(
      onPressed: isLoading ? null : onPressed,
      style: ElevatedButton.styleFrom(
        backgroundColor: theme.colorScheme.primary,
        foregroundColor: theme.colorScheme.onPrimary,
        padding: const EdgeInsets.symmetric(vertical: 14),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      ),
      child: isLoading
          ? const SizedBox(height: 20, width: 20, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
          : Text(label, style: const TextStyle(fontWeight: FontWeight.bold)),
    );
  }
}

// 2. Input
class AppTextField extends StatelessWidget {
  final String labelText;
  final String? hintText;
  final IconData? prefixIcon;
  final String? Function(String?)? validator;

  const AppTextField({super.key, required this.labelText, this.hintText, this.prefixIcon, this.validator});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return TextFormField(
      validator: validator,
      decoration: InputDecoration(
        labelText: labelText,
        hintText: hintText,
        prefixIcon: prefixIcon != null ? Icon(prefixIcon, color: theme.colorScheme.primary) : null,
        filled: true,
        fillColor: theme.brightness == Brightness.light ? Colors.grey.shade100 : Colors.grey.shade900,
        border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
      ),
    );
  }
}

// 3. Error Box
class ErrorBox extends StatelessWidget {
  final String message;

  const ErrorBox({super.key, required this.message});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: Colors.red.shade50,
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: Colors.red.shade200),
      ),
      child: Row(
        children: [
          const Icon(Icons.error_outline, color: Colors.red),
          const SizedBox(width: 12),
          Expanded(
            child: Text(
              message,
              style: TextStyle(color: Colors.red.shade900, fontSize: 13),
            ),
          ),
        ],
      ),
    );
  }
}

// 4. Status Badge
class StatusBadge extends StatelessWidget {
  final String label;
  final Color color;

  const StatusBadge({super.key, required this.label, required this.color});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
      decoration: BoxDecoration(
        color: color.withOpacity(0.1),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: color),
      ),
      child: Text(
        label,
        style: TextStyle(color: color, fontWeight: FontWeight.bold, fontSize: 12),
      ),
    );
  }
}

// 5. Empty State
class EmptyStateWidget extends StatelessWidget {
  final IconData icon;
  final String title;
  final String subtitle;
  final String? actionLabel;
  final VoidCallback? onActionPressed;

  const EmptyStateWidget({
    super.key,
    required this.icon,
    required this.title,
    required this.subtitle,
    this.actionLabel,
    this.onActionPressed,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Icon(icon, size: 48, color: Colors.grey),
        const SizedBox(height: 8),
        Text(title, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
        Text(subtitle, style: const TextStyle(color: Colors.grey, fontSize: 12), textAlign: TextAlign.center),
        if (actionLabel != null && onActionPressed != null) ...[
          const SizedBox(height: 12),
          ElevatedButton(onPressed: onActionPressed, child: Text(actionLabel!)),
        ],
      ],
    );
  }
}
```

---

## Heti Ellenőrző Kérdések & Válaszok

### 1. Hogyan konfiguráljuk a `ThemeData`-t a `MaterialApp`-ban light és dark mód támogatásához?
A `MaterialApp`-ban a `theme` és a `darkTheme` paraméterekben külön-külön `ThemeData` példányokat adunk meg (mindkettőben beállítva a megfelelő `brightness` értéket vagy a seed színt a `ColorScheme.fromSeed(seedColor: ..., brightness: ...)` segítségével). A `themeMode` paraméterrel pedig szabályozhatjuk, hogy a világos (`ThemeMode.light`), a sötét (`ThemeMode.dark`) vagy a rendszer alapbeállítása (`ThemeMode.system`) legyen érvényben.

### 2. Mi a `ColorScheme` szerepe, és melyek a legfontosabb színszerepek (primary, secondary, surface, error stb.)?
A `ColorScheme` a Material Design színszabványa, ami logikai szerepek szerint osztja fel az alkalmazás színeit:
*   `primary`: Fő vezérlő és kiemelt színek (pl. gombok, AppBar háttere).
*   `onPrimary`: A primary színű elemek feletti szövegek és ikonok színe.
*   `secondary`: Kiegészítő színek (pl. filter chipek, kevésbé fontos elemek).
*   `surface`: A kártyák, panelek, lapok háttere.
*   `background`: A képernyő legalsó, általános háttere.
*   `error`: A hibaüzenetek színe.

### 3. Hogyan regisztrálunk képeket és betűtípusokat a `pubspec.yaml`-ben?
A `pubspec.yaml` fájl `flutter:` szekciója alatt deklaráljuk őket:
*   Assetekhez az `assets:` kulcsszót használjuk, felsorolva a fájlok vagy mappák útvonalait (pl. `- assets/images/logo.png`).
*   Betűtípusokhoz a `fonts:` kulcs alá felvesszük a `family` nevét, és azon belül felsoroljuk a fájlokat az `asset` útvonallal és a hozzájuk tartozó `weight` (súly) vagy `style` jellemzőkkel (pl. `- asset: assets/fonts/Inter-Regular.ttf`).

### 4. Miért fontos egy egyedi reusable widget (pl. `PrimaryButton`) létrehozása ahelyett, hogy minden oldalon külön-külön formáznánk a gombokat?
*   **Kódduplikáció elkerülése:** Ha változik az alkalmazás stílusa (pl. a gombok lekerekítése 8px helyett 16px legyen), azt egyetlen helyen átírva az egész alkalmazásban frissül.
*   **Karbantarthatóság:** Ha egy gombnak olyan állapota is van, mint a betöltő körpörgettyű (`isLoading`), nem kell minden képernyőn megírni ennek az állapotnak az elágazásait.
*   **Konzisztencia:** Biztosítja, hogy az egész csapat ugyanolyan gombokat és spacingeket használjon az appban.

### 5. Hogyan érhetjük el az aktuális téma színeit és szövegstílusait a widget fában (pl. `Theme.of(context)`)?
A `Theme.of(context)` hívással lekérhetjük az aktuális környezethez legközelebbi `ThemeData` objektumot. Például a téma fő színét a `Theme.of(context).colorScheme.primary`, a címsor stílusát pedig a `Theme.of(context).textTheme.headlineMedium` módon érhetjük el és alkalmazhatjuk a widgetjeinkre.
