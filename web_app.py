# web_app.py
# -------------------------------------------------------------------------------------
# A simple Flask server to display PTX IR transformations in a web interface.
# -------------------------------------------------------------------------------------

from flask import Flask, render_template, request
import os

from ptx_parser import PtxParser
from transform_analyzer import TransformAnalyzer
from visualizer import Visualizer

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get PTX texts from form fields or file uploads
        ptx_text_a = request.form.get("ptx_text_a", "")
        ptx_text_b = request.form.get("ptx_text_b", "")

        parser = PtxParser()
        ptx_a = parser.parse_ptx(ptx_text_a)
        ptx_b = parser.parse_ptx(ptx_text_b)

        analyzer = TransformAnalyzer()
        diff_report = analyzer.compare_kernels(ptx_a, ptx_b)

        visual = Visualizer()
        text_diff = visual.text_report(diff_report)

        return render_template("index.html", diff_report=text_diff)
    return render_template("index.html", diff_report=None)

if __name__ == "__main__":
    # In production, use a WSGI server (e.g., gunicorn). For demonstration:
    app.run(debug=True)

