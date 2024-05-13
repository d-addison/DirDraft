# Focused navigation bar action style
FOCUSED_ACTION_STYLE = "color: black; font-weight: bold;"

# Unfocused navigation bar action style
UNFOCUSED_ACTION_STYLE = "color: gray; font-weight: normal;"

# Folder style
FOLDER_STYLE = "green"

# File style
FILE_STYLE = "purple"

# Error style
ERROR_STYLE = "red"

# No style
NO_STYLE = "black"

# Generated node style
GENERATED_STYLE = "#808080"  # Gray color

# Tag styling
TAG_STYLES = {
   "image": "color: blue;",
   "text": "color: green;",
   "video": "color: purple;",
   "audio": "color: orange;",
   "document": "color: brown;",
   "code": "color: darkgreen;",
   "starred": "color: red;",
   "important": "color: darkred;",
   "draft": "color: gray;",
   "final": "color: darkblue;",
   "backup": "color: darkgray;",
   "large_file": "color: darkred;",
   "small_file": "color: darkgreen;",
   "generated": "color: purple;",
   "user_created": "color: black;",
   "folder": "color: green;",
   "file": "color: lightpurple;",
   "renamed": "color: lightred;"
}

# Tag precedence order
TAG_PRECEDENCE = [
   'generated', 
   'folder', 
   'file', 
   'image', 
   'text', 
   'video', 
   'audio', 
   'document', 
   'code', 
   'starred', 
   'important', 
   'draft', 
   'final', 
   'backup', 
   'large_file', 
   'small_file', 
   'user_created',
   'renamed'
]

NO_STYLE = "color: black;"