# Author: Shane Kelly

import random
import pickle

def capitalize_sentences (text):
    """ (string) -> string
    Takes a string containing sentences and returns a string containing those sentence with proper capitalization.
    
    >>> capitalize_sentences ("hello. nice to meet you!")
    Hello. Nice to meet you!
    >>> capitalize_sentences ("tEST")
    TEST
    >>> capitalize_sentences ("...hello. how are you?")
    "...hello. How are you?"
    """
    textArray = []
    
    for x in text:
        textArray.append(x)
    
    # Prevents error that occurs when textArray passes this point completely empty.
    
    textArray.append("")
        
    for x in range (len(textArray)):
        if x == 0:
            textArray[x] = textArray[x].upper()
            
        # Only capitalizes the letter if punctuation is found AND there is a space after the punctuation!
            
        elif len(textArray) > x + 2 and (textArray[x] == "." or textArray[x] == "!" or textArray[x] == "?") and textArray[x + 1] == " ":
            textArray [x + 2] = textArray[x + 2].upper()
    return ("".join(textArray))
    
def capitalize_sentence_grid (gridList):
    """ (list<string>) -> list<string>
    Takes a list of strings and returns a list of strings with the proper capitalization if that list were to be converted into one single text.
    
    >>> capitalize_sentence_grid (["hello", "how", "are"], ["you?", "good."])
    [["Hello", "how", "are"], ["you?", "Good."]]
    >>> capitalize_sentence_grid (["hello.", "how", "are"], ["you", "today?."], ["good!"])
    [["Hello.", "How", "are"], ["you", "today?"], ["Good!"]]
    >>> capitalize_sentence_grid (["test"], ["test"], ["test.", "test?", "test!"])
    [["Test"], ["test"], ["test.", "Test?", "Test!"]]
    """
    holderList = []
    holderGridList = []
    holderString = ""
    counter = 0
    
    # Builds a single String out of the list, capitalizes, then reverts to list.
    
    for x in gridList:
        holderString += (" ".join(x)) + " "
    holderString = capitalize_sentences (holderString.strip(" "))
    
    holderList = holderString.split(" ")
    holderGridList = []
    
    for x in gridList:
        holderGridList.append(holderList[counter : counter + len(x)])
        counter += len(x)
        
    return (holderGridList)

def fill_in_madlib (madlib, dictionary):
    """ (string, dictionary) -> string
    Takes a string and a dictionary of words. Replaces words formated as [TEXT] and replaces with a random word from the dictionary with key TEXT. 
    
    >>> fill_in_madlib ("Hello my name is [AAAAA]", {"NAME" : ["Ted", "Ned", "Zed", "Red"]})
    AssertionError
    >>> fill_in_madlib (1 , {"NAME" : ["Ted", "Ned", "Zed", "Red"]})
    AssertionError
    >>> fill_in_madlib ("Hello my name is [AAAAA]", 1)
    AssertionError
    >>> fill_in_madlib ("Hello my name is [AAAAA]", {"NAME" : [4, 3, 2, 1]})
    AssertionError
    >>> fill_in_madlib ("Hello my name is [NAME]", {"NAME" : ["Ted", "Ned", "Zed", "Red"]})
    Hello my name is Ted
    >>> fill_in_madlib ("Hello my name is [NAME]", {"NAME" : ["Ted", "Ned", "Zed", "Red"]})
    Hello my name is Ned
    >>> fill_in_madlib ("Hello my name is [NAME]", {"NAME" : ["Ted", "Ned", "Zed", "Red"]})
    Hello my name is Red
    """
    
    # Errors are raised if the input is incorrectly formatted.
    
    if type(madlib) != str:
        raise AssertionError ("The inputted madlib must be a String!")
    if type(dictionary) != dict:
        raise AssertionError ("The inputted dictionary must be of type dict!")
    
    nopeChecker = [""]
    replacement = ""
    
    while madlib.find("[") != -1:
        start = madlib.find("[")
        end = madlib.find("]")
        category = (madlib[start + 1: end].split("_"))
        
        if category[0] not in dictionary:
            raise AssertionError ("Your madlib contains a category not included in dictionary!")
        
        
        while replacement in nopeChecker:
            replacement = dictionary[category[0]][random.randint(0, len(dictionary[category[0]]) - 1)]
            
            if type(replacement) != str:
                raise AssertionError ("Dictionary values must only constain string lists!")
        
        nopeChecker.append (replacement)
        madlib = madlib.replace(madlib[start : end + 1], replacement)
        
    return capitalize_sentences(madlib)

def load_and_process_madlib (madlib):
    """ (string) -> None
    Takes a string containing a madlib template from a text file, then writes to another text file the randomly generated filled version of that madlib.
    
    >>> load_and_process_madlib (madlib)
    
    >>> load_and_process_madlib (madlib)
    
    >>> load_and_process_madlib (madlib)
    
    """
    f = open("word_dict.pkl", "rb")
    word_dict = pickle.load(f)
    f.close()
    
    file = open(madlib, "r")
    unfilledMadlib = file.read()
    file.close()
    
    # The split ensures that just the name of the file and not the .txt extension is being considered.
    
    filename = madlib.split(".")[0]
    file = open (filename + "_filled.txt", "w")
    file.write(fill_in_madlib(unfilledMadlib, word_dict))
    file.close()

def generate_comment ():
    """ (None) -> string
    Randomly selects a madlib file, loads it using the load_and_process_madlib command, then reads the text from the filled file.
    
    >>> generate_comment ()
    I really admire Dee. They've got my vote!
    >>> generate_comment ()
    Dee Buh-Ger is amazing. Ian is unskilled.
    >>> generate_comment ()
    Voting for Dee Buh-Ger is a no brainer. Elsa is simply too inexperienced!
    """
    randomint = random.randint(1, 10)
    load_and_process_madlib("madlib" + str(randomint) + ".txt")
    
    file = open("madlib" + str(randomint) + "_filled.txt")
    return (file.read())

