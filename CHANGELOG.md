# Changelog

## 0.1.2

- Show a non-interactive two-second slaughter progress bar.
- Request the vanilla chicken death sound before granting the chicken and feathers.
- Movement and held-item changes do not cancel accepted slaughter.
- Preserve occupied toolbelt slots; use inventory/ground fallback when needed.
- Add the game-shipped Unity IMGUI reference to the existing Windows build.
- New presentation and delayed rewards require in-game verification.

## 0.1.1

- Add adopted custom transparent 160×160 chicken icon to UIAtlases/ItemIconAtlas and the web ItemIcons folder.
- Japanese name: 絞めたニワトリ; English name: Butchered Chicken.
- Slaughter yields 23 feathers, with inventory overflow dropped on the ground.
- Include Windows build scripts and a script to create the compiled install ZIP.
- User confirmed icon rendering and continued coop production after testing.

## 0.1.0

- Secondary action slaughters one carried wild chicken into one cooking ingredient.
- Add alternate ingredient recipes for three vanilla chicken dishes.
- Adjust only wild chicken MoveSpeedPanic from 1.5 to 1.2.
- Preserve live carrying, coop domestication, ordinary hunting, and existing recipes.
