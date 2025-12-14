# Skip Chapter Timers Feature

This feature allows you to skip chapter timers in Social Wars, enabling instant progression through chapters without waiting.

## How it works

The feature provides two ways to skip chapter timers:

1. **Automatic mod-based skipping** - A mod that automatically skips chapter timers when progressing through chapters
2. **Manual button-based skipping** - A button in the Resources Control Panel that lets you manually skip the chapter timer on demand

## Installation

1. The mod is already included in the `mods` folder as `skip_chapter_timers.json`
2. The mod is already enabled in `mods.txt`
3. The API endpoint and button are already added to the control panel

## Usage

### Method 1: Automatic Skipping (Mod)
1. Start a new game or load an existing save
2. The "Skip Chapter Timer Mod" item will be automatically added to your inventory
3. When you complete a chapter, the timer will be skipped automatically
4. You can progress to the next chapter instantly

### Method 2: Manual Skipping (Button)
1. Navigate to the Resources Control Panel (http://127.0.0.1:5055/control)
2. Scroll down to find the "Chapter Timer" card
3. Click the "Skip Timer" button when you want to skip the chapter timer
4. The game will treat the timer as expired and allow you to progress

## Technical Details

### Automatic Method
The mod works by:
- Adding a special item with ID "skip_chapter_timer_mod" to the game
- Modifying the `collect_mission` command to check for this item
- When found, setting the chapter timestamp to 0 instead of the current time
- This effectively removes the timer requirement for chapter progression

### Manual Method
The manual method works by:
- Adding an API endpoint `/api/skip_chapter_timer` that sets the chapter timestamp to 0
- Adding a button in the Resources Control Panel that calls this endpoint
- Allowing users to choose when to skip the timer rather than skipping automatically

## Troubleshooting

If the feature doesn't seem to work:
1. Make sure the mod is listed in `mods.txt`
2. Restart the server to ensure mods are loaded
3. Start a new game to ensure the mod item is added to your inventory
4. For the manual method, ensure you're clicking the button after the timer has started