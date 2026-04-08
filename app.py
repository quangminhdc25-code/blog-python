from flask import Flask
import markdown
import os

app = Flask(__name__)

POSTS_DIR = "posts"

def parse_post(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    parts = content.split("---")
    
    meta = {}
    if len(parts) > 1:
        meta_lines = parts[0].strip().split("\n")
        for line in meta_lines:
            if ":" in line:
                key, value = line.split(":", 1)
                meta[key.strip()] = value.strip()
        body = parts[1]
    else:
        body = content

    html_content = markdown.markdown(body)
    return meta, html_content

def get_posts():
    files = os.listdir(POSTS_DIR)
    posts = []

    for file in files:
        if file.endswith(".md"):
            slug = file.replace(".md", "")
            path = os.path.join(POSTS_DIR, file)
            meta, _ = parse_post(path)

            posts.append({
                "slug": slug,
                "title": meta.get("title", slug),
                "date": meta.get("date", "")
            })

    return posts

@app.route("/")
def home():
    posts = get_posts()

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Blog của tôi</title>
    </head>
    <body style="font-family:sans-serif; max-width:700px; margin:auto;">
        <h1>Blog của tôi</h1>
        <ul>
    """

    for p in posts:
        html += f'<li><a href="/post/{p["slug"]}">{p["title"]}</a> ({p["date"]})</li>'

    html += """
        </ul>
    </body>
    </html>
    """

    return html

@app.route("/post/<slug>")
def post(slug):
    path = os.path.join(POSTS_DIR, slug + ".md")

    if not os.path.exists(path):
        return "Không tìm thấy bài viết"

    meta, html_content = parse_post(path)

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{meta.get("title", slug)}</title>
    </head>
    <body style="font-family:sans-serif; max-width:700px; margin:auto;">
        <a href="/">← Quay lại</a>
        <h1>{meta.get("title", "")}</h1>
        <p><i>{meta.get("date", "")}</i></p>
        {html_content}
    </body>
    </html>
    """

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
