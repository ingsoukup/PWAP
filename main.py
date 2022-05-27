from pickle import TRUE
from website import create_app      #slozka website je python package diky __init.py

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)             #run flask app and server a pokazde zmene server rebootuje - nepouzivat na produkci
