# Patterns

Every surface below passes `render_ui`'s strict validation against the catalog as written. Copy the
closest one, change ids and copy, keep the structure. Pass `components` (and `data` when shown) to `render_ui`.

## Plan to approve (`plan-approval`)

A header with status in the corner, a bordered list of what's planned, and a footer with one primary action. Use for content plans, schedules, anything the user signs off.

```json
{
  "components": [
    {"id": "root", "component": "Card", "children": ["header", "content", "footer"]},
    {"id": "header", "component": "CardHeader", "children": ["title", "description", "badge-wrap"]},
    {"id": "title", "component": "CardTitle", "text": "Week 1 plan"},
    {"id": "description", "component": "CardDescription", "text": "5 posts across Instagram and Pinterest, Mon to Fri."},
    {"id": "badge-wrap", "component": "CardAction", "children": ["status"]},
    {"id": "status", "component": "Badge", "variant": "secondary", "text": "Draft"},
    {"id": "content", "component": "CardContent", "children": ["posts"]},
    {"id": "posts", "component": "ItemGroup", "children": ["post-1", "post-2"]},
    {"id": "post-1", "component": "Item", "variant": "outline", "size": "sm", "children": ["post-1-content", "post-1-actions"]},
    {"id": "post-1-content", "component": "ItemContent", "children": ["post-1-title", "post-1-desc"]},
    {"id": "post-1-title", "component": "ItemTitle", "text": "Mon · Instagram carousel"},
    {"id": "post-1-desc", "component": "ItemDescription", "text": "New spring candles, 4 slides"},
    {"id": "post-1-actions", "component": "ItemActions", "children": ["post-1-badge"]},
    {"id": "post-1-badge", "component": "Badge", "variant": "outline", "text": "10:00"},
    {"id": "post-2", "component": "Item", "variant": "outline", "size": "sm", "children": ["post-2-content", "post-2-actions"]},
    {"id": "post-2-content", "component": "ItemContent", "children": ["post-2-title", "post-2-desc"]},
    {"id": "post-2-title", "component": "ItemTitle", "text": "Wed · Pinterest pin"},
    {"id": "post-2-desc", "component": "ItemDescription", "text": "Gift guide, lavender set"},
    {"id": "post-2-actions", "component": "ItemActions", "children": ["post-2-badge"]},
    {"id": "post-2-badge", "component": "Badge", "variant": "outline", "text": "18:30"},
    {"id": "footer", "component": "CardFooter", "children": ["actions"]},
    {"id": "actions", "component": "Row", "justify": "end", "weight": 1, "children": ["change", "approve"]},
    {"id": "change", "component": "Button", "variant": "outline", "text": "Change something", "action": {"event": {"name": "revise_plan"}}},
    {"id": "approve", "component": "Button", "text": "Approve plan", "action": {"event": {"name": "approve_plan", "context": {"plan": "week-1"}}}}
  ]
}
```

## Form (`settings-form`)

`FieldGroup` gives the fields their 20px rhythm; each `Field` stacks label, control and help. Inputs bind to `data`; the submit button's context reads the same paths back.

```json
{
  "components": [
    {"id": "root", "component": "Card", "children": ["header", "content", "footer"]},
    {"id": "header", "component": "CardHeader", "children": ["title", "description"]},
    {"id": "title", "component": "CardTitle", "text": "Posting preferences"},
    {"id": "description", "component": "CardDescription", "text": "I'll use these for every post until you change them."},
    {"id": "content", "component": "CardContent", "children": ["fields"]},
    {"id": "fields", "component": "FieldGroup", "children": ["tone-field", "cadence-field", "hashtags-field"]},
    {"id": "tone-field", "component": "Field", "children": ["tone-label", "tone-input", "tone-help"]},
    {"id": "tone-label", "component": "FieldLabel", "text": "Brand tone"},
    {"id": "tone-input", "component": "Input", "placeholder": "Warm, a little playful", "value": {"path": "/tone"}},
    {"id": "tone-help", "component": "FieldDescription", "text": "Two or three words is plenty."},
    {"id": "cadence-field", "component": "Field", "children": ["cadence-label", "cadence"]},
    {"id": "cadence-label", "component": "FieldLabel", "text": "Posts per week"},
    {"id": "cadence", "component": "ToggleGroup", "variant": "outline", "spacing": 2, "value": {"path": "/cadence"}, "children": ["c3", "c5", "c7"]},
    {"id": "c3", "component": "ToggleGroupItem", "value": "3", "text": "3"},
    {"id": "c5", "component": "ToggleGroupItem", "value": "5", "text": "5"},
    {"id": "c7", "component": "ToggleGroupItem", "value": "7", "text": "7"},
    {"id": "hashtags-field", "component": "Field", "orientation": "horizontal", "children": ["hashtags", "hashtags-label"]},
    {"id": "hashtags", "component": "Switch", "checked": {"path": "/hashtags"}},
    {"id": "hashtags-label", "component": "FieldLabel", "text": "Add hashtags"},
    {"id": "footer", "component": "CardFooter", "children": ["save"]},
    {"id": "save", "component": "Button", "text": "Save preferences", "action": {"event": {"name": "save_preferences", "context": {"tone": {"path": "/tone"}, "cadence": {"path": "/cadence"}, "hashtags": {"path": "/hashtags"}}}}}
  ],
  "data": {"tone": "", "cadence": "5", "hashtags": true}
}
```

## Pick one of a few things (`choice-picker`)

Each option is an `Item` row with media, a title, a one-line reason and its own button. Use `Card size: sm` when the surface is a quick question.

```json
{
  "components": [
    {"id": "root", "component": "Card", "size": "sm", "children": ["header", "content"]},
    {"id": "header", "component": "CardHeader", "children": ["title"]},
    {"id": "title", "component": "CardTitle", "text": "Which product should lead this week?"},
    {"id": "content", "component": "CardContent", "children": ["options"]},
    {"id": "options", "component": "ItemGroup", "children": ["opt-1", "opt-2"]},
    {"id": "opt-1", "component": "Item", "variant": "outline", "children": ["opt-1-media", "opt-1-content", "opt-1-actions"]},
    {"id": "opt-1-media", "component": "ItemMedia", "variant": "image", "children": ["opt-1-img"]},
    {"id": "opt-1-img", "component": "Image", "url": "https://example.com/candle.jpg", "description": "Lavender candle", "variant": "avatar"},
    {"id": "opt-1-content", "component": "ItemContent", "children": ["opt-1-title", "opt-1-desc"]},
    {"id": "opt-1-title", "component": "ItemTitle", "text": "Lavender candle"},
    {"id": "opt-1-desc", "component": "ItemDescription", "text": "Best seller, 42 sales last month"},
    {"id": "opt-1-actions", "component": "ItemActions", "children": ["opt-1-pick"]},
    {"id": "opt-1-pick", "component": "Button", "size": "sm", "variant": "outline", "text": "Pick", "action": {"event": {"name": "pick_product", "context": {"product": "lavender-candle"}}}},
    {"id": "opt-2", "component": "Item", "variant": "outline", "children": ["opt-2-content", "opt-2-actions"]},
    {"id": "opt-2-content", "component": "ItemContent", "children": ["opt-2-title", "opt-2-desc"]},
    {"id": "opt-2-title", "component": "ItemTitle", "text": "Cedar diffuser"},
    {"id": "opt-2-desc", "component": "ItemDescription", "text": "New, no posts yet"},
    {"id": "opt-2-actions", "component": "ItemActions", "children": ["opt-2-pick"]},
    {"id": "opt-2-pick", "component": "Button", "size": "sm", "variant": "outline", "text": "Pick", "action": {"event": {"name": "pick_product", "context": {"product": "cedar-diffuser"}}}}
  ]
}
```

## Numbers at a glance (`stats-tabs`)

`Tabs` inside `CardContent`; each `TabsContent` holds one `Column` (it has no gap of its own). `Row justify: spaceBetween` puts the figure left and the change badge right.

```json
{
  "components": [
    {"id": "root", "component": "Card", "children": ["header", "content"]},
    {"id": "header", "component": "CardHeader", "children": ["title", "description"]},
    {"id": "title", "component": "CardTitle", "text": "Last 7 days"},
    {"id": "description", "component": "CardDescription", "text": "Compared with the week before."},
    {"id": "content", "component": "CardContent", "children": ["tabs"]},
    {"id": "tabs", "component": "Tabs", "defaultValue": "instagram", "children": ["list", "ig", "pin"]},
    {"id": "list", "component": "TabsList", "children": ["ig-trigger", "pin-trigger"]},
    {"id": "ig-trigger", "component": "TabsTrigger", "value": "instagram", "text": "Instagram"},
    {"id": "pin-trigger", "component": "TabsTrigger", "value": "pinterest", "text": "Pinterest"},
    {"id": "ig", "component": "TabsContent", "value": "instagram", "children": ["ig-body"]},
    {"id": "ig-body", "component": "Column", "children": ["ig-row", "ig-note"]},
    {"id": "ig-row", "component": "Row", "justify": "spaceBetween", "align": "center", "children": ["ig-reach", "ig-delta"]},
    {"id": "ig-reach", "component": "Text", "variant": "h2", "text": "12,480 reach"},
    {"id": "ig-delta", "component": "Badge", "variant": "secondary", "text": "+18%"},
    {"id": "ig-note", "component": "Text", "variant": "caption", "text": "Carousels did 2x better than single images."},
    {"id": "pin", "component": "TabsContent", "value": "pinterest", "children": ["pin-body"]},
    {"id": "pin-body", "component": "Column", "children": ["pin-row"]},
    {"id": "pin-row", "component": "Row", "justify": "spaceBetween", "align": "center", "children": ["pin-saves", "pin-delta"]},
    {"id": "pin-saves", "component": "Text", "variant": "h2", "text": "310 saves"},
    {"id": "pin-delta", "component": "Badge", "variant": "outline", "text": "-4%"}
  ]
}
```

## Nothing here yet (`empty-state`)

`Empty` brings its own padding, border and centering. One sentence on what's missing, one button to fix it.

```json
{
  "components": [
    {"id": "root", "component": "Empty", "children": ["header", "content"]},
    {"id": "header", "component": "EmptyHeader", "children": ["title", "description"]},
    {"id": "title", "component": "EmptyTitle", "text": "No products imported yet"},
    {"id": "description", "component": "EmptyDescription", "text": "Connect your Etsy or Shopify store and I'll start planning posts."},
    {"id": "content", "component": "EmptyContent", "children": ["connect"]},
    {"id": "connect", "component": "Button", "text": "Connect a store", "action": {"event": {"name": "connect_store"}}}
  ]
}
```

## Confirm something risky (`confirm-alert`)

A `Column` root so the `Alert` and the button row get 12px between them. The safe choice is `outline`; the risky one is `destructive`.

```json
{
  "components": [
    {"id": "root", "component": "Column", "children": ["alert", "actions"]},
    {"id": "alert", "component": "Alert", "variant": "destructive", "children": ["alert-title", "alert-desc"]},
    {"id": "alert-title", "component": "AlertTitle", "text": "This deletes 3 scheduled posts"},
    {"id": "alert-desc", "component": "AlertDescription", "text": "They won't publish, and this can't be undone."},
    {"id": "actions", "component": "Row", "justify": "end", "children": ["keep", "delete"]},
    {"id": "keep", "component": "Button", "variant": "outline", "text": "Keep them", "action": {"event": {"name": "cancel_delete"}}},
    {"id": "delete", "component": "Button", "variant": "destructive", "text": "Delete posts", "action": {"event": {"name": "confirm_delete"}}}
  ]
}
```
