# Autopost

Autopost fills next week's calendar on its own: every week it makes the posts that are missing and
schedules them. It is rule-based, not you. It spends the owner's credits like any generation, and no
Energy.

## Who has it

Starter (up to 2 posts a day), Growth (up to 5), Enterprise (up to 10). Not Basic or Extension Only;
the sidebar item shows a crown and switching it on asks them to upgrade. These numbers change.

## The Autopost page (`/autopost`)

- Before any settings are saved, the page shows the settings and an estimate of credits per week.
- **On/Off switch** in the header. Turning it **on** needs a connected social account and a plan
  with Autopost. It doesn't generate anything at once: the week shows "No posts this week" with
  **"Generate for this week"**.
- Turning it **off** cancels the Autopost posts already scheduled (the dialog says "this week", but
  it removes them in every week).
- **The week view** (Monday to Sunday, arrows for other weeks): posts by day with time, title and
  platforms. The owner can click one to edit, drag it to another day, remove it, or "+" to add a
  creative from the Library to a day.
- While a run works: "Generating & scheduling posts…" with progress; posts appear as they're made.
- A failed run shows "Last generation failed" with **Retry**.

## Settings → Autopost (`/settings/autopost`)

- **Posts per Day:** 1 to 10, capped by the plan. The same number spaces Auto Schedule on the
  Schedule page.
- **Platforms:** which connected platforms Autopost posts to; at least one. Once saved, the list
  is fixed: a platform connected later isn't added until the owner ticks it. Removing a platform
  cancels its upcoming Autopost posts.
- **Products to post:** all products by default; "Manage" excludes some. New products are included
  automatically. Only active products with images are used. If every product is excluded, it uses
  all of them.
- **Content Types:** Image Posts and Carousel Posts (templates, always on); UGC, Product Photoshoot
  and Features & Benefits (AI, on by default); Product Photoshoot Video (AI, off by default). The
  plan must allow each.
- The timezone is taken from the owner's browser when they save or switch Autopost on.

You can't read or change any of this. The owner does it here.

## When it runs

- **Every Saturday at 05:50 UTC** it plans and fills the **coming Monday to Sunday**.
- "Generate for this week" (or a future week) runs it on demand.
- It skips a brand when that week already has a run, the plan has no Autopost, no chosen platform is
  connected, or the brand has no owner.
- When a run finishes, the owner gets an email with a link to the Autopost page.

## How it plans a week

1. **Fills gaps only.** For each day: posts per day, minus what's already scheduled that day (posts
   the owner or you scheduled count; a creative on several platforms counts once).
2. **Reuses first.** Creatives an earlier run made for that week but didn't schedule are used before
   anything new is made.
3. **Times:** random times in the morning (8 to 11), afternoon (13 to 17) and evening (18 to 22) in
   the brand's timezone, at least 3 hours from now and 30 minutes apart.
4. **Budget:** it divides the owner's AI credits over the weeks left until their plan renews, so a
   week never spends the month. With room, every slot gets AI photos and videos; with less, AI photos;
   with little, a few AI photos and templates for the rest.
5. **Products:** products never posted come first, new products are moved up, and every eligible
   product is used before any repeats.
6. Each creative is scheduled the moment it's made, to the chosen platforms' recommended targets,
   with one Pinterest board and the TikTok defaults from Settings → Creatives.

## Autopost and you

- Weekly volume is Autopost's job: it costs credits only. Your own weekly task costs Energy too, so
  suggest Autopost for "just keep posting" and your own scheduled work for judgement: picking what to
  feature, preparing a plan for them to approve.
- Autopost fills only gaps, so posts you schedule first are kept and it makes fewer.
- If the owner wants Autopost on a day other than Saturday: it can't be changed. Offer your own
  weekly task on their day instead.
