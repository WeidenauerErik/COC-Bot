# COC Log Monitor

Ein schlichtes, modernes Log-Monitoring-Tool für den COC Bot.

## Setup

```bash
npm install
npm run dev
```

Dann im Browser: **http://localhost:5173**

## Build

```bash
npm run build
npm run preview
```

## Verwendung

1. Starte die App mit `npm run dev`
2. Ziehe deinen `logs/` Ordner in das Browserfenster **oder** klicke auf „Ordner öffnen"
3. Wähle links eine Log-Datei aus
4. Filtere nach Level (Info / Warning / Error / Debug) oder suche im Inhalt

## Tech Stack

- **Vue 3** – Composition API (`<script setup>`)
- **Vite** – Build-Tool
- **Pinia** – State Management
- **Vue Router** – Navigation zwischen Dateien

## Projektstruktur

```
src/
├── assets/          # Globale CSS-Variablen & Reset
├── components/      # Wiederverwendbare UI-Komponenten
│   ├── icons/       # SVG-Icon-Komponenten
│   ├── AppHeader.vue
│   ├── AppSidebar.vue
│   ├── DropZone.vue
│   ├── FileListItem.vue
│   ├── LogLine.vue
│   ├── LogToolbar.vue
│   ├── OverviewCards.vue
│   └── StatPill.vue
├── composables/     # Wiederverwendbare Logik
│   ├── useDragDrop.js
│   ├── useLogFilter.js
│   └── useLogParser.js
├── router/          # Vue Router Konfiguration
├── stores/          # Pinia Stores
│   └── logs.js
└── views/           # Seiten-Komponenten
    ├── HomeView.vue
    └── LogView.vue
```

## Log-Format

Das Tool erwartet folgendes Log-Format (vom `logger.py`):

```
[2026-03-10 14:32:05] [INFO] Nachricht hier
[2026-03-10 14:32:06] [WARNING] Warnung hier
[2026-03-10 14:32:07] [ERROR] Fehler hier
```
