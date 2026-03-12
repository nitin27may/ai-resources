# NBFC Brand Reference

Source: DX-DesignSystem Storybook — Brand Identity/NBFC/Foundation

---

## Color Palette

### Core Brand Colors (use for primary UI surfaces, text, accents)

| Name | Hex | Usage |
|------|-----|-------|
| Soft Black | `#121212` | Body text, high-emphasis elements |
| Grey | `#555659` | Secondary text, borders, icons |
| Primary 1 (Teal-Blue) | `#057398` | Primary actions, links, CTAs |
| Secondary 1 (Deep Purple) | `#632C4F` | Accent, brand headers |
| Secondary 2 (Magenta-Purple) | `#853175` | Accent |
| Secondary 3 (Soft Purple) | `#9E57A2` | Accent |
| Secondary 4 (Navy) | `#004987` | Deep backgrounds, banners |
| Secondary 5 (Bright Blue) | `#00A0DF` | Highlights, active states |
| Secondary 6 (Sky Blue) | `#57C0E8` | Light accents, info states |
| Error | `#FF0000` | Error messages, destructive actions |
| Success | `#259638` | Confirmation, success states |

### Color Anatomy (tints per color)

Each brand color has a full tint scale. For Primary 1 (`#057398`) as an example — apply the same pattern to other colors:

| Tint | Hex |
|------|-----|
| Darkest (75%) | `#011D26` |
| Darker (50%) | `#02394C` |
| Dark (25%) | `#045672` |
| **Default** | **`#057398`** |
| Light (25%) | `#4496B2` |
| Lighter (50%) | `#81B8CB` |
| Lightest (75%) | `#C0DCE5` |
| Faint (90%) | `#E6F1F5` |

**Grey tint scale:**
`#555659` → 80%: `#77787A` → 60%: `#999A9B` → 50%: `#AAAAAC` → 40%: `#BBBBBD` → 30%: `#CCCDCE` → 20%: `#DDDDDE` → 10%: `#EEEEEF`

**Error tint scale:**
`#FF0000` → dark 25%: `#BF0000` → light 25%: `#FF4040` → lighter 50%: `#FF7F7F` → lightest 75%: `#FFBFBF`

**Success tint scale:**
`#259638` → dark 25%: `#1C712A` → light 25%: `#5CB16A` → lighter 50%: `#92CA9B` → lightest 75%: `#C8E5CD`

### Tailwind CSS custom tokens (in tailwind.config.js)

These override Tailwind defaults — **never assume standard Tailwind colors apply**:

| Tailwind token | Actual hex | Notes |
|---------------|------------|-------|
| `green-500` | `#C0D731` | Lime/chartreuse — NOT standard green |
| `gray-500` | `#58585A` | NBFC grey |
| `teal-500` | `#00968F` | NBFC teal |
| `blue-500` | `#DEE8ED` | Very light blue |
| `black` | `#121212` | Soft black |
| `error` | `#f44336` | Error red |

Opacity variant suffixes: `a500` = 80%, `b500` = 60%, `c500` = 40%, `d500` = 20%, `e500` = 10%
Example: `bg-teal-a600` = teal `#00847D` at 80% opacity.

---

## Typography

### Digital Applications

**Font family: Proxima Nova** — used for ALL Northbridge internal digital applications.

Weight hierarchy: bolder = more important.

| Role | Font | Weight | Notes |
|------|------|--------|-------|
| Display / H1 | Proxima Nova | 700 Bold | Page titles |
| H2 / Section | Proxima Nova | 600 SemiBold | Section headers |
| H3 / Subsection | Proxima Nova | 500 Medium | Subsection titles |
| Body | Proxima Nova | 400 Regular | Default body text |
| Label / Caption | Proxima Nova | 400 Regular | Form labels, captions |
| Emphasis | Proxima Nova | 700 Bold | Bold body copy |

### Marketing Materials

- **Primary**: Freight Sans Pro
- **Secondary / Print**: Freight Micro Pro

> Do NOT use marketing typefaces in digital application UI. Proxima Nova only for digital.

---

## Grid & Layout

### Screen sizes

- **Base canvas**: 1440×1024 px or 1280×1024 px
- Mobile: single-column simplified layout

### Grid system

- **6 columns**
- **25 px gutters** between columns
- Margins: space between content and screen edge

### Breakpoints

Defined visually in Storybook (see Breakpoints.png asset). Responsive behavior adapts the column grid for desktop → tablet → mobile.

### Layout Patterns

Choose based on use case:

| Pattern | Best for | Key trait |
|---------|----------|-----------|
| **Dashboard** | KPIs, executive overview | Multiple widgets side-by-side, high data density |
| **Master-Detail** | Admin panels, CRUD | List on left, detail panel on right |
| **Multi-Column** | Knowledge bases, CMS | Side nav + main content + context panel |
| **Responsive Card Grid** | Listings, profiles, galleries | Adapts columns by breakpoint |
| **Split Form/Grid** | Data mgmt, inventory | Grid + inline form side by side |

---

## Iconography

Icons are provided as PNG assets in the stories/assets directory.
Naming pattern: `icon-<action>-<style>.png` (e.g., `icon-edit-circle-filled.png`, `icon-arrow-right.png`).

Styles: `filled` and `outline` (where available).
Icon sizes in data visualization context: 32px and 52px variants.

---

## Accessibility Requirements

All NBFC UI must meet:
- **WCAG 1.4.3 AA** color contrast minimum
- Full **keyboard navigation** for all interactive elements
- **ARIA labels** on all interactive elements and form inputs
- **Alt text** on all meaningful images; empty `alt=""` for decorative images
- **No color-only indicators** — state must be communicated structurally (icon, text, border) as well as by color
