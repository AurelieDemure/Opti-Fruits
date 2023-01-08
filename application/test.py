ALLOWED_EXTENSIONS={'png','jpg','jpeg'}

def allowed_file(filename):
    #return '.' in filename and \
           #filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    n=len(filename)
    print(n)
    c=0
    while c<(n-1) and filename[c]!='.':
        print(c)
        c=c+1
    if c<n:
        extension=filename[(c+1):]
        return(extension in ALLOWED_EXTENSIONS)
    return(False)

print(allowed_file('picture.png'),allowed_file('picture.jpg'),allowed_file('picture.jpeg'),not allowed_file('picture.jqsdpj'),not allowed_file('picture'))