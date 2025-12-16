# Complete Directory Structure of Social Warriors Project

This document contains the complete directory structure of the workspace located at `d:\programs\socialwarriors`, including all subdirectories and files with their full paths.

## Root Directory

```
d:\programs\socialwarriors
├── .gitignore
├── BUILD_INSTRUCTIONS.md
├── CHANGELOG.md
├── FLASH.md
├── LICENSE
├── LINUX.md
├── README.md
├── RELEASES.md
├── SPRITE_FIXES.md
├── SW_mod.py
├── auctions.py
├── bundle.py
├── command.py
├── constants.py
├── diagnose_sprite_issues.py
├── engine.py
├── extract_fusion_units.py
├── get_game_config.py
├── get_player_info.py
├── requirements.txt
├── server.py
├── sessions.py
├── social-warriors_0.02a.spec
├── test_sprite_access.py
├── version.py
```

## .git Directory

```
d:\programs\socialwarriors\.git
├── COMMIT_EDITMSG
├── config
├── description
├── FETCH_HEAD
├── HEAD
├── index
├── ORIG_HEAD
├── packed-refs
├── hooks\
│   ├── applypatch-msg.sample
│   ├── commit-msg.sample
│   ├── fsmonitor-watchman.sample
│   ├── post-update.sample
│   ├── pre-applypatch.sample
│   ├── pre-commit.sample
│   ├── pre-merge-commit.sample
│   ├── pre-push.sample
│   ├── pre-rebase.sample
│   ├── pre-receive.sample
│   ├── prepare-commit-msg.sample
│   └── update.sample
├── info\
│   └── exclude
├── logs\
│   ├── HEAD
│   └── refs\
│       ├── heads\
│       │   ├── master
│       │   └── main
│       └── remotes\
│           └── origin\
│               └── HEAD
├── objects\
│   ├── info\
│   └── pack\
│       ├── pack-05f1180922d5090410c2e401204990047933739b.idx
│       └── pack-05f1180922d5090410c2e401204990047933739b.pack
└── refs\
    ├── heads\
    │   ├── master
    │   └── main
    ├── remotes\
    │   └── origin\
    │       └── HEAD
    └── tags\
```

## .qoder Directory

```
d:\programs\socialwarriors\.qoder
```

## assets Directory

```
d:\programs\socialwarriors\assets
├── characters_2\
├── externalized\
├── flash\
├── fonts\
├── fx\
├── images\
├── magic\
├── sounds\
├── sprites\
├── swf\
└── thumbs\
```

## auctions Directory

```
d:\programs\socialwarriors\auctions
└── auctions.json
```

## build Directory

```
d:\programs\socialwarriors\build
├── build.bat
├── icon.ico
├── launcher_build.bat
├── path_bundle.py
├── social-warriors_0.02a.spec
└── icons\
    ├── sw.ico
    └── sw_bg.ico
```

## config Directory

```
d:\programs\socialwarriors\config
├── auctionhouse.json
├── get_game_config.php_23july2012.txt
├── get_game_config.php_29august2012.txt
├── get_game_config.php_29august2012_nohash.json
├── get_game_config.php_29august2012_nohash.txt
├── main.json
└── patch\
    ├── atom_fusion_item.json
    ├── atom_fusion_items_data.json
    ├── atom_fusion_powerup.json
    ├── patches.txt
    ├── targets.json
    └── unit_patch.json
```

## mods Directory

```
d:\programs\socialwarriors\mods
├── README_SKIP_CHAPTERS.md
├── increased_population.json
├── mods.txt
├── no_hiring_needed.json
└── skip_chapter_timers.json
```

## stub Directory

```
d:\programs\socialwarriors\stub
└── crossdomain.xml
```

## templates Directory

```
d:\programs\socialwarriors\templates
├── SW_Mod_API.html
├── auction_house.html
├── fusion_results.html
├── fusion_units.json
├── login.html
├── play.html
├── avatars\
│   ├── acidcaos.png
│   ├── avatar_basic.png
│   ├── kiriakos.png
│   ├── nerroth.png
│   └── scarlet.png
├── css\
│   └── facebook.css
└── img\
    ├── auction.jpg
    ├── auction.png
    ├── cash.png
    ├── discord.png
    ├── dragoncity.jpg
    ├── gift.png
    ├── github.png
    ├── gold.png
    ├── icon.png
    ├── logo.png
    ├── monsterlegends.jpg
    ├── oil.png
    ├── socialwarsheader.jpg
    ├── steel.png
    ├── wood.png
    ├── worker.png
    └── world.png
```

## tools Directory

```
d:\programs\socialwarriors\tools
├── README.md
├── __init__.py
├── atom_fusion_builder.py
├── atom_fusion_excluded_units.json
├── config.py
├── make_sw_unit_patch.py
├── sw_unit_patch.csv
├── test_formulas.py
├── unit_templates.json
├── utils.py
├── validators.py
└── processors\
    ├── __init__.py
    ├── atom_fusion.py
    └── unit_patches.py
```

## venv Directory

```
d:\programs\socialwarriors\venv
└── Scripts\
    └── python.exe
```

## villages Directory

```
d:\programs\socialwarriors\villages
├── AcidCaos.json
├── General_Mike_30.json
├── Kiriakos.json
├── Nerri.json
├── Neutral.json
├── Scarlet.json
├── initial.json
└── quest\
    ├── 100000001.json
    ├── 100000002.json
    ├── 100000003.json
    ├── 100000004.json
    ├── 100000005.json
    ├── 100000006.json
    ├── 100000007.json
    ├── 100000008.json
    ├── 100000009.json
    ├── 100000010.json
    ├── 100000011.json
    ├── 100000012.json
    ├── 100000013.json
    ├── 100000014.json
    ├── 100000017.json
    ├── 100000018.json
    ├── 100000019.json
    ├── 100000020.json
    ├── 100000021.json
    ├── 100000022.json
    ├── 100000025.json
    ├── 100000026.json
    └── 100000049.json
```

## Notes

1. The `.git` directory contains all Git repository metadata.
2. The `assets` directory contains numerous subdirectories with game assets including characters, images, sounds, and sprites.
3. The `build` directory contains build scripts and configuration files.
4. The `config` directory contains game configuration files and patch data.
5. The `mods` directory contains mod configuration files.
6. The `templates` directory contains HTML templates and UI assets.
7. The `tools` directory contains development tools and utilities.
8. The `venv` directory contains the Python virtual environment (partially cleaned).
9. The `villages` directory contains village configuration files and quest data.

This structure represents a complete archive of the Social Wars Flash game preservation project.