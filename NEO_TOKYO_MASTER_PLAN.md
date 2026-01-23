# 🏯 NEO-TOKYO MASTER PLAN: Full Technical Execution Strategy

> **Project:** AniVibe "Neo-Tokyo" Pivot
> **Goal:** Transform the $10k Backend into a Mobile-First Immersive Experience
> **Target Audience:** Gen Z (Mobile Interact)

---

# 🏗️ Phase 1 Technical Spec: The Visual Core

**Objective:** Establish the "Neo-Tokyo" atmosphere and build the atomic visual units.
**Output:** A working Next.js environment with the new design system, but no complex pages yet.

## 1. Dependency Injection
Execute the following installs immediately:

```bash
# 1. The 3D Engine
npm install three @types/three @react-three/fiber @react-three/drei

# 2. The Physics/Motion Engine
npm install framer-motion

# 3. Utilities
npm install lucide-react clsx tailwind-merge
```

## 2. Global CSS Architecture (`src/styles/globals.css`)
We must override the browser default painting to create the "film look".

### The "Film Grain" Overlay
Use a purely CSS/SVG approach to avoid loading heavy images.
```css
.film-grain {
  position: fixed;
  top: 0; left: 0; width: 100%; height: 100%;
  pointer-events: none;
  z-index: 9999;
  opacity: 0.03; /* 3% opacity */
  background-image: url("data:image/svg+xml,..."); /* SVG Noise */
  mix-blend-mode: overlay;
}
```

### The "Scanlines"
```css
.scanlines {
  background: linear-gradient(
    to bottom,
    rgba(255,255,255,0),
    rgba(255,255,255,0) 50%,
    rgba(0,0,0,0.1) 50%,
    rgba(0,0,0,0.1)
  );
  background-size: 100% 4px;
}
```

## 3. Design Tokens (`tailwind.config.ts`)
Hard-code the "Cyber-Emotion" palette.

```typescript
colors: {
  // The Void
  background: '#050505', 
  
  // The Vibe Spectrum
  spirit: '#8B5CF6', // Default/Magic
  tech: '#00F0FF',   // Info/Action
  hype: '#FF0055',   // Trending
  zen: '#10B981',    // Chill
}
```

## 4. Core Component: `<CinematicContainer />`
This wrapper replaces the standard `<div>` page wrapper.
*   **Responsibility:** Mounts the R3F `<Canvas>` *behind* the HTML content.
*   **Performance:** MUST check `window.devicePixelRatio`. If < 1 (low power), downgrade resolution.

## 5. Core Component: `<HolographicCard />`
The atomic unit of the interface.
*   **Props:** `posterUrl`, `title`, `matchScore`.
*   **Visuals:**
    *   No text descriptions initially.
    *   On Hover: Image scales 1.05x.
    *   On Hover: "Holo" gradient sheen moves across the surface.

---

# 🎮 Phase 2 Technical Spec: Interaction & The "Soul"

**Objective:** Build the interactive elements that make the app feel "alive."
**Focus:** Micro-interactions, haptics (visual), and navigation.

## 1. The `<VibeTuner />` (Search Component)
This replaces the standard input field.

### Visual Spec
*   **Shape:** `rounded-full` (Pill).
*   **Background:** Glassmorphism (`backdrop-blur-xl bg-white/5`).
*   **Border:** `border-white/10`.

### Interaction Logic
*   **State:** `inputValue` (string).
*   **Effect (The Pulse):**
    *   Use `framer-motion` to animate a `box-shadow` glow.
    *   **Logic:**
        *   If `inputValue` contains "Sad" -> Glow Color = Blue.
        *   If `inputValue` contains "Happy" -> Glow Color = Green.
        *   Default -> Glow Color = Purple.

## 2. The `<GlitchText />`
Replace standard headers with this component.
*   **Input:** `text` (string).
*   **Algorithm:**
    *   On mount, generate random characters for `length` of string.
    *   Every 50ms, resolve 1 character to the correct letter.
    *   **Result:** A "Cyberpunk" decoding effect.
*   **Font:** **Clash Display**.

## 3. Navigation Architecture (Mobile First)

### `<BottomNav />`
*   **Position:** Fixed, Bottom (`z-index: 50`).
*   **Items:** Home, Search (Vibe), Profile.
*   **Design:**
    *    Solid Black Glass (`bg-black/90`).
    *   Active State: Icon fills with `spirit` (Purple) color + small dot indicator below.

### The "FAB" (Floating Action Button)
*   **Position:** Center, floating *above* the bottom nav.
*   **Icon:** Sparkles/AI Brain.
*   **Action:** Triggers the "Quick Vibe" modal (Instant Voice/Text search).

## 4. Logic Wiring
*   Connect `<VibeTuner>` to `api.semanticSearch`.
*   **Debounce:** Ensure API calls only happen 500ms after typing stops.
*   **Loading State:** While fetching, the Vibe Tuner should pulse rapidly (Heartbeat animation).

---

# 🧩 Phase 3 Technical Spec: Page Assembly ("The Pivot")

**Objective:** Reassemble the application pages using the components from Phase 1 & 2.
**Strategy:** "Hollow Shell" replacement.

## 1. Landing Page (`src/app/page.tsx`)
**Goal:** Zero-friction acquisition.

*   **Layout:**
    *   **Background:** `<CinematicContainer>` (R3F Particles).
    *   **Center:** `<GlitchText text="What's your vibe?" />`.
    *   **Below Center:** `<VibeTuner />`.
    *   **Footer:** Horizontal scrolling list of "Trending Now" (`<HolographicCard>`).
*   **Critical Change:** Remove the "Hero Carousel". It's too generic. The Search *is* the Hero.

## 2. Detail Page (`src/app/anime/[id]/page.tsx`)
**Goal:** Immersive information consumption.

*   **Layout (The "Glass Pane"):**
    *   **Background:** Full-screen poster image, blurred (`blur-3xl`), darkened (`brightness-50`).
    *   **Foreground:** A single "Glass Sheet" modal rising from the bottom.
*   **Features:**
    *   **"Why This?" Tooltip:** A small "Sparkle" icon next to the Match Score.
        *   *On Click:* Opens a tooltip saying "Because you watched [Similar Anime]."
    *   **"Watch Trailer":** A primary CTA button with a `linear-gradient` border.

## 3. Profile Page (`src/app/profile/page.tsx`)
**Goal:** "Weeb Cred" (Gamification).

*   **Visuals:**
    *   **Avatar:** Hexagonal shape (Cyberpunk style).
    *   **Stats:**
        *   Replace "Table of ratings" with a **Heatmap** (GitHub style dots).
        *   Green Dot = Watched an episode.
        *   Purple Dot = Rated an anime.
*   **Badges:**
    *   Display "Shonen King" or "Romance God" based on genre stats.
    *   *Logic:* Find mostly watched genre -> Assign corresponding Badge.

## 4. Routing Changes
*   **Delete:** `/explore` (Old filter page).
*   **Redirect:** `/explore` -> Focus the `<VibeTuner>` on the Home Page.
*   **Reason:** We want users searching by vibe, not clicking checkboxes.

---

# ⚡ Phase 4 Technical Spec: Performance & Optimization

**Objective:** Ensure the "Neo-Tokyo" aesthetic runs smoothly on mid-range Android devices (~$200 phones).

## 1. The "Low Power" Mode
We cannot run full WebGL particles on every device.

### Detection Logic
Create a hook `useHardwareTier()`:
1.  Check `navigator.hardwareConcurrency` (CPU cores).
2.  Check `window.devicePixelRatio`.
3.  Check Network speed (`navigator.connection.saveData`).

### Implementation
*   **Tier A (High End):** Full R3F Particles + Post-Processing (Bloom).
*   **Tier B (Mid/Low):** Disable Particles. Use a static CSS radial gradient background.
*   **Tier C (Saver):** Disable Glassmorphism (`backdrop-filter`). Use solid semi-transparent colors.

## 2. Bundle Optimization
*   **Tree Shaking:** Ensure `lodash` or full `three` isn't bundled. Import only used sub-modules.
*   **Lazy Loading:**
    *   Wrap `<CinematicContainer>` in `next/dynamic` with `ssr: false`.
    *   This ensures 3D code stays out of the initial HTML payload (improving TTI).

## 3. Image Optimization
*   **Poster Images:**
    *   Enforce `next/image`.
    *   Use `placeholder="blur"` (BlurDataURL) for that "loading in" effect.
    *   Size: `33vw` (Mobile grid), `20vw` (Desktop).

## 4. Security Audit (Pre-Launch)
*   **Auth Token:**
    *   *Audit:* Check where the JWT is stored.
    *   *Action:* If `localStorage`, move to `HttpOnly Cookie`.
    *   *Reason:* XSS attacks can seal `localStorage`. Cookies are safer.
