---
name: shadcn-surfaces
description: Compose well-spaced shadcn chat surfaces with render_ui.
version: 1.0.0
author: Dhruvil Shah (DesignInstantly), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [designinstantly, a2ui, shadcn, ui, layout, spacing, generative-ui, chat]
    category: designinstantly
---

# Shadcn Surfaces Skill

How to build interfaces in the user's chat with the designinstantly MCP server's `render_ui`, using
our shadcn catalog. You cannot set padding, margin, gap, colors or classes: **spacing comes only from
which components you pick and how you nest them.** This skill tells you what each container gives you
and how to compose surfaces that look designed instead of cramped. Component composition rules are
adapted from shadcn/ui's own agent skill (MIT, github.com/shadcn-ui/ui/tree/main/skills/shadcn).

## When to Use

- Before every `render_ui` call: a plan to approve, choices to pick from, a form, stats, a list.
- When a surface came back looking cramped, misaligned, or edge-to-edge.
- Not for plain answers. If a sentence or a short list does the job, write text; render a surface
  only when the user has to act on something or compare things at a glance.

## Prerequisites

- The designinstantly MCP server's `get_ui_catalog` and `render_ui` tools (co-worker sessions only).
- Read `get_ui_catalog` once per session for the exact props. It is facts only; this skill is how.

## How to Run

1. `get_ui_catalog` (once) for component names and props.
2. Pick a pattern from `references/patterns.md` and adapt it. Start from a pattern, not from scratch.
3. Check the draft against the Quick Reference and Pitfalls below, and `references/design.md` for
   hierarchy, grouping, density and action choices.
4. `render_ui` with a `surfaceId` that names the thing (`week-1-plan`), `components`, and `data` for
   anything inputs bind to. Re-rendering the same `surfaceId` replaces it.

## Quick Reference

What each container does to its children (full table: `references/spacing.md`):

| Container | Inside spacing | Gap between children | So put inside it |
|---|---|---|---|
| `Card` | 16px top/bottom, **0 left/right** | 16px | Only `CardHeader`, `CardContent`, `CardFooter` |
| `CardHeader` | 16px left/right | 4px | `CardTitle`, `CardDescription`, `CardAction` |
| `CardContent` | 16px left/right | **none** | **One** child: a `Column`, `FieldGroup`, `ItemGroup`, `Table`, `Tabs` |
| `CardFooter` | 16px all round, muted band, top border | **none** | One `Button`, or a `Row` of buttons (`justify: end`, `weight: 1`) |
| `Column` / `Row` | none | 12px (fixed) | Anything; `Row` wraps when narrow |
| `FieldGroup` | none | 20px | `Field`s, `FieldSet`s |
| `Field` | none | 8px | `FieldLabel`, control, `FieldDescription` / `FieldError` |
| `ItemGroup` | none | 16px | `Item`s |
| `Item` | 12px × 10px | 10px | `ItemMedia`, `ItemContent`, `ItemActions` |
| `TabsContent`, `AccordionContent`, `CollapsibleContent` | none | **none** | One `Column` when more than one child |
| `DialogFooter`, `AlertDialogFooter` | own band | 8px | Buttons directly |
| `Empty` | 24px, dashed border, centered | 16px | `EmptyHeader`, `EmptyContent` |
| `Alert` | own padding | small | `AlertTitle`, `AlertDescription` |

The 12px `Row`/`Column` gap is the only gap you control directly, and you can't change it. Get
bigger separation from structure: a `FieldGroup` (20px), separate `CardHeader` / `CardContent` /
`CardFooter` sections (16px), a `Separator`, or a second `Card`.

## Procedure

1. **Decide the shape.** One surface, one job. The root is usually a `Card`. Use `Empty` for
   nothing-here-yet states and a `Column` root for an `Alert` with buttons under it.
2. **Header first.** `CardTitle` says what this is in 2 to 6 words. `CardDescription` gives the one
   fact the user needs to decide. Status goes in a `Badge` inside `CardAction` (top right).
3. **One body.** `CardContent` gets exactly one child. Pick it by content:
   - a list of things → `ItemGroup` of `Item variant: outline` (never `Card`s inside a `Card`)
   - inputs → `FieldGroup` of `Field`s (see `references/patterns.md` → settings-form)
   - rows of numbers → `Table`
   - mixed text, badges, images → a `Column`
   - views of the same thing → `Tabs`, each `TabsContent` holding one `Column`
4. **Actions last.** Put them in `CardFooter`. One primary `Button` (default variant) for the thing
   you want them to do; everything else `outline` or `ghost`. Two or more buttons go in a `Row`
   with `justify: end` and `weight: 1`. Destructive actions use `variant: destructive`.
5. **Write the words.** Buttons are verbs naming the result ("Approve plan", not "OK"). The button
   `text` is what the user is shown as their reply, so it must read as a sentence on its own.
   Use the brand's voice in copy, sentence case, no trailing periods on titles or buttons.
6. **Bind and act.** Inputs bind `value`/`checked` to `{"path": "/key"}` and you seed `data`.
   The submitting `Button`'s `action.event.context` reads the same paths back.
7. **Check density.** The chat column is narrow. At most 3 things side by side in a `Row`; prefer
   stacking. Keep a surface under about 40 components; split long ones into steps.

## Pitfalls

- **Text or Buttons directly inside `Card`.** `Card` has no side padding; they touch the edge.
  Always go through `CardHeader` / `CardContent` / `CardFooter`.
- **Several children in `CardContent`, `TabsContent`, `AccordionContent`.** No gap: they stack
  flush. Wrap them in one `Column`.
- **Several buttons in `CardFooter`.** No gap: they touch. Wrap them in a `Row`.
- **`Column` inside `Column` to "add space".** It adds nothing. Use structure (see Quick Reference).
- **`Text variant: h3` as a card title.** Use `CardTitle`; headings belong to the section that owns
  them. Use `Text` headings only inside a `Column` body, at most one size step apart.
- **Status as colored text.** There are no colors. Use `Badge` (`secondary` for good news,
  `outline` for neutral, `destructive` for bad).
- **Orphaned parts.** `SelectItem` inside `SelectGroup` inside `SelectContent`; `TabsTrigger` inside
  `TabsList`; `ToggleGroupItem` inside `ToggleGroup`; `DropdownMenuItem` inside `DropdownMenuGroup`;
  `Avatar` always has an `AvatarFallback`; `Dialog`/`Sheet` always have a title.
- **Looping `Button`s as a picker.** 2 to 7 choices are a `ToggleGroup` (`spacing: 2`); a single
  choice from a short list with descriptions is a `RadioGroup`; long lists are a `Select`.
- **Every button primary.** One default-variant button per surface.
- **Labels without `Field`.** A bare `Label` + `Input` has no rhythm; use `Field` + `FieldLabel`.

## Verification

- `render_ui` validates strictly: an unknown prop (for example `padding`) or component is rejected
  with the reason. Fix it and call again; never drop the surface for text because of a rejection.
- Before sending, walk the tree: every `Card` child is a Card section; every `CardContent` /
  `TabsContent` / `CardFooter` with more than one child has been wrapped; exactly one primary button.
- After an action comes back, re-render the same `surfaceId` to show the new state (approved,
  saved) rather than leaving a stale surface with live buttons.
