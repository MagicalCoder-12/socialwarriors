# Changelog

All notable changes to the Social Wars preservation project will be documented in this file.

## [0.03a] - 2025-12-14

### Added
- New `force_collect_mission` API endpoint to bypass all timer checks and force mission collection
- Input field for mission ID in the Chapter Timer section of the Resources Control Panel
- Visual resource icons (gold, wood, steel, oil, cash) replacing generic colored circles in the UI
- Detailed response information in API endpoints for better debugging

### Changed
- Enhanced `skip_chapter_timer` API endpoint with improved session synchronization
- Improved `collect_mission` command to detect forced collections and handle them properly
- Updated version information to alpha 0.03a
- Updated README.md with recent enhancements documentation
- Updated RELEASES.md with new version entry

### Fixed
- Issue with skip timer functionality not properly advancing to the next task/chapter
- Session data synchronization between save files and memory
- Image paths in the Resources Control Panel HTML template

### Removed
- Python cache files (`__pycache__` directories and `.pyc` files)
- Empty `save_backups` directory
- Other temporary and unnecessary files

## [0.02a] - 2024-01-27

### Added
- Initial release with core game preservation functionality
- Flask-based server for serving game assets locally
- Support for mods through JSON configuration files
- Resources Control Panel for managing game resources
- Support for villages, quests, auctions, and player profiles

## [0.01a] - 2022-12-23

### Added
- Initial alpha release
- Basic game server implementation
- Flash game asset serving capabilities
- Core game data structures