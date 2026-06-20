# Commit példa

Hogyan készítsünk tiszta, visszakövethető commitokat fejlesztés közben.

## 🛠️ Példa munkafolyamat:
```bash
# Változások ellenőrzése
git status

# Fájlok hozzáadása a stage-re
git add .

# Commit készítése beszédes üzenettel
git commit -m "feat: add secure token storage using flutter_secure_storage"

# Változások feltöltése a szerverre
git push origin feature/auth-module
```

> [!IMPORTANT]
> Ne csinálj hatalmas, több napos munkát lefedő commitokat. Törekedj a kis, logikailag egy összetartozó módosítást tartalmazó commitok írására!