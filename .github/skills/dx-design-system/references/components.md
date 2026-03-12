# Component Usage Reference

Source: DX-DesignSystem Storybook — Components

All component rules below apply to **NBFC** unless a brand is specified. Federated-specific components are noted.

---

## Table of Contents

1. [Button (NBFC)](#button)
2. [Button Toggle (NBFC)](#button-toggle)
3. [Input (NBFC)](#input)
4. [Dropdown / Select (NBFC)](#dropdown)
5. [Checkbox (NBFC)](#checkbox)
6. [Accordion (NBFC)](#accordion)
7. [Tabs (NBFC)](#tabs)
8. [Dialog (NBFC)](#dialog)
9. [Section Marker (NBFC)](#section-marker)
10. [Datepicker (NBFC)](#datepicker)
11. [Slider (NBFC)](#slider)
12. [Navigation: Top Bar (NBFC)](#top-bar)
13. [Navigation: Breadcrumbs](#breadcrumbs)
14. [Navigation: Step Tracker (NBFC)](#step-tracker)
15. [Cards (Federated)](#cards-federated)
16. [Content Block (Federated)](#content-block)

---

## Button (NBFC) {#button}

### Variants

| Variant | Use case |
|---------|----------|
| **Primary** | The single most important action on a page. One per screen (excluding app header, modal, or side panel). Can have text + optional icon. |
| **Primary Icon** | Icon-only primary button — use when space is constrained and meaning is clear |
| **Secondary** | Subordinate, negative action paired with a primary button (e.g., "Cancel", "Back") |
| **Secondary Icon** | Icon-only secondary button |
| **Text / Tertiary** | Less prominent or independent actions; can appear alone or paired with primary |

### Critical rules

- **Never use a secondary button alone** — it must always accompany a primary button
- **Never use a secondary button for a positive action**
- **Only one primary button per viewport** (modal or panel counts as its own viewport)
- Tertiary buttons may appear in isolation when a primary button exists elsewhere on the page for the main action

---

## Button Toggle (NBFC) {#button-toggle}

Two or more mutually exclusive options. Changes take effect immediately (toggle doesn't require a submit action).

**Orientations**: Vertical or Horizontal

**Rules**:
- Use only for mutually exclusive choices (not for multi-select)
- The selection must update the setting instantly — do not use as a "choose then submit" pattern
- Minimum of 2 options; recommended maximum: 4-5 to avoid overflow

---

## Input (NBFC) {#input}

Text field for collecting user data.

**Accessibility requirements (all mandatory)**:
- Every field must have an **accessible name** (visible label or `aria-label`)
- Must be navigable by **keyboard** as well as mouse
- Background-to-field color contrast must meet **WCAG 1.4.3 AA**

**States**: Default, Hover, Focus, Filled, Error, Disabled

**Error state**: Display error message below the field using the error color (`#FF0000` family). Never use color alone — always include descriptive error text.

---

## Dropdown / Select (NBFC) {#dropdown}

Single-option selection from a list.

**Sizes**: Extra Small, Small, Medium (default), Large

**States**: Default, Hover, Selected, Disabled

**Accessibility**:
- Keyboard accessible
- Follows ARIA combobox pattern
- Clear visual feedback for each state

---

## Checkbox (NBFC) {#checkbox}

Binary yes/no choice for a single option, or multi-select within a group.

**States**: Unchecked, Checked, Indeterminate (for parent of mixed-state children)

**Usage guidance**:
- Single checkbox = yes/no binary toggle for a feature or option
- Group of checkboxes = multi-select from a list
- Do not use a checkbox where a radio button (mutually exclusive choice) is more appropriate

---

## Accordion (NBFC) {#accordion}

Collapsible sections for organizing large amounts of content.

### Variations

| Variation | Description |
|-----------|-------------|
| **Minimal** | No visible border around each section. Use for visually simple, content-focused interfaces. |
| **Read-Only Fields** | Accordion panels contain non-editable input fields. Visually distinct from editable versions. |

**Rules**:
- Ideal for compressing large amounts of content into a space-saving layout
- Read-only field variant: clearly communicate that fields are non-editable (visual treatment + disabled state)

---

## Tabs (NBFC) {#tabs}

Organize content into separate views — only one view visible at a time.

**Behavior**:
- Active tab is indicated by an **animated ink bar** and **background color change**
- **Always have a default selected tab** — typically the first tab
- Tab selection does not navigate to a new page; it switches the visible content panel

**Rules**:
- Do not use tabs for navigation between different pages/routes
- Tab labels must be concise and clearly describe the panel content

---

## Dialog (NBFC) {#dialog}

Modal window for critical, task-relevant information.

**Behavior**:
- **Disables all app functionality** until dismissed or required action is completed
- Centered by default with a **semi-transparent overlay** behind it
- Dismisses when: user completes the action, or clicks **outside** the dialog area
- Background does **not** scroll while dialog is open

**Scrolling inside dialog**:
- When content requires scrolling, the **title is pinned at the top** and **action button is pinned at the bottom**
- Dialog content scrolls independently of the background

**Accessibility**:
- All elements navigable by keyboard
- Apply `role="dialog"` with `aria-labelledby` and `aria-describedby`
- Maintain high contrast and legible fonts
- No color-only state indicators

---

## Section Marker (NBFC) {#section-marker}

Non-interactive visual cue for highlighting areas or indicating grouping.

**Critical rules**:
- **Purely decorative** — not clickable, not removable, triggers no actions
- Use NBFC **secondary colors** (never primary colors) to avoid competing with interactive elements
- Must combine color with another visual cue (border, icon, or spacing) — no color-only meaning
- Contrast: minimum **3:1** for UI component contrast; ideally **4.5:1** for text alongside markers
- Keep style and placement **consistent** across the application

---

## Datepicker (NBFC) {#datepicker}

Calendar-based date selection component.

**Accessibility**: Keyboard accessible; all date cells must be reachable via Tab/arrow keys.

---

## Slider (NBFC) {#slider}

Range or single-value selection via a draggable handle.

**Variations**: single value, range (two handles)

**Accessibility**: Keyboard controllable (arrow keys to increment/decrement value).

---

## Top Bar / Navigation System (NBFC) {#top-bar}

The Top Bar is composed of two components:

### 1. Header

- Primary area for **branding and utility actions**
- **4 variations**, available in **grey** or **teal**
- Responsive: adapts across screen sizes; simplified single-version on mobile

### 2. Navigation Menu

- Access to **main application sections**
- **2 variations**, designed for **desktop and tablet** only
- Mobile: use simplified header layout instead

**Rules**:
- Header and Navigation Menu together form the complete Top Bar
- Do not place the Navigation Menu on mobile viewports

---

## Breadcrumbs (NBFC & Federated) {#breadcrumbs}

Hierarchical trail showing the user's current location.

**Rules** (same for both brands):
- Reflect the actual page hierarchy — do not fabricate breadcrumb steps
- The last item (current page) should not be a link
- Keep breadcrumb labels short and consistent with page titles

---

## Step Tracker (NBFC) {#step-tracker}

Visual indicator of progress through a multi-step flow.

**States per step**: Completed, Active, Upcoming

**Rules**:
- Steps are numbered and always displayed in sequence
- Do not skip or reorder steps in the tracker
- The active step should be visually distinct from completed and upcoming steps

---

## Cards (Federated) {#cards-federated}

See `federated-brand.md` for full card specification and layout rules.

**Quick reference**:
- Static: icon, testimonial, steps variants
- Interactive: link/dynamic behavior
- Interactive Image-based: visual-first, entire card is a link
- Layouts: 1–4 columns; spacing principles apply to all

---

## Content Block (Federated) {#content-block}

A structured modular section for organizing content on a page.

**Three do/don't patterns are defined** (see Storybook asset: `Content Block Specs.jpg`).

**Rules**:
- Use for grouping related information with consistent internal spacing
- Do not use as a replacement for a card when interactivity is required
- Follow the visual hierarchy within the block (heading → body → action link if any)

---

## Shared Accessibility Rules (All Components)

1. All interactive elements must support **keyboard navigation** (Tab, Enter, Space, arrow keys as appropriate)
2. Every form input must have an **accessible name** (visible label, `aria-label`, or `aria-labelledby`)
3. All images must have **alt text** — empty `alt=""` if purely decorative
4. Color contrast must meet **WCAG 1.4.3 AA** (4.5:1 for normal text, 3:1 for large text and UI components)
5. **No color-only indicators** — state changes must be communicated via structure, text, or icons in addition to color
6. Use appropriate **ARIA roles and attributes** (`role="dialog"`, `aria-expanded`, `aria-current`, etc.)
