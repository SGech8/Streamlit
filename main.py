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
        levelArray = []

        for child in root:
            if child.attrib.get('sofaString') is not None:
                sofaString = child.attrib.get('sofaString')
                #st.write(sofaString)
            if child.attrib.get('pos') is not None and child.attrib.get('begin') is not None:
                posArray.append(int(child.attrib.get('pos')))
                beginArray.append(int(child.attrib.get('begin')))
                endArray.append(int(child.attrib.get('end')))
                if child.attrib.get('id') is not None:
                    idArray.append(int(child.attrib.get('id')))
            if child.attrib.get('name') is not None and child.attrib.get('begin') is not None:
                typeArray.append([str(child.attrib.get('name')), int(child.attrib.get('begin'))])
                levelArray.append(str(child.attrib.get('level')))
                level.append([str(child.attrib.get('level')), int(child.attrib.get('begin'))])
        st.write("posArray: ", posArray)
        st.write("beginArray: ", beginArray)
        st.write("level: ", level)

        #pos und tatsächlicher typ sind da drin, mit pos kann man bessser mit den worten matchen, so mein gedanke
        def infoPos(array):
            finalArray = []
            for i in array:
                if int(i[1]) in beginArray:
                    indexNow = beginArray.index(i[1])
                    posNow = posArray[indexNow]
                    finalArray.append([str(i[0]), posNow])
                #TODO: Hier stimmt was nicht, warum findet er gewisse worte nicht? Problem umgangen aber sehr gefährlich!
                else:
                    posNow = posArray[indexNow + 1]
                    finalArray.append([str(i[0]), posNow])
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


        splitSofaString = sofaString.split()
        st.write("Sofa: ", splitSofaString)

        actualIndex = 0
        newWord = ""
        pos = 0
        wordIndexList = []
        for word in splitSofaString:
            #TODO: hier ist das problem! ein "a" wird durch index im z.b. Wort "band" gefunden,
            # aber nur beim Wort davor wird verglichen!
            index = sofaString.index(word, actualIndex)
            wordIndexList.append([word, index])
            actualIndex = index + 1
            pos += 1

        st.write("wordIndexList", wordIndexList)
        finalXmiListRep = infoPos(wordIndexList)
        st.write("Final Xmi: ", finalXmiListRep)

        finalTypeArray = infoPos(typeArray)
        finalLevel = infoPos(level)
        finalLevel.remove(finalLevel[0])

        #st.write(finalTypeArray)
        st.write("final Level: ", finalLevel)

        #TODO brauch Array mit Level und Wort DONE
        actualIndexLevel = 0
        i = 0
        wordIndexListLevel = []
        #for i in finalLevel:
        while i < len(finalLevel) and actualIndexLevel < len(finalXmiListRep):
            if int(finalLevel[i][1]) is finalXmiListRep[actualIndexLevel][1]:
                indexNow = str(finalXmiListRep[actualIndexLevel][0])
                wordIndexListLevel.append([str(finalLevel[i][0]), indexNow])
                actualIndexLevel += 1
                i += 1
            else:
                wordIndexListLevel.append(["", str(finalXmiListRep[actualIndexLevel][0])])
                actualIndexLevel += 1
        st.write("LevelWort: ", wordIndexListLevel)

        alreadySeenLevel = noRep(level)
        #st.write("AlreadySeenLevel: ", alreadySeenLevel)
        alreadySeen = noRep(typeArray)
        #st.write("AlreadySeen: ", alreadySeen)

        counter = counting(alreadySeen, finalTypeArray)
        #st.write("Counter: ", counter)
        counterLevel = counting(alreadySeenLevel, finalLevel)
        #st.write("Final level-counter: ", counterLevel)

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
        #st.write(typeCount)
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




        # finalXmiRep ist meine liste mit allen gefundenen typen und benötigten infos drin


        # in currentType speichere ich alle ausgewählten typen
        #currentPoss = st.radio("Select Type: ", alreadySeen)
        currentType = st.multiselect("Wähle aus welche Worte du markiert haben willst: ", alreadySeenLevel,
                                     default=None)
        chosenTypes = []
        for element in currentType:
            st.write(element)
            chosenTypes.append(str(element))
            # current max: 6

        if len(chosenTypes) == 0:
            st.write(sofaString)

        # hier fängt der html kram an
        # TODO multiselect marking DONE
        else:
            st.write("Multiselect marking")
            availableColors = ["coral", "chartreuse", "orchid", "gold", "cornflowerblue", "lightseagreen", "mediumpurple"]
            # stringwithcolors ist der finale string zum anzeigen
            stringWithColors = ""
            if len(chosenTypes) > 6 or len(chosenTypes) == 0:
                limitReached = "Currently only six Types can be displayed at the same time!"
                st.write(limitReached)
            else:
                finalText = ""
                for wordTypePair in wordIndexListLevel:
                    if wordTypePair[0].lower() in chosenTypes:
                        typePosition = chosenTypes.index(str(wordTypePair[0].lower()))
                        #st.write(typePosition)
                        wordTypePair[1] = "<span style=\"background-color: " + availableColors[typePosition] + "\">" + wordTypePair[1] + "</span>"
                        #st.write(wordTypePair)

                    stringWithColors = stringWithColors + " " + wordTypePair[1]

                # und hier die wichtigste Zeile
                st.write(stringWithColors, unsafe_allow_html=True)

    grade = st.slider("Wähle eine Note", 0, 6)
    score = st.slider("Wie gut ist der Wortschatz?", 0, 6)
    st.button("Weiter")

