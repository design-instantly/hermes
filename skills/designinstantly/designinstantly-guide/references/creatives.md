# Creatives: types, Generate, jobs, Library, captions

A **creative** is one finished piece of media (an image, a carousel or a video) with a title and
ready-made captions for every platform. A **post** is that creative scheduled to one place on one
platform. One creative can become several posts.

## Types

`start_generate_creative` gives the exact fields and cost for a type; this table is what each one
is for. "Per product" means one creative per selected product. Every product used needs an image.

| App name | Tool `contentType` / format | What it makes | Input | Credits |
|---|---|---|---|---|
| Standard Image | `basic` / image | a designed template filled with one product photo; copy written by AI | product images, one creative each | standard |
| Carousel | `basic` / carousel | a multi-slide template from one product's photos | products | standard |
| UGC Image | `ugc` / image | creator-style photo, an AI person holding or using the product | products | AI |
| UGC Video | `ugc` / video | a 15 to 20 second AI creator talking about the product, lip-synced voiceover | **exactly 1 product** and a script | AI, Growth and Enterprise only |
| Photoshoot Image | `photoshoot` / image | polished product shot in any setting, product only or with a model | products | AI |
| Photoshoot Video | `photoshoot` / video | a 10 second product film with a generated soundtrack | products | AI, Growth and Enterprise only |
| Features & Benefits | `features_benefits` / image | ad-style image calling out the product's features | products | AI |
| This or That | `this_or_that` / image | two products side by side as a poll, 4:5 | **exactly 2 products**, 1 creative | AI |
| Guess the Price | `guess_the_price` / image | teaser image with room for a price (never shows one), 4:5 | products | AI |
| Quotes | `quotes` / image | a quote set in type on an AI background in the brand colours | no products; one per run | AI |
| Recreate from Reference | `reference` / image or video | the owner's product in the style of a reference image or video | products and a reference | AI |
| Manual Post | `manual_post` | the owner's own image, carousel or video, with AI captions | the owner uploads it | free; **not possible over your tools** |

Options worth knowing:
- **UGC Image:** "Customize" picks the person (ethnicity, sex, age range, an avatar from a set
  library) and extra instructions; without it they're chosen for you.
- **UGC Video:** language (13), script style (problem → solution, lifestyle, review, introduction),
  the script itself (about 35 words fits the 15 seconds), voice, subtitles. You can write the
  script; you can't list voices, avatars or subtitle styles, so leave those out and the app picks.
- **Photoshoot:** "Product Only" or "With Model", plus extra instructions.
- **Quotes:** quote up to 110 characters (the exact words set in the image), tone (motivational,
  witty, luxury, minimal, bold), optional theme and attribution.
- **Reference:** an image reference makes an image; a video reference (up to 45 seconds) makes a
  video of the same length and shape, scene by scene.
- **Include logo** (most AI types): asks the model to place the brand logo in the scene. It's a
  request to the model, not a guaranteed overlay. Templates never carry the logo.
- Up to 20 products or images per item, up to 10 items per request.

## Aspect ratios and where they fit

- AI images default to 3:4, videos to 9:16, carousels lean to 4:5.
- **9:16** fits every platform (and is the only way onto stories and reels).
- **4:5** fits Instagram, Facebook and Pinterest feeds; TikTok shows bars.
- **1:1** fits Instagram and Facebook; Pinterest crops it.
- Videos never go to an Instagram or Facebook feed post, only to reels and stories.

## The Generate page (`/generate`)

1. **Content Type:** pick a card (AI section, Standard section, Manual Post).
2. **Select Products / Images** (or Write Quote, or Upload): search and filter by store and status;
   a footer badge shows "uses X of Y credits".
3. **Configure** (UGC Video and Reference only).
4. **Review:** the type, how many creatives, "N needed / M available", options, then
   "Generate Creatives".

The owner is taken straight to the job's page. The plan check (videos) only happens on this click.

## Jobs

- One request is one **job**. Statuses: Queued, Generating, Complete, **Partly complete** (some
  creatives failed), Failed (none made), cancelled.
- Credits are taken one creative at a time as each is made. Failed creatives cost nothing.
  Cancelling stops what hasn't started; what's made stays, and stays paid.
- The job page (`/jobs/<id>`) fills in live. There's no list of past jobs in the app; you have
  `list_jobs`.
- Rough time per creative: template images 1 to 2 minutes, AI images 2 to 5, videos 3 to 7. AI
  creatives run in parallel, so a batch takes about as long as its slowest piece.
- No reason is recorded for a failed creative or job, so you can't explain why; offer to try again.

## The Library (`/library`)

- Tabs **Generated** (not scheduled yet), **Scheduled**, **Posted** (links to the live posts).
  Search by title, filter by type.
- Card menu: Download (carousels: Download All) and Delete. "Select" lets the owner delete many at
  once, with no confirmation.
- Clicking a creative opens the **creative drawer**: preview, per-platform captions, schedule
  (see `channels-and-posting.md`) and **Edit Creative**.
- **AI edit:** "Describe your change" → "Generate edit". Each edit is a new version; the original is
  always kept and "Keep version N" switches back. It costs AI credits. UGC videos can also change
  subtitle style here (free).
- There's no "regenerate" button: make it again on Generate, or AI-edit it.
- Deleting a creative is permanent and removes its posts, scheduled and published.

## Captions

- Written by AI for all four platforms when the creative is made, from the product's title and
  description, the brand's caption instructions (Settings → Creatives), and the Pinterest board
  names. Quotes and Manual Posts also use the brand description.
- House style: Instagram hook, body, call to action, then 10 to 20 hashtags; Facebook the same with
  3 to 5 hashtags and no links; Pinterest a keyword-first title and description, no hashtags or
  emojis; TikTok a hook line and 3 to 5 hashtags. The product link becomes the Pinterest and
  Facebook link.
- Limits: Instagram 2,200 characters; Facebook 500; Pinterest title 100 and description 500;
  TikTok video caption 2,200, photo title 90 and description 4,000.
- The owner edits captions in the creative drawer, and the edit is saved **only into the scheduled
  post**. Closing the drawer without scheduling loses it. There's no "rewrite caption" button, and
  you can't save a caption: draft it in chat and they paste it in.

## Settings → Creatives (`/settings/creatives`)

- **Include logo** default for new creatives.
- **Caption instructions** per platform (Instagram caption, Facebook message, Pinterest title and
  description, TikTok caption), added to the AI's instructions. `get_brand_settings` shows them.
- **TikTok defaults** (when TikTok is on): who can view (default Everyone), comments (on), Duet and
  Stitch (off), brand disclosure, recommended music. Used for every post nobody sets up by hand:
  Autopost, your `create_post`, drag-and-drop and Auto Schedule. Not used in the drawer.

## The brand's look (Settings → Brand)

- **Logo:** used when Include logo is on (AI types).
- **Colours:** templates and Quotes use them; AI types get them as brand context.
- **Heading font:** shapes the type in Quotes and the ad-style AI types; templates keep their own.
- **Description:** brand context for AI types, Quotes and Manual Post captions; not used for
  product captions.
- You can't read the description, colours or fonts with your tools. Ask the owner, or look at their
  storefront in your browser.
