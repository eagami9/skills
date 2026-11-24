---
name: ailist
description: Read and update an AIList household shopping list through its REST API. Use when the user asks to add, check, uncheck, edit, move or remove items on their AIList list, or asks what is still unchecked before a shopping trip.
---

# AIList

AIList (https://ai-list.web.app) is a shared household shopping-list app. An agent works with one household's lists through its REST API v1. The API key is created in the household settings in the app (owner only) and is shown once at creation; the user gives it to the agent. Every request sends it in the `X-API-Key` header.

Base URL: https://ai-list.web.app/api/v1
Auth: `X-API-Key` header with the household API key.
Errors: no key or a bad key returns 401; a bad request body returns 400; a list, item or category not found in this household returns 404.
Full OpenAPI spec: https://ai-list.web.app/openapi.json
Guides: https://ai-list.web.app/guides

## Workflow

- Before every shopping trip, GET /lists and then GET /lists/{id} to see what is still unchecked.
- Add items with POST /lists/{id}/items; the app auto-categorizes each item (household product dictionary first, then a general dictionary, then "אחר").
- Check items with POST /lists/{id}/items/{itemId}/check, uncheck with POST /lists/{id}/items/{itemId}/uncheck.
- Edit with PATCH /lists/{id}/items/{itemId}; move an item to another category with POST /lists/{id}/items/{itemId}/move; delete with DELETE /lists/{id}/items/{itemId}.

## Endpoints

- GET /lists — the household's lists with item counts (id, title, emoji, type, totalCount, uncheckedCount). List types: shopping, todo, packing, generic.
- GET /lists/{id} — the full list: categories and items.
- GET /lists/{id}/categories — the list's categories.
- GET /lists/{id}/items/{itemId} — one item.
- POST /lists/{id}/items — body: {text, quantity?, unit?, barcode?}. Returns the item with categoryId and categoryName.
- PATCH /lists/{id}/items/{itemId} — any of: checked, text, quantity, unit, categoryId, barcode (null clears quantity, unit or barcode).
- DELETE /lists/{id}/items/{itemId} — returns {"ok": true}.
- POST /lists/{id}/items/{itemId}/move — body: {categoryId}. Moving also teaches the household dictionary, so the same product lands in the new category next time.
- POST /lists/{id}/items/{itemId}/check — shortcut for PATCH {"checked": true}.
- POST /lists/{id}/items/{itemId}/uncheck — shortcut for PATCH {"checked": false}.

## Item fields

- text: product name (required on add). quantity: a number. unit: a string such as "1l". Pack sizes and weights go in unit (for example "250g"), not in quantity.
- barcode: the exact product's barcode (מק"ט), a preference for a specific product, not just a product name. Never invent a barcode; only set one when the user gave it. When comparing the basket across stores, an item with a barcode must be compared by the exact barcode, not by a generic name, so the price found is for that exact product.

## Notes

- The app itself has no price database; the agent compares prices fresh each time (see il-supermarket-compare for Israeli supermarket baskets).
