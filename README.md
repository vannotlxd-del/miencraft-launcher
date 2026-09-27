# Night Launcher v1.0.0

Night Launcher adalah launcher Minecraft Java modern berbasis desktop yang ditargetkan untuk Windows. Proyek ini menggabungkan pengalaman launcher modern yang ringan, bersih, dan siap dikembangkan lebih lanjut untuk kebutuhan:

- login akun offline, Ely.by, Microsoft
- versi Minecraft dari jadul sampai terbaru
- Java 17, 21, 25
- loader Fabric, Forge, Quilt
- download mod, modpack, resource pack, shader, world
- profil gamer, friend list, chat room, dan manajemen launcher

## Fitur utama

- Login mode: offline, Ely.by, microsoft
- Versi katalog: 1.7.10, 1.8.9, 1.12.2, 1.16.5, 1.18.2, 1.19.2, 1.20.1, 1.20.4, 1.21.1, 1.21.4, 1.21.5, 1.25.x
- Loader: Fabric, Forge, Quilt
- Kategori download: loader, mod, modpack, resource pack, shader, world
- Java detection otomatis
- Profil pengguna dan konfigurasi disimpan ke file JSON
- Friend list dan chat room sederhana

## Struktur proyek

- `night_launcher.py` : aplikasi launcher utama
- `build_windows.ps1` : build Windows ke `.exe`
- `launch_windows.bat` : shortcut untuk menjalankan launcher di Windows
- `.github/workflows/release.yml` : workflow GitHub Actions untuk release
- `requirements.txt` : dependency build
- `assets/icon.svg` : ikon launcher

## Cara jalankan di Windows

```bat
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python night_launcher.py
```

Atau:

```bat
launch_windows.bat
```

## Build .exe untuk Windows

```powershell
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
pyinstaller --onefile --name NightLauncher --noconsole .\night_launcher.py
```

Output akan berada di folder `dist` sebagai `NightLauncher.exe`.

## GitHub Release

```bash
git tag v1.0.0
git push origin v1.0.0
```

Workflow GitHub Actions akan membuat build artifact untuk Windows dan Linux.

## Catatan

Versi ini adalah launcher yang sudah lebih lengkap dan siap dikembangkan. Untuk integrasi login Microsoft dan Ely.by yang benar-benar autentik, serta launcher real Minecraft Java yang menjalankan game `.jar` secara nyata, perlu ditambahkan backend autentikasi dan logic Minecraft runtime yang lebih kompleks.

## Lisensi

Proyek ini dibuat sebagai launcher starter modern untuk Minecraft Java.
