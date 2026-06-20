# Modellezés

A Dart nyelvben az immutable (módosíthatatlan) adatstruktúrák és a típusbiztosság kiemelt fontosságúak. A kézzel írt JSON szerializáció viszont sok hibalehetőséget rejt.

## 📦 Ajánlott Csomagok:
* **`freezed`:** Kódgenerátor immutable osztályokhoz, amely automatikusan elkészíti a `copyWith`, `toString`, `operator ==` metódusokat és támogatja a union típusokat.
* **`json_serializable`:** Létrehozza a `fromJson` és `toJson` konverziós függvényeket.

### Freezed Példa:
```dart
@freezed
class User with _$User {
  const factory User({
    required String id,
    required String name,
    required String email,
    @Default(false) bool isAdmin,
  }) = _User;

  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
}
```