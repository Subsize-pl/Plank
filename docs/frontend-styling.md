# ADR 01: Use CSS Modules for frontend styling

## Context

KAN-9 introduces the read-only board UI with Board, Column, and Card
components. We need one styling approach for the frontend.

## Decision

Use CSS Modules for component styles. Keep each stylesheet next to its
component, for example `Column.module.css` next to `Column.tsx`.
Use a global stylesheet for shared defaults such as fonts and page margins.

## Rationale

CSS Modules use standard CSS and are supported by Vite out of the box.
Class names are scoped to each module, so components can use names like
`header` without conflicts.

## Consequences

Component styles live in `.module.css` files and are imported into the
corresponding React components. The frontend uses CSS Modules consistently.
