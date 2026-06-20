# 21. hét — Natív integráció: Platform Channel és FFI

## Cél
A lecke célja, hogy a tanuló megértse, hogyan kommunikál a Flutter alkalmazás a natív Android (Kotlin/Java) és iOS (Swift/Objective-C) operációs rendszer rétegeivel. Megtanuljuk a `MethodChannel`, `EventChannel` használatát, megismerjük az adattípusok konverziós szabályait a nyelvek között, és bepillantást nyerünk a Dart FFI (Foreign Function Interface) világába.

---

## Elmélet

### 1. A Platform Channel architektúra működése
A Flutter nem közvetlenül natív bájtkódot futtat, hanem a Dart virtuális gépben (VM) hajtja végre az üzleti logikát. Ha olyan hardveres funkciót vagy gyártói SDK-t kell elérni, amelyhez nincs kész Flutter csomag, akkor közvetlenül a natív operációs rendszer API-jaihoz kell nyúlnunk. Ehhez a Flutter a **Platform Channel** mintát biztosítja.

A kommunikáció aszinkron és üzenetküldés alapú:
- A Dart kliens elküld egy üzenetet egy egyedi nevű csatornán.
- A natív gazda (Android vagy iOS) fogadja az üzenetet, végrehajtja a natív Java/Kotlin vagy Objective-C/Swift kódot, majd visszaküld egy választ.
- A csatornák szálbiztosak: a hívások a fő szálon (Main Thread / UI Thread) futnak mind Dart, mind natív oldalon, ezért a nehéz natív számításokat háttérszálra kell terelni natív oldalon, hogy ne akadjon meg a UI.

```text
+------------------+                   +--------------------+
|   Flutter Dart   | <-- MethodChannel | Natív Android/iOS  |
|  (UI / VM Szál)  |      (Async)      | (UI / Main Thread) |
+------------------+                   +--------------------+
```

### 2. A platform csatornák típusai
1. **MethodChannel:** Kérés-válasz (Request-Response) alapú kétirányú kommunikáció. Dartból metódusokat hívhatunk natív oldalon, és argumentumokat is átadhatunk, valamint válaszértéket kapunk vissza.
2. **EventChannel:** Folyamatos adatsorozatok (Stream) továbbítására szolgál. Natív oldalról küldhetünk eseményeket vagy szenzoradatokat (pl. giroszkóp, lépésszámláló) folyamatosan a Dart oldalra.
3. **BasicMessageChannel:** Egyszerű, aszinkron üzenetváltás tetszőleges adatformátummal (szöveg vagy bináris adatok).

### 3. Típuskonverziós táblázat
Az üzenetek küldésekor a Flutter automatikusan szerializálja és deszerializálja az adatokat a standard üzenetkódolóval (`StandardMessageCodec`).

| Dart Típus | Android Kotlin/Java Típus | iOS Swift Típus |
|:---|:---|:---|
| `null` | `null` | `nil` |
| `bool` | `java.lang.Boolean` / `Boolean` | `NSNumber` (Boolean) |
| `int` | `java.lang.Integer` / `Int` vagy `Long` | `NSNumber` (Int) |
| `double` | `java.lang.Double` / `Double` | `NSNumber` (Double) |
| `String` | `java.lang.String` / `String` | `String` |
| `Uint8List` | `byte[]` | `FlutterStandardTypedData` |
| `List` | `java.util.ArrayList` / `List<*>` | `Array` |
| `Map` | `java.util.HashMap` / `Map<*, *>` | `Dictionary` |

### 4. Dart FFI (Foreign Function Interface)
A Platform Channel egy általános, de viszonylag lassú megoldás a szerializációs és szálak közötti overhead miatt. Ha nagy teljesítményű, C/C++ vagy Rust nyelven írt könyvtárakat (.so, .dll, .dylib fájlok) akarunk közvetlenül, másolásmentesen (zero-copy) hívni a Dart VM-ből, a **Dart FFI**-t használjuk. Az FFI közvetlen memóriahozzáférést biztosít a C struktúrákhoz és függvényekhez platformcsatorna nélkül.

---

## Kódpéldák

### 1. MethodChannel megvalósítás
A következő kódpéldák bemutatják, hogyan kérhetjük le az akkumulátor töltöttségi szintjét natív API segítségével.

#### A) Dart Kód (`battery_channel.dart`):
```dart
import 'package:flutter/services.dart';

class BatteryChannel {
  // Egyedi csatornanév definiálása (ajánlott a domain-szerű név)
  static const MethodChannel _channel = MethodChannel('hu.prstart.flutter/battery');

  /// Akkumulátor szint lekérése natív oldalról.
  /// Visszatérési érték: százalékos arány (0-100 között)
  Future<int> getBatteryLevel() async {
    try {
      // Hívjuk a natív metódust
      final int result = await _channel.invokeMethod<int>('getBatteryLevel') ?? 0;
      return result;
    } on PlatformException catch (e) {
      // Natív oldalról dobott egyedi hiba elkapása
      throw Exception("Hiba a natív hívás során: '${e.message}'");
    }
  }

  /// Paraméterátadásos példa: Eszköz üdvözlése
  Future<String> sayHelloToNative(String userName) async {
    try {
      final String result = await _channel.invokeMethod<String>(
        'sayHello',
        {'name': userName}, // Map-ként adjuk át az argumentumokat
      ) ?? '';
      return result;
    } on PlatformException catch (e) {
      return 'Hiba: ${e.message}';
    }
  }
}
```

#### B) Android Kotlin Kód (`MainActivity.kt`):
Gyakran a `MainActivity`-ben regisztráljuk a csatornákat az `configureFlutterEngine` felülírásával.

```kotlin
package hu.prstart.flutter_app

import android.content.Context
import android.content.ContextWrapper
import android.content.Intent
import android.content.IntentFilter
import android.os.BatteryManager
import android.os.Build
import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.MethodChannel

class MainActivity: FlutterActivity() {
    private val CHANNEL = "hu.prstart.flutter/battery"

    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)
        
        MethodChannel(flutterEngine.dartExecutor.binaryMessenger, CHANNEL).setMethodCallHandler { call, result ->
            // A metódus nevének ellenőrzése
            if (call.method == "getBatteryLevel") {
                val batteryLevel = getBatteryLevel()

                if (batteryLevel != -1) {
                    result.success(batteryLevel) // Siker esetén visszaküldjük a számot
                } else {
                    result.error("UNAVAILABLE", "Az akkumulátor szint nem elérhető.", null)
                }
            } else if (call.method == "sayHello") {
                // Argumentum kiolvasása a küldött Map-ből
                val name = call.argument<String>("name")
                if (name != null) {
                    result.success("Helló $name natív Androidról!")
                } else {
                    result.error("INVALID_ARGUMENT", "A 'name' paraméter hiányzik.", null)
                }
            } else {
                result.notImplemented() // Nem definiált hívás esetén
            }
        }
    }

    private fun getBatteryLevel(): Int {
        val batteryLevel: Int
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            val batteryManager = getSystemService(Context.BATTERY_SERVICE) as BatteryManager
            batteryLevel = batteryManager.getIntProperty(BatteryManager.BATTERY_PROPERTY_CAPACITY)
        } else {
            val intent = ContextWrapper(applicationContext).registerReceiver(null, IntentFilter(Intent.ACTION_BATTERY_CHANGED))
            batteryLevel = intent!!.getIntExtra(BatteryManager.EXTRA_LEVEL, -1) * 100 / intent.getIntExtra(BatteryManager.EXTRA_SCALE, -1)
        }
        return batteryLevel
    }
}
```

#### C) iOS Swift Kód (`AppDelegate.swift`):
iOS-en a `Runner/AppDelegate.swift` fájlban végezzük a konfigurációt.

```swift
import UIKit
import Flutter

@main
@objc class AppDelegate: FlutterAppDelegate {
  override func application(
    _ application: UIApplication,
    didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?
  ) -> Bool {
    
    let controller : FlutterViewController = window?.rootViewController as! FlutterViewController
    let batteryChannel = FlutterMethodChannel(name: "hu.prstart.flutter/battery",
                                              binaryMessenger: controller.binaryMessenger)
    
    batteryChannel.setMethodCallHandler({
      [weak self] (call: FlutterMethodCall, result: @escaping FlutterResult) -> Void in
      
      if call.method == "getBatteryLevel" {
        guard let batteryLevel = self?.getBatteryLevel() else {
          result(FlutterError(code: "UNAVAILABLE",
                              message: "Nem sikerült lekérni a töltöttséget iOS-en",
                              details: nil))
          return
        }
        result(Int32(batteryLevel))
      } else if call.method == "sayHello" {
        if let args = call.arguments as? [String: Any],
           let name = args["name"] as? String {
          result("Helló \(name) natív iOS-ről!")
        } else {
          result(FlutterError(code: "INVALID_ARGUMENT",
                              message: "A 'name' paraméter hiányzik.",
                              details: nil))
        }
      } else {
        result(FlutterMethodNotImplemented)
      }
    })

    GeneratedPluginRegistrant.register(with: self)
    return super.application(application, didFinishLaunchingWithOptions: launchOptions)
  }

  private func getBatteryLevel() -> Int {
    let device = UIDevice.current
    device.isBatteryMonitoringEnabled = true
    if device.batteryState == .unknown {
      return -1
    } else {
      return Int(device.batteryLevel * 100)
    }
  }
}
```

### 2. EventChannel megvalósítás
Natív oldalon generált periodikus értékek küldése Dart-ba egy `Stream`-en keresztül.

#### Dart oldal (`sensor_channel.dart`):
```dart
import 'package:flutter/services.dart';

class SensorChannel {
  static const EventChannel _eventChannel = EventChannel('hu.prstart.flutter/sensor');

  /// Szenzor események figyelése
  Stream<double> getSensorDataStream() {
    return _eventChannel.receiveBroadcastStream().map((dynamic event) => event as double);
  }
}
```

#### Android Kotlin oldal (Regisztráció a MainActivity-ben):
```kotlin
import io.flutter.plugin.common.EventChannel
import android.os.Handler
import android.os.Looper

// A MainActivity.kt-ben lévő configureFlutterEngine belsejében:
EventChannel(flutterEngine.dartExecutor.binaryMessenger, "hu.prstart.flutter/sensor").setStreamHandler(
    object : EventChannel.StreamHandler {
        private var handler: Handler? = null
        private var runnable: Runnable? = null

        override fun onListen(arguments: Any?, events: EventChannel.EventSink?) {
            handler = Handler(Looper.getMainLooper())
            var count = 0.0
            
            runnable = object : Runnable {
                override fun run() {
                    count += 1.5
                    events?.success(count) // Adat küldése Dartba
                    handler?.postDelayed(this, 1000) // 1 másodpercenként
                }
            }
            handler?.post(runnable!!)
        }

        override fun onCancel(arguments: Any?) {
            handler?.removeCallbacks(runnable!!)
            handler = null
            runnable = null
        }
    }
)
```

---

## Gyakorlófeladatok & Megoldások

### 1. Feladat: Akkumulátor állapot lekérő gomb
Készíts egy UI felületet, amely az előző elméleti szakaszban bemutatott `BatteryChannel` osztály segítségével egy gomb megnyomására kiírja a telefon aktuális akkumulátor szintjét.

#### Megoldás:
```dart
import 'package:flutter/material.dart';
// Tételezzük fel, hogy a BatteryChannel a fenti módon be van importálva
import 'battery_channel.dart'; 

class BatteryExercisePage extends StatefulWidget {
  const BatteryExercisePage({super.key});

  @override
  State<BatteryExercisePage> createState() => _BatteryExercisePageState();
}

class _BatteryExercisePageState extends State<BatteryExercisePage> {
  final BatteryChannel _batteryChannel = BatteryChannel();
  String _batteryLevelText = 'Ismeretlen';
  bool _isLoading = false;

  Future<void> _fetchBattery() async {
    setState(() {
      _isLoading = true;
    });
    try {
      final int level = await _batteryChannel.getBatteryLevel();
      setState(() {
        _batteryLevelText = '$level%';
      });
    } catch (e) {
      setState(() {
        _batteryLevelText = 'Hiba: $e';
      });
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Akku szint natívan')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Text('Akkumulátor töltöttsége:', style: TextStyle(fontSize: 16)),
            const SizedBox(height: 10),
            _isLoading
                ? const CircularProgressIndicator()
                : Text(
                    _batteryLevelText,
                    style: const TextStyle(fontSize: 32, fontWeight: FontWeight.bold),
                  ),
            const SizedBox(height: 30),
            ElevatedButton(
              onPressed: _isLoading ? null : _fetchBattery,
              child: const Text('Töltöttség Lekérése'),
            ),
          ],
        ),
      ),
    );
  }
}
```

### 2. Feladat: Szöveg küldése natív oldalra és megfordítása
Készíts egy beviteli mezőt (TextField). Gombnyomásra küldd át a beírt szöveget natív oldalra platformcsatornán, ott fordítsd meg (Reverse) Kotlin/Swift segítségével, és írd ki a kapott eredményt.

#### Megoldás:

**Dart kód:**
```dart
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class TextReversePage extends StatefulWidget {
  const TextReversePage({super.key});

  @override
  State<TextReversePage> createState() => _TextReversePageState();
}

class _TextReversePageState extends State<TextReversePage> {
  static const _channel = MethodChannel('hu.prstart.flutter/reverse');
  final _controller = TextEditingController();
  String _resultText = '';

  Future<void> _sendAndReverse() async {
    if (_controller.text.isEmpty) return;
    try {
      final String reversed = await _channel.invokeMethod('reverseText', {
        'text': _controller.text,
      }) ?? '';
      setState(() {
        _resultText = reversed;
      });
    } on PlatformException catch (e) {
      setState(() {
        _resultText = 'Hiba: ${e.message}';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Szövegmegfordító Natívan')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextField(
              controller: _controller,
              decoration: const InputDecoration(labelText: 'Írj be egy szöveget'),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: _sendAndReverse,
              child: const Text('Megfordítás natív kóddal'),
            ),
            const SizedBox(height: 30),
            Text(
              'Eredmény: $_resultText',
              style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
          ],
        ),
      ),
    );
  }
}
```

**Android Kotlin Megoldás (`MainActivity.kt` részlet):**
```kotlin
MethodChannel(flutterEngine.dartExecutor.binaryMessenger, "hu.prstart.flutter/reverse").setMethodCallHandler { call, result ->
    if (call.method == "reverseText") {
        val originalText = call.argument<String>("text")
        if (originalText != null) {
            result.success(originalText.reversed()) // Szöveg megfordítása Kotlinban
        } else {
            result.error("BAD_ARGS", "Hiányzó paraméter", null)
        }
    } else {
        result.notImplemented()
    }
}
```

### 3. Feladat: PlatformException Kezelése
Készíts egy gombot, amely meghív egy natív metódust (`generateError`), ami szándékosan hibát dob a natív oldalon (pl. Kotlinban throw Exception, iOS-en FlutterError). Kezeld le ezt a hibát Dart oldalon `try-catch` blokk segítségével, és jelenítsd meg a felhasználónak egy párbeszédablakban (AlertDialog).

#### Megoldás:

**Dart kód:**
```dart
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class ExceptionPage extends StatelessWidget {
  const ExceptionPage({super.key});

  static const _channel = MethodChannel('hu.prstart.flutter/error_test');

  Future<void> _triggerError(BuildContext context) async {
    try {
      await _channel.invokeMethod('generateError');
    } on PlatformException catch (e) {
      _showErrorDialog(context, e.code, e.message ?? 'Ismeretlen hiba');
    }
  }

  void _showErrorDialog(BuildContext context, String code, String message) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('Hiba kód: $code'),
        content: Text('Üzenet a natív oldalról:\n$message'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('OK'),
          )
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Hiba Kezelés')),
      body: Center(
        child: ElevatedButton(
          onPressed: () => _triggerError(context),
          child: const Text('Natív Hiba Kiváltása'),
        ),
      ),
    );
  }
}
```

**Android Kotlin Megoldás (`MainActivity.kt` részlet):**
```kotlin
MethodChannel(flutterEngine.dartExecutor.binaryMessenger, "hu.prstart.flutter/error_test").setMethodCallHandler { call, result ->
    if (call.method == "generateError") {
        result.error("NATIVE_CRASH_TEST", "Ez egy szándékosan generált natív hiba Androidon.", "Részletek: MainActivity.kt:L123")
    } else {
        result.notImplemented()
    }
}
```

### 4. Feladat: OS verzió lekérése
Készíts egy platformcsatornát, amely lekéri és kiírja a mobil operációs rendszer verzióját (Android SDK verzió szám, iOS verziószám).

#### Megoldás:

**Dart kód:**
```dart
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class OsVersionPage extends StatefulWidget {
  const OsVersionPage({super.key});

  @override
  State<OsVersionPage> createState() => _OsVersionPageState();
}

class _OsVersionPageState extends State<OsVersionPage> {
  static const _channel = MethodChannel('hu.prstart.flutter/os_version');
  String _osVersion = 'Ismeretlen';

  Future<void> _fetchVersion() async {
    try {
      final String version = await _channel.invokeMethod('getOsVersion') ?? 'Hiba';
      setState(() {
        _osVersion = version;
      });
    } on PlatformException catch (e) {
      setState(() {
        _osVersion = 'Hiba: ${e.message}';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('OS Verzió')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text('Verzió: $_osVersion', style: const TextStyle(fontSize: 20)),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: _fetchVersion,
              child: const Text('OS lekérése'),
            ),
          ],
        ),
      ),
    );
  }
}
```

**Android Kotlin Megoldás:**
```kotlin
MethodChannel(flutterEngine.dartExecutor.binaryMessenger, "hu.prstart.flutter/os_version").setMethodCallHandler { call, result ->
    if (call.method == "getOsVersion") {
        result.success("Android " + Build.VERSION.RELEASE + " (SDK " + Build.VERSION.SDK_INT + ")")
    } else {
        result.notImplemented()
    }
}
```

**iOS Swift Megoldás:**
```swift
// AppDelegate.swift részlet
let osChannel = FlutterMethodChannel(name: "hu.prstart.flutter/os_version", binaryMessenger: controller.binaryMessenger)
osChannel.setMethodCallHandler({ (call, result) in
    if call.method == "getOsVersion" {
        result("iOS " + UIDevice.current.systemVersion)
    } else {
        result(FlutterMethodNotImplemented)
    }
})
```

### 5. Feladat: Natív Toast Üzenet Androidon
Készíts egy platformcsatornát, amely Androidon meghívja a natív `Toast.makeText` metódust a Dartból kapott szöveggel, így megjelenítve a klasszikus szürke Android Toast üzenetet.

#### Megoldás:

**Dart kód:**
```dart
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class ToastExercisePage extends StatelessWidget {
  const ToastExercisePage({super.key});

  static const _channel = MethodChannel('hu.prstart.flutter/toast');

  Future<void> _showNativeToast(String text) async {
    try {
      await _channel.invokeMethod('showToast', {'message': text});
    } on PlatformException catch (e) {
      print('Hiba: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Toast Gyakorlat')),
      body: Center(
        child: ElevatedButton(
          onPressed: () => _showNativeToast('Helló ez egy natív Android Toast!'),
          child: const Text('Toast Megjelenítése'),
        ),
      ),
    );
  }
}
```

**Android Kotlin Megoldás:**
```kotlin
import android.widget.Toast

// configureFlutterEngine-ben
MethodChannel(flutterEngine.dartExecutor.binaryMessenger, "hu.prstart.flutter/toast").setMethodCallHandler { call, result ->
    if (call.method == "showToast") {
        val msg = call.argument<String>("message")
        if (msg != null) {
            Toast.makeText(context, msg, Toast.LENGTH_SHORT).show()
            result.success(null)
        } else {
            result.error("MISSING_ARG", "Üzenet hiányzik", null)
        }
    } else {
        result.notImplemented()
    }
}
```

---

## Heti Mini Projekt: Natív rendszerinformáció app (NativeSysInfo)

### Leírás és Funkciók
A heti mini projekt egy **Natív rendszerinformáció app (NativeSysInfo)**. Az alkalmazás egyetlen elegáns képernyőből áll, amely gombnyomásra vagy betöltéskor lekérdezi az eszköz legfontosabb hardveres adatait közvetlenül a natív API-kon keresztül (Platform Channel):
1. Az operációs rendszer verziószáma.
2. Az eszköz gyártója és modellje.
3. Az eszközön elérhető szabad fizikai memória (RAM) aránya és mérete.

### Megvalósítás

A projektben a csatorna neve: `hu.prstart.flutter/sysinfo`

#### A) A teljes Dart kód (`lib/main.dart`):
```dart
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

void main() {
  runApp(const NativeSysApp());
}

class NativeSysApp extends StatelessWidget {
  const NativeSysApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'NativeSysInfo',
      theme: ThemeData(
        brightness: Brightness.dark,
        primaryColor: Colors.deepPurple,
        scaffoldBackgroundColor: const Color(0xFF090D16),
        useMaterial3: true,
      ),
      home: const SysInfoPage(),
    );
  }
}

class SysInfoPage extends StatefulWidget {
  const SysInfoPage({super.key});

  @override
  State<SysInfoPage> createState() => _SysInfoPageState();
}

class _SysInfoPageState extends State<SysInfoPage> {
  static const _channel = MethodChannel('hu.prstart.flutter/sysinfo');

  String _osVersion = 'Betöltés...';
  String _deviceModel = 'Betöltés...';
  String _freeMemory = 'Betöltés...';
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    _fetchSystemInfo();
  }

  Future<void> _fetchSystemInfo() async {
    setState(() {
      _isLoading = true;
    });

    try {
      // 1. OS verzió lekérése
      final String os = await _channel.invokeMethod('getOsVersion') ?? 'Ismeretlen';
      // 2. Gyártó/modell lekérése
      final String model = await _channel.invokeMethod('getDeviceModel') ?? 'Ismeretlen';
      // 3. Szabad memória lekérése
      final String ram = await _channel.invokeMethod('getFreeMemory') ?? 'Ismeretlen';

      setState(() {
        _osVersion = os;
        _deviceModel = model;
        _freeMemory = ram;
      });
    } on PlatformException catch (e) {
      setState(() {
        _osVersion = 'Hiba';
        _deviceModel = 'Hiba';
        _freeMemory = 'Hiba: ${e.message}';
      });
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Native System Information'),
        backgroundColor: Colors.deepPurple[900],
        elevation: 0,
      ),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(
              Icons.developer_board,
              size: 80,
              color: Colors.deepPurpleAccent,
            ),
            const SizedBox(height: 30),
            _buildInfoCard('Operációs Rendszer', _osVersion, Icons.phone_android),
            const SizedBox(height: 12),
            _buildInfoCard('Eszköz Modell', _deviceModel, Icons.smartphone),
            const SizedBox(height: 12),
            _buildInfoCard('Szabad Memória (RAM)', _freeMemory, Icons.memory),
            const SizedBox(height: 40),
            ElevatedButton.icon(
              onPressed: _isLoading ? null : _fetchSystemInfo,
              icon: const Icon(Icons.refresh),
              label: const Text('Adatok Frissítése'),
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.deepPurpleAccent,
                foregroundColor: Colors.white,
                padding: const EdgeInsets.symmetric(vertical: 14),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(10),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildInfoCard(String label, String value, IconData icon) {
    return Card(
      color: const Color(0xFF161B26),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
        side: const BorderSide(color: Colors.deepPurple, width: 0.5),
      ),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Row(
          children: [
            Icon(icon, size: 30, color: Colors.deepPurpleAccent),
            const SizedBox(width: 16),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    label,
                    style: const TextStyle(fontSize: 12, color: Colors.grey),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    value,
                    style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
```

#### B) Android Kotlin Kód (`android/app/src/main/kotlin/.../MainActivity.kt`):
```kotlin
package hu.prstart.flutter_app

import android.app.ActivityManager
import android.content.Context
import android.os.Build
import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.MethodChannel

class MainActivity: FlutterActivity() {
    private val CHANNEL = "hu.prstart.flutter/sysinfo"

    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)

        MethodChannel(flutterEngine.dartExecutor.binaryMessenger, CHANNEL).setMethodCallHandler { call, result ->
            when (call.method) {
                "getOsVersion" -> {
                    result.success("Android " + Build.VERSION.RELEASE + " (API " + Build.VERSION.SDK_INT + ")")
                }
                "getDeviceModel" -> {
                    val manufacturer = Build.MANUFACTURER
                    val model = Build.MODEL
                    result.success("$manufacturer $model".capitalize())
                }
                "getFreeMemory" -> {
                    val freeMem = getAvailableMemory()
                    result.success(freeMem)
                }
                else -> {
                    result.notImplemented()
                }
            }
        }
    }

    private fun getAvailableMemory(): String {
        val activityManager = getSystemService(Context.ACTIVITY_SERVICE) as ActivityManager
        val memoryInfo = ActivityManager.MemoryInfo()
        activityManager.getMemoryInfo(memoryInfo)
        // Megabájtban számolva
        val freeBytes = memoryInfo.availMem
        val freeMb = freeBytes / (1024 * 1024)
        val totalBytes = memoryInfo.totalMem
        val totalMb = totalBytes / (1024 * 1024)
        return "$freeMb MB / $totalMb MB szabad"
    }
}
```

#### C) iOS Swift Kód (`ios/Runner/AppDelegate.swift`):
```swift
import UIKit
import Flutter

@main
@objc class AppDelegate: FlutterAppDelegate {
  override func application(
    _ application: UIApplication,
    didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?
  ) -> Bool {
    
    let controller : FlutterViewController = window?.rootViewController as! FlutterViewController
    let sysInfoChannel = FlutterMethodChannel(name: "hu.prstart.flutter/sysinfo",
                                              binaryMessenger: controller.binaryMessenger)
    
    sysInfoChannel.setMethodCallHandler({
      (call: FlutterMethodCall, result: @escaping FlutterResult) -> Void in
      
      switch call.method {
      case "getOsVersion":
        result("iOS " + UIDevice.current.systemVersion)
      case "getDeviceModel":
        // iOS model neve (pl. iPhone14,2)
        var systemInfo = utsname()
        uname(&systemInfo)
        let machineMirror = Mirror(reflecting: systemInfo.machine)
        let identifier = machineMirror.children.reduce("") { identifier, element in
          guard let value = element.value as? Int8, value != 0 else { return identifier }
          return identifier + String(UnicodeScalar(UInt8(value)))
        }
        result("Apple Device (" + identifier + ")")
      case "getFreeMemory":
        // iOS szabad memória lekérdezése
        var pagesize: vm_size_t = 0
        let host_port: mach_port_t = mach_host_self()
        var host_size: mach_msg_type_number_t = mach_msg_type_number_t(MemoryLayout<vm_statistics_data_t>.stroke / MemoryLayout<integer_t>.stroke)
        host_page_size(host_port, &pagesize)
        
        var vm_stat = vm_statistics_data_t()
        let kern: kern_return_t = withUnsafeMutablePointer(to: &vm_stat) {
          $0.withMemoryRebound(to: integer_t.self, capacity: Int(host_size)) {
            host_statistics(host_port, HOST_VM_INFO, $0, &host_size)
          }
        }
        
        if kern == KERN_SUCCESS {
          let freeMem = Double(vm_stat.free_count) * Double(pagesize) / (1024.0 * 1024.0)
          result(String(format: "%.0f MB szabad", freeMem))
        } else {
          result("Nem érhető el memória adat iOS-en")
        }
      default:
        result(FlutterMethodNotImplemented)
      }
    })

    GeneratedPluginRegistrant.register(with: self)
    return super.application(application, didFinishLaunchingWithOptions: launchOptions)
  }
}
```

---

## Heti Ellenőrző Kérdések

### 1. Kérdés: Mit jelent az, hogy a Platform Channel hívások aszinkronok, és miért fontos ez a UI fonal szempontjából?
**Válasz:**
Mivel a Dart kódnak át kell haladnia a Flutter motoron, át kell konvertálnia az adatokat bináris formátumba, és el kell juttatnia a natív operációs rendszer szálára, ez a hívás időt vesz igénybe. Ha a hívás szinkron lenne (blokkolná a végrehajtást), a Flutter renderelő motorja nem tudna új képkockákat rajzolni, és a felhasználói felület azonnal megakadna (Frame Drop, Jank). Az aszinkron működés (`Future` használata Dart oldalon) biztosítja, hogy a hívás ideje alatt a UI szál szabad maradjon, lehessen animációkat futtatni, betöltő ikonokat pörgetni, és a választ csak akkor dolgozza fel az app, ha az megérkezik a háttérből.

### 2. Kérdés: Mi történik, ha egy olyan metódust hívunk meg a Dart oldalról (`invokeMethod`), amelyet a natív Kotlin vagy Swift oldalon nem kezeltünk le (nincs hozzá `case` vagy `if` ág)? Hogyan kell ezt natívan jelezni?
**Válasz:**
Ha a natív kód nem ismeri fel a metódus nevét, akkor nem szabad sikeres választ küldeni (`result.success`), sem általános hibát dobni. Ehelyett az erre a célra fenntartott visszahívást kell használni:
- **Kotlin:** `result.notImplemented()`
- **Swift:** `result(FlutterMethodNotImplemented)`
Ebben az esetben a Dart oldalon egy `PlatformException` váltódik ki, amely jelzi, hogy a kért funkció nincs implementálva a célplatformon.

### 3. Kérdés: Mi a különbség a `MethodChannel` és az `EventChannel` között? Mikor melyiket választanád?
**Válasz:**
- A **MethodChannel** kérés-válasz alapú, egyszeri hívásokra való (One-shot). A Dart kezdeményezi, elküld egy kérést és vár egyetlen választ (pl. akkumulátorszint lekérése, kamera megnyitása).
- Az **EventChannel** stream alapú folyamatos adatáramlásra való. A Dart egyszer feliratkozik a csatornára, és ezután a natív oldal tetszőleges gyakorisággal és ideig küldhet eseményeket anélkül, hogy a Dart újabb kérést indítana (pl. giroszkóp folyamatos mérései, lépésszámláló, valós idejű letöltési folyamatjelző).

### 4. Kérdés: Hogyan történik a típusok egyeztetése a Dart és a natív platformok között? Mi történik egy egyedi Dart osztály küldésekor?
**Válasz:**
A típusok fordítását a háttérben a `StandardMessageCodec` végzi a standard leképezések alapján (pl. Dart `List` -> Kotlin `ArrayList` -> Swift `Array`). 
Ha egy saját, egyedi Dart osztályt (pl. `User` objektumot) szeretnénk átküldeni, azt a Standard Codec nem tudja közvetlenül konvertálni, és hibát dob. Megoldásként az egyedi objektumot át kell alakítani `Map<String, dynamic>` típusú adattá (JSON-szerű formátum), amit a rendszer könnyen átvisz a csatornán, majd a natív oldalon kiolvashatjuk a kulcs-érték párokat (Kotlinban `call.argument`, Swiftben dictionary castolással).

### 5. Kérdés: Mikor indokolt a Dart FFI használata a hagyományos Platform Channel helyett?
**Válasz:**
A Dart FFI használata akkor indokolt, ha:
1. **Nagy teljesítményű számításokra van szükség:** Pl. képelemzés, titkosítás, videótömörítés, fizikai szimuláció, ahol a platformcsatorna bináris szerializációs ideje már szűk keresztmetszetté válna.
2. **Meglévő C/C++ vagy Rust kódbázis integrálása a cél:** Pl. beágyazott adatbázis motor (SQLite natív könyvtár) vagy egyedi C-ben írt matematikai algoritmus közvetlen futtatása mobil és asztali platformokon egyaránt.
Az FFI-vel kiküszöbölhető az Android és iOS UI szálak és a Dart szál közötti átjárási idő, mivel a Dart közvetlenül a C ABI-n keresztül hívja meg a lefordított natív binárist.
