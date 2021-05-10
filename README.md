# MicroThoughts 🔬📝

A truly minimalistic, statically generated, markdown-based microblogging platform.

## Demo Site: [https://thoughts.markzhang.io](https://thoughts.markzhang.io)

## Notable Features
* Simplistic setup, if you know markdown you are all set!
* Supports LaTeX for all you mathy people. Simply use `\\( your_math_here \\)` for inline math, and `$$ more_math_here $$` for displayed mathematical expressions.
* Supports automatic code snippet syntax highlighting. Surround your code with \`\`\` code here \`\`\` to create a code block. 

## Setup
1. Install dependencies
```
pip install -r requirements.txt
```
2. Add markdown files to the `thoughts` folder, name it using the format `YYYYMMDDHHmm.md`.
3. Execute renderer
```
python render.py
```
4. Site generated to the `output` folder

## TODO:
- [x] Pagination: automatically paginate to reduce page load time
- [x] Permalink support for post sharing
- [ ] Use a better html template engine (avoid hardcoding string constants in Python)
- [ ] Remove unnecessary css/js dependencies (specifically skeleton.css)