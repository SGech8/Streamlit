import logging
import streamlit as st
from xml.etree import ElementTree as ET


logging.warning('warning')
logging.debug('debug')

st.title('Bachelorarbeit')
st.write("""*TODO: find better title*""")


col1, col2 = st.columns([2,6])
with col1:
    file = st.file_uploader("Essays")
with col2:
    st.write("""
        # Hello
        Ich habs endlich rausgefunden""")
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

        # hier führe ich meine xmi in ein repräsentatives array/liste um
        # achte darauf dass ich nicht alle arrays benutzt habe die hier drunter stehen
        xmiArray = []
        alreadyAddedId = []
        alreadyAddedPosition = []
        splitSofaString = sofaString.split()
        # st.write(splitSofaString)

        actualIndex = 0
        wordIndexList = []
        for word in splitSofaString:
            index = sofaString.index(word, actualIndex)
            wordIndexList.append([word, index])
            actualIndex = index

        # st.write(wordIndexList)

        # finalXmiRep ist meine liste mit allen gefundenen typen und benötigten infos drin
        finalXmiListRep = []
        for couple in wordIndexList:
            # st.write(couple[1])
            if int(couple[1]) in beginArray:
                indexNow = beginArray.index(couple[1])
                posNow = typeArray[indexNow]
                finalXmiListRep.append([str(couple[0]), posNow])
            else:
                finalXmiListRep.append(str(couple[0], ))
        # st.write(finalXmiListRep)


            # in currentType speichere ich alle ausgewählten typen
            # currentPoss = st.radio("Select Type: ", alreadySeen)
        currentType = st.multiselect("Select Type: ", alreadySeen)


        # hier fängt der html kram an
        # TODO multiselect marking DONE
        if currentType is not None:
            limitReached = ""
            st.write(limitReached)
            chosenTypes = []
            st.write("Multiselect marking")

            for element in currentType:
                st.write(element)
                chosenTypes.append(str(element))
                # current max: 7

            # stringwithcolors ist der finale string zum anzeigen
            stringWithColors = ""
            if len(chosenTypes) > 7 or len(chosenTypes) == 0:
                limitReached = "Currently only seven Types can be displayed at the same time!"
            else:
                finalText = ""
                for wordTypePair in finalXmiListRep:
                    if wordTypePair[0] != "" and wordTypePair[1] in chosenTypes:
                        typePosition = chosenTypes.index(str(wordTypePair[0]))
                    # st.write(typePosition)
                    # wordTypePair[0] = "<span style=\"background-color: " + availableColors[typePosition] + "\">" + wordTypePair[0] + "</span>"
                    st.write(wordTypePair[0])

            for finalWord in finalXmiListRep:
                stringWithColors = stringWithColors + finalWord[0] + " "

            # und hier die wichtigste Zeile
            st.write(stringWithColors, unsafe_allow_html=True)

    grade = st.slider("Wähle eine Note", 1, 6)
