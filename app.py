from flask import Flask
import markdown
import os

app = Flask(__name__)

POSTS_DIR = "posts"

# 🔥 đảm bảo folder tồn tại
if not os.path.exists(POSTS_DIR):
    os.makedirs(POSTS_DIR)

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
    # 🔥 đảm bảo không crash nếu folder trống
    if not os.path.exists(POSTS_DIR):
        return []

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
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-50 text-gray-800">
        <div class="max-w-2xl mx-auto py-10 px-4">
            <h1 class="text-3xl font-bold mb-6">Blog của tôi</h1>
    """

    if not posts:
        html += "<p>Chưa có bài viết nào.</p>"
    else:
        html += "<div class='space-y-4'>"
        for p in posts:
            html += f"""
            <div class="border-b pb-3">
                <a href="/post/{p['slug']}" class="text-xl font-semibold text-blue-600 hover:underline">
                    {p['title']}
                </a>
                <p class="text-sm text-gray-500">{p['date']}</p>
            </div>
            """
        html += "</div>"

    html += """
        </div>
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
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-50 text-gray-800">
        <div class="max-w-2xl mx-auto py-10 px-4">
            <a href="/" class="text-sm text-blue-600 hover:underline">← Quay lại</a>
            <h1 class="text-3xl font-bold mt-4 mb-2">{meta.get("title", "")}</h1>
            <p class="text-sm text-gray-500 mb-6">{meta.get("date", "")}</p>

            <div class="prose max-w-none">
                {html_content}
            </div>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
