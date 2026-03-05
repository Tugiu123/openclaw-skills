# Tasks: Photo Gallery Management

**Input**: Design documents from `/specs/001-photo-gallery/`
**Prerequisites**: plan.md, spec.md, research.md

**Tests**: Tests are OPTIONAL - not explicitly requested in feature specification

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project directory structure per implementation plan
- [ ] T002 Initialize React 18.3.1 + TypeScript 5.6.2 project with Vite 6.0.1
- [ ] T003 [P] Install and configure ESLint and Prettier for code quality
- [ ] T004 [P] Configure TypeScript strict mode in tsconfig.json
- [ ] T005 [P] Set up CSS Modules support in Vite configuration
- [ ] T006 Create base App.tsx and main.tsx entry files
- [ ] T007 Install sql.js for SQLite database support
- [ ] T008 [P] Install Vitest and Playwright for testing framework
- [ ] T009 Create initial README with project setup instructions

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Type Definitions

- [ ] T010 Create Album type definition in src/types/album.ts
- [ ] T011 [P] Create Photo type definition in src/types/photo.ts
- [ ] T012 [P] Create shared types index in src/types/index.ts

### Storage Layer

- [ ] T013 Initialize SQLite database wrapper in src/services/storage/sqlite.ts
- [ ] T014 [P] Initialize IndexedDB wrapper for photo blobs in src/services/storage/indexeddb.ts
- [ ] T015 Create database schema initialization script in src/services/storage/schema.sql
- [ ] T016 [P] Create albums table schema with id, name, cover_photo_id, created_at, modified_at, sort_order
- [ ] T017 [P] Create photos table schema with id, album_id, original_filename, taken_at, file_size, thumbnail_url
- [ ] T018 Implement database migration utility in src/services/storage/migrations.ts

### State Management

- [ ] T019 Create Store class for state management in src/store/Store.ts
- [ ] T020 [P] Create album state management in src/store/albumStore.ts
- [ ] T021 [P] Create photo state management in src/store/photoStore.ts

### Core Utilities

- [ ] T022 Implement image processing utilities in src/utils/imageUtils.ts
- [ ] T023 [P] Implement date formatting utilities in src/utils/dateUtils.ts
- [ ] T024 [P] Create file validation utilities in src/utils/fileUtils.ts

### Base UI Components

- [ ] T025 Create Button component in src/components/UI/Button.tsx
- [ ] T026 [P] Create Modal component in src/components/UI/Modal.tsx
- [ ] T027 [P] Create LoadingSpinner component in src/components/UI/LoadingSpinner.tsx

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create and Organize Albums (Priority: P1) 🎯 MVP

**Goal**: Users can create albums, import photos, and organize albums via drag-and-drop with date grouping

**Independent Test**: User can create a new album, import 5 photos, and rearrange albums via drag-and-drop. All changes persist after page refresh.

### Models for User Story 1

- [ ] T028 [P] [US1] Create Album entity class in src/models/Album.ts
- [ ] T029 [P] [US1] Create Photo entity class in src/models/Photo.ts

### Services for User Story 1

- [ ] T030 [US1] Implement AlbumService in src/services/albumService.ts with create, update, delete, getAll methods
- [ ] T031 [US1] Implement PhotoService in src/services/photoService.ts with import, get, delete methods
- [ ] T032 [US1] Add album cover photo management to AlbumService
- [ ] T033 [US1] Add album sorting and date grouping logic to AlbumService

### Components for User Story 1

- [ ] T034 [P] [US1] Create AlbumCard component in src/components/AlbumCard.tsx with drag handle
- [ ] T035 [P] [US1] Create DragDropArea component in src/components/DragDropArea.tsx for album reordering
- [ ] T036 [P] [US1] Create PhotoTile component in src/components/PhotoTile.tsx for album thumbnails
- [ ] T037 [P] [US1] Create CreateAlbumDialog component in src/components/CreateAlbumDialog.tsx

### Pages for User Story 1

- [ ] T038 [US1] Implement HomePage in src/pages/HomePage.tsx with album list and drag-drop
- [ ] T039 [US1] Add album creation modal integration to HomePage
- [ ] T040 [US1] Add date grouping display to HomePage album list
- [ ] T041 [US1] Implement drag-and-drop event handlers for album reordering in HomePage

### Integration for User Story 1

- [ ] T042 [US1] Connect AlbumStore to HomePage for real-time album updates
- [ ] T043 [US1] Connect PhotoStore to AlbumCard for photo count display
- [ ] T044 [US1] Add navigation routing between home and album detail pages
- [ ] T045 [US1] Implement persistent album order storage to localStorage

### Hooks for User Story 1

- [ ] T046 [P] [US1] Create useAlbums hook in src/hooks/useAlbums.ts for album state
- [ ] T047 [P] [US1] Create useDragDrop hook in src/hooks/useDragDrop.ts for drag operations

**Checkpoint**: User Story 1 fully functional - users can create albums, import photos, and reorder via drag-drop

---

## Phase 4: User Story 2 - View Photos in Album (Priority: P2)

**Goal**: Users can browse photos in album detail page using tile interface with full-size viewer

**Independent Test**: User can open any album, see all photos in tile grid, scroll smoothly, and click photos to view full-size

### Services for User Story 2

- [ ] T048 [US2] Add photo pagination to PhotoService in src/services/photoService.ts
- [ ] T049 [US2] Implement lazy loading logic for photos in PhotoService
- [ ] T050 [US2] Add thumbnail generation optimization to imageUtils in src/utils/imageUtils.ts

### Components for User Story 2

- [ ] T051 [P] [US2] Create PhotoTile for album view in src/components/PhotoTile.tsx (extend base PhotoTile)
- [ ] T052 [P] [US2] Create PhotoViewer modal in src/components/PhotoViewer.tsx for full-size view
- [ ] T053 [P] [US2] Create PhotoGrid component in src/components/PhotoGrid.tsx for tile layout
- [ ] T054 [P] [US2] Create EmptyState component in src/components/EmptyState.tsx for empty albums

### Pages for User Story 2

- [ ] T055 [US2] Implement AlbumDetail page in src/pages/AlbumDetail.tsx
- [ ] T056 [US2] Add photo tile grid display to AlbumDetail page
- [ ] T057 [US2] Implement scroll handling and lazy loading in AlbumDetail
- [ ] T058 [US2] Add photo viewer modal integration to AlbumDetail
- [ ] T059 [US2] Add empty state prompt for albums with no photos

### Performance for User Story 2

- [ ] T060 [US2] Implement virtual scrolling for large photo collections in PhotoGrid
- [ ] T061 [US2] Add progressive image loading with blur-up effect in PhotoTile
- [ ] T062 [US2] Optimize thumbnail caching in PhotoService

### Hooks for User Story 2

- [ ] T063 [P] [US2] Create usePhotos hook in src/hooks/usePhotos.ts for photo state
- [ ] T064 [P] [US2] Create useVirtualScroll hook in src/hooks/useVirtualScroll.ts for performance

**Checkpoint**: User Stories 1 AND 2 both work independently - users can manage albums and view photos

---

## Phase 5: User Story 3 - Move Photos Between Albums (Priority: P3)

**Goal**: Users can move photos between albums with single and batch selection

**Independent Test**: User can select one or multiple photos in an album and move them to another album

### Services for User Story 3

- [ ] T065 [US3] Add photo move method to PhotoService in src/services/photoService.ts
- [ ] T066 [US3] Implement batch photo move operation in PhotoService
- [ ] T067 [US3] Add validation to prevent moving photos to same album

### Components for User Story 3

- [ ] T068 [P] [US3] Create PhotoSelector component in src/components/PhotoSelector.tsx for selection
- [ ] T069 [P] [US3] Create MovePhotoDialog in src/components/MovePhotoDialog.tsx
- [ ] T070 [P] [US3] Update PhotoTile with selection state in src/components/PhotoTile.tsx

### Pages for User Story 3

- [ ] T071 [US3] Add photo selection mode to AlbumDetail page in src/pages/AlbumDetail.tsx
- [ ] T072 [US3] Add move photos button and dialog to AlbumDetail
- [ ] T073 [US3] Implement photo selection state management in AlbumDetail
- [ ] T074 [US3] Add confirmation prompt for batch move operations

### Integration for User Story 3

- [ ] T075 [US3] Update PhotoStore to handle photo moves across albums
- [ ] T076 [US3] Update AlbumCard to reflect photo count changes after move
- [ ] T077 [US3] Add user feedback notifications for successful moves

**Checkpoint**: All user stories independently functional - complete photo organization workflow

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

### Error Handling

- [ ] T078 [P] Add global error boundary component in src/components/ErrorBoundary.tsx
- [ ] T079 [P] Add error handling for image loading failures in PhotoTile
- [ ] T080 [P] Add error handling for file upload failures in PhotoService
- [ ] T081 [P] Add error handling for storage quota exceeded in IndexedDB service

### Validation

- [ ] T082 [P] Add album name validation (1-100 characters, no special chars) in AlbumService
- [ ] T083 [P] Add file type validation (JPG, PNG, HEIC) in fileUtils
- [ ] T084 [P] Add file size limits in fileUtils

### User Experience

- [ ] T085 [P] Add loading states to all async operations
- [ ] T086 [P] Add confirmation dialogs for destructive operations (delete album, delete photos)
- [ ] T087 [P] Add responsive design for mobile devices
- [ ] T088 [P] Add keyboard navigation for all interactive elements
- [ ] T089 [P] Add ARIA labels for accessibility

### Performance Optimization

- [ ] T090 Add image compression for storage optimization in imageUtils
- [ ] T091 [P] Add database query optimization with indexes in schema.sql
- [ ] T092 [P] Add memory cleanup for off-screen images in PhotoGrid

### Documentation

- [ ] T093 [P] Update README with usage instructions
- [ ] T094 [P] Add inline documentation for component APIs
- [ ] T095 Create quickstart guide for new developers

**Checkpoint**: Feature complete - all polish and cross-cutting concerns addressed

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Depends on albums and photos existing (US1/US2 context)

### Within Each User Story

- Models before services
- Services before components/pages
- Components before pages
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T003-T009)
- All Foundational type definitions can run in parallel (T010-T012)
- All Foundational storage tasks can run in parallel (T014-T015, T016-T017)
- All Foundational state management tasks can run in parallel (T020-T021)
- All Foundational utilities can run in parallel (T023-T024)
- All Foundational UI components can run in parallel (T026-T027)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All models within a user story marked [P] can run in parallel
- All components within a user story marked [P] can run in parallel
- All polish tasks marked [P] can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch all models for User Story 1 together:
Task: "Create Album entity class in src/models/Album.ts"
Task: "Create Photo entity class in src/models/Photo.ts"

# Launch all components for User Story 1 together:
Task: "Create AlbumCard component in src/components/AlbumCard.tsx"
Task: "Create DragDropArea component in src/components/DragDropArea.tsx"
Task: "Create PhotoTile component in src/components/PhotoTile.tsx"
Task: "Create CreateAlbumDialog component in src/components/CreateAlbumDialog.tsx"

# Launch all hooks for User Story 1 together:
Task: "Create useAlbums hook in src/hooks/useAlbums.ts"
Task: "Create useDragDrop hook in src/hooks/useDragDrop.ts"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T009)
2. Complete Phase 2: Foundational (T010-T027) - CRITICAL
3. Complete Phase 3: User Story 1 (T028-T047)
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo MVP

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add Polish → Final release

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (T028-T047)
   - Developer B: User Story 2 (T048-T064)
   - Developer C: User Story 3 (T065-T077)
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [US1], [US2], [US3] labels map task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Tests are optional - not included per feature specification
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
