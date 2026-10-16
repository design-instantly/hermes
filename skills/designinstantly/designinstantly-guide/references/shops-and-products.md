# Stores and products

## Connecting a store

Stores connect in onboarding, on Integrations (Shops tab), or from the Your Products empty page.
One store of each kind per brand: one Shopify, one Etsy, one WooCommerce.

| Store | How it connects | What it brings besides products |
|---|---|---|
| Shopify | sign in to Shopify (read-only access) | logo and brand colours |
| Etsy | sign in to Etsy | the shop icon as logo |
| WooCommerce | enter the Store URL, approve on the store's own page | site icon as logo, site tagline as description |

- A store can be connected to one brand only, across every account. Moving it between the owner's
  own brands works from onboarding ("Link store here"); from Integrations the owner just sees
  "Connection failed", and WooCommerce says the store is linked to another organization.
- Installing from the Shopify App Store signs the owner up (or in) automatically and starts
  onboarding with the shop's name.
- Missing a store type? Integrations → "Request Integration".

## What gets imported

- **Imported:** title, description, product link, the store's status, and images in order
  (Shopify: up to 10 per product).
- **Not imported:** prices, variants, stock, tags, collections. You never know a product's price.
- Etsy imports active listings only; Shopify and WooCommerce import every status.

## Keeping in sync

- On connect, a full import.
- **Every day** around 04:00 UTC, every store syncs on its own.
- **The Sync button** on Your Products syncs the current tab's store (on "All" it syncs one store).
  There's no "last synced" time shown.
- **Shopify** also pushes edits to known products straight away; a brand-new Shopify product only
  appears after the next sync. Deleting a product in Shopify deletes it here (its creatives stay).
- Products that vanish from a store are marked **inactive**, not deleted. Images removed in the
  store are removed here.
- Your `sync_shop` tool doesn't work at the moment. Ask the owner to press Sync, or wait for the
  daily sync.

## Product status

- **Active:** live in the store (Shopify and Etsy "active", WooCommerce "publish"), and every
  hand-added product.
- **Inactive:** drafts, archived, private, pending, sold out, expired, unlisted, or gone from the
  store.
- Inactive products show an "Inactive" badge. Generate can still use them; Autopost never does.
- Products without images can't be made into creatives: Generate hides them, Autopost skips them.

## The Your Products page (`/products`)

- Tabs: All, one per store, and Manual. Search by title and description.
- **Free plan:** the owner sees only their 5 newest products with 2 images each, here, in Generate
  and in the extension, with an "Unlock your full product catalog" banner. Everything is still
  imported, and your tools see all of it.
- Clicking a product opens its page: its creatives (Generated, Scheduled, Posted) and its details.

## Hand-added products

- "Add Product": Title (required), Description, Product link, up to 20 photos (PNG, JPG or WEBP,
  10 MB each).
- Only hand-added products can be edited or deleted in DesignInstantly. Store products are changed
  in the store, then synced.
- Deleting a product keeps the creatives made from it.

## Disconnecting a store

Integrations → the store → Disconnect (owners and admins only). This **deletes all of that
store's products and their images** here; creatives made from them stay. Reconnecting imports the
products again as new records. The dialog only says the store "will stop syncing", so warn the owner
before they do it. Uninstalling the app from Shopify keeps the products but stops syncing
("Access removed" with Reconnect).

## Uploads (`/uploads`)

- The brand's own images (PNG, JPG, WEBP, up to 10 MB): "Upload", drag and drop, delete.
- Also used for: reference images and videos for "Recreate from Reference" (uploaded on Generate),
  photos of hand-added products, and files for Manual Posts.
- Files uploaded on this page don't appear in Generate's pickers, but your `list_media` lists them
  and you can use one as a reference (`reference.mediaId`).
