First "touch" on flask api.

Build docker image with:
    docker build -t myflask .
Run docker image :
    docker run -p 5000:5000 myflaskapi

Accessing the localhost url on port 5000 (http://localhost:5000/) downloads a sample file (report.docx) on ur pc. The report.docx is made with docx and python

TODO
add docx templates and jinja tags