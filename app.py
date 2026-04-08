from flask import Flask
import markdown
import os

app = Flask(__name__)

POSTS_DIR = "posts"

def get_posts():
    files = os.listdir(POSTS_DIR)
    posts = []
    for file in files:
        if file.endswith(".md"):
            posts.append(file.replace(".md", ""))
    return posts

@app.route("/")
def home():
    posts = get_posts()
    html = "<h1>Blog của tôi</h1><ul>"
    for p in posts:
        html += f'<li><a href="/post/{p}">{p}</a></li>'
    html += "</ul>"
    return html

@app.route("/post/<slug>")
def post(slug):
    path = os.path.join(POSTS_DIR, slug + ".md")
    if not os.path.exists(path):
        return "Không tìm thấy bài viết"

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    html_content = markdown.markdown(content)
    return f"<div style='max-width:700px;margin:auto;font-family:sans-serif'>{html_content}</div>"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
