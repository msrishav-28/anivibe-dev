# 💎 AniVibe: $10k Commercial Strategy & Design Masterplan

**Status:** Living Document
**Target Audience:** Gen Z Students (India)
**Design Philosophy:** "Neo-Tokyo Ethereal" / Cinematic Engineering
**Current State:** Backend Complete (100%) | Frontend Re-Architecture (0%)

---

## 1. Executive Audit & Pivot Strategy

### The "Iceberg" Reality
*   **Backend (The Engine):** Production-grade. 43 Endpoints, 5 ML Models (CLIP, BERT, GNN), Explainability. **Grade: A+**
*   **Frontend (The Body):** Currently functional skeleton. Lacks "soul" and visual connection to the AI backend. **Grade: C-**
*   **The Pivot:** We are moving from a "Corporate Dashboard" look to an **"Immersive Digital Experience"** to justify the $10k price tag.

### The $10k Differentiators (USPs)
1.  **Vibe Search (Not Genre Search):** Users search by *feeling* ("Depressing rainy days"), not just metadata.
2.  **Explainability (Glass Box AI):** We show *why* a recommendation happened ("98% Match because you like Cyberpunk").
3.  **Zero Cold Start:** Immediate utility for new users via content-based features.

---

## 2. Visual Identity System: "Neo-Tokyo Ethereal"

We are abandoning standard "SaaS" aesthetics for a high-contrast, kinetic anime look.

### A. Color Palette (Cyber-Emotion)
*   **Base (The Void):** `#050505` (Deep AMOLED Black - darker than standard gray)
*   **Primary (Spirit):** `#8B5CF6` (Electric Violet) - Used for "Vibe" elements.
*   **Secondary (Tech):** `#00F0FF` (Neon Cyan) - Used for UI interactive elements.
*   **Alert (Hype):** `#FF0055` (Crimson) - Used for Trending/Hot items.
*   **Glass:** `bg-black/40 backdrop-blur-xl border-white/10` (Frosted Acrylic).

### B. Typography (Manga-Editorial)
*   **Headers (Personality):** **Clash Display** (Open Source). Sharp edges, structural.
*   **Body (Utility):** **Satoshi** or **General Sans**. Clean, geometric, legible.
*   **Accents:** **Zen Tokyo Zoo** or **Noto Sans JP**. Used for faint, large Kanji watermarks behind English headers.

### C. Texture & Atmosphere
*   **Global Film Grain:** A fixed `div` overlay with noise texture (Opacity: 3%) to kill the "flat digital" look.
*   **Scanlines:** Faint horizontal lines (Opacity: 2%) for a retro-future CRT feel.
*   **Lighting:** The background lighting shifts color based on the selected "Vibe" (e.g., Sad = Blue, Hype = Red).

---

## 3. Core Component Blueprints

### A. The "Vibe Tuner" (Search Bar)
*   **Concept:** Not a text input, but a "Mood Synthesizer."
*   **Visual:** Glassmorphic pill shape.
*   **Interaction:**
    *   **Glitch Reveal:** Placeholder text decodes on load (`_` -> `#` -> `Type your mood`).
    *   **Pulse:** A rhythmic glowing pulse on the right side that speeds up as the user types.
    *   **Lighting:** Changing keywords changes the global R3F background color.

### B. The Holographic Anime Card
*   **Structure:**
    *   **Layer 1:** High-res Poster.
    *   **Layer 2 (Holo Foil):** CSS Gradient overlay that moves on `mousemove` (Parallax).
    *   **Layer 3 (Glass Pane):** Bottom info slide-up.
*   **Data Display:**
    *   **Score:** Neon Badge "98% MATCH" (No raw numbers).
    *   **Tooltip:** "Sparkle" icon reveals SHAP explanation ("Why this?").
*   **Interaction:** On hover, the character image subtly "pops" forward (Z-axis translation).

### C. The 3D Environment (R3F)
*   **Object:** **"Digital Petals"** or **"Data Embers."**
*   **Tech:** `InstancedMesh` (500-1000 particles).
*   **Physics:** Particles drift upward against gravity. Mouse cursor creates a "Repulsion Field" (turbulence).
*   **Performance:** Must use `drei/Instances` for mobile optimization. No heavy GLTF models.

---

## 4. User Experience (UX) & Flow

### Target Demographic: Gen Z Students (India)
*   **Constraint:** Mobile-first (90% traffic), Data-conscious, WhatsApp-heavy.

### A. Navigation (The Thumb Zone)
*   **Bottom Bar (Sticky):**
    1.  **Home** (Feed)
    2.  **Explore** (Vibe Tuner)
    3.  **My List** (Watchlist - Locked)
    4.  **Profile** (Stats/Cred)
*   **FAB (Floating Action Button):** "Quick Vibe" (AI Search) centered above the bar.

### B. The Acquisition Flow (Guest Mode)
1.  **Landing:** Hero Section -> Vibe Tuner -> Results. **(No Login Required)**.
2.  **Hook:** User sees results + "Reasoning Chips" (Proof of AI).
3.  **Conversion:** User taps "Add to Watchlist" -> Modal: "Sign up to save your vibe."

### C. The Retention Flow (Gamification)
*   **Weeb Cred:** Gamified profile stats (e.g., "Shonen King" badge).
*   **Heatmap:** GitHub-style watch history graph.
*   **Sharing:** Native WhatsApp Share button (generates a stat image).

---

## 5. Technical Implementation Roadmap

### Phase 1: The "Visual Core" (Days 1-2)
- [ ] Install `three`, `r3f`, `drei`, `framer-motion`.
- [ ] Create `GlobalStyles` (Noise, Scanlines, Typography).
- [ ] Build `CinematicContainer` (R3F Background Wrapper).
- [ ] Build `HolographicCard` (The primary UI unit).

### Phase 2: The "Interaction" (Days 3-4)
- [ ] Build `VibeTuner` (Search Component).
- [ ] Implement `api.semanticSearch` connection.
- [ ] Create `GlitchText` component for headers.

### Phase 3: The "Pages" (Days 5-7)
- [ ] Assemble `Landing Page` (Hero + Trending Carousel).
- [ ] Assemble `Detail Page` (Glassmorphic layout + SHAP tooltips).
- [ ] Assemble `Profile Page` (Heatmap + Charts).

### Phase 4: Optimization (Day 8)
- [ ] **Lighthouse Check:** Ensure TTI < 2s.
- [ ] **Lazy Loading:** Dynamic import for Recharts/D3.
- [ ] **Image Opt:** Strict `next/image` usage with Blur-up.

---

## 6. Critical Audits (Do Not Ignore)

1.  **Security:** Move JWT from `localStorage` to **HttpOnly Cookies** immediately.
2.  **Performance:** Do NOT load Three.js on low-power mode (check `navigator.hardwareConcurrency`).
3.  **Network:** Handle "N+1" API calls. Use **React Query** for caching and optimistic updates.
4.  **Mobile:** Kill the "Sidebar" concept. Use Bottom Navigation.

---

## 7. The $10k Checklist (Client Handoff)

*   [ ] Does the Search feel "magical" (Visual feedback)?
*   [ ] Is the "Why" (Explainability) clearly visible?
*   [ ] Does the app look "expensive" (Grain, Glow, Smooth Motion)?
*   [ ] Can a user find an anime in <30 seconds without login?
*   [ ] Is there a "Share to WhatsApp" button?

---

*Use this document as the source of truth for all design and engineering decisions moving forward.*
