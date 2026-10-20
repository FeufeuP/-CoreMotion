"""Monta o deck web autocontido (fontes embutidas em base64).

Uso:  python build_web.py            -> ../CoreMotion-Pitch-Web.html
"""
import pathlib
import sys

HERE = pathlib.Path(__file__).parent
SRC = HERE / "src"
OUT = HERE.parent / "CoreMotion-Pitch-Web.html"

PARTS = ["01_hero.html", "02_why.html", "03_product.html", "04_market.html", "05_team.html"]


def read(p):
    return (SRC / p).read_text(encoding="utf-8")


def main():
    html = read("00_head.html")
    html = html.replace("/*__FONTS__*/", read("fonts.css"))
    html = html.replace("/*__BASE__*/", read("base.css"))
    html = html.replace("/*__UI__*/", read("ui.css"))
    html = html.replace("/*__S1__*/", read("scenes1.css"))
    html = html.replace("/*__S2__*/", read("scenes2.css"))
    html = html.replace("/*__S3__*/", read("scenes3.css"))
    html = html.replace("/*__S4__*/", read("scenes4.css"))

    body = "\n".join(read(p) for p in PARTS)
    html += body + "\n" + read("09_tail.html")
    html = html.replace("/*__APP__*/", read("app.js"))

    OUT.write_text(html, encoding="utf-8")
    kb = len(html.encode()) / 1024
    print(f"ok  {OUT.name}  {kb:.0f} KB")


if __name__ == "__main__":
    sys.exit(main())
