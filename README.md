Multiple endpoints for docx creation and manipulation with python and flask

Build docker image with:
    docker build -t myflask .
    
Run docker image :
    docker run -p 5000:5000 myflask

Accessing endpoints in localhost url on port 5000 (http://localhost:5000/) 

#endpoint to upload the file
/upload 
#endpoint to create file based on template files already uploaded
/create 
#endpoint to download files with the filename passed in url
/download/<filename> 
#endpoint to modify file
/modify/<filename>
#endpoint to list all files in folder archive
/list
#endpoint to delete file
/delete/<filename>
