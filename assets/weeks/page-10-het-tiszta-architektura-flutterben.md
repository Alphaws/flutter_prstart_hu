# 10. hét — Tiszta architektúra Flutterben

## Cél
A lecke célja, hogy elsajátítsd a **Tiszta Architektúra (Clean Architecture)** elveit Flutter környezetben. Megtanulod, hogyan válaszd szét az alkalmazásodat rétegekre (Presentation, Domain, Data), hogyan csökkentsd a komponensek közötti szoros csatolást (coupling), és hogyan használd a **GetIt** szolgáltatáslokátort (Service Locator) a függőségek feloldására és a tesztelhetőség maximalizálására. A hét végére képes leszel egy skálázható, karbantartható és tesztelhető projektstruktúrát önállóan felépíteni.

---

## Elmélet

### 1. A Tiszta Architektúra (Clean Architecture) alapelvei
Robert C. Martin („Uncle Bob”) által megalkotott architektúra célja a szoftver kódjának olyan rétegekre tagolása, amelyek függetlenek a keretrendszerektől, az adatbázisoktól, a felhasználói felülettől és bármely külső tényezőtől.

Az architektúra legfőbb szabálya a **Függőségi Szabály (Dependency Rule)**: a forráskód-függőségek csak befelé mutathatnak. A belső körök (üzleti logika) semmit sem tudhatnak a külső körökről (UI, adatbázis, hálózat).

```text
  +---------------------------------------+
  |              DATA LAYER               |
  |  (Models, Data Sources, Repositories  |
  |              Implementations)         |
  +-------------------+-------------------+
                      | (Valósítja meg)
                      v
  +-------------------+-------------------+
  |             DOMAIN LAYER              |
  |    (Entities, Use Cases, Repository   |
  |              Interfaces)              |
  +-------------------+-------------------+
                      ^
                      | (Meghívja a Use Case-eket)
  +-------------------+-------------------+
  |          PRESENTATION LAYER           |
  |    (Widgets, Pages, State Providers/  |
  |             ViewModels/Blocs)         |
  +---------------------------------------+
```

### 2. A három fő réteg Flutterben

#### A. Domain réteg (Domain Layer)
Ez az alkalmazás legbelső, legfontosabb rétege. Nem függ semmitől (tiszta Dart kód, nincs benne Flutter widget vagy harmadik fél által készített csomag-függőség, pl. `Dio` vagy `shared_preferences`).
*   **Entities (Entitások):** Az alapvető üzleti modellek. Egyszerű Dart osztályok, amelyek a valós üzleti entitásokat reprezentálják.
*   **Use Cases (Üzleti esetek):** Az alkalmazás specifikus üzleti logikáját tartalmazó osztályok (pl. `GetUserProfile`, `AuthenticateUser`). Egy use case egyetlen feladatot hajt végre.
*   **Repositories (Interfészek):** Absztrakt osztályok, amelyek definiálják, milyen adat-műveletekre van szüksége a domainnek. Az implementációjuk már a Data rétegben történik.

#### B. Data réteg (Data Layer)
Ez a réteg felelős az adatok beszerzéséért, mentéséért és formázásáért. Itt kommunikálunk API-kkal vagy helyi adatbázisokkal.
*   **Models (DTO - Data Transfer Object):** Az entitások kiterjesztései, amelyek tartalmazzák a JSON-szerializációs logikát (`fromJson`, `toJson`).
*   **Data Sources (Adatforrások):** 
    *   *Remote Data Source:* API hívásokat bonyolít (pl. `Dio` használatával).
    *   *Local Data Source:* Helyi perzisztens tárolást kezel (pl. SQLite, Secure Storage).
*   **Repositories (Implementációk):** Megvalósítják a Domain rétegben definiált absztrakt repository interfészeket. Döntést hoznak az adatok áramlásáról (pl. ha nincs net, a lokális adatforrást kérdezik le, különben a távolit).

#### C. Presentation réteg (Presentation Layer)
Ez a felhasználói felületért és a felhasználói interakciókért felelős réteg.
*   **Widgets / Pages:** A Flutter UI elemek.
*   **State Management (Providers / Blocs / Notifiers):** Kezelik a UI állapotát, meghívják a Domain réteg Use Case-eit, és a visszakapott adatokat UI-állapottá alakítják (pl. betöltési állapot, hibaállapot, sikeres adatállapot).

### 3. Dependency Injection (DI) és a GetIt szerepe
A tiszta architektúrában a rétegek lazán csatlakoznak egymáshoz. Annak érdekében, hogy a `Presentation` rétegben lévő `Notifier` el tudja érni a `UseCase`-t, a `UseCase` a `Repository`-t, a `Repository` pedig a `DataSource`-okat anélkül, hogy manuálisan példányosítanánk őket mindenhol, **függőségi injektálást** használunk.

A **GetIt** egy rendkívül gyors és egyszerű *Service Locator* Flutterben. Segítségével egy központi helyen regisztrálhatjuk az osztályainkat:
*   `Singleton` vagy `LazySingleton`: Az osztályból egyetlen példány jön létre az app teljes élettartama alatt (pl. adatbázisok, API kliensek).
*   `Factory`: Minden lekéréskor új példány jön létre (pl. UI állapotkezelők).

---

## Kódpéldák

A következő példában egy felhasználói profil lekérését valósítjuk meg tiszta architektúrában.

### 1. Domain réteg: Entitás, Repository interfész és Use Case

```dart
// lib/features/auth/domain/entities/user_entity.dart
class UserEntity {
  final String id;
  final String email;
  final String name;

  const UserEntity({
    required this.id,
    required this.email,
    required this.name,
  });
}
```

```dart
// lib/features/auth/domain/repositories/user_repository.dart
import '../entities/user_entity.dart';

abstract class UserRepository {
  Future<UserEntity> getUserProfile(String userId);
}
```

```dart
// lib/features/auth/domain/usecases/get_user_profile.dart
import '../entities/user_entity.dart';
import '../repositories/user_repository.dart';

class GetUserProfileUseCase {
  final UserRepository repository;

  GetUserProfileUseCase(this.repository);

  Future<UserEntity> call(String userId) async {
    // Itt elvégezhető bármilyen üzleti ellenőrzés vagy validáció
    if (userId.trim().isEmpty) {
      throw Exception('A felhasználó azonosító nem lehet üres!');
    }
    return await repository.getUserProfile(userId);
  }
}
```

### 2. Data réteg: Model, Adatforrás és Repository implementáció

```dart
// lib/features/auth/data/models/user_model.dart
import '../../domain/entities/user_entity.dart';

class UserModel extends UserEntity {
  const UserModel({
    required super.id,
    required super.email,
    required super.name,
  });

  factory UserModel.fromJson(Map<String, dynamic> json) {
    return UserModel(
      id: json['id'] as String,
      email: json['email'] as String,
      name: json['name'] as String,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'email': email,
      'name': name,
    };
  }
}
```

```dart
// lib/features/auth/data/datasources/user_remote_data_source.dart
import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/user_model.dart';

abstract class UserRemoteDataSource {
  Future<UserModel> fetchUserFromApi(String userId);
}

class UserRemoteDataSourceImpl implements UserRemoteDataSource {
  final http.Client client;

  UserRemoteDataSourceImpl({required this.client});

  @override
  Future<UserModel> fetchUserFromApi(String userId) async {
    final response = await client.get(
      Uri.parse('https://api.prstart.hu/users/$userId'),
      headers: {'Content-Type': 'application/json'},
    );

    if (response.statusCode == 200) {
      final Map<String, dynamic> jsonMap = json.decode(response.body) as Map<String, dynamic>;
      return UserModel.fromJson(jsonMap);
    } else {
      throw Exception('Szerver hiba történt a profil lekérése során.');
    }
  }
}
```

```dart
// lib/features/auth/data/repositories/user_repository_impl.dart
import '../../domain/entities/user_entity.dart';
import '../../domain/repositories/user_repository.dart';
import '../datasources/user_remote_data_source.dart';

class UserRepositoryImpl implements UserRepository {
  final UserRemoteDataSource remoteDataSource;

  UserRepositoryImpl({required this.remoteDataSource});

  @override
  Future<UserEntity> getUserProfile(String userId) async {
    // Itt kezelhetnénk az offline cache-t is (Local Data Source)
    return await remoteDataSource.fetchUserFromApi(userId);
  }
}
```

### 3. Dependency Injection (GetIt) beállítás

```dart
// lib/injection_container.dart
import 'package:get_it/get_it.dart';
import 'package:http/http.dart' as http;
import 'features/auth/data/datasources/user_remote_data_source.dart';
import 'features/auth/data/repositories/user_repository_impl.dart';
import 'features/auth/domain/repositories/user_repository.dart';
import 'features/auth/domain/usecases/get_user_profile.dart';
import 'features/auth/presentation/providers/user_profile_notifier.dart';

final sl = GetIt.instance; // sl: Service Locator

Future<void> initDependencies() async {
  // 1. External dependencies (Külső függőségek)
  sl.registerLazySingleton<http.Client>(() => http.Client());

  // 2. Data sources (Adatforrások)
  sl.registerLazySingleton<UserRemoteDataSource>(
    () => UserRemoteDataSourceImpl(client: sl<http.Client>()),
  );

  // 3. Repositories (Repository implementációk)
  sl.registerLazySingleton<UserRepository>(
    () => UserRepositoryImpl(remoteDataSource: sl<UserRemoteDataSource>()),
  );

  // 4. Use cases (Üzleti esetek)
  sl.registerLazySingleton<GetUserProfileUseCase>(
    () => GetUserProfileUseCase(sl<UserRepository>()),
  );

  // 5. Presentation - Notifiers/ViewModels (Mindig Factory!)
  sl.registerFactory<UserProfileNotifier>(
    () => UserProfileNotifier(getUserProfileUseCase: sl<GetUserProfileUseCase>()),
  );
}
```

### 4. Presentation réteg: UI állapotkezelő és Widget

```dart
// lib/features/auth/presentation/providers/user_profile_notifier.dart
import 'package:flutter/material.dart';
import '../../domain/entities/user_entity.dart';
import '../../domain/usecases/get_user_profile.dart';

enum UserProfileStatus { initial, loading, loaded, error }

class UserProfileNotifier extends ChangeNotifier {
  final GetUserProfileUseCase getUserProfileUseCase;

  UserProfileNotifier({required this.getUserProfileUseCase});

  UserProfileStatus _status = UserProfileStatus.initial;
  UserProfileStatus get status => _status;

  UserEntity? _user;
  UserEntity? get user => _user;

  String _errorMessage = '';
  String get errorMessage => _errorMessage;

  Future<void> loadUserProfile(String userId) async {
    _status = UserProfileStatus.loading;
    notifyListeners();

    try {
      _user = await getUserProfileUseCase(userId);
      _status = UserProfileStatus.loaded;
    } catch (e) {
      _errorMessage = e.toString();
      _status = UserProfileStatus.error;
    }
    notifyListeners();
  }
}
```

```dart
// lib/features/auth/presentation/pages/user_profile_page.dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../../../injection_container.dart';
import '../providers/user_profile_notifier.dart';

class UserProfilePage extends StatelessWidget {
  final String userId;

  const UserProfilePage({super.key, required this.userId});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Felhasználói Profil')),
      body: ChangeNotifierProvider<UserProfileNotifier>(
        // A GetIt segítségével kérjük el az állapotkezelőt
        create: (_) => sl<UserProfileNotifier>()..loadUserProfile(userId),
        child: Consumer<UserProfileNotifier>(
          builder: (context, notifier, child) {
            if (notifier.status == UserProfileStatus.loading) {
              return const Center(child: CircularProgressIndicator());
            }

            if (notifier.status == UserProfileStatus.error) {
              return Center(
                child: Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Text(
                    'Hiba: ${notifier.errorMessage}',
                    style: const TextStyle(color: Colors.red, fontSize: 16),
                  ),
                ),
              );
            }

            if (notifier.status == UserProfileStatus.loaded && notifier.user != null) {
              final user = notifier.user!;
              return Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text('Név: ${user.name}', style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
                    const SizedBox(height: 8),
                    Text('Email: ${user.email}', style: const TextStyle(fontSize: 16)),
                    const SizedBox(height: 8),
                    Text('ID: ${user.id}', style: const TextStyle(fontSize: 12, color: Colors.grey)),
                  ],
                ),
              );
            }

            return const Center(child: Text('Nincs megjeleníthető adat.'));
          },
        ),
      ),
    );
  }
}
```

```dart
// lib/main.dart
import 'package:flutter/material.dart';
import 'injection_container.dart' as di;
import 'features/auth/presentation/pages/user_profile_page.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await di.initDependencies(); // Dependency injection inicializálása
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Clean Architecture Demo',
      theme: ThemeData(primarySwatch: Colors.indigo),
      home: const UserProfilePage(userId: 'user-123'),
    );
  }
}
```

---

## Gyakorlófeladatok & Megoldások

### Gyakorlófeladat
Alakítsd át az alkalmazásodat úgy, hogy a profil lekérése ne API-ból történjen, hanem egy statikus mock adatforrásból (`UserMockDataSource`), anélkül, hogy a `Presentation` réteget vagy a `Domain` réteg use case-ét módosítanád.

### Megoldás

1.  Hozzuk létre a mock adatforrást a Data rétegben:
```dart
// lib/features/auth/data/datasources/user_mock_data_source.dart
import '../models/user_model.dart';
import 'user_remote_data_source.dart';

class UserMockDataSourceImpl implements UserRemoteDataSource {
  @override
  Future<UserModel> fetchUserFromApi(String userId) async {
    // Szimuláljunk hálózati késleltetést
    await Future.delayed(const Duration(milliseconds: 800));
    return UserModel(
      id: userId,
      email: 'mock.elemer@prstart.hu',
      name: 'Mock Elemer (Teszt)',
    );
  }
}
```

2.  Módosítsuk az `injection_container.dart` fájlban a regisztrációt. A korábbi `UserRemoteDataSourceImpl` helyett az új `UserMockDataSourceImpl`-t regisztráljuk be:
```dart
// lib/injection_container.dart módosítása
// ...
sl.registerLazySingleton<UserRemoteDataSource>(
  () => UserMockDataSourceImpl(), // Cserélve a valódi implementáció a mockra
);
// ...
```
Ezzel a lépéssel az egész alkalmazás adatforrását kicseréltük anélkül, hogy a felületet (UI) vagy az üzleti logikát (Domain) akár egyetlen soron is módosítani kellett volna. Ez a Clean Architecture és a Dependency Injection igazi ereje!

---

## Heti Mini Projekt: Clean Todo App

**Projekt leírása:**
Készíts egy teljesen működőképes teendő (Todo) kezelő alkalmazást Clean Architecture szerint felépítve. Az alkalmazásban lehessen megtekinteni a listát, hozzáadni egy új teendőt, törölni egy meglévőt, valamint váltani annak befejezett állapotát.

A projektnek a következő felépítést kell követnie:
1.  **Domain:** `TodoEntity`, `TodoRepository` (absztrakt interfész), `GetTodosUseCase`, `AddTodoUseCase`, `DeleteTodoUseCase`, `ToggleTodoStatusUseCase`.
2.  **Data:** `TodoModel` (JSON parserekkel), `TodoLocalDataSource` (akár egy egyszerű, memóriában tárolt listával megvalósítva), `TodoRepositoryImpl`.
3.  **Presentation:** `TodoListNotifier` (állapotkezelő), `TodoPage` és `TodoItemWidget` (UI).
4.  **DI:** `GetIt` konfiguráció az app indításakor.

### Teljes kódimplementáció

```dart
// lib/features/todo/domain/entities/todo_entity.dart
class TodoEntity {
  final String id;
  final String title;
  final bool isCompleted;

  const TodoEntity({
    required this.id,
    required this.title,
    this.isCompleted = false,
  });

  TodoEntity copyWith({String? id, String? title, bool? isCompleted}) {
    return TodoEntity(
      id: id ?? this.id,
      title: title ?? this.title,
      isCompleted: isCompleted ?? this.isCompleted,
    );
  }
}
```

```dart
// lib/features/todo/domain/repositories/todo_repository.dart
import '../entities/todo_entity.dart';

abstract class TodoRepository {
  Future<List<TodoEntity>> getTodos();
  Future<void> addTodo(TodoEntity todo);
  Future<void> deleteTodo(String id);
  Future<void> updateTodo(TodoEntity todo);
}
```

```dart
// lib/features/todo/domain/usecases/todo_usecases.dart
import '../entities/todo_entity.dart';
import '../repositories/todo_repository.dart';

class GetTodosUseCase {
  final TodoRepository repository;
  GetTodosUseCase(this.repository);
  Future<List<TodoEntity>> call() => repository.getTodos();
}

class AddTodoUseCase {
  final TodoRepository repository;
  AddTodoUseCase(this.repository);
  Future<void> call(TodoEntity todo) async {
    if (todo.title.trim().isEmpty) {
      throw Exception('A teendő címe nem lehet üres!');
    }
    await repository.addTodo(todo);
  }
}

class DeleteTodoUseCase {
  final TodoRepository repository;
  DeleteTodoUseCase(this.repository);
  Future<void> call(String id) => repository.deleteTodo(id);
}

class UpdateTodoUseCase {
  final TodoRepository repository;
  UpdateTodoUseCase(this.repository);
  Future<void> call(TodoEntity todo) => repository.updateTodo(todo);
}
```

```dart
// lib/features/todo/data/models/todo_model.dart
import '../../domain/entities/todo_entity.dart';

class TodoModel extends TodoEntity {
  const TodoModel({
    required super.id,
    required super.title,
    required super.isCompleted,
  });

  factory TodoModel.fromJson(Map<String, dynamic> json) {
    return TodoModel(
      id: json['id'] as String,
      title: json['title'] as String,
      isCompleted: json['isCompleted'] as bool,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'title': title,
      'isCompleted': isCompleted,
    };
  }

  factory TodoModel.fromEntity(TodoEntity entity) {
    return TodoModel(
      id: entity.id,
      title: entity.title,
      isCompleted: entity.isCompleted,
    );
  }
}
```

```dart
// lib/features/todo/data/datasources/todo_local_data_source.dart
import '../models/todo_model.dart';

abstract class TodoLocalDataSource {
  Future<List<TodoModel>> getCachedTodos();
  Future<void> cacheTodo(TodoModel todo);
  Future<void> removeTodo(String id);
  Future<void> updateTodo(TodoModel todo);
}

// Egyszerű memóriabeli implementáció
class TodoLocalDataSourceImpl implements TodoLocalDataSource {
  final List<TodoModel> _memoryStorage = [
    const TodoModel(id: '1', title: 'Tiszta Architektúra tanulása', isCompleted: true),
    const TodoModel(id: '2', title: 'Mini projekt kódolása', isCompleted: false),
  ];

  @override
  Future<List<TodoModel>> getCachedTodos() async {
    await Future.delayed(const Duration(milliseconds: 300));
    return List.from(_memoryStorage);
  }

  @override
  Future<void> cacheTodo(TodoModel todo) async {
    _memoryStorage.add(todo);
  }

  @override
  Future<void> removeTodo(String id) async {
    _memoryStorage.removeWhere((item) => item.id == id);
  }

  @override
  Future<void> updateTodo(TodoModel todo) async {
    final index = _memoryStorage.indexWhere((item) => item.id == todo.id);
    if (index != -1) {
      _memoryStorage[index] = todo;
    }
  }
}
```

```dart
// lib/features/todo/data/repositories/todo_repository_impl.dart
import '../../domain/entities/todo_entity.dart';
import '../../domain/repositories/todo_repository.dart';
import '../datasources/todo_local_data_source.dart';
import '../models/todo_model.dart';

class TodoRepositoryImpl implements TodoRepository {
  final TodoLocalDataSource localDataSource;

  TodoRepositoryImpl({required this.localDataSource});

  @override
  Future<List<TodoEntity>> getTodos() async {
    return await localDataSource.getCachedTodos();
  }

  @override
  Future<void> addTodo(TodoEntity todo) async {
    await localDataSource.cacheTodo(TodoModel.fromEntity(todo));
  }

  @override
  Future<void> deleteTodo(String id) async {
    await localDataSource.removeTodo(id);
  }

  @override
  Future<void> updateTodo(TodoEntity todo) async {
    await localDataSource.updateTodo(TodoModel.fromEntity(todo));
  }
}
```

```dart
// Dependency injection bővítése
// Illeszd be ezeket a regisztrációkat a meglévő lib/injection_container.dart initDependencies metódusába:
/*
  // Data Source
  sl.registerLazySingleton<TodoLocalDataSource>(() => TodoLocalDataSourceImpl());

  // Repository
  sl.registerLazySingleton<TodoRepository>(() => TodoRepositoryImpl(localDataSource: sl()));

  // Use cases
  sl.registerLazySingleton<GetTodosUseCase>(() => GetTodosUseCase(sl()));
  sl.registerLazySingleton<AddTodoUseCase>(() => AddTodoUseCase(sl()));
  sl.registerLazySingleton<DeleteTodoUseCase>(() => DeleteTodoUseCase(sl()));
  sl.registerLazySingleton<UpdateTodoUseCase>(() => UpdateTodoUseCase(sl()));

  // Notifier
  sl.registerFactory<TodoListNotifier>(
    () => TodoListNotifier(
      getTodosUseCase: sl(),
      addTodoUseCase: sl(),
      deleteTodoUseCase: sl(),
      updateTodoUseCase: sl(),
    ),
  );
*/
```

```dart
// lib/features/todo/presentation/providers/todo_list_notifier.dart
import 'package:flutter/material.dart';
import '../../domain/entities/todo_entity.dart';
import '../../domain/usecases/todo_usecases.dart';

class TodoListNotifier extends ChangeNotifier {
  final GetTodosUseCase getTodosUseCase;
  final AddTodoUseCase addTodoUseCase;
  final DeleteTodoUseCase deleteTodoUseCase;
  final UpdateTodoUseCase updateTodoUseCase;

  TodoListNotifier({
    required this.getTodosUseCase,
    required this.addTodoUseCase,
    required this.deleteTodoUseCase,
    required this.updateTodoUseCase,
  });

  List<TodoEntity> _todos = [];
  List<TodoEntity> get todos => _todos;

  bool _isLoading = false;
  bool get isLoading => _isLoading;

  String _error = '';
  String get error => _error;

  Future<void> fetchTodos() async {
    _isLoading = true;
    _error = '';
    notifyListeners();
    try {
      _todos = await getTodosUseCase();
    } catch (e) {
      _error = e.toString();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<void> addNewTodo(String title) async {
    final newTodo = TodoEntity(
      id: DateTime.now().millisecondsSinceEpoch.toString(),
      title: title,
    );
    try {
      await addTodoUseCase(newTodo);
      await fetchTodos();
    } catch (e) {
      _error = e.toString();
      notifyListeners();
    }
  }

  Future<void> removeTodoItem(String id) async {
    try {
      await deleteTodoUseCase(id);
      await fetchTodos();
    } catch (e) {
      _error = e.toString();
      notifyListeners();
    }
  }

  Future<void> toggleTodoStatus(TodoEntity todo) async {
    final updatedTodo = todo.copyWith(isCompleted: !todo.isCompleted);
    try {
      await updateTodoUseCase(updatedTodo);
      await fetchTodos();
    } catch (e) {
      _error = e.toString();
      notifyListeners();
    }
  }
}
```

```dart
// lib/features/todo/presentation/pages/todo_page.dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../../../injection_container.dart';
import '../providers/todo_list_notifier.dart';

class TodoPage extends StatefulWidget {
  const TodoPage({super.key});

  @override
  State<TodoPage> createState() => _TodoPageState();
}

class _TodoPageState extends State<TodoPage> {
  final TextEditingController _controller = TextEditingController();

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider<TodoListNotifier>(
      create: (_) => sl<TodoListNotifier>()..fetchTodos(),
      child: Scaffold(
        appBar: AppBar(
          title: const Text('Clean Todo App'),
          backgroundColor: Colors.teal,
        ),
        body: Consumer<TodoListNotifier>(
          builder: (context, notifier, child) {
            return Column(
              children: [
                if (notifier.error.isNotEmpty)
                  Container(
                    color: Colors.redAccent,
                    width: double.infinity,
                    padding: const EdgeInsets.all(8.0),
                    child: Text(notifier.error, style: const TextStyle(color: Colors.white)),
                  ),
                Padding(
                  padding: const EdgeInsets.all(12.0),
                  child: Row(
                    children: [
                      Expanded(
                        child: TextField(
                          controller: _controller,
                          decoration: const InputDecoration(
                            labelText: 'Új teendő hozzáadása',
                            border: OutlineInputBorder(),
                          ),
                        ),
                      ),
                      const SizedBox(width: 8),
                      ElevatedButton(
                        onPressed: () {
                          if (_controller.text.isNotEmpty) {
                            notifier.addNewTodo(_controller.text);
                            _controller.clear();
                          }
                        },
                        style: ElevatedButton.styleFrom(
                          backgroundColor: Colors.teal,
                          padding: const EdgeInsets.symmetric(vertical: 16, horizontal: 16),
                        ),
                        child: const Icon(Icons.add, color: Colors.white),
                      )
                    ],
                  ),
                ),
                Expanded(
                  child: notifier.isLoading
                      ? const Center(child: CircularProgressIndicator())
                      : notifier.todos.isEmpty
                          ? const Center(child: Text('Nincs teendőd! Hurrá!'))
                          : ListView.builder(
                              itemCount: notifier.todos.length,
                              itemBuilder: (context, index) {
                                final todo = notifier.todos[index];
                                return ListTile(
                                  title: Text(
                                    todo.title,
                                    style: TextStyle(
                                      decoration: todo.isCompleted
                                          ? TextDecoration.lineThrough
                                          : TextDecoration.none,
                                    ),
                                  ),
                                  leading: Checkbox(
                                    value: todo.isCompleted,
                                    onChanged: (_) => notifier.toggleTodoStatus(todo),
                                  ),
                                  trailing: IconButton(
                                    icon: const Icon(Icons.delete, color: Colors.redAccent),
                                    onPressed: () => notifier.removeTodoItem(todo.id),
                                  ),
                                );
                              },
                            ),
                ),
              ],
            );
          },
        ),
      ),
    );
  }
}
```

---

## Heti Ellenőrző Kérdések

1.  **Miért nem szabad, hogy a Domain réteg függjön a Data vagy a Presentation rétegtől?**
    *   *Válasz:* A Domain réteg tartalmazza az alkalmazás alapvető üzleti logikáját és szabályait. Ha függne a Data rétegtől (pl. adatbázis technológia, API könyvtárak) vagy a Presentation rétegtől (UI widgetek), akkor az üzleti logika sérülékennyé válna a technológiai környezet változásaival szemben. Például egy adatbázis-váltás (SQLite -> Hive) vagy UI refaktorálás miatt az üzleti logikát is módosítani kellene. Így a kód nehezebben tesztelhetővé és törékennyé válna.
2.  **Mi a különbség a Model (DTO) és az Entity (Entitás) között, és miért van szükség mindkettőre?**
    *   *Válasz:* Az Entity egy tiszta üzleti modell a Domain rétegben, amely csak az üzletileg fontos attribútumokat tartalmazza. A Model a Data rétegben van, az Entity-ből öröklődik, és fel van szerelve a technikai feladatokhoz szükséges funkciókkal, mint a JSON szerializáció (`fromJson`, `toJson`), adatbázis-rekord transzformációk stb. Ezzel elkerüljük, hogy a Domain rétegbeli entitások tele legyenek zsúfolva olyan technikai annotációkkal vagy metódusokkal, amelyek csak egy adott API-hoz vagy adatbázishoz kötődnek.
3.  **Mikor használunk `registerLazySingleton`-t és mikor `registerFactory`-t a GetIt lokátorban?**
    *   *Válasz:* `registerLazySingleton`-t használunk olyan szolgáltatásokhoz, amelyekből csak egyetlen globális példányra van szükség az app teljes futása alatt (pl. `http.Client`, `DatabaseHelper`, vagy a `Repository` implementációk), és ezt a példányt ráérünk akkor létrehozni, amikor először ténylegesen hivatkozunk rá. `registerFactory`-t használunk minden olyan komponenshez (leginkább `Notifier`, `Bloc`, `Controller`), amelyből minden egyes lekéréskor (pl. egy új képernyő megnyitásakor) egy teljesen új, tiszta példányt akarunk kapni, megelőzve az állapotok nemkívánatos megmaradását vagy ütközését.
4.  **Mit jelent az, hogy a Data réteg "elfedi az adat eredetét" a felsőbb rétegek elől?**
    *   *Válasz:* A Domain és Presentation rétegek csak a Repository interfészen keresztül kommunikálnak az adatokkal. Nem tudják (és nem is kell tudniuk), hogy a kért adat éppen egy távoli REST API-ból, GraphQL végpontból, egy lokális SQLite táblából vagy egy memóriabeli tömbből származik-e. A Data rétegbeli repository implementáció feladata eldönteni, honnan hozza le az adatot, hogyan cache-eli azt, miközben a UI csak annyit lát, hogy meghívta a `getTodos()` függvényt és megkapta a várt listát.
5.  **Milyen előnyt nyújt a Tiszta Architektúra a Unit tesztelés szempontjából?**
    *   *Válasz:* Mivel a komponensek közötti függőségek lazák és interfészeken keresztül valósulnak meg, a tesztelés során bármelyik réteg külső függőségét rendkívül egyszerűen tudjuk helyettesíteni (mockolni). Így például a Domain use case tesztelésekor nem kell valós HTTP kéréseket küldenünk az interneten keresztül vagy adatbázis-fájlt létrehoznunk; elegendő a tesztben egy MockRepository-t injektálni a GetIt segítségével, ami azonnal visszaadja az előre beállított tesztadatokat.
