from flask import Flask, render_template_string
import os

app = Flask(__name__)

POSTS_DIR = "posts"

# Lấy danh sách bài viết
def get_posts():
    files = os.listdir(POSTS_DIR)
    posts = []
    for file in files:
        if file.endswith(".md"):
            posts.append(file.replace(".md", ""))
    return posts

# Trang chủ
@app.route("/")
def home():
    posts = get_posts()
    html = "<h1>Blog của tôi</h1><ul>"
    for p in posts:
        html += f'<li><a href="/post/{p}">{p}</a></li>'
    html += "</ul>"
    return html

# Trang đọc bài
@app.route("/post/<slug>")
def post(slug):
    path = os.path.join(POSTS_DIR, slug + ".md")
    if not os.path.exists(path):
        return "Không tìm thấy bài viết"

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    return f"<pre>{content}</pre>"

# chạy server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
