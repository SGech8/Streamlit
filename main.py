import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from xml.etree import ElementTree as ET


st.title('Bachelorarbeit')
st.write("""*TODO: find better title*""")


col1, col2 = st.columns([2, 6])
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
        level = []

        for child in root:
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
                level.append([str(child.attrib.get('level')), int(child.attrib.get('begin'))])
        st.write(typeArray)

        #pos und tatsächlicher typ sind da drin, mit pos kann man bessser mit den worten matchen, so mein gedanke
        #ToDo: die unsinnigen Arten rausstreichen DONE
        def infoPos(array):
            finalArray = []
            for i in array:
                if int(i[1]) in beginArray:
                    indexNow = beginArray.index(i[1])
                    posNow = posArray[indexNow]
                    finalArray.append([str(i[0]), posNow])
                else:
                    finalArray.append(str(i[0]), )
            return finalArray

        # Erstellt eine Liste, welche Typen vorkommen (jeder Typ nur 1 mal drin)
        def noRep(array):
            finalArray = []
            for x in array:
                if x[0].lower() not in finalArray:
                    finalArray.append(x[0].lower())
            finalArray.remove(finalArray[0])
            return finalArray

        # Anzahl jedes Types bestimmen
        # TODO Methode draus machen DONE
        def counting(seen, array):
            countArray = []
            for i in range(len(seen)):
                count = 0
                for x in range(len(array)):
                    if array[x][0].lower() in seen[i]:
                        count += 1
                if seen[i] == "num":
                    seen[i] = "numbers"
                elif seen[i] == "none":
                    seen[i] = "conjunctions"
                countArray.append(count)
            return countArray

        finalTypeArray = infoPos(typeArray)
        finalLevel = infoPos(level)
        st.write(finalTypeArray)

        alreadySeenLevel = noRep(level)
        st.write("AlreadySeenLevel: ", alreadySeenLevel)
        alreadySeen = noRep(typeArray)
        st.write("AlreadySeen: ", alreadySeen)

        counter = counting(alreadySeen, finalTypeArray)
        st.write("Counter: ", counter)
        counterLevel = counting(alreadySeenLevel, finalLevel)
        st.write("Final level-counter: ", counterLevel)

        #TODO Wortarten und ihre Anzahl im Essay... nicht schön aber funktioniert
        if len(alreadySeen) == 9:
            typeCount = pd.DataFrame(counter, index=[str(alreadySeen[0]), str(alreadySeen[1]), str(alreadySeen[2]),
                                                     str(alreadySeen[3]), str(alreadySeen[4]), str(alreadySeen[5]),
                                                     str(alreadySeen[6]), str(alreadySeen[7]), str(alreadySeen[8])],
                                     columns=['Count'])
        else:
            typeCount = pd.DataFrame(counter, index=[str(alreadySeen[0]), str(alreadySeen[1]), str(alreadySeen[2]),
                                                     str(alreadySeen[3]), str(alreadySeen[4]), str(alreadySeen[5]),
                                                     str(alreadySeen[6]), str(alreadySeen[7])],
                                     columns=['Count'])
        st.write(typeCount)
        st.bar_chart(typeCount)

        fig = go.Figure(
            go.Pie(
                labels=alreadySeenLevel,
                values=counterLevel,
                hoverinfo="label+percent",
                textinfo="value"
            ))
        st.header("Pie chart")
        st.plotly_chart(fig)

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
        finalXmiListRep = infoPos(wordIndexList)
        st.write("Final Xmi: ", finalXmiListRep)

        # in currentType speichere ich alle ausgewählten typen
        #currentPoss = st.radio("Select Type: ", alreadySeen)
        currentType = st.multiselect("Wähle aus welche Worte du markiert haben willst: ", alreadySeen)


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
    score = st.slider("Wie gut ist der Wortschatz?", 0, 6)
    st.button("Weiter")

