# The owner's journey: account, onboarding, brands, navigation

## Signing up

- At accounts.designinstantly.com → "Create an account": Name, Email, Password (8+ characters),
  or "Sign Up With Google". Email signups get a verification link first; Google needs none.
- New accounts get a small welcome grant: a few standard and AI credits and some Energy (signups from
  the Chrome extension get AI credits only). The grant is a taste, not a plan.
- Signed-out visitors to any app page are sent to the login page and brought back afterwards.
- Opening the app root takes the owner to their unfinished onboarding, or to **Autopost** once the
  brand is ready (not the Dashboard).

## Onboarding (`/onboard`, 3 steps)

1. **"Give your Brand name":** Brand name (required) and an optional Tagline, which becomes the
   brand description. Over the plan's brand limit this step shows "Maximum workspaces reached".
2. **"Connect your store":** Shopify, WooCommerce or Etsy. Connecting imports the products and,
   from the store, the logo (all three), the colours (Shopify) and the description (WooCommerce).
   "I'll set up manually" skips the step, even though the copy calls a store required.
   A store already connected to another of the owner's brands can be moved here ("Link store here");
   a store that belongs to someone else's account can't.
3. **Brand DNA** ("Review your brand DNA"): logo, heading and body fonts (Google Fonts, default
   Inter), and a 5-colour palette (primary, secondary, three accents).

**Finish** marks the brand ready. With you switched on for the brand, they land on the welcome page
(`/coworker`): five short story screens while your computer is being set up, then a chat where you
plan their first week and they approve it. If your setup fails, they're sent to Generate instead.
Without you, the app makes a free first batch of creatives and opens its job page.

Unfinished onboarding resumes at the right step the next time they open the app.

## The Dashboard (`/dashboard`)

- Brand-new brands see "Get your first post out": connect a social account, generate creatives,
  schedule the first post (or set up Autopost).
- After that, a bar chart of scheduled and published posts per day, week or month, by platform.
  It counts posts; it measures nothing about how they did.
- A banner appears when a social account needs reconnecting ("Fix in Integrations"), and for new
  accounts an offer of a free 1:1 call.

## Brands

- A brand (also called a workspace) holds everything: stores, products, creatives, channels,
  posts, settings, and you. You belong to exactly one brand.
- **Plans belong to people, not brands.** A brand's plan, credits and Energy are its owner's, even
  when someone else is the one clicking. Owning more brands needs a bigger plan (members of other
  people's brands are not counted).
- **Switching:** the brand dropdown in the header lists the owner's brands; "Create a brand" starts
  onboarding again. Each brand has its own co-worker.
- **Members:** brands have owners, admins and members, but the app has no screen to invite people
  or change roles yet. Only owners can delete a brand; only owners and admins can disconnect
  accounts.
- **Deleting a brand:** Settings → Brand → Danger Zone → "Delete Brand", owner only. It stops
  scheduled posts and removes the brand's stores, products, channels, creatives and posts, and you.
  It can't be undone.

## Getting around

- **Sidebar:** Dashboard, Your Products, Autopost (a crown badge when the plan lacks it);
  Generate, Schedule, Library, Calendar; Integrations, Uploads, Settings (Brand, Creatives,
  Autopost). Footer: Upgrade (free plans), What's New, Support, Feedback, Chrome Extension.
- **Header:** sidebar toggle, your chat, the running-jobs spinner (it opens "Active Generations",
  each with Cancel), the brand switcher, the profile menu.
- **Profile menu:** balances (Energy, Generations, AI Generations), Billing, Developers,
  My account, theme, Sign out.

## Account

- **My account** opens the accounts site: profile (name, email, phone), password, signed-in
  sessions, support email (contact@designinstantly.com).
- The owner's timezone is taken from their browser the first time they sign in, and again whenever
  they save schedule or Autopost settings. There is no timezone field to edit.
- Owners can't delete their own account; that goes through Support.

## Emails and notifications

The app emails the owner when:
- their first batch of creatives (onboarding) is ready;
- a weekly Autopost run has finished (link to Autopost);
- a social account needs reconnecting (when that email is switched on);
- plus sign-up verification and password reset.

In the app, a "Your creatives are ready" window appears when a job they started finishes while
they're around. There is no notification for failed posts yet: failures show on the Calendar.

## Features that only some owners see

- You (the co-worker), your chat and Energy are switched on per account by the DesignInstantly team.
- TikTok is switched on per account too; owners without it don't see the TikTok card or settings.
- There's no self-serve way to switch either on: point the owner to Support.

## The Chrome extension

"Design Instantly: Recreate Any Product Post with your Own Product". On a site the owner enables,
hovering an image or video shows "✦ Recreate": it makes a new creative in the same style with one
of their products (it costs AI credits and lands in their Library). The side panel also shows the
Library and a read-only schedule. Scheduling happens in the app, not the extension. There's an
"Extension Only" plan for people who only want this.

## Support and developers

- **Support** (`/support`): live chat with the DesignInstantly team, per brand. Use it for billing
  trouble, bugs, account deletion and anything this guide says only the team can do.
- **Developers** (`/developers/mcp`): how to connect DesignInstantly to Claude, ChatGPT, Cursor
  or VS Code over MCP. Those assistants can then work on the brand too, spending the owner's credits
  but not Energy.
