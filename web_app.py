# web_app.py
# -------------------------------------------------------------------------------------
# A simple Flask server to display PTX IR transformations in a web interface.
# -------------------------------------------------------------------------------------

from flask import Flask, render_template, request
from ptx_parser import PtxParser
from transform_analyzer import TransformAnalyzer

# Initialize the Flask app
app = Flask(__name__)

# Define the main route
@app.route("/", methods=["GET", "POST"])
def index():
    ptx_text_a = ""
    ptx_text_b = ""
    diff_report = None

    if request.method == "POST":
        # Get PTX texts from form fields
        ptx_text_a = request.form.get("ptx_text_a", "")
        ptx_text_b = request.form.get("ptx_text_b", "")

        if ptx_text_a and ptx_text_b:
            # Parse both PTX inputs
            parser = PtxParser()
            ptx_a = parser.parse_ptx(ptx_text_a)
            ptx_b = parser.parse_ptx(ptx_text_b)

            # Compare PTX files
            analyzer = TransformAnalyzer()
            diff_report = analyzer.compare_kernels(ptx_a, ptx_b)

    return render_template("index.html", ptx_text_a=ptx_text_a, ptx_text_b=ptx_text_b, diff_report=diff_report)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)

