# web_app.py
# -------------------------------------------------------------------------------------
# A simple Flask server to display PTX IR transformations in a web interface.
# -------------------------------------------------------------------------------------

from flask import Flask, render_template, request
from ptx_parser import PtxParser
from transform_analyzer import TransformAnalyzer
from visualizer import Visualizer

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get PTX texts from form fields
        ptx_text_a = request.form.get("ptx_text_a", "").strip()
        ptx_text_b = request.form.get("ptx_text_b", "").strip()

        # Log received inputs
        print("\nReceived PTX Version A:\n", ptx_text_a)
        print("\nReceived PTX Version B:\n", ptx_text_b)

        # Parse the PTX inputs
        parser = PtxParser()
        ptx_a = parser.parse_ptx(ptx_text_a)
        ptx_b = parser.parse_ptx(ptx_text_b)

        # Log parsed results
        print("\nParsed PTX A:\n", ptx_a)
        print("\nParsed PTX B:\n", ptx_b)

        # Compare the parsed PTX files
        analyzer = TransformAnalyzer()
        diff_report = analyzer.compare_kernels(ptx_a, ptx_b)

        # Generate the diff text report
        visual = Visualizer()
        text_diff = visual.text_report(diff_report)

        # Log diff report
        print("\nDiff Report:\n", text_diff)

        # Return the result to the HTML page
        if text_diff.strip():
            return render_template("index.html", diff_report=text_diff)
        else:
            return render_template("index.html", diff_report="No differences found.")

    # Initial page load
    return render_template("index.html", diff_report=None)

if __name__ == "__main__":
    app.run(debug=True)
