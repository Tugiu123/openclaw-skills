# Research Notes: Photo Gallery Management

**Feature Branch**: `001-photo-gallery`
**Date**: 2026-03-05
**Purpose**: Technical research and decision documentation for Phase 0 of implementation

---

## Technology Stack Decisions

### 1. Database: SQLite via sql.js WASM

**Decision**: Use SQLite database running in the browser via sql.js (WebAssembly)

**Rationale**:
- Zero server dependency: Runs entirely in the browser, perfect for offline-first requirements
- Familiar SQL syntax: Easier development and debugging
- Mature technology: SQLite is battle-tested with excellent reliability
- In-memory or persistent storage: Can use IndexedDB for persistence
- Full-text search capability: Built-in FTS5 extension for future search features

**Alternatives Considered**:
- **IndexedDB directly**: More complex query handling, no relational features
- **LocalStorage**: Too small (5MB limit), no query capabilities
- **PouchDB**: Overhead of sync replication not needed for local-only app

**Implementation Notes**:
- Load SQLite database from IndexedDB on app startup
- Save database state to IndexedDB after write operations
- Use WAL mode for better performance with concurrent reads
- Consider database size limits (IndexedDB typically allows >100MB)

---

### 2. Image Storage: IndexedDB for Blobs

**Decision**: Store image files as blobs in IndexedDB, with metadata in SQLite

**Rationale**:
- Large storage capacity: IndexedDB can store hundreds of MB of data
- Structured API: Easy to store and retrieve blobs by ID
- Indexed access: Can efficiently query by photo ID from SQLite metadata
- No external dependencies: Native browser API
- Works offline: No network calls required

**Alternatives Considered**:
- **Base64 in LocalStorage**: Too small, 33% overhead from encoding
- **File System Access API**: Limited browser support, permission complexity
- **Cache API**: Optimized for HTTP resources, not general storage

**Implementation Notes**:
- Store images in a dedicated IndexedDB object store
- Use photo ID (from SQLite) as the IndexedDB key
- Implement lazy loading for thumbnails to reduce memory usage
- Consider image compression for storage optimization
- Implement cleanup for deleted photos

---

### 3. Drag and Drop: Native HTML5 Drag and Drop API

**Decision**: Use native HTML5 Drag and Drop API without third-party libraries

**Rationale**:
- Zero dependencies: No additional libraries to load
- Browser native performance: Optimized by browser engines
- Touch support: Modern browsers support touch events with drag API
- Full control: Can implement custom behavior easily
- Smaller bundle size: No drag-drop library overhead

**Alternatives Considered**:
- **SortableJS**: Additional dependency, overkill for simple sorting
- **React DnD**: Not using React framework
- **Draggable**: More complex API than needed

**Implementation Notes**:
- Implement drag start, drag over, and drop event handlers
- Use dataTransfer API to pass album/photo IDs
- Add visual feedback during drag (opacity, drop zones)
- Implement touch event handlers for mobile support
- Prevent default behavior to enable custom drop handling

---

### 4. Image Processing: Canvas API with EXIF.js for metadata

**Decision**: Use HTML5 Canvas for thumbnail generation and EXIF.js for photo metadata extraction

**Rationale**:
- Built-in browser API: No external dependencies for basic operations
- Performance: GPU-accelerated rendering for fast image processing
- EXIF support: Extract camera settings, GPS, and拍摄日期
- Client-side only: No server processing required

**Alternatives Considered**:
- **sharp**: Node.js library, requires backend
- **jimp**: Heavy for browser, better alternatives exist
- **browser-image-compression**: Good but adds dependency

**Implementation Notes**:
- Use Canvas to resize images for thumbnails (e.g., 200x200)
- Extract EXIF data for拍摄日期 and camera info
- Store both original and thumbnail versions
- Implement progressive loading for large images
- Consider web workers for heavy image processing

---

### 5. Build Tool: Vite

**Decision**: Use Vite as the development server and build tool

**Rationale**:
- Fast HMR (Hot Module Replacement): Excellent development experience
- Native ES modules: No bundling overhead in development
- Optimized production builds: Rollup-based with excellent tree-shaking
- Simple configuration: Minimal setup required
- TypeScript support: Can add TypeScript later if needed

**Alternatives Considered**:
- **Webpack**: Slower HMR, more complex configuration
- **Parcel**: Less control over optimization
- **No build tool**: Harder to deploy, no optimization

**Implementation Notes**:
- Use vanilla JavaScript/HTML/CSS plugins
- Configure path aliases for cleaner imports
- Enable source maps for debugging
- Set up production build optimization
- Consider adding plugins for image optimization

---

### 6. Testing Framework: Vitest + Playwright

**Decision**: Use Vitest for unit/integration tests and Playwright for end-to-end tests

**Rationale**:
- **Vitest**:
  - Native Vite integration: Same config and HMR
  - Fast execution: Optimized test runner
  - Jest-compatible: Familiar API and matchers
  - Built-in mocking: Easy to mock dependencies

- **Playwright**:
  - Cross-browser testing: Chrome, Firefox, Safari
  - Auto-waiting: Reliable test execution
  - Visual regression: Can test UI consistency
  - Mobile testing: Emulated mobile devices

**Alternatives Considered**:
- **Jest**: Slower in Vite projects
- **Cypress**: More opinionated, heavier setup
- **Selenium**: Slower, less reliable than Playwright

**Implementation Notes**:
- Test database operations with in-memory SQLite
- Mock IndexedDB for unit tests
- Test drag-drop interactions with Playwright's drag API
- Test image upload with file input manipulation
- Use snapshot testing for UI components

---

### 7. UI Framework: Vanilla CSS with CSS Modules

**Decision**: Use vanilla CSS with CSS Modules for scoped styling

**Rationale**:
- Minimal dependencies: No framework overhead
- Scoped styles: Avoid global style conflicts
- Build-time processing: Vite handles CSS modules
- Performance: No runtime style processing
- Easy to learn: Standard CSS with minimal additions

**Alternatives Considered**:
- **Tailwind CSS**: Additional build complexity
- **Bootstrap/Foundation**: Too opinionated, heavy
- **Styled-components**: Not using React

**Implementation Notes**:
- Use CSS modules for component-specific styles
- Implement responsive design with CSS Grid and Flexbox
- Use CSS custom properties (variables) for theming
- Implement dark mode support with media queries
- Use modern CSS features (subgrid, container queries) where supported

---

## Architecture Patterns

### Data Flow

1. **Model Layer**: JavaScript classes representing Album and Photo entities
2. **Service Layer**: Database operations and business logic
3. **Storage Layer**: SQLite for metadata, IndexedDB for blobs
4. **View Layer**: DOM manipulation and event handling
5. **Component Layer**: Reusable UI components

### State Management

**Decision**: Simple state management with custom Store class

**Rationale**:
- No external dependencies needed
- Simple event-based updates
- Sufficient complexity for this app size
- Easy to understand and maintain

**Alternatives Considered**:
- **Redux/Vuex**: Overkill for this complexity
- **Zustand/Pinia**: External dependency not needed
- **Context API**: Not using React

---

## Performance Considerations

### 1. Image Loading Strategy

- Lazy loading for off-screen photos in tile view
- Progressive image loading with blur-up effect
- Thumbnail-first approach (load thumbnail, then full image on demand)
- Image caching with IndexedDB to avoid re-downloading

### 2. Database Optimization

- Use indexes on frequently queried columns (album_id, created_at)
- Implement pagination for large photo sets (e.g., 50 photos per page)
- Use prepared statements for repeated queries
- Consider denormalization for display-heavy queries

### 3. Drag and Drop Performance

- Use native drag API (already optimized by browsers)
- Implement debounce for reordering operations
- Update database in batches rather than on every drag event
- Use CSS transforms for smooth visual feedback

### 4. Memory Management

- Implement cleanup for off-screen images
- Use object pooling for frequently created/destroyed objects
- Monitor memory usage in production and implement limits

---

## Security Considerations

### 1. File Upload Validation

- Validate file type by checking magic bytes, not just extension
- Limit file size to prevent DoS attacks
- Sanitize file names to prevent path traversal
- Reject executables and potentially harmful files

### 2. XSS Prevention

- Escape user input before rendering to DOM
- Use textContent instead of innerHTML where possible
- Sanitize HTML if absolutely necessary (rare in this app)

### 3. Data Privacy

- All data stays client-side (no server transmission)
- Clear sensitive data on logout or explicit request
- Implement export functionality for user data portability

---

## Accessibility Considerations

- Keyboard navigation for all interactive elements
- ARIA labels for drag-drop controls
- Screen reader announcements for state changes
- Focus management for modals and dialogs
- Color contrast meeting WCAG AA standards
- Alternative text for all images

---

## Future Extensions (Out of Scope but Considered)

- PWA support for offline installation
- Full-text search using SQLite FTS5
- Face detection and auto-tagging
- Photo geolocation and map view
- Duplicate photo detection
- Automatic backup to cloud services
- Video support with thumbnail generation
