from flask import Flask, request, render_template_string
import lxml.etree as ET
import io

app = Flask(__name__)

upload_form = '''
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Tenacy ctf 001</title>
  </head>
  <body>
    <h1>Upload dat XML File</h1>
    <form method="post" enctype="multipart/form-data">
      <input type="file" name="file">
      <input type="submit" value="Upload">
    </form>
    <!-- TODO: Remove password from secrets.txt -->
    <!-- TODO: Migrate to a newer Docker version - fleblond07 -->
  </body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.xml'):
            xml_content = file.read()
            try:
                # Vulnerable XML parsing with lxml
                parser = ET.XMLParser(load_dtd=True, no_network=False)
                tree = ET.parse(io.BytesIO(xml_content), parser)
                root = tree.getroot()
                # Ensure a valid return response, even if data element is not found
                data_text = root.find('data').text if root.find('data') is not None else 'Data was either not found or is empty'
                return f"Parsed <data>: {data_text}"
            except ET.XMLSyntaxError as e:
                return f"Error parsing XML: {e}"
        else:
            return "Invalid file or no file provided. Please upload an XML file."
    return render_template_string(upload_form)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
