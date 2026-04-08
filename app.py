from flask import Flask
import markdown
import os

app = Flask(__name__)

POSTS_DIR = "posts"

if not os.path.exists(POSTS_DIR):
    os.makedirs(POSTS_DIR)

# ---------- LAYOUT ----------
def layout(content, title="Blog"):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{title}</title>
        <script src="https://cdn.tailwindcss.com"></script>

        <style>
        body {{
            background: #f5f5f7;
        }}

        /* glass effect giống Windows 11 */
        .glass {{
            backdrop-filter: blur(10px);
            background: rgba(255,255,255,0.7);
        }}

        .menu-item:hover {{
            background: rgba(0,0,0,0.05);
            border-radius: 8px;
        }}

        .fade {{
            animation: fadeIn 0.3s ease-in-out;
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        </style>

    </head>

    <body class="text-gray-900">

        <!-- NAVBAR -->
        <div class="glass border-b sticky top-0 z-50">
            <div class="max-w-5xl mx-auto px-4 py-3 flex gap-6 items-center">

                <a href="/" class="font-bold text-lg">My App</a>

                <!-- Dự án 1 -->
                <div class="relative group">
                    <div class="menu-item px-3 py-2 cursor-pointer">Dự án 1</div>

                    <!-- submenu -->
                    <div class="absolute hidden group-hover:block bg-white shadow-lg rounded-lg mt-2 w-40 fade">
                        <a href="/project1/info" class="block px-4 py-2 hover:bg-gray-100">Thông tin</a>
                        <a href="/project1/guide" class="block px-4 py-2 hover:bg-gray-100">Hướng dẫn</a>
                    </div>
                </div>

                <!-- Dự án 2 -->
                <a href="/project2" class="menu-item px-3 py-2">Dự án 2</a>

                <!-- Dự án 3 -->
                <a href="/project3" class="menu-item px-3 py-2">Dự án 3</a>

            </div>
        </div>

        <!-- CONTENT -->
        <div class="max-w-3xl mx-auto px-4 py-10 fade">
            {content}
        </div>

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
    return layout(content, "Trang chủ")


# ----- PROJECT 1 -----
@app.route("/project1/info")
def project1_info():
    content = """
    <h1 class="text-2xl font-bold mb-4">Dự án 1 - Thông tin</h1>
    <p>Đây là phần giới thiệu dự án.</p>
    """
    return layout(content, "Dự án 1 - Thông tin")


@app.route("/project1/guide")
def project1_guide():
    content = """
    <h1 class="text-2xl font-bold mb-4">Dự án 1 - Hướng dẫn</h1>
    <p>Đây là phần hướng dẫn sử dụng.</p>
    """
    return layout(content, "Dự án 1 - Hướng dẫn")


# ----- PROJECT 2 -----
@app.route("/project2")
def project2():
    content = "<h1 class='text-2xl font-bold'>Dự án 2</h1>"
    return layout(content, "Dự án 2")


# ----- PROJECT 3 -----
@app.route("/project3")
def project3():
    content = "<h1 class='text-2xl font-bold'>Dự án 3</h1>"
    return layout(content, "Dự án 3")


# ---------- RUN ----------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
