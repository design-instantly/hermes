# Design judgment for chat surfaces

The catalog fixes the spacing, type scale and colors, so most "make it look good" choices are
already made. What's left is judgment: what to show, in what order, and how much.

## Hierarchy

- **One focal point.** Every surface answers one question ("approve this?", "which one?"). The
  title names it; the primary button resolves it. Everything else supports those two.
- **Read top to bottom: what, why, what next.** Title → the one fact that matters
  (`CardDescription`) → the detail (`CardContent`) → the decision (`CardFooter`).
- **Size means importance.** One large figure (`Text h2`) per stat block, its label in `caption`.
  Never two headings of the same size next to each other.
- **Muted for metadata.** Times, counts, platforms and secondary facts go in `ItemDescription`,
  `CardDescription`, `caption` or an `outline` `Badge`, not body text.

## Grouping

- **Proximity is meaning.** Things that belong together sit in the same container (one `Item`, one
  `Field`); different groups get structural separation (`ItemGroup`, `FieldGroup`, a `Separator`,
  separate Card sections). If two groups are only 12px apart, the user reads them as one.
- **Repeat the same shape.** List rows all use the same parts in the same order (media, content,
  actions). A row that breaks the pattern looks like a bug.
- **Align to one edge.** Text left-aligned; actions right-aligned (`ItemActions`, `Row justify: end`).
  Center only `Empty` states.

## Density

- **The chat column is narrow.** Stack by default; a `Row` holds at most 3 short things.
- **Show 3 to 7 items.** More than 7 rows: show the top ones and add a "Show all" `ghost` button, or
  use a `Table`. One item: no list, just say it.
- **Cut words.** Titles 2 to 6 words. Descriptions one line. No instructions the layout already
  makes obvious ("Click the button below to...").
- **No decoration.** No separators between every row, no badges that repeat the title, no images
  unless the picture is the content (a product, a creative).

## Actions

- **One primary.** Default-variant button for the main path, `outline` for the alternative, `ghost`
  for "later", `destructive` only for something that deletes or can't be undone.
- **Buttons say what happens.** "Schedule 5 posts", "Use this caption", not "Submit", "OK", "Yes".
  The label becomes the user's reply in the thread, so it must read well there.
- **Make the safe path easy.** For risky actions, put the consequence in an `Alert` above and make
  the safe button the first one.
- **Close the loop.** After the user acts, re-render the surface in its finished state (a `Badge`
  saying "Approved", buttons removed) so old buttons can't be pressed again.

## States

- Nothing to show → `Empty` with one action.
- Partial or failed → `Alert` above the content saying what's missing and what you'll do.
- In progress → say so in the description, or show `Progress` with a `caption`; don't render
  `Skeleton`s, since a surface doesn't update itself.
