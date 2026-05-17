from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "canjia-dev-secret"

FIELDS = [
    "AGI",
    "ACTF",
    "수영",
    "스카이 다이빙",
    "암벽 등반",
    "카페 취업",
    "기술 연마",
]

ARTICLES = {field: [] for field in FIELDS}


@app.route("/")
def home():
    return render_template("home.html", fields=FIELDS)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/signup")
def signup():
    return render_template("auth_placeholder.html", title="회원 가입")


@app.route("/login")
def login():
    return render_template("auth_placeholder.html", title="로그인")


@app.route("/profile")
def profile():
    return render_template("auth_placeholder.html", title="프로필 작성")


@app.route("/mfa")
def mfa():
    return render_template("auth_placeholder.html", title="2차 인증")


@app.route("/fields/<field>")
def field_page(field: str):
    if field not in ARTICLES:
        return redirect(url_for("home"))
    return render_template("field.html", field=field, docs=ARTICLES[field])


@app.route("/fields/<field>/new", methods=["GET", "POST"])
def new_document(field: str):
    if field not in ARTICLES:
        return redirect(url_for("home"))

    if request.method == "POST":
        author = request.form.get("author", "").strip()
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()

        if not author or not title or not content:
            flash("작성자, 제목, 내용을 모두 입력해주세요.", "error")
            return render_template("editor.html", field=field)

        ARTICLES[field].append({"author": author, "title": title, "content": content})
        flash("문서가 등록되었습니다.", "success")
        return redirect(url_for("field_page", field=field))

    return render_template("editor.html", field=field)


if __name__ == "__main__":
    app.run(debug=True)
