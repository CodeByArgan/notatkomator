# UI dla Notatkomatora

## Odpalenie

Standardowo odpalamy poprzez `npm run dev`.

## Prettier

Żeby VSCode automatycznie poprawiał tekst, wymagana jest oficjalna wtyczka do Prettiera. Jako że mamy monorepo, trzeba pamiętać o zmianie konfiguracji ścieżek do naszego folderu `ui`, gdzie znajduje się plik `.prettierrc` oraz `node_modules` z zainstalowanym Prettierem.

Oczywiście, jeśli ktoś ma zainstalowanego Prettiera globalnie, może dodać globalną ścieżkę.
