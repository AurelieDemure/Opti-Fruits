ALLOWED_EXTENSIONS={'png','jpg','jpeg'}

def allowed_file(filename):
    namelist=filename.split('.')
    if len(namelist)==2:
        return(namelist[1] in ALLOWED_EXTENSIONS)
    return(False)

def test_allowed_file():
    assert(allowed_file('picture.png'))
    assert(allowed_file('picture.jpg'))
    assert(allowed_file('picture.jpeg'))
    assert(not allowed_file('picture.jqsdpj'))
    assert(not allowed_file('picture'))
    assert(not allowed_file('pic.ture.jpeg'))