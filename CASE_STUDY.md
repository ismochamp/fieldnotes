# Fieldnotes — A Searchable Engineering Knowledge Library

**Category:** Web Development  
**Project type:** New independent publishing asset for Ismail Habib, created in September 2026  
**Status:** Implemented and verified locally in real WordPress; not publicly deployed

## The problem

Useful technical notes become hard to find when they sit in an unstructured list. A compact resource library should help a reader find a specific answer, understand it and save it for later.

## The implementation

Built an original responsive WordPress theme and content plugin. Eight original resources cover AI automation, API integration, legacy software and WordPress. A custom content type makes the resources editable in WordPress; metadata describes topic, format and reading time. Search covers full article text, topic filters narrow the library, and each resource has a permalink, a practical checklist and an illustrative workflow. Browser bookmarks provide a saved reading list without accounts or tracking services.

The interface uses a cool editorial palette, restrained typography and color-coded CSS illustrations. A separate Python runtime serves the same structured content for easy local use. Source, installable packages and local WordPress setup are included.

## Evidence and results

The actual WordPress implementation runs on WordPress 7.1.2 with eight imported, editable resources. Seven WordPress integration checks verified theme rendering, content count, full-text search, topic filtering, empty states, article permalinks, the custom content API and the saved-list view. Five standalone tests verified search, combined filtering, complete article pages, escaped search input and missing routes.

## Boundaries

The project does not claim audience growth, customer usage, SEO rankings or paid-client attribution. Reading times are estimates. Browser bookmarks are local to one browser and origin; they do not synchronize across devices. No public launch is included.

## Suggested screenshots

1. Library homepage with all topic filters and original article cards.
2. A search result proving that the term is found inside article content.
3. Full article with workflow and checklist.
4. Saved-resource view after using the real bookmark button.
5. Narrow-screen library layout.
