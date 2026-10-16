# Troubleshooting

Start with what your tools can see, say what you found in plain words, then the fix and who does it.

## A post failed

`list_posts` with `status: "failed"`; read `errorMessage` (it's written for people).

| The message says | Means | Fix |
|---|---|---|
| "Reconnect {platform} to publish this post" | the account's access ran out or was revoked | owner: Integrations → Reconnect. Posts that failed this way in the last 48 hours publish again by themselves after reconnecting |
| "We couldn't confirm whether this post was published" | the platform didn't answer clearly | owner checks the account first; schedule again only if it isn't there |
| "This post's details are invalid" | a caption or setting broke a platform rule | owner edits it in the creative drawer and schedules again |
| "This post missed its scheduled time" | it was more than 48 hours late after an outage | schedule it again |
| "…kept failing…" | 5 tries over about an hour all failed | schedule again later; if it repeats, Support |
| "Instagram needs an aspect ratio between 4:5 and 1.91:1" | wrong shape for that target | a 4:5 or 1:1 version, or a different target |
| "reached its limit of 25 posts per day" | Instagram's own daily cap | move it to another day |
| "The Pinterest board was not found" | the board was deleted | owner picks another board |
| "TikTok did not finish reviewing this post within a day" | TikTok held it | owner checks TikTok |
| "TikTok flagged the caption as possible spam" | TikTok's filter | fewer hashtags or links, schedule again |

You can't retry a failed post yourself: `create_post` again with the same creative (a new post), or
the owner reschedules it.

## An account needs reconnecting

`list_channels` shows `isConnected: false`. You can't see why; the Integrations card can ("Needs
reconnect", "Setup incomplete", "Almost done"). Scheduled posts on it wait and fail when due until
it's fixed. Common causes: the owner changed their password or removed the app's access on the
platform, or a token expired.

## Can't schedule

- "scheduledAt must be a future date": pick a later time (mind the timezone).
- "Daily scheduling limit of N posts reached for {platform}": the plan's per-platform cap for that
  day; another day, or a bigger plan.
- "A {ratio} {format} can't be published as a {platform} {target}": wrong shape for that target
  (videos can't go to feed posts; stories and reels need 9:16).
- "Integration for {platform} is not connected": reconnect first.
- Without targets, a platform can be skipped silently (daily limit). Compare with `list_channels`.

## A product is missing

- **New in the store:** not synced yet. It arrives with the daily sync, or the owner presses Sync on
  Your Products (`sync_shop` doesn't work).
- **Inactive:** draft, archived, sold out, unlisted or gone from the store. Autopost skips it.
- **No images:** Generate hides it and Autopost skips it. Add images in the store and sync.
- **Free plan:** the owner only sees 5 products. You see more; that's why they can't find one.
- **Store disconnected:** its products were deleted with it; reconnecting imports them again.
- Prices never come across; that's expected.

## A job failed or partly failed

No reason is recorded, so don't guess one. Failed creatives cost nothing. Offer to make the missing
ones again (same items in a new `generate_creative`), maybe with other products. If the same type
keeps failing, Support.

## Generating is refused

- "Insufficient … credits": not enough of that kind; smaller plan, template types, or a top-up on
  Billing (paid plans) or an upgrade (free).
- "… is available on the Growth and Enterprise plans": UGC and Photoshoot videos.
- "products without images": pick other products.
- "AI generations are not available for guest users": the owner has to sign up.

## Autopost didn't make anything

Check with the owner (you can't see the settings): Is it switched on? Does the plan include it?
Is a chosen platform connected? Are there active products with images? Was it Saturday yet (it fills
next week)? Did that week already run (it only fills gaps, so a full week makes nothing)? If the
page says "Last generation failed", Retry.

## TikTok posts are private

Each post uses the privacy it was given. Find out which kind of post it is:
- **Posts nobody set up by hand** (Autopost, yours, drag-and-drop, Auto Schedule) use the default.
  Check `get_brand_settings` → `tiktok.post_settings.privacyLevel`. If it isn't
  `PUBLIC_TO_EVERYONE`, the owner changes "Who can view" in Settings → Creatives → TikTok; it
  applies to posts scheduled from then on.
- **Posts scheduled in the drawer** use what was picked there ("Who can view" starts blank and must
  be chosen). The owner changes it by editing the scheduled post.
- **The TikTok account itself:** TikTok only accepts what the account allows. If the account is
  private in the TikTok app, it can't post to Everyone: a post goes out with the only option left,
  or fails with "The chosen TikTok privacy setting is not available for this account". The owner
  changes that in TikTok's own settings, or picks another level for the post.
- "Branded content" can never be posted as "Only me".

## Can't connect an account

- **Instagram:** personal accounts can't connect; switch it to Business or Creator in the Instagram
  app. "Via Facebook Page" needs the Instagram account linked to the Page in Meta Business Suite.
- **Pinterest "Setup incomplete":** create a board on Pinterest, then Sync.
- **TikTok "didn't grant permission":** connect again and leave every permission switched on.
- **"This account is already connected to another brand":** disconnect it there first.
- **Store "already connected":** move it in onboarding if it's the owner's other brand; otherwise
  Support.

## Out of Energy

You won't be asked anything: the owner sees "Otto is out of Energy" and the chat closes until they
top up or the plan renews. If they ask later, explain Energy (`plans-credits-energy.md`).

## The app says something this guide doesn't

Believe what the owner sees, tell them, and save the difference with `hindsight_retain`. Don't
invent an explanation.
