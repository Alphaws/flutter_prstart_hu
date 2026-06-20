# 20. hét — Platform specifikus funkciók

## Cél
A lecke célja, hogy a tanuló megismerje és magabiztosan használja a mobiltelefonok hardveres és operációs rendszer szintű képességeit Flutterből. Megtanuljuk a jogosultságok kezelését, a GPS alapú helymeghatározást, a kamera és galéria elérését, a helyi értesítések küldését, a hálózati kapcsolat és az eszközadatok lekérdezését, valamint a háttérfeladatok alapjait.

---

## Elmélet

### 1. Hogyan működnek a natív wrapper pluginok?
A Flutter alapvetően egy grafikus motor, amely a saját UI-elemeit közvetlenül a képernyőre rajzolja. A hardveres képességek (például a GPS chip, a kamera vagy az akkumulátor) eléréséhez azonban az operációs rendszer (Android vagy iOS) natív API-jait kell meghívni. 
A Flutter ezt az áthidalást **Platform Channel** architektúrával oldja meg. A fejlesztők kényelme érdekében a `pub.dev`-en található népszerű csomagok (mint a `geolocator` vagy az `image_picker`) ezeket a platformcsatorna hívásokat előre csomagolják (wrapperként működnek). Dart nyelven kínálnak egy tiszta API-t, miközben a háttérben meghívják az Android (Kotlin/Java) és iOS (Swift/Objective-C) megfelelő rendszerfüggvényeit.

### 2. Jogosultságkezelés (Permissions)
A modern operációs rendszerek szigorú biztonsági modellel rendelkeznek. Két szintű jogosultságkezelést alkalmazunk:
1. **Manifest szintű deklaráció:** Az alkalmazás konfigurációs fájljaiban előre jelezni kell, hogy az app milyen erőforrásokat kíván használni.
   - **Android:** `AndroidManifest.xml` (pl. `<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />`)
   - **iOS:** `Info.plist` (pl. `NSLocationWhenInUseUsageDescription`)
2. **Futásidejű kérés:** Amikor az alkalmazás ténylegesen hozzá szeretne férni a hardverhez, a felhasználónak egy rendszerszintű párbeszédpanelen jóvá kell hagynia azt. Ehhez Flutterben a `permission_handler` csomag az iparági sztenderd.

### 3. GPS és Helymeghatározás (`geolocator`)
A helymeghatározás történhet GPS műholdak, mobil cellainformációk vagy Wi-Fi hálózatok alapján.
- **Pontosság (Accuracy):** A geolocator különböző pontossági szinteket biztosít (`lowest`, `low`, `medium`, `high`, `best`).
- **Akkumulátor és teljesítmény:** A magas pontosság (GPS chip folyamatos járatása) drasztikusan meríti a telefont. Mindig a célhoz szükséges legkisebb pontosságot válaszd!
- **Helyszolgáltatások ellenőrzése:** A hely lekérése előtt ellenőrizni kell, hogy a telefonon be van-e kapcsolva a GPS/helyszolgáltatás, és hogy az alkalmazás rendelkezik-e a szükséges engedéllyel.

### 4. Kamera és Galéria (`image_picker`)
Az `image_picker` segítségével egyszerűen indíthatunk rendszer-szándékot (Intent Androidon, UIImagePickerController iOS-en):
- **Kamera indítása:** Közvetlenül megnyitja a rendszer kameráját fotó vagy videó készítésére.
- **Galéria megnyitása:** Lehetővé teszi egy vagy több kép kiválasztását a médiatárból.
A visszakapott fájl ideiglenes elérési úttal (`path`) rendelkezik, amelyet átmásolhatunk az alkalmazás saját tárolójába, vagy feltölthetünk egy szerverre.

### 5. Értesítések (Local & Push Notifications)
- **Local Notification:** Az alkalmazás saját maga ütemezi az értesítést a telefon helyi rendszerén keresztül (pl. emlékeztető 10 perc múlva). Ehhez a `flutter_local_notifications` csomagot használjuk.
- **Push Notification:** Egy külső szerver (pl. Firebase Cloud Messaging - FCM) küld üzenetet az Apple APNs vagy Google FCM rendszeren keresztül, ami felébreszti az eszközt és megjeleníti az értesítést.

---

## Kódpéldák

### 1. GPS Helymeghatározó és Jogosultságkezelő Szerviz
A következő osztály egy teljesen implementált, típusbiztos szolgáltatás, amely ellenőrzi a jogosultságot, engedélyt kér, majd lekéri az aktuális koordinátákat a `geolocator` és a `permission_handler` segítségével.

```dart
import 'package:geolocator/geolocator.dart';
import 'package:permission_handler/permission_handler.dart';

class LocationService {
  /// Ellenőrzi a GPS szolgáltatás állapotát és a jogosultságokat,
  /// majd lekéri az aktuális földrajzi pozíciót.
  Future<Position?> getCurrentLocation() async {
    // 1. Ellenőrizzük, hogy be van-e kapcsolva a helyszolgáltatás a telefonon
    bool serviceEnabled = await Geolocator.isLocationServiceEnabled();
    if (!serviceEnabled) {
      throw Exception('A helyszolgáltatás (GPS) ki van kapcsolva az eszközön.');
    }

    // 2. Ellenőrizzük a jogosultság aktuális állapotát
    LocationPermission permission = await Geolocator.checkPermission();
    
    if (permission == LocationPermission.denied) {
      // Ha elutasított, futás közben kérünk jogosultságot
      permission = await Geolocator.requestPermission();
      if (permission == LocationPermission.denied) {
        throw Exception('A felhasználó elutasította a helymeghatározási jogosultságot.');
      }
    }

    // Ha véglegesen elutasította (beállításokban le van tiltva)
    if (permission == LocationPermission.deniedForever) {
      // Megnyithatjuk a beállításokat a felhasználónak
      await Geolocator.openAppSettings();
      throw Exception('A jogosultság véglegesen elutasítva. Kérjük, engedélyezze a beállításokban.');
    }

    // 3. Pozíció lekérése közepes pontossággal az erőforrások kímélése érdekében
    return await Geolocator.getCurrentPosition(
      desiredAccuracy: LocationAccuracy.medium,
      timeLimit: const Duration(seconds: 10),
    );
  }

  /// Ellenőrzi, hogy van-e engedélyünk, anélkül hogy feldobnánk a kérő ablakot
  Future<bool> hasLocationPermission() async {
    final status = await Permission.locationWhenInUse.status;
    return status.isGranted;
  }
}
```

### 2. Képválasztó Segédosztály (Kamera és Galéria)
Segítségével képeket kérhetünk be az `image_picker` csomaggal.

```dart
import 'dart:io';
import 'package:image_picker/image_picker.dart';

class ImagePickerHelper {
  final ImagePicker _picker = ImagePicker();

  /// Kép készítése a kamerával
  Future<File?> takePhoto() async {
    final XFile? photo = await _picker.pickImage(
      source: ImageSource.camera,
      imageQuality: 80, // Tömörítés a hálózati forgalom csökkentésére
      maxWidth: 1920,
    );

    if (photo != null) {
      return File(photo.path);
    }
    return null;
  }

  /// Kép kiválasztása a galériából
  Future<File?> pickImageFromGallery() async {
    final XFile? image = await _picker.pickImage(
      source: ImageSource.gallery,
      imageQuality: 85,
    );

    if (image != null) {
      return File(image.path);
    }
    return null;
  }
}
```

### 3. Helyi Értesítések Ütemezője
Példa a `flutter_local_notifications` inicializálására és azonnali, illetve időzített értesítések küldésére.

```dart
import 'package:flutter_local_notifications/flutter_local_notifications.dart';

class NotificationService {
  final FlutterLocalNotificationsPlugin _notificationsPlugin =
      FlutterLocalNotificationsPlugin();

  /// Szerviz inicializálása Android és iOS platformra
  Future<void> initNotification() async {
    // Android beállítások - meg kell adni egy alapértelmezett ikont (pl. @mipmap/ic_launcher)
    const AndroidInitializationSettings initializationSettingsAndroid =
        AndroidInitializationSettings('@mipmap/ic_launcher');

    // iOS / Darwin beállítások
    const DarwinInitializationSettings initializationSettingsDarwin =
        DarwinInitializationSettings(
      requestAlertPermission: true,
      requestBadgePermission: true,
      requestSoundPermission: true,
    );

    const InitializationSettings initializationSettings = InitializationSettings(
      android: initializationSettingsAndroid,
      iOS: initializationSettingsDarwin,
    );

    await _notificationsPlugin.initialize(initializationSettings);
  }

  /// Azonnali értesítés küldése
  Future<void> showNotification({
    required int id,
    required String title,
    required String body,
  }) async {
    const AndroidNotificationDetails androidDetails = AndroidNotificationDetails(
      'main_channel',
      'Fő Értesítési Csatorna',
      channelDescription: 'Fontos alkalmazás értesítések',
      importance: Importance.max,
      priority: Priority.high,
      playSound: true,
    );

    const DarwinNotificationDetails iosDetails = DarwinNotificationDetails(
      presentAlert: true,
      presentBadge: true,
      presentSound: true,
    );

    const NotificationDetails platformDetails = NotificationDetails(
      android: androidDetails,
      iOS: iosDetails,
    );

    await _notificationsPlugin.show(
      id,
      title,
      body,
      platformDetails,
    );
  }
}
```

### 4. Hálózati Kapcsolat és Változás Figyelő
A hálózati kapcsolat meglétének ellenőrzése és valós idejű figyelése a `connectivity_plus` csomaggal.

```dart
import 'dart:async';
import 'package:connectivity_plus/connectivity_plus.dart';

class NetworkConnectivityService {
  final Connectivity _connectivity = Connectivity();
  StreamSubscription<List<ConnectivityResult>>? _subscription;

  /// Aktuális állapot lekérdezése
  Future<bool> isConnected() async {
    final List<ConnectivityResult> result = await _connectivity.checkConnectivity();
    return _hasInternetAccess(result);
  }

  /// Változások figyelése egy streamen keresztül
  void monitorConnection(Function(bool) onConnectionChanged) {
    _subscription = _connectivity.onConnectivityChanged.listen((List<ConnectivityResult> result) {
      onConnectionChanged(_hasInternetAccess(result));
    });
  }

  bool _hasInternetAccess(List<ConnectivityResult> results) {
    // Ha a lista nem tartalmaz none elemet, van hálózati kapcsolat (wifi, mobilnet, ethernet)
    if (results.isEmpty || results.contains(ConnectivityResult.none)) {
      return false;
    }
    return true;
  }

  void dispose() {
    _subscription?.cancel();
  }
}
```

---

## Gyakorlófeladatok & Megoldások

### 1. Feladat: Kép kiválasztása galériából és megjelenítése
Készíts egy egyszerű felületet, ahol egy gomb megnyomására a felhasználó kiválaszthat egy képet a galériából, és az alkalmazás megjeleníti azt a képernyőn.

#### Megoldás:
```dart
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';

class ImagePickerExercise extends StatefulWidget {
  const ImagePickerExercise({super.key});

  @override
  State<ImagePickerExercise> createState() => _ImagePickerExerciseState();
}

class _ImagePickerExerciseState extends State<ImagePickerExercise> {
  File? _selectedImage;
  final ImagePicker _picker = ImagePicker();

  Future<void> _pickImage() async {
    try {
      final XFile? image = await _picker.pickImage(source: ImageSource.gallery);
      if (image != null) {
        setState(() {
          _selectedImage = File(image.path);
        });
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Hiba a kép kiválasztásakor: $e')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Képválasztó Gyakorlat')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            _selectedImage != null
                ? Image.file(
                    _selectedImage!,
                    height: 300,
                    width: 300,
                    fit: BoxFit.cover,
                  )
                : const Icon(Icons.image, size: 100, color: Colors.grey),
            const SizedBox(height: 20),
            ElevatedButton.icon(
              onPressed: _pickImage,
              icon: const Icon(Icons.photo_library),
              label: const Text('Kép kiválasztása galériából'),
            ),
          ],
        ),
      ),
    );
  }
}
```

### 2. Feladat: Aktuális GPS koordináták lekérése és megjelenítése
Készíts egy képernyőt egy gombbal. A gomb megnyomására kérd le a GPS koordinátákat, közben jeleníts meg egy `CircularProgressIndicator` betöltőt, a végén pedig írd ki a szélességi és hosszúsági fokot.

#### Megoldás:
```dart
import 'package:flutter/material.dart';
import 'package:geolocator/geolocator.dart';

class GpsExercise extends StatefulWidget {
  const GpsExercise({super.key});

  @override
  State<GpsExercise> createState() => _GpsExerciseState();
}

class _GpsExerciseState extends State<GpsExercise> {
  String _locationText = 'Nyomd meg a gombot a lekéréshez';
  bool _isLoading = false;

  Future<void> _fetchGps() async {
    setState(() {
      _isLoading = true;
    });

    try {
      // Jogosultság ellenőrzése
      LocationPermission permission = await Geolocator.checkPermission();
      if (permission == LocationPermission.denied) {
        permission = await Geolocator.requestPermission();
      }

      if (permission == LocationPermission.whileInUse || 
          permission == LocationPermission.always) {
        Position position = await Geolocator.getCurrentPosition(
          desiredAccuracy: LocationAccuracy.high,
        );
        setState(() {
          _locationText = 'Lat: ${position.latitude}\nLong: ${position.longitude}';
        });
      } else {
        setState(() {
          _locationText = 'Nincs GPS jogosultság.';
        });
      }
    } catch (e) {
      setState(() {
        _locationText = 'Hiba történt: $e';
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
      appBar: AppBar(title: const Text('GPS lekérő gyakorlat')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            _isLoading
                ? const CircularProgressIndicator()
                : Text(
                    _locationText,
                    textAlign: TextAlign.center,
                    style: const TextStyle(fontSize: 18),
                  ),
            const SizedBox(height: 30),
            ElevatedButton(
              onPressed: _isLoading ? null : _fetchGps,
              child: const Text('Koordináták lekérése'),
            ),
          ],
        ),
      ),
    );
  }
}
```

### 3. Feladat: Kamera jogosultság kezelése
Készíts egy gombot, amely ellenőrzi a kamera jogosultságot a `permission_handler` csomaggal. Ha nincs engedélyezve, kérje el. Ha elutasított vagy korlátozott, jelenítsen meg egy megfelelő státuszüzenetet a képernyőn.

#### Megoldás:
```dart
import 'package:flutter/material.dart';
import 'package:permission_handler/permission_handler.dart';

class CameraPermissionExercise extends StatefulWidget {
  const CameraPermissionExercise({super.key});

  @override
  State<CameraPermissionExercise> createState() => _CameraPermissionExerciseState();
}

class _CameraPermissionExerciseState extends State<CameraPermissionExercise> {
  String _permissionStatus = 'Ismeretlen';

  Future<void> _checkAndRequestPermission() async {
    // Jogosultság ellenőrzése
    PermissionStatus status = await Permission.camera.status;
    
    if (status.isDenied) {
      // Kérjük el, ha még nem döntött a felhasználó
      status = await Permission.camera.request();
    }

    setState(() {
      if (status.isGranted) {
        _permissionStatus = 'Engedélyezve (Kamera használható)';
      } else if (status.isPermanentlyDenied) {
        _permissionStatus = 'Véglegesen megtagadva (Nyisd meg a Beállításokat)';
      } else {
        _permissionStatus = 'Megtagadva';
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Kamera Jogosultság')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              'Kamera státusz: $_permissionStatus',
              style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: _checkAndRequestPermission,
              child: const Text('Jogosultság vizsgálata / kérése'),
            ),
          ],
        ),
      ),
    );
  }
}
```

### 4. Feladat: Azonnali helyi értesítés küldése
Hozz létre egy gombot, amely megnyomásakor azonnal küld egy helyi értesítést a telefon értesítési sávjába.

#### Megoldás:
```dart
import 'package:flutter/material.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart';

class NotificationExercise extends StatefulWidget {
  const NotificationExercise({super.key});

  @override
  State<NotificationExercise> createState() => _NotificationExerciseState();
}

class _NotificationExerciseState extends State<NotificationExercise> {
  final FlutterLocalNotificationsPlugin _flutterLocalNotificationsPlugin =
      FlutterLocalNotificationsPlugin();

  @override
  void initState() {
    super.initState();
    _initNotifications();
  }

  Future<void> _initNotifications() async {
    const androidSettings = AndroidInitializationSettings('@mipmap/ic_launcher');
    const iosSettings = DarwinInitializationSettings();
    const settings = InitializationSettings(android: androidSettings, iOS: iosSettings);
    await _flutterLocalNotificationsPlugin.initialize(settings);
  }

  Future<void> _sendInstantNotification() async {
    const androidDetails = AndroidNotificationDetails(
      'exercise_channel',
      'Gyakorló csatorna',
      importance: Importance.max,
      priority: Priority.high,
    );
    const platformDetails = NotificationDetails(android: androidDetails);
    
    await _flutterLocalNotificationsPlugin.show(
      99,
      'Sikeres Gyakorlat!',
      'Ez egy azonnali helyi értesítés.',
      platformDetails,
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Értesítés Gyakorlat')),
      body: Center(
        child: ElevatedButton(
          onPressed: _sendInstantNotification,
          child: const Text('Értesítés küldése most!'),
        ),
      ),
    );
  }
}
```

### 5. Feladat: Connectivity Figyelés
Készíts egy képernyőt, amely folyamatosan figyeli a hálózati kapcsolatot. Ha megszakad az internet, dobjon fel egy piros SnackBar-t „Nincs internetkapcsolat” szöveggel, ha pedig visszatér, egy zöld SnackBar-t „A hálózat helyreállt” felirattal.

#### Megoldás:
```dart
import 'dart:async';
import 'package:connectivity_plus/connectivity_plus.dart';
import 'package:flutter/material.dart';

class ConnectivityExercise extends StatefulWidget {
  const ConnectivityExercise({super.key});

  @override
  State<ConnectivityExercise> createState() => _ConnectivityExerciseState();
}

class _ConnectivityExerciseState extends State<ConnectivityExercise> {
  final Connectivity _connectivity = Connectivity();
  StreamSubscription<List<ConnectivityResult>>? _subscription;
  bool? _wasConnected;

  @override
  void initState() {
    super.initState();
    _subscription = _connectivity.onConnectivityChanged.listen((List<ConnectivityResult> results) {
      final bool hasNet = results.isNotEmpty && !results.contains(ConnectivityResult.none);
      
      if (_wasConnected != null && _wasConnected != hasNet) {
        _showStatusSnackBar(hasNet);
      }
      _wasConnected = hasNet;
    });
  }

  void _showStatusSnackBar(bool hasNet) {
    ScaffoldMessenger.of(context).clearSnackBars();
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(hasNet ? 'A hálózat helyreállt!' : 'Nincs internetkapcsolat!'),
        backgroundColor: hasNet ? Colors.green : Colors.red,
        duration: const Duration(seconds: 3),
      ),
    );
  }

  @override
  void dispose() {
    _subscription?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Kapcsolat Figyelő')),
      body: Center(
        child: Text(
          _wasConnected == true ? 'Online vagy' : 'Offline vagy',
          style: TextStyle(
            fontSize: 20,
            color: _wasConnected == true ? Colors.green : Colors.red,
            fontWeight: FontWeight.bold,
          ),
        ),
      ),
    );
  }
}
```

---

## Heti Mini Projekt: Helyalapú jegyzet app (GeoNotes)

### Leírás és Funkciók
A heti mini projekt egy **Helyalapú jegyzet app (GeoNotes)**. Az alkalmazás lehetővé teszi, hogy szöveges jegyzeteket hozzunk létre, amelyekhez gombnyomásra csatolhatjuk az aktuális tartózkodási helyünk GPS koordinátáit, valamint készíthetünk vagy csatolhatunk egy fotót is. A jegyzeteket az alkalmazás lokálisan, memóriában vagy perzisztens módon tárolja, és listázza.

### Projekt felépítése és kódja
A futtatáshoz add hozzá a `pubspec.yaml`-hez a következő csomagokat:
```yaml
dependencies:
  flutter:
    sdk: flutter
  geolocator: ^11.0.0
  image_picker: ^1.0.7
  permission_handler: ^11.3.1
```

Itt a teljes, másolható és azonnal futtatható `main.dart` fájl tartalma:

```dart
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:geolocator/geolocator.dart';
import 'package:image_picker/image_picker.dart';
import 'package:permission_handler/permission_handler.dart';

void main() {
  runApp(const GeoNotesApp());
}

class GeoNotesApp extends StatelessWidget {
  const GeoNotesApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'GeoNotes - Helyalapú Jegyzetek',
      theme: ThemeData(
        brightness: Brightness.dark,
        primaryColor: Colors.teal,
        scaffoldBackgroundColor: const Color(0xFF0F172A),
        colorScheme: const ColorScheme.dark(
          primary: Colors.teal,
          secondary: Colors.tealAccent,
        ),
        useMaterial3: true,
      ),
      home: const NotesListPage(),
    );
  }
}

/// Jegyzet adatmodell
class Note {
  final String id;
  final String title;
  final String content;
  final double? latitude;
  final double? longitude;
  final String? imagePath;
  final DateTime createdAt;

  Note({
    required this.id,
    required this.title,
    required this.content,
    this.latitude,
    this.longitude,
    this.imagePath,
    required this.createdAt,
  });
}

class NotesListPage extends StatefulWidget {
  const NotesListPage({super.key});

  @override
  State<NotesListPage> createState() => _NotesListPageState();
}

class _NotesListPageState extends State<NotesListPage> {
  final List<Note> _notes = [];

  void _addNote(Note note) {
    setState(() {
      _notes.add(note);
    });
  }

  void _deleteNote(String id) {
    setState(() {
      _notes.removeWhere((n) => n.id == id);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('GeoNotes Jegyzetek'),
        backgroundColor: Colors.teal[800],
      ),
      body: _notes.isEmpty
          ? const Center(
              child: Text(
                'Nincs még mentett jegyzeted.\nNyomd meg a + gombot!',
                textAlign: TextAlign.center,
                style: TextStyle(color: Colors.grey, fontSize: 16),
              ),
            )
          : ListView.builder(
              itemCount: _notes.length,
              itemBuilder: (context, index) {
                final note = _notes[index];
                return Card(
                  margin: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                  color: const Color(0xFF1E293B),
                  child: ListTile(
                    leading: note.imagePath != null
                        ? ClipRRect(
                            borderRadius: BorderRadius.circular(6),
                            child: Image.file(
                              File(note.imagePath!),
                              width: 50,
                              height: 50,
                              fit: BoxFit.cover,
                            ),
                          )
                        : const CircleAvatar(
                            backgroundColor: Colors.teal,
                            child: Icon(Icons.note, color: Colors.white),
                          ),
                    title: Text(
                      note.title,
                      style: const TextStyle(fontWeight: FontWeight.bold),
                    ),
                    subtitle: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(note.content, maxLines: 2, overflow: TextOverflow.ellipsis),
                        const SizedBox(height: 4),
                        if (note.latitude != null && note.longitude != null)
                          Row(
                            children: [
                              const Icon(Icons.location_on, size: 14, color: Colors.tealAccent),
                              const SizedBox(width: 4),
                              Text(
                                '${note.latitude!.toStringAsFixed(4)}, ${note.longitude!.toStringAsFixed(4)}',
                                style: const TextStyle(fontSize: 12, color: Colors.tealAccent),
                              ),
                            ],
                          ),
                      ],
                    ),
                    trailing: IconButton(
                      icon: const Icon(Icons.delete, color: Colors.redAccent),
                      onPressed: () => _deleteNote(note.id),
                    ),
                    isThreeLine: note.latitude != null,
                  ),
                );
              },
            ),
      floatingActionButton: FloatingActionButton(
        backgroundColor: Colors.tealAccent,
        foregroundColor: Colors.black,
        child: const Icon(Icons.add),
        onPressed: () async {
          final Note? newNote = await Navigator.push(
            context,
            MaterialPageRoute(builder: (context) => const CreateNotePage()),
          );
          if (newNote != null) {
            _addNote(newNote);
          }
        },
      ),
    );
  }
}

class CreateNotePage extends StatefulWidget {
  const CreateNotePage({super.key});

  @override
  State<CreateNotePage> createState() => _CreateNotePageState();
}

class _CreateNotePageState extends State<CreateNotePage> {
  final _titleController = TextEditingController();
  final _contentController = TextEditingController();
  
  double? _latitude;
  double? _longitude;
  File? _imageFile;
  bool _isLocating = false;

  final ImagePicker _imagePicker = ImagePicker();

  /// GPS Koordináta lekérése jogosultság ellenőrzéssel
  Future<void> _getLocation() async {
    setState(() {
      _isLocating = true;
    });

    try {
      LocationPermission permission = await Geolocator.checkPermission();
      if (permission == LocationPermission.denied) {
        permission = await Geolocator.requestPermission();
      }

      if (permission == LocationPermission.whileInUse || 
          permission == LocationPermission.always) {
        Position position = await Geolocator.getCurrentPosition(
          desiredAccuracy: LocationAccuracy.high,
        );
        setState(() {
          _latitude = position.latitude;
          _longitude = position.longitude;
        });
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('GPS pozíció sikeresen rögzítve!')),
        );
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Helymeghatározás megtagadva.')),
        );
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Hiba a GPS lekérdezésben: $e')),
      );
    } finally {
      setState(() {
        _isLocating = false;
      });
    }
  }

  /// Kép készítése a kamerával
  Future<void> _getImage() async {
    // Kamera jogosultság kérése a biztonság kedvéért
    PermissionStatus status = await Permission.camera.request();
    if (status.isGranted) {
      final XFile? pickedFile = await _imagePicker.pickImage(
        source: ImageSource.camera,
        imageQuality: 80,
      );
      if (pickedFile != null) {
        setState(() {
          _imageFile = File(pickedFile.path);
        });
      }
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Nincs hozzáférés a kamerához.')),
      );
    }
  }

  void _saveNote() {
    if (_titleController.text.isEmpty || _contentController.text.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('A cím és tartalom kitöltése kötelező!')),
      );
      return;
    }

    final newNote = Note(
      id: DateTime.now().millisecondsSinceEpoch.toString(),
      title: _titleController.text,
      content: _contentController.text,
      latitude: _latitude,
      longitude: _longitude,
      imagePath: _imageFile?.path,
      createdAt: DateTime.now(),
    );

    Navigator.pop(context, newNote);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Új GeoJegyzet'),
        backgroundColor: Colors.teal[800],
        actions: [
          IconButton(
            icon: const Icon(Icons.check),
            onPressed: _saveNote,
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            TextField(
              controller: _titleController,
              decoration: const InputDecoration(
                labelText: 'Cím',
                border: OutlineInputBorder(),
                prefixIcon: Icon(Icons.title),
              ),
            ),
            const SizedBox(height: 16),
            TextField(
              controller: _contentController,
              maxLines: 4,
              decoration: const InputDecoration(
                labelText: 'Tartalom',
                border: OutlineInputBorder(),
                prefixIcon: Icon(Icons.text_fields),
              ),
            ),
            const SizedBox(height: 20),
            Row(
              children: [
                Expanded(
                  child: ElevatedButton.icon(
                    onPressed: _isLocating ? null : _getLocation,
                    icon: _isLocating
                        ? const SizedBox(
                            width: 20,
                            height: 20,
                            child: CircularProgressIndicator(strokeWidth: 2),
                          )
                        : const Icon(Icons.location_on),
                    label: const Text('GPS koordináta'),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.teal[700],
                      foregroundColor: Colors.white,
                    ),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: ElevatedButton.icon(
                    onPressed: _getImage,
                    icon: const Icon(Icons.camera_alt),
                    label: const Text('Fotó készítése'),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.teal[700],
                      foregroundColor: Colors.white,
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 20),
            if (_latitude != null && _longitude != null)
              Card(
                color: const Color(0xFF1E293B),
                child: Padding(
                  padding: const EdgeInsets.all(12.0),
                  child: Row(
                    children: [
                      const Icon(Icons.map, color: Colors.tealAccent),
                      const SizedBox(width: 10),
                      Text(
                        'Mentett pozíció:\nLat: $_latitude, Long: $_longitude',
                        style: const TextStyle(color: Colors.tealAccent),
                      ),
                    ],
                  ),
                ),
              ),
            const SizedBox(height: 16),
            if (_imageFile != null)
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text('Csatolt fotó:', style: TextStyle(fontWeight: FontWeight.bold)),
                  const SizedBox(height: 8),
                  ClipRRect(
                    borderRadius: BorderRadius.circular(8),
                    child: Image.file(
                      _imageFile!,
                      height: 200,
                      width: double.infinity,
                      fit: BoxFit.cover,
                    ),
                  ),
                ],
              ),
          ],
        ),
      ),
    );
  }
}
```

---

## Heti Ellenőrző Kérdések

### 1. Kérdés: Miért van szükség a jogosultságok ellenőrzésére mind a konfigurációban (Manifest/Info.plist), mind futási időben (runtime)?
**Válasz:**
A konfigurációban történő deklaráció (pl. `AndroidManifest.xml`) elengedhetetlen ahhoz, hogy a mobil operációs rendszer egyáltalán tudja, hogy az alkalmazásnak szüksége lehet arra a hardverre, így a rendszer engedélyezi a hozzá tartozó API csomag használatát és láthatóvá teszi ezt a Play Store-ban is. A futásidejű ellenőrzés és kérés viszont a felhasználó adatvédelmét szolgálja. Lehetővé teszi, hogy a felhasználó eldöntse: engedélyezi-e az adott funkciót a konkrét szituációban (pl. csak akkor használja a helyadatot, amikor megnyomja a gombot), ráadásul a felhasználó bármikor utólag is visszavonhatja a jogosultságot a telefon beállításaiban. Futási időben történő vizsgálat nélkül az app egyszerűen összeomlana (Crash) a hardver hívásakor, ha az engedély hiányozna.

### 2. Kérdés: Mi a különbség a `Geolocator.getCurrentPosition()` és a `Geolocator.getLastKnownPosition()` között? Mikor melyiket érdemes használni?
**Válasz:**
A `getCurrentPosition()` közvetlenül lekérdezi a GPS chiptől vagy a helymeghatározó szolgáltatótól az aktuális koordinátákat. Ez aktívan használja az eszköz hardverét, pontosabb adatot ad, viszont időbe telik (akár másodpercekbe), és magas az akkumulátor fogyasztása.
A `getLastKnownPosition()` a telefon gyorsítótárában tárolt, legutóbbi helymeghatározás adatait adja vissza azonnal, anélkül hogy a GPS chipet újra bekapcsolná. Ez energiatakarékos és azonnali választ ad, viszont előfordulhat, hogy az adat elavult (pl. a felhasználó azóta 50 km-rel arrébb utazott) vagy `null` értéket ad vissza, ha nincs gyorsítótárazott adat.
**Használat:** Akkor érdemes a `getLastKnownPosition()`-t használni indításkor gyors pozicionálásra, ha az elavultabb adat nem kritikus. Ha viszont pontos és friss adatra van szükségünk (pl. útvonaltervezés indításakor), a `getCurrentPosition()` a helyes választás.

### 3. Kérdés: Hogyan segít a `connectivity_plus` csomag a felhasználói élmény (UX) növelésében offline helyzetben?
**Válasz:**
A connectivity csomag segítségével az alkalmazás azonnal értesül a hálózati kapcsolat elvesztéséről vagy visszatéréséről. Ezzel elkerülhető, hogy a felhasználó a betöltő gombra kattintva másodpercekig a timeout hibára várjon. Offline állapotban az app letilthatja a küldő/lekérő gombokat, megjeleníthet egy egyértelmű offline jelzést (pl. „Offline mód”), betöltheti az adatokat a helyi cache-ből, és eltárolhatja a szerverre szánt műveleteket egy helyi sorban, amelyeket a kapcsolat visszatérésekor automatikusan szinkronizálhat.

### 4. Kérdés: Miért kötelező Androidon az értesítési csatornák (Notification Channels) definiálása, és hogyan valósítjuk meg ezt Flutterben?
**Válasz:**
Az Android 8.0 (API szint 26) óta kötelezőek az értesítési csatornák. Ezek lehetővé teszik a felhasználó számára, hogy ne az egész alkalmazás értesítéseit tiltsa le, hanem csatornánként szabályozza a viselkedést (pl. a marketing üzeneteket elnémítja, de a chat üzenetekről kér hangjelzést és felugró ablakot).
Flutterben a `flutter_local_notifications` csomagban a `AndroidNotificationDetails` osztály példányosításakor meg kell adnunk a csatorna azonosítóját (`channelId`), nevét (`channelName`) és leírását. Ezek az adatok jelennek meg a telefon Beállítások menüpontjában az alkalmazás adatlapjánál.

### 5. Kérdés: Milyen korlátok vannak a háttérben futó feladatok (Background Tasks) esetén mobilplatformokon?
**Válasz:**
A mobil operációs rendszerek szigorúan korlátozzák az alkalmazások háttérben történő futását az akkumulátor kímélése és a memória megőrzése érdekében.
- **Android:** A háttérben futó kódokat a rendszer egy idő után leállítja, kivéve ha az alkalmazás indít egy látható ikonos háttérszolgáltatást (Foreground Service).
- **iOS:** A háttérben futás rendkívül limitált. A rendszer maga dönti el, mikor ad futási időt az appnak (Background Fetch), jellemzően 15 percnél nem gyakrabban, és a futási ablak nagyon rövid (30 másodperc).
- **Általánosságban:** Nem futtathatunk folyamatos nehéz számításokat a háttérben. Megoldásként a `workmanager` csomagot vagy natív ütemezőket érdemes használni a periodikus, nem azonnali háttérmunkák végzésére.
