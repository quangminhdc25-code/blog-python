from flask import Flask
import markdown
import os

app = Flask(__name__)

POSTS_DIR = "posts"

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
                "date": meta.get("date", ""),
                "desc": meta.get("description", "")
            })

    # 🔥 sắp xếp mới nhất lên trên
    posts = sorted(posts, key=lambda x: x["date"], reverse=True)

    return posts

def layout(content, title="Blog"):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{title}</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-white text-gray-900">

        <!-- NAVBAR -->
        <div class="border-b">
            <div class="max-w-2xl mx-auto px-4 py-4 flex justify-between">
                <a href="/" class="font-semibold text-lg">Blog của tôi</a>
            </div>
        </div>

        <!-- CONTENT -->
        <div class="max-w-2xl mx-auto px-4 py-10">
            {content}
        </div>

    </body>
    </html>
    """

@app.route("/")
def home():
    posts = get_posts()

    if not posts:
        content = "<p>Chưa có bài viết nào.</p>"
    else:
        content = ""

        for p in posts:
            content += f"""
            <div class="mb-8">
                <a href="/post/{p['slug']}" class="text-2xl font-bold hover:underline">
                    {p['title']}
                </a>
                <p class="text-gray-500 text-sm mt-1">{p['date']}</p>
                <p class="mt-2 text-gray-700">{p['desc']}</p>
            </div>
            """

    return layout(content, "Trang chủ")

@app.route("/post/<slug>")
def post(slug):
    path = os.path.join(POSTS_DIR, slug + ".md")

    if not os.path.exists(path):
        return "Không tìm thấy bài viết"

    meta, html_content = parse_post(path)

    content = f"""
    <a href="/" class="text-sm text-blue-600 hover:underline">← Quay lại</a>

    <h1 class="text-4xl font-bold mt-4 mb-2">{meta.get("title", "")}</h1>
    <p class="text-gray-500 text-sm mb-6">{meta.get("date", "")}</p>

    <div class="prose prose-lg max-w-none">
        {html_content}
    </div>
    """

    return layout(content, meta.get("title", slug))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
