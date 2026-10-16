# Social accounts, scheduling and publishing

## Words

- **Channel:** a connected account: an Instagram account, a Facebook Page, a Pinterest account,
  a TikTok account.
- **Target:** where on that account a post goes. Instagram: Feed Post, Reel, Story. Facebook: Page
  Post, Page Story, Page Reel. Pinterest: one target per board. TikTok: one.
- **Post:** one creative to one target at one time. A 9:16 video sent everywhere can become six
  posts (Instagram Reel and Story, Facebook Reel and Story, a Pinterest board, TikTok).

## Connecting accounts (Integrations, Socials tab)

| Platform | Needs | Notes |
|---|---|---|
| Instagram | a **Business or Creator** account; personal accounts can't connect | "Instagram Direct (Recommended)", or "Via Facebook Page" (the Page must have the Instagram account linked in Meta Business Suite) |
| Facebook | a Facebook Page | picks one Page; choosing another later replaces it |
| Pinterest | at least one board | no boards → "Setup incomplete": create a board on Pinterest, then Sync |
| TikTok | keep every permission switched on when approving | only for owners with TikTok switched on |

- One account per platform per brand. Connecting a different one replaces it. An account can belong
  to one brand only. Reconnect must use the same account.
- Anyone in the brand can connect; only owners and admins can disconnect.
- **Card states:** Connected; **Needs reconnect** (expired or revoked access, missing permission);
  **Setup incomplete** (no boards); **Almost done** (pick the Page or account); Not Connected.
  Amber cards say how many scheduled posts are waiting on them.
- Access is refreshed automatically every day, and accounts are checked daily (boards and Pages
  re-synced). A broken account may email the owner.
- **Disconnect** pauses that account's scheduled posts and keeps published history. Reconnecting
  the same account puts the paused posts back at their times.
- **After reconnecting,** posts that failed for access reasons in the last 48 hours are published
  again a few minutes later. **After connecting a new platform,** future scheduled creatives get a
  post on it too, at the same time.
- `list_channels` shows `isConnected: false` for an account that needs reconnecting, but not why.
  The Integrations card says why.

## What each platform takes

- Videos never go to an Instagram or Facebook feed post: reels and stories only. Reels need a video.
  Stories take one image or video, shown at 9:16.
- Instagram feed images outside 4:5 to 1.91:1 are padded, not refused. Carousels up to 10 items.
  Instagram itself allows 25 posts a day per account.
- Pinterest: up to 5 images per pin, all the same shape; a board must be chosen. The owner can create
  a board from the creative drawer ("Create new board").
- TikTok: photo posts up to 35 photos; one video per post. A privacy level is required.
- Caption limits: see `creatives.md` → Captions.

## Scheduling

**The creative drawer** (click any creative in Library, Schedule, Calendar or Autopost):
- A tab per platform with a "Publish to {platform}" switch, target chips (Post, Reel, Story, with
  "(Recommended)"), the account it posts to, and editable post details: Instagram caption; Facebook
  message and Product Link; Pinterest board, Pin Title, Description, Outbound Link; TikTok caption,
  "Who can view", comments, Duet, Stitch, disclosure, music.
- **TikTok in the drawer starts blank:** the owner must choose who can view, and every toggle starts
  off (TikTok's rule). The Settings → Creatives defaults don't apply here.
- Date and time in the owner's browser timezone; defaults to tomorrow at a random time.
- "Schedule Post" / "Schedule to N Platforms" / "Save Changes".

**Schedule page** (`/schedule`): unscheduled creatives on the left, a month on the right.
- **Drag a creative onto a day:** scheduled at once at a random time (today: from an hour from now;
  other days: 06:00 to 23:59), to every connected platform's recommended targets.
- **Click a day:** pick several creatives, "Schedule N posts".
- **Auto Schedule (N):** spreads every unscheduled creative over the coming days, posts-per-day at a
  time (the same number as Autopost's posts per day).

**Calendar** (`/calendar`): month and week.
- A day shows its posts with time, type and status ("Scheduled" or "Published", or
  "{Platform} failed: reason"), and "View on {platform}" links for published ones.
- Click a scheduled post to edit time, captions, platforms. **Drag to another day** to reschedule
  (keeps the time of day). **Cancel** deletes it.
- Only scheduled posts can be edited or cancelled.

**Daily limits per plan**, per platform, counted as distinct creatives per day:

| Plan | Instagram | Facebook | Pinterest | TikTok |
|---|---|---|---|---|
| Basic, Extension Only | 3 | 3 | 10 | 3 |
| Starter | 5 | 5 | 20 | 5 |
| Growth | 15 | 15 | 40 | 10 |
| Enterprise | 75 | 75 | 100 | 15 |

Over the limit the owner sees "Daily Limit Reached". These numbers change; quote them as current.

## Your `create_post`

- Needs a future time; give the owner's timezone (`timeZone`), or it's read as UTC.
- Without `channelTargetIds` it posts to every connected platform that fits the creative, to the
  recommended targets, with one Pinterest board. Platforms that fail (daily limit, wrong shape) are
  skipped with no error, so check the result against `list_channels`.
- With `channelTargetIds` (from `targets[].id`) it reports each target that failed and why.
- Captions come from the creative (written when it was made); TikTok settings from Settings →
  Creatives. You can't change either, or choose the Pinterest board.
- Scheduling the same creative to the same target twice returns the existing post.

## Publishing

- At the time, DesignInstantly publishes on its own. Nothing needs to be open.
- **Statuses:** scheduled → published; **processing** (TikTok is still reviewing it; shown as
  Scheduled); **failed** (with a reason); **cancelled** (its account was disconnected).
- **Retries:** passing problems (a platform hiccup, a rate limit) are retried up to 5 times over
  about an hour. Access problems fail at once and mark the account "Needs reconnect". If
  DesignInstantly can't tell whether a post went out, it fails it rather than risk a duplicate:
  "We couldn't confirm whether this post was published."
- **TikTok** can take a while to review a post; after a day without an answer the post fails.
- A post more than an hour late (an outage) is published if it's less than 48 hours late, otherwise
  failed with "This post missed its scheduled time."
- No email or alert for failed posts yet. They show on the Calendar with their reason and in
  `list_posts` (`status: "failed"`, `errorMessage`).
- **TikTok privacy** is what was chosen: in the drawer for that post, otherwise the Settings →
  Creatives default. At publish time TikTok only accepts what the account allows: if the choice
  isn't allowed, the post goes out with the only option left, or fails asking for another choice.

## Results

DesignInstantly records whether a post published and links to it. It has no likes, comments, saves,
clicks, reach or sales for any post. The Dashboard chart only counts posts. If the owner asks how
posts did, say so plainly, and offer what you can do: check the live posts in your browser where the
platform allows it, or ask them what they've seen.
