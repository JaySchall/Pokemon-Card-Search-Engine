# Search-Engine
Program in Python made to parse a file containing information on pokemon cards, create an inverted index, and create a search engine for the cards.
File contains approx. 13,000 cards from up to gen 8.

## Requirements

Needs Python 3 and a few libraries which can be installed using the following pip commands:

```sh
pip install pystemmer
pip install requests
```

## Running the Program

Ensure that the 2 python files and the train.csv file are in the same directory. cd into the directory in the command line and type the following command:

```sh
python cardInverted.py
```

This will generate an inverted index split into multiple files and a doc that assists in sorting through them. The inverted index only needs to be generated when it doesn't exist or the train.csv is changed.

Now you can run the search engine. This requires internet access in order to load the card images from the web. To start, run the command:

```sh
python cardSearch.py
```

This should bring up a UI window. Before doing anything, resize it to whatever best fits your screen. Now you can search up cards using the input box at the top. You can search using pokemon names, move names, element type, card type, etc. just insure the spelling is correct. The search will display the 3 most relevant cards. Whenever you are finished using the search you can just close the window.
