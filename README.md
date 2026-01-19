## background
I made a Python script a while back, to automate study-group scheduling.  It creates markdown files, from which I copy-paste into the Forum post & events page.  It also makes that handy code block with all courses, and handles time-zone conversions.

It's very ugly (made even more ugly by AI), do not judge me pls 🙏

## usage
  - Edit the configs in `main.py`, including modifying your schedule.
  - Customize messages in `messages.json`, if desired
  - Ensure the output path is empty to make room for new files.  Any existing files won't be overwritten.
  - Run the script `python main.py`
  - If necessary, Drag and drop the output .md files into your obsidian vault
  - Execute the todo's within each .md file
  - Rejoice!

## misc notes
  - Obsidian-flavored markdown:  If you use it with another application, some features may look a bit strange, eg the double-`==` surrounding the ==highlights==
