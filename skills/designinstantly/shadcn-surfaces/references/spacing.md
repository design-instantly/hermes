# Spacing: what every container gives you

Read from DesignInstantly's shadcn components (`packages/ui`), which the catalog renders. Values are
the default size; `Card size: sm` and `Item size: sm | xs` tighten them. Nothing here is adjustable from
`render_ui`, so pick the container whose spacing you want.

## Layout primitives

| Component | Padding | Gap | Notes |
|---|---|---|---|
| `Column` | none | 12px | `align` defaults to `stretch` (children fill the width). `justify` and `weight` (flex-grow) available |
| `Row` | none | 12px | Wraps when the chat is narrow. `justify: spaceBetween` pins a label left and a value/badge right. Give it `weight: 1` inside a flex parent (such as `CardFooter`) so `justify` has room to work |
| `Separator` | none | n/a | A 1px rule. Use between groups inside a `Column`, never as the first or last child |
| `Text` | none | n/a | `h1` 24px, `h2` 20px, `h3` 18px, `h4` 16px, `h5` 14px (all semibold), `body` 14px, `caption` 12px muted |
| `Image` | none | n/a | `icon` 24px, `avatar` 40px round, `smallFeature` 96px wide, `mediumFeature` 240px wide, `largeFeature` full width up to 384px tall, `header` full width 192px tall |

## Card

| Part | Padding | Gap | Notes |
|---|---|---|---|
| `Card` | 16px top and bottom, 0 sides | 16px between sections | Rounded, ringed. With a `CardFooter` the bottom padding drops to 0 so the footer band sits flush. `size: sm` gives 12px |
| `CardHeader` | 16px sides | 4px | Grid: title and description stack; `CardAction` sits in the top-right corner |
| `CardTitle` | none | n/a | The surface's heading |
| `CardDescription` | none | n/a | 14px muted |
| `CardContent` | 16px sides | **none** | A plain box. Give it one child |
| `CardFooter` | 16px all sides | **none** | Muted background, top border, `flex` with items centered. Give it one `Button` or one `Row` |

## Forms

| Part | Padding | Gap | Notes |
|---|---|---|---|
| `FieldGroup` | none | 20px | The form body. Nested `FieldGroup`s get 16px |
| `FieldSet` | none | 16px | Related checkboxes, radios or switches with a `FieldLegend` |
| `Field` | none | 8px | `orientation: horizontal` puts control and label on one line (switches, checkboxes) |
| `FieldContent` | none | 2px | Label + description stacked beside a horizontal control |
| `FieldSeparator` | n/a | n/a | Labeled divider between form sections |
| `RadioGroup` | none | 8px | |
| `ToggleGroup` | none | `spacing` prop | `spacing: 2` (8px) separates the items; 0 joins them into one segmented control |
| `InputGroup` | own | own | Input with an addon (prefix text, a button). Use `InputGroupInput`, not `Input`, inside it |

## Lists, tables, feedback

| Part | Padding | Gap | Notes |
|---|---|---|---|
| `ItemGroup` | none | 16px | `size: sm` items tighten it to 10px |
| `Item` | 12px sides, 10px top and bottom | 10px | `variant: outline` gives each row a border (the list-in-a-card look); `muted` gives a filled row |
| `ItemContent` | none | 4px | `ItemTitle` + `ItemDescription` |
| `ItemActions` | none | 8px | Right-aligned buttons or badges |
| `ItemMedia` | none | 8px | `variant: image` for a thumbnail, `icon` for an icon tile |
| `Table` | n/a | n/a | Header cells 40px tall, 8px side padding; body cells 8px all round. Put it in `CardContent` |
| `Alert` | 10px × 8px | 2px | `AlertTitle` + `AlertDescription`; `variant: destructive` for warnings |
| `Empty` | 24px, dashed border | 16px | Centered; `EmptyHeader` (title, description) then `EmptyContent` (one button) |
| `Badge` | own | n/a | Small pill; the only way to show status |
| `Progress` | none | n/a | 4px bar, full width |

## Overlays and disclosure

| Part | Padding | Gap | Notes |
|---|---|---|---|
| `DialogContent` | 16px | 16px | `DialogHeader` (8px gap) then body then `DialogFooter` |
| `DialogFooter`, `AlertDialogFooter` | 16px, muted band | 8px | Buttons go in directly; right-aligned on wide screens |
| `SheetFooter` | 16px | 8px | Stacked buttons |
| `TabsContent` | none | **none** | One `Column` child |
| `AccordionContent` | 10px bottom | **none** | One `Column` child, or `text` alone |
| `CollapsibleContent` | none | **none** | One `Column` child |
