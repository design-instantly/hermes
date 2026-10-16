---
name: designinstantly-guide
description: How DesignInstantly works and how to do each task in it.
version: 1.0.0
author: Dhruvil Shah (DesignInstantly)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [designinstantly, product, guide, tasks, troubleshooting, otto]
    category: designinstantly
    related_skills: [shadcn-surfaces]
---

# DesignInstantly Guide Skill

DesignInstantly from start to end, the way the owner sees it and the way you work it: every page,
what each setting does, which of your tools does a task, and which tasks only the owner can do and
where. It does not hold the brand's own facts (products, posts, credits left): those come from your
tools, always.

## When to Use

- The owner asks how something works, where something is, what a setting does, what something
  costs, or whether you can do something.
- Before a task you haven't done in this conversation: making creatives, scheduling, cancelling,
  deleting.
- When a tool result surprises you: an error, a skipped platform, a failed post or job.
- Not for small talk. A greeting or a thank-you needs no guide, and the page the owner happens to
  be on is no reason to open it.

## Prerequisites

- The `designinstantly` MCP server's tools. They appear as `mcp_designinstantly_<name>`; this skill
  uses the short names (`generate_creative`, `create_post`, ...).
- `render_ui` and the `shadcn-surfaces` skill for anything the owner has to approve or pick.

## How to Run

1. Find the task in the Task map below. It names your tool, or the page where the owner does it.
2. Before acting or explaining in detail, open that area's reference with `skill_view`, for example
   `skill_view(name="designinstantly-guide", file_path="references/creatives.md")`:

   | File | Covers |
   |---|---|
   | `references/journey.md` | signup, onboarding, brands, navigation, account, emails, extension |
   | `references/shops-and-products.md` | connecting stores, syncing, product status, manual products, uploads |
   | `references/creatives.md` | creative types and options, Generate, jobs, Library, edits, captions, brand look |
   | `references/channels-and-posting.md` | social accounts, platform rules, scheduling, calendar, publishing |
   | `references/autopost.md` | Autopost settings, when it runs, how it plans a week |
   | `references/plans-credits-energy.md` | plans, credits, Energy, costs, billing |
   | `references/tools.md` | every tool of yours: when, how, gotchas; what has no tool |
   | `references/troubleshooting.md` | something went wrong: cause and fix |

3. Owner-only task: say exactly where (sidebar item, then the button's label) and offer the part
   you can do now.

## Quick Reference

### The owner's journey

1. **Sign up** at accounts.designinstantly.com (email and password, or Google).
2. **Onboarding, 3 steps:** name the brand; connect a store (Shopify, Etsy or WooCommerce, or skip
   and add products by hand); review the brand look (logo, fonts, colours).
3. **Meet you** on the welcome page, where you plan their first week together.
4. **Connect social accounts** in Integrations: Instagram, Facebook, Pinterest, TikTok.
5. **Make creatives** on Generate, or you make them.
6. **Put them on the calendar:** the creative drawer, Schedule, Calendar, or Autopost every week.
7. **Posts publish on their own** at their time. Published posts link to the platform from
   Calendar and Library.

DesignInstantly does **not** measure how posts perform: there are no likes, clicks, saves, reach or
sales figures anywhere, for you or the owner.

### App map

| Sidebar | Path | What's there |
|---|---|---|
| Dashboard | /dashboard | first-post checklist; then a chart of how many posts per day, by platform |
| Your Products | /products | synced and hand-added products; Sync; Add Product |
| Autopost | /autopost | this week's Autopost posts; the on/off switch; Generate for this week |
| Generate | /generate | make creatives step by step |
| Schedule | /schedule | creatives not yet scheduled; drag onto days; Auto Schedule |
| Library | /library | every creative (Generated, Scheduled, Posted); the creative drawer |
| Calendar | /calendar | month and week view; edit, drag to reschedule, cancel; failed posts |
| Integrations | /integrations | connect, reconnect, disconnect stores and social accounts |
| Uploads | /uploads | the owner's own images |
| Settings → Brand | /settings/brand | logo, name, description, colours, fonts; delete the brand |
| Settings → Creatives | /settings/creatives | include logo; caption instructions per platform; TikTok defaults |
| Settings → Autopost | /settings/autopost | posts per day, platforms, products, content types |
| Profile menu → Billing | /billing | plan, balances, top-ups, subscription |
| Support | /support | chat with the DesignInstantly team |

The header has the brand switcher, a spinner for running jobs, and your chat. The profile menu (top
right) shows three balances: **Energy**, **Generations** (standard credits) and **AI Generations**.

### Task map

| Task | You | The owner |
|---|---|---|
| Read products, shops, channels, posts, jobs, creatives | `list_*`, `get_*`, `search_products` | |
| Learn a creative type's inputs and cost | `start_generate_creative`, then `generate_creative` with `dryRun` | |
| Make creatives | `generate_creative`, after their yes | Generate |
| Schedule a creative | `create_post`, after their yes | creative drawer, Schedule, Calendar |
| Cancel a scheduled post | `cancel_post`, after their yes | Calendar → Cancel |
| Delete a creative | `delete_creative`, after their yes | Library |
| Reschedule; edit a scheduled caption; pick a Pinterest board; per-post TikTok options | no tool | Calendar or the creative drawer |
| Sync a store's products | no working tool | Your Products → Sync (also syncs daily) |
| Autopost on or off; posts per day, platforms, products, types | no tool | Autopost switch; Settings → Autopost |
| Caption instructions, include logo, TikTok defaults | read with `get_brand_settings` | Settings → Creatives |
| Logo, description, colours, fonts | no tool | Settings → Brand |
| Connect or reconnect a store or account | no tool | Integrations |
| AI-edit a creative; go back to an earlier version | no tool | Library → the creative → Edit Creative |
| A post from their own photo or video | no tool | Generate → Manual Post |
| Upload media | no tool (`list_media` reads it) | Uploads |
| Stop a running job | no tool | the job page → ⋯ → Cancel generation |
| Balances, plan, top-ups | no tool | Billing |
| Do something later, or every week | `cronjob` (see SOUL, Scheduled work) | |
| Show a plan or choices | `render_ui` | |

## Procedure

**Making creatives** (details: `references/creatives.md`, `references/tools.md`)
1. Pick products with `list_products` or `search_products`. Skip inactive ones and ones without
   images.
2. `start_generate_creative` for each type and format: it lists the item's fields and its cost.
3. `generate_creative` with `dryRun: true` for the exact credits. A quote does not check the
   owner's balance or plan.
4. Show the plan with `render_ui` and wait for their yes.
5. One `generate_creative` call for the whole plan, `idempotencyKey` set to the plan's surfaceId.
6. The app takes the owner to the job page. Nothing tells you when it ends: call `get_job_status`
   once when you need the result, never in a loop.

**Scheduling** (details: `references/channels-and-posting.md`)
1. `list_channels`. Only channels with `isConnected: true` can publish; targets are `targets[].id`.
2. `create_post` with a future time and the owner's timezone. Leave out `channelTargetIds` to post
   to every connected platform that fits the creative.
3. Compare the result with `list_channels`: a platform at its daily limit is skipped without an
   error.

**"Can you...?"** Task map first. No tool: say where the owner does it, then offer what you can do
now. Never describe a feature this skill doesn't.

## Pitfalls

- **Two kinds of credits plus Energy, all the brand owner's.** Standard credits (Generations) pay
  for template creatives; AI credits (AI Generations) pay for AI creatives and edits; Energy pays for
  your own work. Manual posts are free.
- **Some tool messages assume a different chat.** "The job view will post a message when
  generation finishes" is not true here.
- **A quote is not a go-ahead.** The real `generate_creative` call can still fail on the balance or
  the plan (UGC and Photoshoot videos need Growth or Enterprise).
- **`create_post` can't set captions, a Pinterest board or TikTok privacy.** It uses the creative's
  captions and the Settings → Creatives TikTok defaults.
- **`cancel_post` and `delete_creative` are permanent.** Deleting a creative also deletes its posts,
  published ones included.
- **`sync_shop` fails** with "backend service may be unavailable". Ask the owner to press Sync.
- **No performance data.** Never quote likes, clicks, saves or reach, or call a post a success.
- **Products have no prices.** Stores' prices are never imported.
- **The free plan shows the owner only 5 products, 2 images each.** You see all of them; say so when
  you mention a product they can't see.
- **Some app labels are wrong:** This or That and Guess the Price say "uses standard credits" but
  cost AI credits; the Photoshoot Video card says 5 seconds, it is 10; the "How Credits Work" window
  shows old prices. Trust the tool's quote.
- **Never edit this skill** with `skill_manage`. DesignInstantly maintains it, and an edited copy
  stops receiving updates. Save what you learn with `hindsight_retain` instead.

## Verification

- After `create_post`: `list_posts` with `status: "scheduled"` shows one post per platform it took.
- After `generate_creative`: one `get_job_status` before you report the outcome.
- When the app and this skill disagree, believe what the owner sees in the app, tell them, and save
  the difference with `hindsight_retain`.
