First "touch" on flask api.

Build docker image with:
    docker build -t myflask .
    
Run docker image :
    docker run -p 5000:5000 myflask

Accessing endpoints the localhost url on port 5000 (http://localhost:5000/) 
/upload
/create
/download/<filename>
/modify/<filename>
/list
/delete/<filename>
TODO
add docx templates and jinja tags
