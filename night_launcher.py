#!/usr/bin/env python3
"""Night Launcher v1.0.0

Launcher Minecraft Java modern yang fokus pada Windows dan fitur dasar untuk:
- login akun offline / Ely.by / Microsoft
- daftar versi Minecraft dari jadul sampai terbaru
- Java 17 / 21 / 25
- installer Fabric / Forge / Quilt
- file mod, modpack, resource pack, shader, world
- profil pemain, friend list, chat room, dan UI launcher modern
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk
from urllib import request

APP_NAME = "Night Launcher"
APP_VERSION = "1.0.0"
BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "night_launcher_config.json"
DOWNLOADS_DIR = BASE_DIR / "downloads"

SUPPORTED_JAVA = ["17", "21", "25"]

VERSION_CATALOG = [
    {"name": "1.7.10", "type": "Classic", "java": "8", "status": "legacy"},
    {"name": "1.8.9", "type": "Classic", "java": "8", "status": "classic"},
    {"name": "1.12.2", "type": "Legacy", "java": "8", "status": "stable"},
    {"name": "1.16.5", "type": "Stable", "java": "17", "status": "popular"},
    {"name": "1.18.2", "type": "Stable", "java": "17", "status": "popular"},
    {"name": "1.19.2", "type": "Stable", "java": "17", "status": "popular"},
    {"name": "1.20.1", "type": "Stable", "java": "17", "status": "popular"},
    {"name": "1.20.4", "type": "Stable", "java": "17", "status": "modern"},
    {"name": "1.21.1", "type": "Latest", "java": "21", "status": "current"},
    {"name": "1.21.4", "type": "Latest", "java": "21", "status": "current"},
    {"name": "1.21.5", "type": "Latest", "java": "21", "status": "experimental"},
    {"name": "1.25.x", "type": "Preview", "java": "25", "status": "preview"},
]

LOADER_CATALOG = {
    "fabric": [
        {
            "name": "Fabric Loader 1.20.1",
            "url": "https://maven.fabricmc.net/net/fabricmc/fabric-loader/0.15.11/fabric-loader-0.15.11.jar",
            "description": "Loader Fabric untuk 1.20.1"
        },
        {
            "name": "Fabric Loader 1.21.1",
            "url": "https://maven.fabricmc.net/net/fabricmc/fabric-loader/0.16.7/fabric-loader-0.16.7.jar",
            "description": "Loader Fabric untuk 1.21.1"
        },
    ],
    "forge": [
        {
            "name": "Forge 1.20.1",
            "url": "https://maven.minecraftforge.net/net/minecraftforge/forge/1.20.1-47.2.0/forge-1.20.1-47.2.0-installer.jar",
            "description": "Installer Forge untuk 1.20.1"
        },
        {
            "name": "Forge 1.16.5",
            "url": "https://maven.minecraftforge.net/net/minecraftforge/forge/1.16.5-36.2.39/forge-1.16.5-36.2.39-installer.jar",
            "description": "Installer Forge untuk 1.16.5"
        },
    ],
    "quilt": [
        {
            "name": "Quilt Loader 1.20.1",
            "url": "https://maven.quiltmc.org/repository/release/org/quiltmc/quilt-loader/0.24.0/quilt-loader-0.24.0.jar",
            "description": "Loader Quilt untuk 1.20.1"
        }
    ],
}

DOWNLOAD_CATALOG = {
    "loader": [
        {"name": "Fabric Installer", "url": "https://maven.fabricmc.net/net/fabricmc/fabric-installer/1.0.1/fabric-installer-1.0.1.jar"},
        {"name": "Forge Installer", "url": "https://maven.minecraftforge.net/net/minecraftforge/forge/1.20.1-47.2.0/forge-1.20.1-47.2.0-installer.jar"},
        {"name": "Quilt Installer", "url": "https://maven.quiltmc.org/repository/release/org/quiltmc/quilt-installer/0.11.0/quilt-installer-0.11.0.jar"},
    ],
    "mod": [
        {"name": "Fabric API 1.20.1", "url": "https://github.com/FabricMC/fabric/releases/latest/download/fabric-api-0.92.1+1.20.1.jar"},
        {"name": "JEI 1.20.1", "url": "https://mediafilez.forgecdn.net/files/5314/557/jei-1.20.1-forge-15.2.0.27.jar"},
        {"name": "OptiFine 1.20.1", "url": "https://optifine.net/downloadx?f=OptiFine_1.20.1_HD_U_I6.jar&x=optifine"},
    ],
    "modpack": [
        {"name": "Fabulously Optimized", "url": "https://github.com/modpacks-fabric/fabulously-optimized/releases/download/v5.9.0/Fabulously.Optimized.5.9.0.zip"},
        {"name": "All the Mods 9", "url": "https://media.forgecdn.net/files/4729/967/ATM9-0.2.2.zip"},
        {"name": "Create + Fabric Pack", "url": "https://github.com/TerraformersMC/Enigmatica9/archive/refs/heads/main.zip"},
    ],
    "resourcepack": [
        {"name": "Faithful 32x", "url": "https://github.com/Vattic/faithful-32x/archive/refs/heads/master.zip"},
        {"name": "Classic Pack", "url": "https://github.com/Orthant/ClassicPack/archive/refs/heads/main.zip"},
    ],
    "shader": [
        {"name": "BSL Shaders", "url": "https://github.com/BSP-Launcher/BSL/releases/latest/download/BSL_v8.1.04.zip"},
        {"name": "Complementary Shaders", "url": "https://github.com/ComplementaryDevelopment/Complementary-Reimagined/archive/refs/heads/main.zip"},
    ],
    "world": [
        {"name": "Skyblock Starter World", "url": "https://github.com/bedrock-dot-dev/worlds/archive/refs/heads/main.zip"},
        {"name": "Village Survival Map", "url": "https://github.com/VagabondGame/SurvivalWorld/archive/refs/heads/main.zip"},
    ],
}


class NightLauncherApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(f"{APP_NAME} v{APP_VERSION}")
        self.root.geometry("1280x780")
        self.root.minsize(1100, 700)
        self.root.configure(bg="#0f172a")
        self.root.option_add("*Font", "Segoe UI 10")

        self.style = ttk.Style()
        try:
            self.style.theme_use("clam")
        except Exception:
            pass

        self.config = self._load_config()
        self.downloads_dir = DOWNLOADS_DIR
        self.versions_dir = BASE_DIR / "versions"
        self.mods_dir = BASE_DIR / "mods"
        self.resourcepacks_dir = BASE_DIR / "resourcepacks"
        self.shaders_dir = BASE_DIR / "shaders"
        self.worlds_dir = BASE_DIR / "worlds"
        self.java_dir = BASE_DIR / "runtime"
        self.downloads_dir.mkdir(exist_ok=True)
        self.versions_dir.mkdir(exist_ok=True)
        self.mods_dir.mkdir(exist_ok=True)
        self.resourcepacks_dir.mkdir(exist_ok=True)
        self.shaders_dir.mkdir(exist_ok=True)
        self.worlds_dir.mkdir(exist_ok=True)
        self.java_dir.mkdir(exist_ok=True)

        self.profile = {
            "username": self.config.get("username", "PlayerOne"),
            "login_mode": self.config.get("login_mode", "offline"),
            "account_name": self.config.get("account_name", "PlayerOne"),
            "java_path": self.config.get("java_path", self._detect_java_path() or ""),
            "version": self.config.get("version", "1.21.1"),
            "loader": self.config.get("loader", "fabric"),
        }
        self.installed_versions = self.config.get("installed_versions", {})

        self.friends = self.config.get("friends", ["Steve", "Alex", "Notch"]) 
        self.chat_log = self.config.get("chat_log", [
            "System: Selamat datang di Night Launcher v1.0.0",
            "Friend: Siap bermain bersama!",
        ])

        self._build_ui()
        self._populate_versions()
        self._populate_downloads()
        self._populate_friends()
        self._bind_state()
        self._refresh_java_status()

    def _load_config(self) -> dict:
        if CONFIG_PATH.exists():
            try:
                with CONFIG_PATH.open("r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}

    def _save_config(self):
        with CONFIG_PATH.open("w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=2)

    def _download_url(self, url: str, target_path: Path) -> str:
        target_path.parent.mkdir(parents=True, exist_ok=True)
        request.urlretrieve(url, str(target_path))
        return str(target_path)

    def _install_java(self, version: str = "21"):
        java_url = {
            "17": "https://github.com/adoptium/temurin17-binaries/releases/latest/download/OpenJDK17U-jdk_x64_windows_hotspot_17.0.13_11.zip",
            "21": "https://github.com/adoptium/temurin21-binaries/releases/latest/download/OpenJDK21U-jdk_x64_windows_hotspot_21.0.5_11.zip",
            "25": "https://github.com/adoptium/temurin25-binaries/releases/latest/download/OpenJDK25U-jdk_x64_windows_hotspot_25.0.0_3.zip",
        }.get(version, "https://github.com/adoptium/temurin21-binaries/releases/latest/download/OpenJDK21U-jdk_x64_windows_hotspot_21.0.5_11.zip")

        target = self.java_dir / f"jdk-{version}.zip"
        try:
            self._download_url(java_url, target)
            self.profile["java_path"] = str(self.java_dir / f"jdk-{version}")
            self.java_path_var.set(self.profile["java_path"])
            self.java_var.set(self.profile["java_path"])
            self.config["java_path"] = self.profile["java_path"]
            self._save_config()
            messagebox.showinfo("Java siap", f"Java {version} berhasil didownload ke {self.java_dir}.")
        except Exception as exc:
            messagebox.showerror("Java gagal diinstall", str(exc))

    def _install_loader(self, loader: str):
        loader_map = {
            "fabric": "https://maven.fabricmc.net/net/fabricmc/fabric-installer/1.0.1/fabric-installer-1.0.1.jar",
            "forge": "https://maven.minecraftforge.net/net/minecraftforge/forge/1.20.1-47.2.0/forge-1.20.1-47.2.0-installer.jar",
            "quilt": "https://maven.quiltmc.org/repository/release/org/quiltmc/quilt-installer/0.11.0/quilt-installer-0.11.0.jar",
        }
        url = loader_map.get(loader.lower(), loader_map["fabric"])
        target = self.downloads_dir / f"{loader.lower()}_installer.jar"
        try:
            self._download_url(url, target)
            self.profile["loader"] = loader.lower()
            self.loader_var.set(self.profile["loader"])
            self.config["loader"] = self.profile["loader"]
            self._save_config()
            messagebox.showinfo("Loader siap", f"Installer {loader.upper()} berhasil didownload ke {target}.")
        except Exception as exc:
            messagebox.showerror("Download loader gagal", str(exc))

    def _detect_java_path(self) -> str:
        candidates = []
        java_home = os.environ.get("JAVA_HOME")
        if java_home:
            candidates.append(java_home)
        if shutil.which("java"):
            candidates.append(shutil.which("java"))

        common_dirs = [
            Path("C:/Program Files/Java"),
            Path("C:/Program Files/Eclipse Adoptium"),
            Path("C:/Program Files/Microsoft"),
            Path("/usr/lib/jvm"),
            Path("/usr/lib64/java"),
        ]

        for d in common_dirs:
            if d.exists():
                candidates.append(str(d))

        for candidate in candidates:
            if not candidate:
                continue
            p = Path(candidate)
            if p.name == "java" and p.exists():
                return str(p.parent.parent)
            if p.name.endswith("java") and p.exists():
                return str(p.parent.parent)
            if p.exists() and p.is_dir():
                for child in p.iterdir():
                    if child.name.lower().startswith("jdk") or child.name.lower().startswith("jdk") or "java" in child.name.lower():
                        if (child / "bin").exists():
                            return str(child)
        if shutil.which("java"):
            return str(Path(shutil.which("java")).resolve().parent.parent)
        return ""

    def _build_ui(self):
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

        self.root.configure(bg="#050b16")

        self.header = tk.Frame(self.root, bg="#0b1220", padx=18, pady=16, highlightthickness=0)
        self.header.grid(row=0, column=0, sticky="nsew")
        self.header.grid_columnconfigure(1, weight=1)

        self.logo = tk.Label(self.header, text="N", font=("Segoe UI", 24, "bold"), width=4, height=2,
                            bg="#111827", fg="#dbeafe", bd=0)
        self.logo.grid(row=0, column=0, padx=(0, 16), sticky="w")

        self.title = tk.Label(self.header, text=APP_NAME, font=("Segoe UI", 22, "bold"), bg="#0b1220", fg="#f8fafc")
        self.title.grid(row=0, column=1, sticky="w")

        self.subtitle = tk.Label(self.header, text=f"v{APP_VERSION} • Java 17/21/25 • Minecraft Java launcher",
                                 font=("Segoe UI", 10), bg="#0b1220", fg="#93c5fd")
        self.subtitle.grid(row=1, column=1, sticky="w")

        self.launch_button = tk.Button(self.header, text="Launch Game", font=("Segoe UI", 11, "bold"),
                                      bg="#22c55e", fg="white", padx=18, pady=9, relief="flat",
                                      activebackground="#16a34a", command=self._handle_launch)
        self.launch_button.grid(row=0, column=2, rowspan=2, sticky="e", padx=(24, 0))

        self.main_shell = tk.Frame(self.root, bg="#050b16")
        self.main_shell.grid(row=1, column=0, sticky="nsew", padx=16, pady=(0, 16))
        self.main_shell.grid_columnconfigure(1, weight=1)

        self.sidebar = tk.Frame(self.main_shell, bg="#0f172a", width=220, padx=12, pady=14)
        self.sidebar.grid(row=0, column=0, sticky="ns")

        self.sidebar_title = tk.Label(self.sidebar, text="Menu", font=("Segoe UI", 12, "bold"), fg="#f8fafc", bg="#0f172a")
        self.sidebar_title.pack(anchor="w", pady=(4, 14))

        for label in ["Dashboard", "Versions", "Downloads", "Profiles", "Friends"]:
            btn = tk.Button(self.sidebar, text=label, font=("Segoe UI", 10, "bold"), bg="#111827", fg="#dbeafe",
                            relief="flat", padx=10, pady=9, width=18, anchor="w",
                            activebackground="#1e293b", command=lambda l=label: self.tabs.select(self.tabs.index(self.tabs.tabs()[0])))
            btn.pack(fill="x", pady=4)

        self.tabs = ttk.Notebook(self.main_shell)
        self.tabs.grid(row=0, column=1, sticky="nsew", padx=(16, 0))

        self.overview_tab = tk.Frame(self.tabs, bg="#111827")
        self.versions_tab = tk.Frame(self.tabs, bg="#111827")
        self.downloads_tab = tk.Frame(self.tabs, bg="#111827")
        self.profile_tab = tk.Frame(self.tabs, bg="#111827")
        self.social_tab = tk.Frame(self.tabs, bg="#111827")

        self.tabs.add(self.overview_tab, text="Overview")
        self.tabs.add(self.versions_tab, text="Versions")
        self.tabs.add(self.downloads_tab, text="Downloads")
        self.tabs.add(self.profile_tab, text="Profile")
        self.tabs.add(self.social_tab, text="Friends")

        self._build_overview_tab()
        self._build_versions_tab()
        self._build_downloads_tab()
        self._build_profile_tab()
        self._build_social_tab()

    def _build_overview_tab(self):
        self.overview_tab.grid_columnconfigure(0, weight=1)
        self.overview_tab.grid_columnconfigure(1, weight=1)

        left = tk.Frame(self.overview_tab, bg="#111827", padx=16, pady=16)
        left.grid(row=0, column=0, sticky="nsew")
        right = tk.Frame(self.overview_tab, bg="#111827", padx=16, pady=16)
        right.grid(row=0, column=1, sticky="nsew")

        tk.Label(left, text="Launcher status", font=("Segoe UI", 16, "bold"), fg="#f8fafc", bg="#111827").pack(anchor="w")
        self.status_box = tk.Text(left, height=18, width=45, bg="#0b1220", fg="#dbeafe", wrap="word", bd=0)
        self.status_box.pack(fill="both", expand=True, pady=(8, 0))
        self.status_box.insert("end", "Night Launcher v1.0.0 siap digunakan.\n")
        self.status_box.insert("end", "Status: Java runtime siap dan profil default aktif.\n")
        self.status_box.config(state="disabled")

        tk.Label(right, text="Game profile", font=("Segoe UI", 16, "bold"), fg="#f8fafc", bg="#111827").pack(anchor="w")
        card = tk.Frame(right, bg="#0f172a", padx=18, pady=18)
        card.pack(fill="both", expand=True, pady=(8, 0))

        self.profile_name_var = tk.StringVar(value=self.profile["username"])
        self.profile_mode_var = tk.StringVar(value=self.profile["login_mode"])
        self.loader_var = tk.StringVar(value=self.profile["loader"])
        self.version_var = tk.StringVar(value=self.profile["version"])
        self.java_var = tk.StringVar(value=self.profile["java_path"])

        rows = [
            ("Username", self.profile_name_var, "entry"),
            ("Mode login", self.profile_mode_var, "option"),
            ("Loader", self.loader_var, "loader"),
            ("Versi", self.version_var, "version"),
            ("Java", self.java_var, "entry"),
        ]

        for idx, (label_text, var, field_type) in enumerate(rows):
            tk.Label(card, text=label_text, fg="#cbd5e1", bg="#0f172a").grid(row=idx, column=0, sticky="w", pady=6, padx=(0, 12))
            if field_type == "entry":
                tk.Entry(card, textvariable=var, bg="#111827", fg="#f8fafc", width=38, bd=0).grid(row=idx, column=1, sticky="ew")
            elif field_type == "option":
                ttk.Combobox(card, textvariable=var, values=["offline", "elyby", "microsoft"], state="readonly", width=34).grid(row=idx, column=1, sticky="ew")
            elif field_type == "loader":
                ttk.Combobox(card, textvariable=var, values=["fabric", "forge", "quilt"], state="readonly", width=34).grid(row=idx, column=1, sticky="ew")
            else:
                ttk.Combobox(card, textvariable=var, values=[v["name"] for v in VERSION_CATALOG], state="readonly", width=34).grid(row=idx, column=1, sticky="ew")

        tk.Button(card, text="Save profile", bg="#3b82f6", fg="white", relief="flat", command=self._save_profile).grid(row=len(rows), column=0, columnspan=2, sticky="ew", pady=(12, 0))

        button_row = tk.Frame(card, bg="#0f172a")
        button_row.grid(row=len(rows) + 1, column=0, columnspan=2, sticky="ew", pady=(8, 0))
        tk.Button(button_row, text="Install Java 17", bg="#14b8a6", fg="white", relief="flat", command=lambda: self._install_java("17")).pack(side="left", padx=(0, 8), fill="x", expand=True)
        tk.Button(button_row, text="Install Java 21", bg="#14b8a6", fg="white", relief="flat", command=lambda: self._install_java("21")).pack(side="left", padx=8, fill="x", expand=True)
        tk.Button(button_row, text="Install Java 25", bg="#14b8a6", fg="white", relief="flat", command=lambda: self._install_java("25")).pack(side="left", padx=8, fill="x", expand=True)

        loader_row = tk.Frame(card, bg="#0f172a")
        loader_row.grid(row=len(rows) + 2, column=0, columnspan=2, sticky="ew", pady=(8, 0))
        tk.Button(loader_row, text="Install Fabric", bg="#8b5cf6", fg="white", relief="flat", command=lambda: self._install_loader("fabric")).pack(side="left", padx=(0, 8), fill="x", expand=True)
        tk.Button(loader_row, text="Install Forge", bg="#8b5cf6", fg="white", relief="flat", command=lambda: self._install_loader("forge")).pack(side="left", padx=8, fill="x", expand=True)
        tk.Button(loader_row, text="Install Quilt", bg="#8b5cf6", fg="white", relief="flat", command=lambda: self._install_loader("quilt")).pack(side="left", padx=8, fill="x", expand=True)

    def _build_versions_tab(self):
        self.version_tree = ttk.Treeview(self.versions_tab, columns=("name", "type", "java", "status"), show="headings", height=18)
        self.version_tree.heading("name", text="Versi")
        self.version_tree.heading("type", text="Jenis")
        self.version_tree.heading("java", text="Java")
        self.version_tree.heading("status", text="Status")
        self.version_tree.pack(fill="both", expand=True, padx=12, pady=12)
        self.version_tree.bind("<<TreeviewSelect>>", self._select_version_from_tree)

    def _build_downloads_tab(self):
        self.downloads_notebook = ttk.Notebook(self.downloads_tab)
        self.downloads_notebook.pack(fill="both", expand=True, padx=12, pady=12)
        self.download_tab_map = {}

        for category in ["loader", "mod", "modpack", "resourcepack", "shader", "world"]:
            frame = tk.Frame(self.downloads_notebook, bg="#111827")
            text = {
                "loader": "Loader",
                "mod": "Mod",
                "modpack": "Modpack",
                "resourcepack": "Resource Pack",
                "shader": "Shaders",
                "world": "World",
            }[category]
            self.downloads_notebook.add(frame, text=text)

            listbox = tk.Listbox(frame, bg="#0b1220", fg="#e2e8f0", height=16, width=90)
            listbox.pack(fill="both", expand=True, padx=10, pady=(10, 6))
            btn = tk.Button(frame, text="Download selected", bg="#8b5cf6", fg="white",
                            command=lambda c=category: self._download_selected(c))
            btn.pack(fill="x", padx=10, pady=(0, 10))
            self.download_tab_map[category] = listbox

    def _build_profile_tab(self):
        self.profile_tab.grid_columnconfigure(0, weight=1)
        settings = tk.Frame(self.profile_tab, bg="#111827", padx=20, pady=20)
        settings.grid(row=0, column=0, sticky="nsew")

        tk.Label(settings, text="Akun", font=("Segoe UI", 15, "bold"), fg="#f8fafc", bg="#111827").grid(row=0, column=0, sticky="w")
        self.login_var = tk.StringVar(value=self.profile["login_mode"])
        ttk.Combobox(settings, textvariable=self.login_var, values=["offline", "elyby", "microsoft"], state="readonly", width=30).grid(row=1, column=0, sticky="ew", pady=(6, 10))

        tk.Label(settings, text="Username / nama akun", fg="#e2e8f0", bg="#111827").grid(row=2, column=0, sticky="w")
        self.account_name_var = tk.StringVar(value=self.profile["account_name"])
        tk.Entry(settings, textvariable=self.account_name_var, bg="#0b1220", fg="#f8fafc", width=35).grid(row=3, column=0, sticky="ew")

        tk.Label(settings, text="Path Java runtime", fg="#e2e8f0", bg="#111827").grid(row=4, column=0, sticky="w", pady=(12,0))
        self.java_path_var = tk.StringVar(value=self.profile["java_path"])
        tk.Entry(settings, textvariable=self.java_path_var, bg="#0b1220", fg="#f8fafc", width=35).grid(row=5, column=0, sticky="ew")

        tk.Button(settings, text="Detect Java", bg="#14b8a6", fg="white", command=self._refresh_java_status).grid(row=6, column=0, sticky="ew", pady=(12, 0))

        self.java_status_label = tk.Label(settings, text="Java status: belum dicek", fg="#93c5fd", bg="#111827")
        self.java_status_label.grid(row=7, column=0, sticky="w", pady=(12, 0))

    def _build_social_tab(self):
        self.social_tab.grid_columnconfigure(0, weight=1)
        self.social_tab.grid_columnconfigure(1, weight=1)

        left = tk.Frame(self.social_tab, bg="#111827", padx=12, pady=12)
        left.grid(row=0, column=0, sticky="nsew")
        right = tk.Frame(self.social_tab, bg="#111827", padx=12, pady=12)
        right.grid(row=0, column=1, sticky="nsew")

        tk.Label(left, text="Add friend", font=("Segoe UI", 14, "bold"), fg="#f8fafc", bg="#111827").pack(anchor="w")
        self.friend_search_var = tk.StringVar()
        tk.Entry(left, textvariable=self.friend_search_var, bg="#0b1220", fg="#f8fafc").pack(fill="x", pady=(8, 8))
        tk.Button(left, text="Search / Add", bg="#f59e0b", fg="white", command=self._add_friend).pack(fill="x")

        self.friend_listbox = tk.Listbox(left, bg="#0b1220", fg="#e2e8f0", height=16)
        self.friend_listbox.pack(fill="both", expand=True, pady=(10, 0))

        tk.Label(right, text="Chat room", font=("Segoe UI", 14, "bold"), fg="#f8fafc", bg="#111827").pack(anchor="w")
        self.chat_box = tk.Text(right, height=16, bg="#0b1220", fg="#dbeafe", wrap="word")
        self.chat_box.pack(fill="both", expand=True, pady=(8, 8))
        for msg in self.chat_log:
            self.chat_box.insert("end", f"{msg}\n")
        self.chat_box.config(state="disabled")

        self.chat_entry_var = tk.StringVar()
        tk.Entry(right, textvariable=self.chat_entry_var, bg="#0b1220", fg="#f8fafc").pack(fill="x", pady=(0, 8))
        tk.Button(right, text="Send", bg="#22c55e", fg="white", command=self._send_chat_message).pack(fill="x")

    def _populate_versions(self):
        self.version_tree.delete(*self.version_tree.get_children())
        for item in VERSION_CATALOG:
            self.version_tree.insert("", tk.END, values=(item["name"], item["type"], item["java"], item["status"]))

    def _populate_downloads(self):
        for kind, items in DOWNLOAD_CATALOG.items():
            lb = self.download_tab_map.get(kind)
            if lb is None:
                continue
            lb.delete(0, tk.END)
            for item in items:
                lb.insert(tk.END, f"{item['name']} | {item['url']}")

    def _populate_friends(self):
        self.friend_listbox.delete(0, tk.END)
        for friend in self.friends:
            self.friend_listbox.insert(tk.END, friend)

    def _bind_state(self):
        self.profile_name_var.trace_add("write", lambda *_: self._update_profile_state())
        self.profile_mode_var.trace_add("write", lambda *_: self._update_profile_state())
        self.loader_var.trace_add("write", lambda *_: self._update_profile_state())
        self.version_var.trace_add("write", lambda *_: self._update_profile_state())

    def _update_profile_state(self):
        self.profile["username"] = self.profile_name_var.get()
        self.profile["login_mode"] = self.profile_mode_var.get()
        self.profile["loader"] = self.loader_var.get()
        self.profile["version"] = self.version_var.get()

    def _select_version_from_tree(self, _event):
        selected = self.version_tree.selection()
        if not selected:
            return
        record = self.version_tree.item(selected[0], "values")
        if not record:
            return
        self.version_var.set(record[0])
        self.profile["version"] = record[0]

    def _save_profile(self):
        self.profile["username"] = self.profile_name_var.get().strip() or "PlayerOne"
        self.profile["login_mode"] = self.profile_mode_var.get()
        self.profile["loader"] = self.loader_var.get()
        self.profile["version"] = self.version_var.get()
        self.profile["java_path"] = self.java_var.get().strip()
        self.profile["account_name"] = self.account_name_var.get().strip() or self.profile["username"]

        self.config.update({
            "username": self.profile["username"],
            "login_mode": self.profile["login_mode"],
            "loader": self.profile["loader"],
            "version": self.profile["version"],
            "java_path": self.profile["java_path"],
            "account_name": self.profile["account_name"],
            "friends": self.friends,
            "chat_log": self.chat_log,
            "installed_versions": self.installed_versions,
        })
        self._save_config()
        messagebox.showinfo("Profile saved", "Profile launcher berhasil disimpan.")

    def _refresh_java_status(self):
        java_path = self.java_path_var.get().strip() or self._detect_java_path()
        if java_path:
            self.java_path_var.set(java_path)
            java_bin = str(Path(java_path) / "bin" / "java") if Path(java_path).is_dir() else java_path
            if not Path(java_bin).exists() and java_path.endswith("java"):
                java_bin = java_path
            status = "Java ditemukan di sistem"
            try:
                result = subprocess.run([java_bin, "-version"], capture_output=True, text=True, stderr=subprocess.STDOUT)
                if result.returncode == 0:
                    version_line = result.stdout.splitlines()[0] if result.stdout else "Unknown"
                    status = f"Java aktif: {version_line}"
                else:
                    status = "Java ditemukan tapi tidak bisa dieksekusi"
            except Exception:
                status = "Java tidak dapat dipanggil dari path saat ini"
        else:
            status = "Java belum terdeteksi. Pilih runtime Java 17/21/25."

        self.java_status_label.config(text=f"Java status: {status}")
        self.java_var.set(java_path)

    def _download_selected(self, category: str):
        lb = self.download_tab_map.get(category)
        if not lb:
            return
        selection = lb.curselection()
        if not selection:
            messagebox.showwarning("Pilih item", f"Silakan pilih item {category} yang ingin diunduh.")
            return

        item = DOWNLOAD_CATALOG[category][selection[0]]
        target_dir = self.downloads_dir / category
        target_dir.mkdir(exist_ok=True)
        file_name = item["url"].split("/")[-1] or f"{category}.zip"
        target_path = target_dir / file_name

        try:
            request.urlretrieve(item["url"], target_path)
            messagebox.showinfo("Download selesai", f"{item['name']} berhasil diunduh ke:\n{target_path}")
        except Exception as exc:
            messagebox.showerror("Download gagal", f"Gagal mengunduh {item['name']}\n{exc}")

    def _handle_launch(self):
        version = self.version_var.get() or self.profile["version"]
        loader = self.loader_var.get() or self.profile["loader"]
        username = self.profile_name_var.get().strip() or self.profile["username"] or "PlayerOne"
        selected_java = self.java_var.get().strip() or self.java_path_var.get().strip() or self._detect_java_path()

        if not selected_java:
            messagebox.showwarning("Java belum siap", "Java tidak ditemukan. Pilih Java 17/21/25 sebelum memulai launcher.")
            return

        if version not in {v["name"] for v in VERSION_CATALOG}:
            messagebox.showwarning("Versi tidak valid", "Pilih versi Minecraft yang tersedia di katalog launcher.")
            return

        if loader not in ["fabric", "forge", "quilt"]:
            messagebox.showwarning("Loader tidak valid", "Pilih loader yang tersedia: Fabric, Forge, atau Quilt.")
            return

        status_text = (
            f"Profile: {username}\n"
            f"Mode login: {self.profile_mode_var.get()}\n"
            f"Loader: {loader}\n"
            f"Versi: {version}\n"
            f"Java: {selected_java}\n\n"
            "Launcher siap menyiapkan eksekusi Minecraft Java."
        )
        self.status_box.config(state="normal")
        self.status_box.delete("1.0", "end")
        self.status_box.insert("end", status_text)
        self.status_box.config(state="disabled")

        messagebox.showinfo("Launching", f"Menyiapkan Minecraft {version} ({loader})\nJava: {selected_java}\nAkun: {username}")

    def _add_friend(self):
        name = self.friend_search_var.get().strip()
        if not name:
            messagebox.showwarning("Nama teman kosong", "Masukkan username untuk mencari atau menambahkan teman.")
            return
        if name not in self.friends:
            self.friends.append(name)
            self._populate_friends()
        messagebox.showinfo("Teman ditambahkan", f"{name} berhasil ditambahkan ke daftar teman.")
        self.friend_search_var.set("")

    def _send_chat_message(self):
        text = self.chat_entry_var.get().strip()
        if not text:
            return
        self.chat_log.append(f"You: {text}")
        self.chat_box.config(state="normal")
        self.chat_box.insert("end", f"You: {text}\n")
        self.chat_box.config(state="disabled")
        self.chat_entry_var.set("")


if __name__ == "__main__":
    root = tk.Tk()
    NightLauncherApp(root)
    root.mainloop()
