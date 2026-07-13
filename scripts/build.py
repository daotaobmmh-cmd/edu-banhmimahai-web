import os
import subprocess
import shutil
import re

# File paths
hoinhap_dir = "hoinhap"
src_html = os.path.join(hoinhap_dir, "index.src.html")
dest_html = os.path.join(hoinhap_dir, "index.html")
custom_css = os.path.join(hoinhap_dir, "styles.css")
questions_js = os.path.join(hoinhap_dir, "questions.js")
app_js = os.path.join(hoinhap_dir, "app.js")
alpine_js = os.path.join(hoinhap_dir, "alpine.min.js")

# Config files
tailwind_config_path = "tailwind.config.js"
input_css_path = os.path.join(hoinhap_dir, "input.css")
compiled_css_path = os.path.join(hoinhap_dir, "compiled.css")

print("=== STARTING HOINHAP INLINE BUILD ===")

# 1. Save original index.html as source if index.src.html does not exist
if not os.path.exists(src_html):
    print(f"Renaming {dest_html} to source template {src_html}")
    shutil.move(dest_html, src_html)
else:
    print(f"Using existing source template {src_html}")

# 2. Write tailwind.config.js
print("Writing tailwind.config.js...")
tailwind_config_content = """module.exports = {
  content: [
    "./hoinhap/index.src.html",
    "./hoinhap/app.js"
  ],
  theme: {
    extend: {
      colors: {
        primary: "#39B54A",
        error: "#EC1C24",
        secondary: "#00ADEF",
        warning: "#F4CC34",
        background: "#FAF7F2",
        "surface-variant": "#e4e2e2",
        "on-surface-variant": "#3e4a3c"
      },
      borderRadius: {
        xl: "0.75rem",
        "2xl": "1.25rem"
      }
    }
  },
  plugins: []
}
"""
with open(tailwind_config_path, "w", encoding="utf-8") as f:
    f.write(tailwind_config_content)

# 3. Write input.css for Tailwind directives
print("Writing input.css...")
with open(input_css_path, "w", encoding="utf-8") as f:
    f.write("@tailwind base;\n@tailwind components;\n@tailwind utilities;\n")

# 4. Compile Tailwind CSS
print("Compiling Tailwind CSS...")
try:
    cmd = [
        "npx", "-y", "tailwindcss@3.4.1",
        "-i", input_css_path,
        "-o", compiled_css_path,
        "-c", tailwind_config_path,
        "--minify"
    ]
    # Under Windows, npx might need shell=True
    subprocess.run(cmd, shell=True, check=True)
    print("Tailwind compiled successfully.")
except Exception as e:
    print(f"Error compiling Tailwind: {e}")
    # Fallback to empty if failed
    with open(compiled_css_path, "w", encoding="utf-8") as f:
        f.write("")

# 5. Read CSS assets
compiled_css = ""
if os.path.exists(compiled_css_path):
    with open(compiled_css_path, "r", encoding="utf-8") as f:
        compiled_css = f.read()

styles_css = ""
if os.path.exists(custom_css):
    with open(custom_css, "r", encoding="utf-8") as f:
        styles_css = f.read()

combined_css = compiled_css + "\n" + styles_css

# 6. Read JS assets
with open(questions_js, "r", encoding="utf-8") as f:
    questions_content = f.read()

with open(app_js, "r", encoding="utf-8") as f:
    app_content = f.read()

with open(alpine_js, "r", encoding="utf-8") as f:
    alpine_content = f.read()

# 7. Read source template HTML
with open(src_html, "r", encoding="utf-8") as f:
    html = f.read()

# 8. Perform inline replacements
print("Inlining assets into template...")

# Remove Tailwind CDN script tag
cdn_pattern = r'<!-- Tailwind CSS CDN and Configuration -->.*?<script src="https://cdn.tailwindcss.com\?plugins=forms,container-queries"></script>'
html = re.sub(cdn_pattern, "", html, flags=re.DOTALL)

# Remove Tailwind CDN config block tag
config_pattern = r'<script id="tailwind-config">.*?</script>'
html = re.sub(config_pattern, "", html, flags=re.DOTALL)

# Replace CSS style and link tag separately to avoid regex wildcard issues
style_pattern = """    <style>
        [x-cloak] {
            display: none !important;
        }
    </style>"""
replacement_css = f"<style>\n[x-cloak] {{\n    display: none !important;\n}}\n/* Inline CSS */\n{combined_css}\n</style>"
html = html.replace(style_pattern, replacement_css)

link_tag = '<link rel="stylesheet" href="./styles.css?v=1.4" />'
html = html.replace(link_tag, '')

# Extract raw JSON from questions.js contents
json_content = questions_content.strip()
if json_content.startswith("window.HOINHAP_QUESTIONS ="):
    json_content = json_content[len("window.HOINHAP_QUESTIONS ="):].strip()
if json_content.endswith(";"):
    json_content = json_content[:-1].strip()

# Replace questions.js
replacement_q = f'<script id="questions-json" type="application/json">\n{json_content}\n</script>\n<script id="inline-questions-loaded">\nmarkScriptLoaded("questions.js");\n</script>'
html = re.sub(r'<script\s+[^>]*src="\.?/questions\.js[^>]*>.*?</script>', lambda m: replacement_q, html, flags=re.DOTALL)

# Replace app.js
replacement_a = f"<script id=\"inline-app\">\n{app_content}\nmarkScriptLoaded('app.js');\n</script>"
html = re.sub(r'<script\s+[^>]*src="\.?/app\.js[^>]*>.*?</script>', lambda m: replacement_a, html, flags=re.DOTALL)

# Replace alpine.min.js
replacement_alp = f"<script defer id=\"inline-alpine\">\n{alpine_content}\nmarkScriptLoaded('alpine.min.js');\n</script>"
html = re.sub(r'<script\s+[^>]*src="\.?/alpine\.min\.js[^>]*>.*?</script>', lambda m: replacement_alp, html, flags=re.DOTALL)

# 9. Write back inlined output
with open(dest_html, "w", encoding="utf-8") as f:
    f.write(html)
print(f"Self-contained index.html generated at {dest_html}")

# 10. Cleanup temp files
for temp in [input_css_path, compiled_css_path]:
    if os.path.exists(temp):
        os.remove(temp)

print("=== HOINHAP INLINE BUILD COMPLETED SUCCESSFULLY ===")
