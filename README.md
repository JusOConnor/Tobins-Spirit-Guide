# Tobin's Spirit Guide
This is originally started out as a companion app for Phasmophobia during the early versions of the game.  The is meant to help you rule out Ghost types as you collect or rule out eveidence.  As you get closer to solving the puzzle it help identify which tools to use next.  The timer is meant for lower difficulty levels where you get a short window of time before the Ghost can start hunting.

Works great with VR to add to the immersion. 

Web Version:  
https://jusoconnor.github.io/Tobins-Spirit-Guide/

*The game now includes some of this functionality so this is mostly a passion project, but still very usable*

___
Mark each piece of evidence as Ruled Out, Unknown, or Found, and the guide shows which ghosts are still possible.

## Setup

From this folder, run:

```
uv sync
```

UV creates the virtual environment and installs customtkinter. If the window fails to open with a message about `tkinter`, install a UV managed Python (which includes it) and sync again:

```
uv python install 3.13
uv sync --python-preference only-managed
```

## Running the guide

From a terminal in this folder:

```
uv run start_guide.py
```

From Jupyter, open `spirit_guide.ipynb`, choose the `.venv` kernel in this folder, and run the cells.

## Reading the colors

| Ghost name color | Meaning |
| --- | --- |
| Green | All three pieces of evidence found |
| Orange | Two found; the last piece to look for glows green |
| Yellow | One found |
| Light grey | No evidence found yet, still possible |
| Dark | Eliminated |

A ghost is eliminated when you rule out evidence it always leaves, or find evidence it never leaves.

## Files

| File | What it holds |
| --- | --- |
| `start_guide.py` | Opens the window. |
| `functions/ghost_data.json` | The ghost list. Edit this to add or change ghosts. |
| `functions/data.py` | Loads the ghost list. |
| `functions/logic.py` | The rules for matching evidence to ghosts. |
| `functions/desktop_app.py` | The customtkinter window. |
| `spirit_guide.ipynb` | Test the rules and open the window. |

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/JusOConnor) \
[If you like my work or if you found this at all helpful please feel free to contribute.](buymeacoffee.com/JusOConnor) \
buymeacoffee.com/JusOConnor