from flask import Flask
import os
import markdown

app = Flask(__name__)

# ---------- LOAD MARKDOWN ----------
def load_markdown(file_name):
    path = os.path.join("posts", file_name)

    if not os.path.exists(path):
        return "<p>Không có nội dung</p>"

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    return markdown.markdown(content, extensions=["fenced_code"])


# ---------- LAYOUT ----------
def layout(content, title="App"):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{title}</title>
        <script src="https://cdn.tailwindcss.com"></script>

        <style>
        body {{
            transition: background 0.3s, color 0.3s;
        }}

        .glass {{
            backdrop-filter: blur(10px);
        }}

        .fade {{
            animation: fadeIn 0.25s ease-in-out;
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(8px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .prose {{
            line-height: 1.8;
            font-size: 18px;
        }}

        .prose img {{
            border-radius: 10px;
            margin: 20px 0;
        }}
        </style>
    </head>

    <body class="bg-white text-gray-900">

        <!-- NAVBAR -->
        <div id="navbar" class="glass border-b sticky top-0 z-50 bg-white/70">
            <div class="max-w-5xl mx-auto px-4 py-3 flex justify-between items-center">

                <div class="flex gap-6 items-center">

                    <a href="/" class="font-bold text-lg">My App</a>

                    <!-- Dự án 1 -->
                    <div class="relative group py-2">
                        <div class="px-3 py-2 cursor-pointer hover:bg-gray-200 rounded-lg">
                            Dự án 1
                        </div>

                        <div class="absolute hidden group-hover:block top-full left-0 w-44 bg-white shadow-lg rounded-lg fade">

                            <a href="/project1/info"
                               class="block px-4 py-3 hover:bg-gray-100 rounded-t-lg">
                               Thông tin
                            </a>

                            <a href="/project1/guide"
                               class="block px-4 py-3 hover:bg-gray-100 rounded-b-lg">
                               Hướng dẫn
                            </a>

                        </div>
                    </div>

                    <a href="/project2" class="px-3 py-2 hover:bg-gray-200 rounded-lg">Dự án 2</a>
                    <a href="/project3" class="px-3 py-2 hover:bg-gray-200 rounded-lg">Dự án 3</a>

                </div>

                <!-- DARK MODE -->
                <button onclick="toggleDark()" class="px-3 py-2 rounded-lg border">
                    🌙
                </button>

            </div>
        </div>

        <!-- CONTENT -->
        <div id="content" class="max-w-3xl mx-auto px-4 py-10 fade">
            {content}
        </div>

        <!-- DARK MODE SCRIPT -->
        <script>
        function setDarkMode(enabled) {{
            const body = document.body;
            const navbar = document.getElementById("navbar");

            if (enabled) {{
                body.classList.remove("bg-white", "text-gray-900");
                body.classList.add("bg-gray-900", "text-gray-100");

                navbar.classList.remove("bg-white/70");
                navbar.classList.add("bg-gray-800/70");

                localStorage.setItem("theme", "dark");
            }} else {{
                body.classList.remove("bg-gray-900", "text-gray-100");
                body.classList.add("bg-white", "text-gray-900");

                navbar.classList.remove("bg-gray-800/70");
                navbar.classList.add("bg-white/70");

                localStorage.setItem("theme", "light");
            }}
        }}

        function toggleDark() {{
            const current = localStorage.getItem("theme");
            setDarkMode(current !== "dark");
        }}

        window.onload = function() {{
            const saved = localStorage.getItem("theme");
            if (saved === "dark") {{
                setDarkMode(true);
            }}
        }}
        </script>

    </body>
    </html>
    """


# ---------- ROUTES ----------

@app.route("/")
def home():
    content = """
    <h1 class="text-3xl font-bold mb-4">Trang chủ</h1>
    <p>Chọn một dự án từ menu phía trên.</p>
    """
    return layout(content)


@app.route("/project1/info")
def project1_info():
    html_content = load_markdown("project1_info.md")

    content = f"""
    <h1 class="text-2xl font-bold mb-6">Dự án 1 - Thông tin</h1>
    <div class="prose max-w-none">
        {html_content}
    </div>
    """

    return layout(content, "Dự án 1 - Thông tin")


@app.route("/project1/guide")
def project1_guide():
    html_content = load_markdown("project1_guide.md")

    content = f"""
    <h1 class="text-2xl font-bold mb-6">Dự án 1 - Hướng dẫn</h1>
    <div class="prose max-w-none">
        {html_content}
    </div>
    """

    return layout(content, "Dự án 1 - Hướng dẫn")


@app.route("/project2")
def project2():
    content = "<h1 class='text-2xl font-bold'>Dự án 2</h1>"
    return layout(content)


@app.route("/project3")
def project3():
    content = "<h1 class='text-2xl font-bold'>Dự án 3</h1>"
    return layout(content)


# ---------- RUN ----------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
