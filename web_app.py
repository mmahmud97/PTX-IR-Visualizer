# web_app.py
# -------------------------------------------------------------------------------------
# A simple Flask server to display PTX IR transformations in a web interface.
# -------------------------------------------------------------------------------------

from flask import Flask, render_template, request
import os

from ptx_parser import PtxParser
from transform_analyzer import TransformAnalyzer
from visualizer import Visualizer  # ✅ Make sure this line is included!

# Initialize the Flask app
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            # Get PTX texts from form fields or file uploads
            ptx_text_a = request.form.get("ptx_text_a", "")
            ptx_text_b = request.form.get("ptx_text_b", "")

            print("\nReceived PTX Version A:\n", ptx_text_a)
            print("\nReceived PTX Version B:\n", ptx_text_b)

            parser = PtxParser()
            ptx_a = parser.parse_ptx(ptx_text_a)
            ptx_b = parser.parse_ptx(ptx_text_b)

            print("\nParsed PTX A:\n", ptx_a)
            print("\nParsed PTX B:\n", ptx_b)

            analyzer = TransformAnalyzer()
            diff_report = analyzer.compare_kernels(ptx_a, ptx_b)

            print("\nDiff Report:\n", diff_report)  # ✅ Debug Print

            # Check if the diff report is empty
            if not diff_report["changed_kernels"]:
                print("No changes detected.")
            else:
                print("Changes detected!")

            visual = Visualizer()
            text_diff = visual.text_report(diff_report)

            print("\nGenerated Text Diff:\n", text_diff)  # ✅ Debug Print

            return render_template("index.html", diff_report=text_diff)

        except Exception as e:
            print("\nError occurred:", str(e))
            return "An error occurred: " + str(e), 500

    return render_template("index.html", diff_report=None)


# Run the app
if __name__ == "__main__":
    app.run(debug=True)

