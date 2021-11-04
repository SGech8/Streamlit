import streamlit as st
import pandas as pd
from xml.etree import ElementTree as ET


st.title('Bachelorarbeit')
st.write("""*TODO: find better title*""")


col1, col2 = st.columns([2,6])
with col1:
    file = st.file_uploader("Essays")
with col2:
    st.write("""
        # Hello
        Ich habs endlich rausgefunden""")

    if file is not None:
        myf = ET.parse(file)
        root = myf.getroot()
        name = file.name
        type = file.type

        content = ''
        typeArray = []
        posArray = []
        beginArray = []
        endArray = []
        idArray = []
        sofaString = ''

        for child in root:
            #st.write(child.attrib.get('coarseValue'))
            # st.write(child.attrib.get('pos'))
            if child.attrib.get('sofaString') is not None:
                sofaString = child.attrib.get('sofaString')
                #st.write(sofaString)
            if child.attrib.get('pos') is not None:
                posArray.append(str(child.attrib.get('pos')))
                beginArray.append(int(child.attrib.get('begin')))
                endArray.append(int(child.attrib.get('end')))
                if child.attrib.get('id') is not None:
                    idArray.append(int(child.attrib.get('id')))
            if child.attrib.get('name') is not None and child.attrib.get('begin') is not None:
                typeArray.append([str(child.attrib.get('name')), int(child.attrib.get('begin'))])
        st.write(typeArray)

        #pos und tatsächlicher typ sind da drin, mit pos kann man bessser mit den worten matchen, so mein gedanke
        #ToDo: die unsinnigen Arten rausstreichen
        finalTypeArray = []
        for i in typeArray:
            if int(i[1]) in beginArray:
                indexNow = beginArray.index(i[1])
                posNow = posArray[indexNow]
                finalTypeArray.append([str(i[0]), posNow])
        st.write(finalTypeArray)

        alreadySeen = []
        for x in typeArray:
            if x[0] not in alreadySeen:
                alreadySeen.append(x[0])
            # st.button(pos)

        #Anzahl jedes Types bestimmen
        counter = []
        for i in range(len(alreadySeen)):
            count = 0
            for x in range(len(finalTypeArray)):
                if finalTypeArray[x][0] in alreadySeen[i]:
                    count += 1
            counter.append(count)
        st.write("Counter: ", counter)

        #Wortarten und ihre Anzahl im Essay... ich hasse mich
        typeCount = pd.DataFrame(counter, index=['ptb', 'determiner', 'verb', 'noun', 'preposition', 'none',
                                                 'adjective', 'pronoun', 'adverb', 'NUM'], columns=['Count'])
        st.write(typeCount)
        st.bar_chart(typeCount)

        # hier führe ich meine xmi in ein repräsentatives array/liste um
        # achte darauf dass ich nicht alle arrays benutzt habe die hier drunter stehen
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

        st.write(wordIndexList)

        # finalXmiRep ist meine liste mit allen gefundenen typen und benötigten infos drin
        finalXmiListRep = []
        for couple in wordIndexList:
            #st.write(couple[1])
            if int(couple[1]) in beginArray:
                indexNow = beginArray.index(couple[1])
                posNow = posArray[indexNow]
                finalXmiListRep.append([str(couple[0]), posNow])
            else:
                finalXmiListRep.append(str(couple[0], ))
        st.write("Final Xmi: ", finalXmiListRep)
        #st.write(finalXmiListRep[0][1])

        # in currentType speichere ich alle ausgewählten typen
        #currentPoss = st.radio("Select Type: ", alreadySeen)
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
                    if wordTypePair[0] is not None and wordTypePair[1] in chosenTypes:
                        typePosition = chosenTypes.index(str(wordTypePair[0]))
                    # st.write(typePosition)
                    #wordTypePair[0] = "<span style=\"background-color: " + availableColors[typePosition] + "\">" + wordTypePair[0] + "</span>"
                    #st.write(wordTypePair[0])

            for finalWord in finalXmiListRep:
                stringWithColors = stringWithColors + finalWord[0] + " "

            # und hier die wichtigste Zeile
            st.write(stringWithColors, unsafe_allow_html=True)

    grade = st.slider("Wähle eine Note", 0, 6)

