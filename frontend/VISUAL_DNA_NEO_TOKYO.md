# 🧬 AniVibe Visual DNA: "Neo-Tokyo Ethereal"
**Version:** 1.0 (Commercial Grade)
**Target:** $10k Premium MVP
**Aesthetic Core:** Immersive, Kinetic, Atmospheric, High-Contrast

---

## 1. The Core Philosophy
**"It's not a database; it's a window into a digital world."**
Standard web design (flat colors, simple cards) is forbidden. Every element must feel like it exists in a 3D, light-emitting environment. The interface should feel like a high-end HUD from a Makoto Shinkai film or *Cyberpunk: Edgerunners*.

---

## 2. Global Atmosphere & Texture

### A. The "Void" Foundation
*   **Background Color:** `#050505` (Deep AMOLED Black). Never pure `#000000` (too harsh), never `#1F1F1F` (too gray/cheap).
*   **Vignette:** A radial gradient overlay to darken the edges, focusing attention on the center.
    ```css
    background: radial-gradient(circle at center, transparent 0%, #000000 100%);
    opacity: 0.6;
    pointer-events: none;
    ```

### B. The "Film" Grain (Crucial)
A fixed, full-screen overlay to break the "digital sharpness."
*   **Technique:** SVG Noise Filter or high-res noise PNG.
*   **Opacity:** `3% - 4%` (Subtle).
*   **Blend Mode:** `overlay` or `soft-light`.
*   **Animation:** Use `steps(10)` to jitter the noise slightly every frame (12fps) for a "live" film feel.

### C. The "Scanline" Mesh
A faint overlay of horizontal lines to mimic high-end CRT or HUD displays.
*   **Height:** `2px` repeating pattern.
*   **Color:** `#FFFFFF` at `1%` opacity.
*   **Pointer Events:** `none`.

---

## 3. Typography System ("Manga Editorial")

### A. Display Headings (The "Personality")
*   **Font Family:** **Clash Display** (Weights: Semibold, Bold).
*   **Characteristics:** Sharp edges, high contrast strokes.
*   **Usage:** Hero titles, Section headers.
*   **Letter Spacing:** `-0.02em` (Tight).
*   **Effect:** Often paired with a "Glitch" reveal animation or a subtle glow.

### B. Body & UI (The "Utility")
*   **Font Family:** **Satoshi** or **General Sans** (Weights: Regular, Medium).
*   **Characteristics:** Geometric, highly legible at small sizes.
*   **Usage:** Descriptions, Button text, Metadata.

### C. Decorative Accents (The "Soul")
*   **Font Family:** **Zen Tokyo Zoo** or **Noto Sans JP** (Bold).
*   **Usage:** Massive, low-opacity (5%) Kanji watermarks behind English headers.
    *   *Example:* Behind "TRENDING", place huge "流行" text.

---

## 4. Color Palette & Lighting

### A. The "Vibe" Spectrum
Lighting is dynamic. The accent color shifts based on the user's "Mood" selection.

| Mood | Hex Code | Visual Feeling |
| :--- | :--- | :--- |
| **Spirit (Default)** | `#8B5CF6` (Electric Violet) | Mysterious, Magic, Ethereal |
| **Tech/UI** | `#00F0FF` (Neon Cyan) | Action, Digital, Clean |
| **Hype/Warning** | `#FF0055` (Crimson Red) | Intensity, Danger, Trending |
| **Melancholy** | `#4F46E5` (Indigo) | Deep, Sad, Rain |
| **Peace** | `#10B981` (Emerald) | Slice of Life, Nature |

### B. Glassmorphism 2.0 (The "Frosted Acrylic")
Standard blur is boring. We use "Etched Glass."
*   **Background:** `rgba(0, 0, 0, 0.4)` (Dark).
*   **Backdrop Blur:** `blur(16px)` or `blur-xl`.
*   **Border:** `1px solid rgba(255, 255, 255, 0.08)` (Very faint white).
*   **Inner Shadow:** `inset 0 0 20px rgba(255, 255, 255, 0.02)` (To give volume).

---

## 5. Component DNA

### A. The "Holographic" Anime Card
*   **Ratio:** 2:3 (Vertical Manga Cover).
*   **Corner Radius:** `12px` or `16px`.
*   **The "Holo" Foil:**
    *   A pseudo-element overlay with a `linear-gradient(115deg, transparent, rgba(255,255,255,0.2), transparent)`.
    *   **Interaction:** Moves opposite to mouse position (`transform: translateX()`).
*   **The "Pop-Out":**
    *   On hover, the main image scales (`1.05`).
    *   The container has `overflow: visible` (if possible) or uses 3D tilt (`rotateX/Y`) to feel physical.
*   **The Badge:**
    *   **"98% MATCH"** tag using a Neon Green glow (`box-shadow: 0 0 10px #10B981`).

### B. The "Vibe Tuner" (Search Bar)
*   **Shape:** Full Pill (`border-radius: 9999px`).
*   **Height:** `64px` (Large, finger-friendly).
*   **Visual:** Glassmorphic container.
*   **Animation:**
    *   **Idle:** A soft, breathing glow on the right edge (`box-shadow` pulse).
    *   **Typing:** The glow intensifies and changes color to match the typed keyword (e.g., "Sad" -> Blue Glow).

### C. Buttons & CTAs
*   **Primary Button:**
    *   **Background:** Linear Gradient (`#8B5CF6` to `#6366F1`).
    *   **Glow:** `box-shadow: 0 0 20px rgba(139, 92, 246, 0.5)`.
    *   **Text:** Uppercase, tracked wide (`0.05em`), Bold.
*   **Secondary Button:**
    *   **Style:** Ghost/Outline (`border: 1px solid rgba(255,255,255,0.2)`).
    *   **Hover:** Fills with white (`bg-white text-black`).

---

## 6. Motion Physics (Framer Motion)

### A. "Kinetic Snappiness"
Anime action is fast. Don't use "slow, luxurious" springs.
*   **Spring Config:** `{ stiffness: 400, damping: 25 }`.
*   **Feeling:** Sharp, precise, instant settling.

### B. "Glitch" Text Reveal
*   **Trigger:** On mount / scroll into view.
*   **Effect:** Characters cycle random glyphs (`X`, `#`, `?`, `∆`) for 300ms before snapping to the correct letter.

### C. Staggered Lists
*   **Container:** `staggerChildren: 0.05`.
*   **Items:** `y: 20` -> `y: 0`, `opacity: 0` -> `opacity: 1`.
*   **Effect:** Cards ripple in like a deck being spread out.

---

## 7. The 3D Environment (R3F)

### A. The "Digital Petals" System
*   **Object:** `InstancedMesh` (Triangle or Petal geometry).
*   **Count:** ~500 - 800 particles.
*   **Movement:** Slow upward drift (`y += speed`).
*   **Material:** `MeshBasicMaterial` with `additive` blending (glowing).
*   **Interaction:**
    *   **Turbulence:** Mouse movement adds velocity to nearby particles (Fluid dynamics simplified).
    *   **Color:** Particles inherit the global "Mood" color.

### B. The "Aura" Background
*   **Object:** A giant, blurred sphere behind the content.
*   **Shader:** `NoiseMaterial`.
*   **Animation:** Slowly morphs shape and color. Acts as the ambient light source for the UI.

---

## 8. Mobile Specifics ("Thumb Zone")

### A. Bottom Navigation
*   **Height:** `80px`.
*   **Material:** Solid Black Glass (`bg-black/80 backdrop-blur-xl`).
*   **Icons:** Lucide React icons, stroke width `1.5px`.
*   **Active State:** Icon glows and fills with Accent color.

### B. FAB (Floating Action Button)
*   **Position:** Center, floating 20px above the Bottom Bar.
*   **Size:** `56px`.
*   **Icon:** A sparkle or "AI" brain icon.
*   **Effect:** Constant slow pulse animation.

---

**Use this DNA as the strict source of truth for all visual decisions.**
