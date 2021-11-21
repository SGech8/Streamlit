# achte beim kopieren auf die richtige einrückung, python ist da sehr pingelig

import streamlit as st
from xml.etree import ElementTree as ET

# wenn du kopierst, achte drauf dass ab hier alles eine ebene nach links gerückt werden müsste, der editor wollte das nicht so machen wie ich wollte
st.title('UIMA XMI APP')
st.write("""*TODO: find better title*""")

# das ist der file uploader, über 'file' kannst du kannst du auf die datei zugreifen
file = st.file_uploader("Upload xmi file")
    # plaintext = "here will be text"
name = ""
type = ""
content = ""
if file is not None:
    myf = ET.parse(file)
    root = myf.getroot()
    name = file.name
    type = file.type

    content = ''

    typeArray = []
    beginArray = []
    endArray = []
    idArray = []
    sofaString = ''

    # radio buttons/multiselect vorbereitung (ich hab mich für multiselect entschieden, radio buttons wären auch möglich)
    for child in root:
        # st.write(child)
        # st.write(child.attrib.get('pos'))
        if child.attrib.get('sofaString') is not None:
            sofaString = child.attrib.get('sofaString')
        if child.attrib.get('pos') is not None:
            typeArray.append(str(child.attrib.get('pos')))
            beginArray.append(int(child.attrib.get('begin')))
            endArray.append(int(child.attrib.get('end')))
            if child.attrib.get('id') is not None:
                idArray.append(int(child.attrib.get('id')))

    alreadySeen = []
    for pos in typeArray:
        if pos not in alreadySeen:
            alreadySeen.append(pos)
        # st.button(pos)

    #in currentType speichere ich alle ausgewählten typen
    #currentPoss = st.radio("Select Type: ", alreadySeen)
    currentType = st.multiselect("Select Type: ", alreadySeen)

    #st.write("Radio " + currentPoss)
    #st.write(currentPos)
    #st.write(posArray)
    #st.write(beginArray)

    # TODO xmi to array conversion DONE
    # hier führe ich meine xmi in ein repräsentatives array/liste um
    # achte darauf dass ich nicht alle arrays benutzt habe die hier drunter stehen
    xmiArray = []
    alreadyAddedId = []
    alreadyAddedPosition = []
    splitSofaString = sofaString.split()
    #st.write(splitSofaString)

    actualIndex = 0
    wordIndexList = []
    for word in splitSofaString:
        index = sofaString.index(word, actualIndex)
        wordIndexList.append([word, index])
        actualIndex = index

    #st.write(wordIndexList)

    # finalXmiRep ist meine liste mit allen gefundenen typen und benötigten infos drin
    finalXmiListRep = []
    for couple in wordIndexList:
        #st.write(couple[1])
        if int(couple[1]) in beginArray:
            indexNow = beginArray.index(couple[1])
            posNow = typeArray[indexNow]
            finalXmiListRep.append([str(couple[0]), posNow])
        else:
            finalXmiListRep.append(str(couple[0],))
    #st.write(finalXmiListRep)

    # hier fängt der html kram an
    # TODO multiselect marking DONE
if currentType is not None:
    limitReached = ""
    st.write(limitReached)
    chosenTypes = []
    st.write("Hello I do work!")

    for element in currentType:
        st.write(element)
        chosenTypes.append(str(element))
        # current max: 7
        # TODO: dark theme support DONE
    availableColors = []
    #chosenTheme = st.radio("Choose used theme: ", ["light", "dark"])
    #if chosenTheme == "light":
        #availableColors = ["coral", "chartreuse", "orchid", "gold", "cornflowerblue", "lightseagreen", "mediumpurple"]
    #else:
        #availableColors = ["maroon", "seagreen", "darkmagenta", "teal", "slategrey", "chocolate", "darkgoldenrod"]

    # stringwithcolors ist der finale string zum anzeigen
    stringWithColors = ""
    if len(chosenTypes) > 7 or len(chosenTypes) == 0:
        limitReached = "Currently only seven Types can be displayed at the same time!"
    else:
        finalText = ""
        for wordTypePair in finalXmiListRep:
            if wordTypePair[0] != "" and wordTypePair[1] in chosenTypes:
                typePosition = chosenTypes.index(str(wordTypePair[0]))
            #st.write(typePosition)
            wordTypePair[0] = "<span style=\"background-color: " + availableColors[typePosition] + "\">" + wordTypePair[0] + "</span>"
            st.write(wordTypePair[0])

    for finalWord in finalXmiListRep:
        stringWithColors = stringWithColors + finalWord[0] + " "

# und hier die wichtigste Zeile
    st.write(stringWithColors, unsafe_allow_html=True)




    getPositionInArray = [i for i, x in enumerate(typeArray) if x in chosenTypes]
    st.write(getPositionInArray)
    coloredArray = []
    #todo multi color and each word in array representation
    coloredString = ""
    if len(getPositionInArray) == 1:
        st.write("i do work too")
        if beginArray[getPositionInArray[0]] != 0:
            beginning = (sofaString[0:int(beginArray[getPositionInArray[0]])])
            innerPart = sofaString[int(beginArray[getPositionInArray[0]]):int(endArray[getPositionInArray[0]])]
            annoInnerPart = "<span style=\"background-color: darkseagreen\">" + str(innerPart) + "<sup>" + str(
                                currentType) + "</sup></span>"
            middle = (str(annoInnerPart))
            ending = (sofaString[int(endArray[getPositionInArray[0]]):len(sofaString)])
            coloredString = beginning + middle + ending
    #if len(getPositionInArray) > 1:
        #for j in getPositionInArray:
            #st.write("More than one occurence!")
    else:
        st.write("Nothing was selected!")

    # das hier brauchst du nicht
    #for child in root:
        #if child.attrib.get('sofaString') is not None:
            # content = child.attrib.get('sofaString')
            # content = "<b>" + content + "</b>"
            # content = coloredString
           # content = stringWithColors
