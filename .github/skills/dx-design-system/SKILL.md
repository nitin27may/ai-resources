---
name: dx-design-system
description: Apply the NBFC / Federated design system from the DX-DesignSystem repository to generate spec-compliant UI or audit existing UI for design violations. Use this skill whenever the user asks to: create, build, or generate any UI component or screen for NBFC or Federated; review, audit, check, or validate existing UI against the design system; fix UI inconsistencies or off-brand styles; or apply design tokens, theming, colors, typography, or spacing from the Northbridge Financial / TruShield / Federated design system. Trigger even for casual requests like "does this look right?" or "make this match our design system" — any UI quality question in this repo should use this skill.
---

# DX Design System Skill

This skill represents the **NBFC / Federated design system** from the DX-DesignSystem Storybook repository. Use it to generate spec-compliant UI (framework-agnostic — produce design tokens and rules) or to audit existing UI and produce a structured report of violations with fix suggestions.

## Step 1: Determine Mode

Read the user's request and decide which mode to use:

- **Generate mode** — User wants to create new UI (components, screens, layouts)
- **Audit mode** — User wants to check existing UI against the design system
- **Both** — User wants to fix existing UI (audit then apply fixes)

If unclear, ask: "Do you want me to generate new UI following the design system, or audit existing UI for violations?"

## Step 2: Identify Brand

Check whether the request is for **NBFC** (Northbridge Financial / TruShield Insurance internal apps) or **Federated** (federated.ca website/consumer product). If unclear, ask.

Then load the appropriate reference file:
- NBFC → read `references/nbfc-brand.md`
- Federated → read `references/federated-brand.md`
- Both → read both

Also read `references/components.md` for shared component usage rules.

---

## Generate Mode

When generating UI, always output **framework-agnostic design guidance** that includes:

1. **Token values** — Exact hex colors, font names, font sizes/weights, spacing values
2. **Component structure** — What elements to use and their hierarchy
3. **Coded example** — A working implementation in whichever framework the user specifies (or HTML/CSS if unspecified)

### Layout defaults (NBFC)

- Base canvas: **1440×1024 px** or **1280×1024 px**
- Grid: **6 columns**, **25 px gutters**
- Choose a layout pattern based on use case:
  - **Dashboard** → executive overviews, KPIs, multiple widgets at a glance
  - **Master-Detail** → admin panels, CRUD, data entry
  - **Multi-Column** → knowledge bases, CMS, side-nav + content + tools
  - **Responsive Card Grid** → product listings, profiles, galleries
  - **Split Form/Grid** → data management, inventory, form-driven dashboards

### Generate checklist

Before returning generated UI, verify:
- [ ] Colors are from the brand palette (not generic CSS/framework defaults)
- [ ] Typography uses the correct font family (Proxima Nova for NBFC, Century Gothic Pro + Museo Slab for Federated)
- [ ] Interactive elements have keyboard navigation and ARIA labels
- [ ] Error/success states use the semantic status colors (not arbitrary colors)
- [ ] Component behavior matches the rules in `references/components.md`

---

## Audit Mode

Systematically review the provided UI code or description against the design system. After reviewing, produce a structured **Audit Report** in this exact format:

```
# Design System Audit Report

## Summary
- **Brand**: NBFC | Federated | Both
- **Files reviewed**: [list]
- **Total violations found**: N (Critical: X, Warning: Y, Info: Z)

## Violations

### [CRITICAL] <Short violation title>
- **Location**: `filename.vue` line 42 / component name / CSS class
- **Issue**: What is wrong and why it breaks the design system
- **Fix**: Exact corrected value or code snippet

### [WARNING] <Short violation title>
- **Location**: ...
- **Issue**: ...
- **Fix**: ...

### [INFO] <Short violation title>
- **Location**: ...
- **Issue**: ...
- **Suggestion**: ...

## Compliant Elements
Brief note of what already follows the design system correctly.
```

### Severity guide

| Level | When to use |
|-------|-------------|
| CRITICAL | Wrong brand color, wrong font family, missing accessibility attribute (ARIA/alt), broken contrast ratio |
| WARNING | Off-spec tint/shade, wrong font weight, spacing not aligned to grid, component used outside its intended purpose |
| INFO | Minor inconsistency, stylistic deviation, documentation suggestion |

### Audit checklist

Check each of these in order:

**Colors**
- Are all colors from the brand palette? (check `references/nbfc-brand.md` or `references/federated-brand.md`)
- Are semantic colors used correctly? (error → #FF0000 family, success → #259638 family)
- Are opacity variants using the defined tints, not arbitrary opacity or mix()? (NBFC Tailwind uses `a500`/`b500`... suffixes)

**Typography**
- Is the correct font family applied? (Proxima Nova for NBFC digital; Century Gothic Pro + Museo Slab for Federated)
- Are font weights from the defined weight set?
- Are heading/body/label sizes following the text token table?

**Spacing & Layout**
- Does the layout match one of the five defined patterns?
- Are gutters/margins consistent with the 25 px gutter grid?
- Are screen sizes within the 1280–1440 px base range?

**Components**
- Is each component being used according to its rules in `references/components.md`?
- Are forbidden usage patterns present (e.g., standalone secondary button, misuse of primary button hierarchy)?

**Accessibility**
- Does every input have an accessible label?
- Do all interactive elements support keyboard navigation?
- Do images have alt text (empty `alt=""` for decorative)?
- Does color contrast meet WCAG 1.4.3 AA minimum?
- Are color-only indicators absent (state always communicated structurally too)?

---

## Reference files

| File | When to read |
|------|-------------|
| `references/nbfc-brand.md` | Any NBFC-brand work — colors, typography, grid |
| `references/federated-brand.md` | Any Federated-brand work — colors, typography |
| `references/components.md` | Specific component rules, dos/don'ts, and usage guidance |
