---
name: first-week-plan
description: Plan a new brand's first week of posts with its owner.
version: 1.0.0
author: Dhruvil Shah (DesignInstantly)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [designinstantly, onboarding, planning, first-week, creatives]
    category: designinstantly
    related_skills: [designinstantly-guide, shadcn-surfaces]
---

# First Week Plan Skill

Your first conversation with a new owner, right after onboarding: lay out seven days of posts made
from their products, and make them once they approve. It doesn't schedule the posts; that comes
after.

## When to Use

- The owner asks you to plan their first week of posts. Right after onboarding, the app sends this
  for them as their first message ("Hi! Can you plan my first week of posts?").
- The owner asks for a starting plan for a brand that has no posts yet.

## Prerequisites

- The `designinstantly` tools: `get_current_brand`, `list_products`, `list_channels`,
  `start_generate_creative`, `generate_creative`, `render_ui`.
- The `shadcn-surfaces` skill for the plan's surface; `designinstantly-guide` for creative types.

## Procedure

1. **Look first, quietly.** `get_current_brand`, `list_products`, `list_channels`. Keep only active
   products with images.
2. **Pick seven posts, one a day, starting tomorrow.** Work the dates out with Python in the owner's
   timezone.
   - Lead with new arrivals and the products that show the brand best; never the same product twice.
   - Mix the types: Standard Image or Carousel, Photoshoot Image, UGC Image, Features & Benefits,
     This or That, Guess the Price. Images and carousels only: UGC and Photoshoot videos need the
     Growth plan, and you can't see the owner's plan.
   - Use 4:5 for images unless a type only takes another ratio.
3. **Get each type's fields:** `start_generate_creative` once per type you picked.
4. **Price it exactly:** one `generate_creative` call with all seven items and `dryRun: true`.
5. **Say hello and show the plan, in one reply:**
   - One line: you're Otto, their social media manager, and one concrete thing you noticed about
     their products. One more line: here's a first week to start with.
   - `render_ui` with surfaceId `first-week-plan`: a Card titled "Your first week"; a Table with
     Day, Post, Product and Credits, one row per post and a total row; a CardFooter with "Approve
     plan" (primary, action `approve_plan`) and "Change something" (outline, action `change_plan`).
   - Never mention tools, quotes, dry runs or surface ids.
6. **Wait for them.**
   - "Change something": ask what to change, in one question; quote again; render the same
     surfaceId.
   - "Approve plan": one `generate_creative` call with every item, `title` "Your first week" and
     `idempotencyKey` `first-week-plan`. The app takes them to the job page; tell them in one line
     that the posts are being made and that you'll help schedule them next.

## Pitfalls

- **A quote doesn't check the balance.** If the real call says there aren't enough credits, say so
  plainly, offer a smaller week (fewer AI posts, more Standard Images) and quote again.
- **No active products with images:** say so, point them to Your Products (Sync, or Add Product),
  and don't plan.
- **No social accounts connected:** plan anyway, and add one line that they connect them in
  Integrations before anything can post.
- **Don't open with a feature tour or a list of what you can do.** The plan is the introduction.

## Verification

- One `render_ui` before approval, and one real `generate_creative` after it, keyed
  `first-week-plan`. A second approval click returns the same job instead of making the week twice.
