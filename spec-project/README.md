# Photo Gallery Management

A local photo organization web application that allows users to create albums, import photos, organize albums via drag-and-drop, and browse photos in a tile-based interface.

## Features

- ✅ Create and manage photo albums
- ✅ Import photos from local device
- ✅ Drag-and-drop album reordering
- ✅ Date-based album grouping
- ✅ Tile-based photo browsing
- ✅ Full-size photo viewing
- ✅ Move photos between albums
- ✅ Offline-capable (browser-local storage)

## Tech Stack

- **Frontend**: React 18.3.1 + TypeScript 5.6.2
- **Build Tool**: Vite 6.0.1
- **Database**: SQLite (sql.js) for metadata + IndexedDB for photo blobs
- **Styling**: CSS Modules
- **Testing**: Vitest + Playwright (optional)

## Project Structure

```
src/
├── components/           # Reusable UI components
│   ├── AlbumCard.tsx   # Album thumbnail card
│   ├── PhotoTile.tsx   # Photo tile for album view
│   ├── PhotoViewer.tsx # Full-size photo viewer
│   ├── DragDropArea.tsx # Drag and drop zone
│   └── UI/             # Base UI components
│       ├── Button.tsx
│       ├── Modal.tsx
│       └── LoadingSpinner.tsx
├── pages/                # Page-level components
│   ├── HomePage.tsx     # Album gallery home
│   └── AlbumDetail.tsx  # Album photos in tile layout
├── hooks/                # Custom React hooks
│   ├── useAlbums.ts     # Album state management
│   ├── usePhotos.ts     # Photo state management
│   └── useDragDrop.ts   # Drag and drop logic
├── services/             # Business logic and data access
│   ├── storage/         # Storage layer
│   │   ├── sqlite.ts    # SQLite database wrapper
│   │   ├── indexeddb.ts # IndexedDB wrapper
│   │   ├── schema.sql   # Database schema
│   │   └── migrations.ts # Database migrations
│   ├── albumService.ts  # Album management
│   └── photoService.ts  # Photo processing
├── store/                # State management
│   ├── Store.ts         # Base store class
│   ├── albumStore.ts    # Album state
│   └── photoStore.ts    # Photo state
├── models/               # Entity classes
│   ├── Album.ts         # Album entity
│   └── Photo.ts         # Photo entity
├── types/                # TypeScript types
│   ├── album.ts         # Album types
│   ├── photo.ts         # Photo types
│   └── index.ts         # Shared types
├── utils/                # Utility functions
│   ├── imageUtils.ts    # Image processing
│   ├── dateUtils.ts     # Date formatting
│   └── fileUtils.ts     # File validation
├── App.tsx              # Root component
└── main.tsx             # Application entry
```

## Getting Started

### Prerequisites

- Node.js 18+ and npm/yarn/pnpm
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Installation

1. Clone the repository and navigate to the project directory:

```bash
cd spec-project
```

2. Install dependencies:

```bash
npm install
```

### Development

Start the development server:

```bash
npm run dev
```

The application will be available at `http://localhost:3000`

### Building

Build for production:

```bash
npm run build
```

Preview the production build:

```bash
npm run preview
```

### Code Quality

Lint the code:

```bash
npm run lint
```

Format the code:

```bash
npm run format
```

### Testing

Run unit tests:

```bash
npm run test
```

Run tests with UI:

```bash
npm run test:ui
```

Run end-to-end tests:

```bash
npm run test:e2e
```

Run e2e tests with UI:

```bash
npm run test:e2e:ui
```

## Performance Goals

- 60fps scrolling for tile interface
- <2s initial load for 200 photos
- <5s complete drag-and-drop operation
- Efficient handling of 1000+ photos

## Storage

The application uses browser-local storage:

- **SQLite (sql.js)**: Stores album and photo metadata
- **IndexedDB**: Stores photo image blobs
- **localStorage**: Stores UI preferences and album order

All data stays client-side - no server transmission required.

## Contributing

This project follows strict code quality standards:

- TypeScript strict mode enabled
- ESLint and Prettier configured
- Comprehensive type definitions
- Performance optimization focus

## License

MIT
