# HTTP/API

A külső backend szerverekkel való kommunikáció a mobilalkalmazások többségének alapfeltétele.

## 📦 Ajánlott Csomagok:
* **`dio`:** Rendkívül robusztus HTTP kliens, amely támogatja az interceptorokat, globális konfigurációkat, fájl feltöltést, timeout kezelést és kérések megszakítását.
* **`pretty_dio_logger`:** Fejlesztés során gyönyörűen formázva naplózza a konzolra a kéréseket és válaszokat.

### Dio interceptor példa:
```dart
final dio = Dio();
dio.interceptors.add(InterceptorsWrapper(
  onRequest: (options, handler) {
    // Token hozzáadása minden kéréshez
    options.headers['Authorization'] = 'Bearer $token';
    return handler.next(options);
  },
));
```