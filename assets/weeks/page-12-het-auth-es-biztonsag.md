# 12. hét — Auth és biztonság

## Cél
A lecke célja, hogy elsajátítsd a professzionális és biztonságos hitelesítési (Authentication - Auth) folyamatok megvalósítását Flutter alkalmazásokban. Megtanulod a JWT (JSON Web Token) alapú munkamenet-kezelést, a tokenek biztonságos tárolását, a kimenő kérések automatikus fejléccel történő kiegészítését (Interceptorok segítségével), a lejárt tokenek csendes frissítését (Silent Token Refresh), valamint a 401-es Unauthorized válaszok globális kezelését. A hét végére képes leszel egy biztonságos, automatikus beléptetéssel és védett útvonalakkal rendelkező alkalmazást felépíteni.

---

## Elmélet

### 1. JWT (JSON Web Token) alapú hitelesítés mobilalkalmazásokban
A modern mobil-backend architektúrák leggyakoribb hitelesítési formája a JWT. A bejelentkezés sikeres lefutása után a szerver két tokent küld vissza a kliensnek:
1.  **Access Token (Hozzáférési token):** Rövid életű (pl. 15 perc - 1 óra). Ezt a tokent küldjük el minden egyes védett API kérés fejlécében (Header) az `Authorization: Bearer <token>` formátumban.
2.  **Refresh Token (Frissítő token):** Hosszabb életű (pl. 7 nap - 30 nap). Kizárólag arra használjuk, hogy új Access Tokent igényeljünk a backenndől, ha a korábbi lejárt.

#### Miért nem használunk hosszú életű Access Tokent?
Ha az Access Token illetéktelen kezekbe kerül (pl. hálózati forgalom lehallgatása során), a támadó korlátozott ideig tud csak visszaélni vele. A Refresh Token ezzel szemben sokkal ritkábban utazik a hálózaton (csak frissítéskor), így kisebb a kompromittálódás esélye.

### 2. A Tokenek tárolása mobil eszközökön
Soha ne tárolj hitelesítési tokeneket a hagyományos `shared_preferences` fájlban, mert az eszköz rootolása vagy feltörése esetén a fájlrendszerből könnyen kiolvashatók. 
*   **Android:** A `flutter_secure_storage` a rendszerszintű **Android Keystore**-t használja, ami hardveres szinten (ha elérhető az eszközön) titkosítja a tárolt kulcsokat.
*   **iOS:** A rendszer saját **Keychain** szolgáltatását használja, ami a legmagasabb szintű biztonsági tároló iOS-en.

### 3. Interceptorok (Kérés-elkapók) szerepe
Ahelyett, hogy minden egyes HTTP kérésnél manuálisan adnánk hozzá a tokeneket a fejlécekhez, a hálózati kliens (pl. **Dio**) **Interceptor** képességét használjuk.
Az interceptor egy olyan köztes szoftver (middleware), amely lefut:
*   A kérés elküldése előtt (`onRequest`): Itt automatikusan beszúrjuk a tárolt Access Tokent az `Authorization` fejlécbe.
*   A válasz megérkezésekor (`onResponse`): Kezelhetjük a globális válaszokat.
*   Hiba esetén (`onError`): Ha a szerver **401 Unauthorized** hibát ad vissza (mert az Access Token lejárt), az interceptor felfüggeszti a folyamatban lévő hálózati kéréseket, a háttérben meghívja a token-frissítési végpontot (Refresh Token-nel), frissíti a tárolt tokeneket, majd automatikusan újraindítja az eredetileg elbukott kérést. Ha a frissítés is elbukik (pl. a Refresh Token is lejárt), azonnali kijelentkeztetést kezdeményez.

```text
  [ App Kérés ] ---> (onRequest: Beszúrja az Access Tokent) ---> [ API Szerver ]
                                                                      |
  [ Újrapróbálás ] <--- (onError: 401 Hiba esetén Refresh hívás) <--- [ 401 Hiba ]
```

---

## Kódpéldák

### 1. Dio Interceptor implementálása a Token-frissítés kezelésére

```dart
// lib/core/network/auth_interceptor.dart
import 'package:dio/dio.dart';
import '../services/secure_token_storage.dart';

class AuthInterceptor extends Interceptor {
  final SecureTokenStorage tokenStorage;
  final Dio dio; // Ugyanaz a Dio példány az újrapróbálásokhoz

  AuthInterceptor({required this.tokenStorage, required this.dio});

  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) async {
    // 1. Megnézzük, hogy van-e elmentett Access Tokenünk
    final accessToken = await tokenStorage.getAccessToken();

    if (accessToken != null) {
      // 2. Ha van, automatikusan hozzáadjuk az Authorization fejlécet
      options.headers['Authorization'] = 'Bearer $accessToken';
    }

    return handler.next(options); // Folytatja a kérést
  }

  @override
  void onError(DioException err, ErrorInterceptorHandler handler) async {
    // 3. Megnézzük, hogy 401 Unauthorized hibát kaptunk-e
    if (err.response?.statusCode == 401) {
      final refreshToken = await tokenStorage.getRefreshToken();

      if (refreshToken != null) {
        try {
          // Készítünk egy külön Dio példányt a Refresh végponthoz,
          // hogy elkerüljük a végtelen ciklust (hurok-hívások)
          final refreshDio = Dio(BaseOptions(baseUrl: dio.options.baseUrl));
          
          final response = await refreshDio.post(
            '/auth/refresh',
            data: {'refresh_token': refreshToken},
          );

          if (response.statusCode == 200) {
            final newAccessToken = response.data['access_token'] as String;
            final newRefreshToken = response.data['refresh_token'] as String;

            // Új tokenek mentése
            await tokenStorage.saveTokens(
              accessToken: newAccessToken,
              refreshToken: newRefreshToken,
            );

            // Frissítsük az eredeti kérés fejlécét az új tokennel
            final requestOptions = err.requestOptions;
            requestOptions.headers['Authorization'] = 'Bearer $newAccessToken';

            // Kérés újraindítása az új adatokkal
            final clonedRequest = await dio.request(
              requestOptions.path,
              options: Options(
                method: requestOptions.method,
                headers: requestOptions.headers,
              ),
              data: requestOptions.data,
              queryParameters: requestOptions.queryParameters,
            );

            return handler.resolve(clonedRequest); // Visszaadjuk a sikeres választ az appnak
          }
        } catch (e) {
          // Ha a refresh hívás is elbukik (pl. lejárt a refresh token is)
          await tokenStorage.clearTokens();
          // Itt értesíthetjük a rendszert (pl. egy event bus-on vagy provideren keresztül) a kijelentkeztetésről
          return handler.next(err);
        }
      }
    }

    return handler.next(err); // Ha nem 401 volt, továbbküldjük a hibát
  }
}
```

### 2. Autentikációs Repository és Állapotkezelő (Auth Provider)

```dart
// lib/features/auth/domain/repositories/auth_repository.dart
abstract class AuthRepository {
  Future<bool> login(String email, String password);
  Future<void> logout();
  Future<bool> checkAuthStatus();
}
```

```dart
// lib/features/auth/data/repositories/auth_repository_impl.dart
import 'package:dio/dio.dart';
import '../../../core/services/secure_token_storage.dart';
import '../../domain/repositories/auth_repository.dart';

class AuthRepositoryImpl implements AuthRepository {
  final Dio dio;
  final SecureTokenStorage tokenStorage;

  AuthRepositoryImpl({required this.dio, required this.tokenStorage});

  @override
  Future<bool> login(String email, String password) async {
    try {
      final response = await dio.post(
        '/auth/login',
        data: {'email': email, 'password': password},
      );

      if (response.statusCode == 200) {
        final accessToken = response.data['access_token'] as String;
        final refreshToken = response.data['refresh_token'] as String;

        await tokenStorage.saveTokens(
          accessToken: accessToken,
          refreshToken: refreshToken,
        );
        return true;
      }
      return false;
    } catch (e) {
      return false;
    }
  }

  @override
  Future<void> logout() async {
    try {
      // Küldjük el a logout hívást a szervernek is, hogy invalidálja a tokent
      await dio.post('/auth/logout');
    } catch (_) {
      // Ha offline vagyunk vagy elbukik, a lokális törlést akkor is meg kell tenni
    } finally {
      await tokenStorage.clearTokens();
    }
  }

  @override
  Future<bool> checkAuthStatus() async {
    final token = await tokenStorage.getAccessToken();
    if (token == null) return false;

    try {
      // Ellenőrizzük a tokent egy védett végponton keresztül (pl. /auth/me)
      final response = await dio.get('/auth/me');
      return response.statusCode == 200;
    } catch (e) {
      // Ha 401 volt, az interceptor megpróbálta frissíteni. Ha itt vagyunk, valószínűleg nem sikerült
      return false;
    }
  }
}
```

```dart
// lib/features/auth/presentation/providers/auth_provider.dart
import 'package:flutter/material.dart';
import '../../domain/repositories/auth_repository.dart';

enum AuthStatus { authenticated, unauthenticated, checking }

class AuthProvider extends ChangeNotifier {
  final AuthRepository authRepository;

  AuthProvider({required this.authRepository}) {
    checkCurrentStatus();
  }

  AuthStatus _status = AuthStatus.checking;
  AuthStatus get status => _status;

  String _errorMessage = '';
  String get errorMessage => _errorMessage;

  Future<void> checkCurrentStatus() async {
    _status = AuthStatus.checking;
    notifyListeners();

    final isAuthenticated = await authRepository.checkAuthStatus();
    
    if (isAuthenticated) {
      _status = AuthStatus.authenticated;
    } else {
      _status = AuthStatus.unauthenticated;
    }
    notifyListeners();
  }

  Future<void> loginUser(String email, String password) async {
    _status = AuthStatus.checking;
    _errorMessage = '';
    notifyListeners();

    final success = await authRepository.login(email, password);

    if (success) {
      _status = AuthStatus.authenticated;
    } else {
      _status = AuthStatus.unauthenticated;
      _errorMessage = 'Sikertelen bejelentkezés. Ellenőrizd az adatokat!';
    }
    notifyListeners();
  }

  Future<void> logoutUser() async {
    await authRepository.logout();
    _status = AuthStatus.unauthenticated;
    notifyListeners();
  }

  // Globális eseményként hívható meg az Interceptor-ból kényszerített kijelentkezéskor
  void forceLogout() {
    _status = AuthStatus.unauthenticated;
    _errorMessage = 'A munkamenet lejárt. Kérjük, jelentkezz be újra!';
    notifyListeners();
  }
}
```

---

## Gyakorlófeladatok & Megoldások

### Gyakorlófeladat
Készíts egy olyan interceptort (`PermissionInterceptor`), amely elkapja a 403 Forbidden hibákat (amikor a felhasználó be van jelentkezve, de nincs jogosultsága egy funkcióhoz) és megjelenít egy globális figyelmeztető dialógust vagy Toast üzenetet anélkül, hogy a felhasználót kijelentkeztetné.

### Megoldás

```dart
// lib/core/network/permission_interceptor.dart
import 'package:dio/dio.dart';
import 'package:flutter/material.dart';

class PermissionInterceptor extends Interceptor {
  // Egy globális kulcs segítségével elérhetjük a BuildContext-et widget fa nélkül is
  final GlobalKey<NavigatorState> navigatorKey;

  PermissionInterceptor({required this.navigatorKey});

  @override
  void onError(DioException err, ErrorInterceptorHandler handler) {
    if (err.response?.statusCode == 403) {
      final context = navigatorKey.currentContext;
      if (context != null) {
        // Megjelenítünk egy szép Material banner-t vagy dialógust a képernyőn
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Hiba: Nincs jogosultságod a művelet végrehajtásához!'),
            backgroundColor: Colors.redAccent,
            duration: Duration(seconds: 4),
          ),
        );
      }
    }
    return handler.next(err); // Továbbengedjük a hibát a hívónak
  }
}
```

---

## Heti Mini Projekt: Bejelentkezős Profil App

**Projekt leírása:**
Készíts egy teljes bejelentkezési folyamatot kezelő alkalmazást. Az app induláskor ellenőrizze a bejelentkezési állapotot (splash screen alatt). Ha a felhasználó be van jelentkezve, vigye a Profil oldalra, egyébként a Login oldalra.
A backend működését egy beépített Mock HTTP klienssel szimuláljuk, amely valós időben reagál a helyes és helytelen tokenekre, valamint támogatja a `/auth/refresh` végpontot.

### Teljes, futtatható kód

```dart
// lib/main.dart
import 'package:flutter/material.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:dio/dio.dart';
import 'package:provider/provider.dart';

// --- MOCK BACKEND ADATOK ÉS DIO ADAPTER ---
// Szimulálja a valós hálózati működést tokenekkel
class MockAuthAdapter extends HttpClientAdapter {
  @override
  Future<ResponseBody> fetch(
    RequestOptions options,
    Stream<void>? requestStream,
    Future<void>? cancelFuture,
  ) async {
    final path = options.path;
    final method = options.method;

    if (path.contains('/auth/login') && method == 'POST') {
      return ResponseBody.fromString(
        '{"access_token": "valid_access_token_123", "refresh_token": "valid_refresh_token_789"}',
        200,
        headers: {
          Headers.contentTypeHeader: [Headers.jsonContentType],
        },
      );
    }

    if (path.contains('/auth/refresh') && method == 'POST') {
      return ResponseBody.fromString(
        '{"access_token": "new_access_token_abc", "refresh_token": "new_refresh_token_xyz"}',
        200,
        headers: {
          Headers.contentTypeHeader: [Headers.jsonContentType],
        },
      );
    }

    if (path.contains('/auth/me') && method == 'GET') {
      final authHeader = options.headers['Authorization'] as String?;
      if (authHeader == 'Bearer valid_access_token_123' || authHeader == 'Bearer new_access_token_abc') {
        return ResponseBody.fromString(
          '{"id": "user-456", "email": "tanulo@prstart.hu", "name": "PrStart Tanulo"}',
          200,
          headers: {
            Headers.contentTypeHeader: [Headers.jsonContentType],
          },
        );
      } else {
        // Ha nem érvényes az access token, küldjünk vissza 401 Unauthorized-et
        return ResponseBody.fromString(
          '{"message": "Unauthorized"}',
          401,
          headers: {
            Headers.contentTypeHeader: [Headers.jsonContentType],
          },
        );
      }
    }

    return ResponseBody.fromString('{"message": "Not Found"}', 404);
  }

  @override
  void close({bool force = false}) {}
}

// --- SECURE STORAGE ---
class TokenStorage {
  final _storage = const FlutterSecureStorage();

  Future<void> save(String access, String refresh) async {
    await _storage.write(key: 'acc', value: access);
    await _storage.write(key: 'ref', value: refresh);
  }

  Future<String?> getAccess() => _storage.read(key: 'acc');
  Future<String?> getRefresh() => _storage.read(key: 'ref');
  Future<void> clear() async {
    await _storage.delete(key: 'acc');
    await _storage.delete(key: 'ref');
  }
}

// --- APP STATE / PROVIDER ---
class AppAuthProvider extends ChangeNotifier {
  final Dio dio;
  final TokenStorage storage;
  bool _isChecking = true;
  bool _isAuthenticated = false;
  String? _userName;
  String? _userEmail;
  String _error = '';

  AppAuthProvider({required this.dio, required this.storage}) {
    _initInterceptor();
    checkAuthStatus();
  }

  bool get isChecking => _isChecking;
  bool get isAuthenticated => _isAuthenticated;
  String get userName => _userName ?? '';
  String get userEmail => _userEmail ?? '';
  String get error => _error;

  void _initInterceptor() {
    dio.interceptors.add(
      InterceptorsWrapper(
        onRequest: (options, handler) async {
          final acc = await storage.getAccess();
          if (acc != null) {
            options.headers['Authorization'] = 'Bearer $acc';
          }
          return handler.next(options);
        },
        onError: (err, handler) async {
          if (err.response?.statusCode == 401) {
            final ref = await storage.getRefresh();
            if (ref != null) {
              try {
                // Token refresh kérés küldése
                final refreshDio = Dio()..httpClientAdapter = MockAuthAdapter();
                final res = await refreshDio.post('/auth/refresh', data: {'refresh_token': ref});
                
                final newAcc = res.data['access_token'] as String;
                final newRef = res.data['refresh_token'] as String;
                await storage.save(newAcc, newRef);

                // Eredeti kérés újraindítása
                final opts = err.requestOptions;
                opts.headers['Authorization'] = 'Bearer $newAcc';
                final clone = await dio.request(
                  opts.path,
                  options: Options(method: opts.method, headers: opts.headers),
                  data: opts.data,
                );
                return handler.resolve(clone);
              } catch (_) {
                await storage.clear();
                _isAuthenticated = false;
                notifyListeners();
              }
            }
          }
          return handler.next(err);
        },
      ),
    );
  }

  Future<void> checkAuthStatus() async {
    _isChecking = true;
    _error = '';
    notifyListeners();

    final acc = await storage.getAccess();
    if (acc == null) {
      _isAuthenticated = false;
      _isChecking = false;
      notifyListeners();
      return;
    }

    try {
      final res = await dio.get('/auth/me');
      _userName = res.data['name'] as String;
      _userEmail = res.data['email'] as String;
      _isAuthenticated = true;
    } catch (_) {
      _isAuthenticated = false;
    } finally {
      _isChecking = false;
      notifyListeners();
    }
  }

  Future<void> login(String email, String password) async {
    _isChecking = true;
    _error = '';
    notifyListeners();

    try {
      final res = await dio.post('/auth/login', data: {'email': email, 'password': password});
      final acc = res.data['access_token'] as String;
      final ref = res.data['refresh_token'] as String;

      await storage.save(acc, ref);
      await checkAuthStatus();
    } catch (e) {
      _error = 'Hiba a bejelentkezés során: ${e.toString()}';
      _isAuthenticated = false;
      _isChecking = false;
      notifyListeners();
    }
  }

  Future<void> logout() async {
    await storage.clear();
    _isAuthenticated = false;
    _userName = null;
    _userEmail = null;
    notifyListeners();
  }

  // Teszt céljából elrontjuk a tokent a háttértárban, szimulálva egy lejárt tokent
  Future<void> simulateExpiredToken() async {
    await storage.save('expired_token_signature_broken', 'valid_refresh_token_789');
    await checkAuthStatus();
  }
}

// --- UI SCREENS ---
void main() {
  final dio = Dio()..httpClientAdapter = MockAuthAdapter();
  final storage = TokenStorage();

  runApp(
    ChangeNotifierProvider(
      create: (_) => AppAuthProvider(dio: dio, storage: storage),
      child: const MaterialApp(
        home: AuthCheckWrapper(),
      ),
    ),
  );
}

class AuthCheckWrapper extends StatelessWidget {
  const AuthCheckWrapper({super.key});

  @override
  Widget build(BuildContext context) {
    final auth = context.watch<AppAuthProvider>();

    if (auth.isChecking) {
      return const Scaffold(
        body: Center(child: CircularProgressIndicator()),
      );
    }

    return auth.isAuthenticated ? const ProfilePage() : const LoginPage();
  }
}

class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final _emailCtrl = TextEditingController(text: 'tanulo@prstart.hu');
  final _passCtrl = TextEditingController(text: 'secret123');

  @override
  Widget build(BuildContext context) {
    final auth = context.read<AppAuthProvider>();
    final error = context.select((AppAuthProvider a) => a.error);

    return Scaffold(
      appBar: AppBar(title: const Text('Bejelentkezés')),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            TextField(controller: _emailCtrl, decoration: const InputDecoration(labelText: 'Email')),
            TextField(
              controller: _passCtrl,
              decoration: const InputDecoration(labelText: 'Jelszó'),
              obscureText: true,
            ),
            const SizedBox(height: 20),
            if (error.isNotEmpty) ...[
              Text(error, style: const TextStyle(color: Colors.red)),
              const SizedBox(height: 10),
            ],
            ElevatedButton(
              onPressed: () => auth.login(_emailCtrl.text, _passCtrl.text),
              child: const Text('Belépés'),
            ),
          ],
        ),
      ),
    );
  }
}

class ProfilePage extends StatelessWidget {
  const ProfilePage({super.key});

  @override
  Widget build(BuildContext context) {
    final auth = context.watch<AppAuthProvider>();

    return Scaffold(
      appBar: AppBar(title: const Text('Profilom')),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(20.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Icon(Icons.account_circle, size: 100, color: Colors.blue),
              const SizedBox(height: 20),
              Text('Név: ${auth.userName}', style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
              Text('Email: ${auth.userEmail}', style: const TextStyle(fontSize: 16)),
              const SizedBox(height: 30),
              ElevatedButton(
                onPressed: auth.logout,
                style: ElevatedButton.styleFrom(backgroundColor: Colors.redAccent),
                child: const Text('Kijelentkezés', style: TextStyle(color: Colors.white)),
              ),
              const SizedBox(height: 10),
              TextButton(
                onPressed: auth.simulateExpiredToken,
                child: const Text('Token Lejárat Szimuláció (Silent Refresh teszt)'),
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

1.  **Mi az a "Silent Token Refresh" (csendes token-frissítés), és miért jó a felhasználónak?**
    *   *Válasz:* A csendes token-frissítés egy olyan folyamat, amely során a felhasználó észrevétlenül kap új jogosultságot (új Access Tokent) a szervertől a háttérben. Amikor egy API kérés lejárati hiba (401 Unauthorized) miatt meghiúsul, az interceptor automatikusan elküldi a Refresh Tokent a frissítési végpontra. Ha a szerver új tokent ad vissza, az interceptor lementi azt, majd automatikusan újra próbálja az eredeti kérést. A felhasználó ebből semmit sem észlel (nincs hibaüzenet, nincs kijelentkezés), a folyamat zökkenőmentes marad.
2.  **Miért kell vigyázni, amikor a Refresh végpontot hívjuk meg az Interceptoron belül?**
    *   *Válasz:* Amikor az interceptoron belül elindítjuk a `/auth/refresh` kérést, ehhez nem szabad ugyanazt a konfigurált Dio példányt használni, amelyen az interceptor fut. Ha ugyanazt a Dio példányt használnánk, és a refresh kérés is véletlenül 401-es hibát kapna (pl. érvénytelen refresh token miatt), a rendszer újra meghívná önmagán belül az `onError` interceptort, ami végtelen hívási ciklushoz (hurokhoz) vezetne, összeomlasztva a mobilalkalmazást és túlterhelve a backend szervert. Ezért a refresh hívást mindig egy tiszta, interceptor nélküli Dio vagy Http példánnyal kell végrehajtani.
3.  **Mi a teendő, ha a Refresh Token is érvénytelenné válik (pl. lejárt a 30 napos érvényessége)?**
    *   *Válasz:* Ha a Refresh Token is érvénytelen vagy lejárt, a szerver 400 Bad Request vagy 401 Unauthorized választ fog adni a refresh kérésre. Ekkor a kliens már semmilyen módon nem tud új hozzáférési tokent szerezni. A lokális biztonságos tárolóból azonnal törölni kell az összes token-adatot, és a felhasználót vissza kell irányítani a bejelentkező (Login) képernyőre, egyértelmű üzenettel tájékoztatva őt arról, hogy a munkamenete lejárt.
4.  **Milyen kockázatot jelent, ha az SSL Pinning hiányzik egy éles banki vagy szenzitív alkalmazásból?**
    *   *Válasz:* Bár a HTTPS titkosítja az adatfolyamot a mobil és a szerver között, a támadók egy ún. **Man-in-the-Middle (MitM)** támadással (pl. egy hamis, de a telefonon kézzel megbízhatónak jelölt gyökértanúsítvány telepítésével) felbonthatják és lehallgathatják a titkosított kapcsolatot. Az SSL Pinning segítségével a mobilalkalmazásba beleégetjük (pineljük) a backend szerver valódi tanúsítványát vagy annak ujjlenyomatát. Így a telefon akkor sem fogja elfogadni a kapcsolatot, ha a rendszer szerint a hamis tanúsítvány érvényes lenne, teljesen megakadályozva a lehallgatást.
5.  **Hogyan növelhetjük meg az alkalmazás indítási sebességét automatikus beléptetésnél?**
    *   *Válasz:* Amikor az app elindul, ne várjunk a hálózati kérés lefutására a Splash screen alatt, ha a token fizikailag sincs meg. Először csak a lokális `SecureStorage`-ból olvassuk be a token meglétét (ami mikroszekundumok alatt megvan). Ha nincs token, azonnal irányítsuk a felhasználót a Login képernyőre. Ha van token, a háttérben elindíthatjuk a `/auth/me` ellenőrzést, miközben a felhasználónak már a Dashboard keretrendszerét mutatjuk (optimista UI betöltés), vagy egy nagyon gyors, natív Splash animáció mögé rejtjük a hitelesítési hálózati késleltetést.
