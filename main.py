import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time
import random
import string
import os
from xml.etree import ElementTree as ET


st.title('Bachelorarbeit')
st.write("""*TODO: find better title*""")

#file = st.sidebar.file_uploader("Essays", accept_multiple_files=True)

if 'currentFile' not in st.session_state:
    st.session_state.currentFile = 0
if 'start' not in st.session_state:
    st.session_state.start = 0
if 'startZeit' not in st.session_state:
    st.session_state.startZeit = 0
if 'endZeit' not in st.session_state:
    st.session_state.endZeit = 0
if 'random' not in st.session_state:
    st.session_state.random = ""
if 'essay' not in st.session_state:
    st.session_state.essay = ""
if 'group' not in st.session_state:
    st.session_state.group = ""


def openFile(fileName, inhalt):
    infos = open(r"C:\Users\jan-niklas\OneDrive - Universität Duisburg-Essen\Bachelorarbeit\Streamlit"+"/"+
                 st.session_state.group+"/"+fileName+".txt", "a")
    infos.write(inhalt+"\n")
    infos.close()


if st.session_state.start == 1:
    st.write("""
        # Hello
        Ich habs endlich rausgefunden""")

    #Klauseln zur Einlesung des richtigen Essaysets
    if st.session_state.essay is "a":
        files = os.listdir(r"C:\Users\jan-niklas\OneDrive - Universität Duisburg-Essen\Bachelorarbeit\Streamlit\XMI_Beispiele")
        file = open(
            r"C:\Users\jan-niklas\OneDrive - Universität Duisburg-Essen\Bachelorarbeit\Streamlit\XMI_Beispiele"+"/"+files[st.session_state.currentFile])
    elif st.session_state.essay is "b":
        files = os.listdir(
            r"C:\Users\jan-niklas\OneDrive - Universität Duisburg-Essen\Bachelorarbeit\Streamlit\Testgruppe2")
        file = open(
            r"C:\Users\jan-niklas\OneDrive - Universität Duisburg-Essen\Bachelorarbeit\Streamlit\Testgruppe2" + "/" +
            files[st.session_state.currentFile])
    elif st.session_state.essay is "c":
        files = os.listdir(
            r"C:\Users\jan-niklas\OneDrive - Universität Duisburg-Essen\Bachelorarbeit\Streamlit\Testgruppe3")
        file = open(
            r"C:\Users\jan-niklas\OneDrive - Universität Duisburg-Essen\Bachelorarbeit\Streamlit\Testgruppe3" + "/" +
            files[st.session_state.currentFile])
    #elif st.session_state.essay is "d":
        #files = os.listdir(
            #r"C:\Users\jan-niklas\OneDrive - Universität Duisburg-Essen\Bachelorarbeit\Streamlit\XMI_Beispiele")
        #file = open(
            #r"C:\Users\jan-niklas\OneDrive - Universität Duisburg-Essen\Bachelorarbeit\Streamlit\XMI_Beispiele" + "/" +
            #files[st.session_state.currentFile])
    #elif st.session_state.essay is "e":
        #files = os.listdir(
            #r"C:\Users\jan-niklas\OneDrive - Universität Duisburg-Essen\Bachelorarbeit\Streamlit\XMI_Beispiele")
        #file = open(
           # r"C:\Users\jan-niklas\OneDrive - Universität Duisburg-Essen\Bachelorarbeit\Streamlit\XMI_Beispiele" + "/" +
            #files[st.session_state.currentFile])
    else:
        st.write("Sorry, das wars.")
    #st.write(file)
    if st.session_state.group == "G1":
        numberOfFiles = len(files)
        if numberOfFiles > st.session_state.currentFile:
            st.write(st.session_state.currentFile)

            myf = ET.parse(file)
            root = myf.getroot()
            name = file.name
            #type = file.type

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
            #st.write("posArray: ", posArray)
            #st.write("beginArray: ", beginArray)
            #st.write("level: ", level)

            #pos und tatsächlicher typ sind da drin, mit pos kann man bessser mit den worten matchen, so mein gedanke
            def infoPos(array):
                indexNow = None
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
            #st.write("Sofa: ", splitSofaString)

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

            #st.write("wordIndexList", wordIndexList)
            finalXmiListRep = infoPos(wordIndexList)
            #st.write("Final Xmi: ", finalXmiListRep)

            finalTypeArray = infoPos(typeArray)
            finalLevel = infoPos(level)
            finalLevel.remove(finalLevel[0])

            #st.write(finalTypeArray)
            #st.write("final Level: ", finalLevel)

            #TODO brauch Array mit Level und Wort DONE
            actualIndexLevel = 0
            i = 0
            wordIndexListLevel = []
            while i < len(finalLevel) and actualIndexLevel < len(finalXmiListRep):
                if int(finalLevel[i][1]) is finalXmiListRep[actualIndexLevel][1]:
                    indexNow = str(finalXmiListRep[actualIndexLevel][0])
                    wordIndexListLevel.append([str(finalLevel[i][0]), indexNow])
                    actualIndexLevel += 1
                    i += 1
                else:
                    wordIndexListLevel.append(["undefined", str(finalXmiListRep[actualIndexLevel][0])])
                    actualIndexLevel += 1
            #st.write("LevelWort: ", wordIndexListLevel)

            alreadySeenLevel = noRep(level)
            alreadySeenLevel.append("undefined")
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
            availableColors = ["coral", "chartreuse", "orchid", "gold", "cornflowerblue", "lightseagreen", "mediumpurple"]
            for element in currentType:
                chosenTypes.append(str(element))
                st.write(element+":", availableColors[chosenTypes.index(element)])
                # current max: 6

            if len(chosenTypes) == 0:
                st.write(sofaString)

            # hier fängt der html kram an
            # TODO multiselect marking DONE
            else:
                # stringwithcolors ist der finale string zum anzeigen
                stringWithColors = ""
                if len(chosenTypes) > 7 or len(chosenTypes) == 0:
                    limitReached = "Currently only seven Types can be displayed at the same time!"
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
        if grade:
            openFile(st.session_state.random, "Grade: " + str(grade))
        score = st.slider("Wie gut ist der Wortschatz?", 0, 6)
        if score:
            openFile(st.session_state.random, "Score: " + str(score))
        #openFile(st.session_state.random, str(score))

    else:
        myf = ET.parse(file)
        root = myf.getroot()
        name = file.name
        #type = file.type

        for child in root:
            if child.attrib.get('sofaString') is not None:
                sofaString = child.attrib.get('sofaString')
        st.write(sofaString)

    grade = st.slider("Wähle eine Note", 0, 6)
    if grade:
        openFile(st.session_state.random, "Grade: " + str(grade))
    score = st.slider("Wie gut ist der Wortschatz?", 0, 6)
    if score:
        openFile(st.session_state.random, "Score: " + str(score))

    next = st.button("Weiter")
    if next:
        st.session_state.currentFile += 1
        st.session_state.endZeit = time.time()
        zeit = st.session_state.endZeit - st.session_state.startZeit
        openFile(st.session_state.random, "Zeit: " + str(zeit))
        st.session_state.startZeit = time.time()
        openFile(st.session_state.random, "Essay: " + str(st.session_state.currentFile + 1))
        #st.write(zeit)
        st.experimental_rerun()
        #st.write("weiter")
        #st.write(st.session_state.currentFile)

else:
    st.write("Hinweise, Hinweise, HINWEISE")
    st.session_state.random = ''.join([random.choice(string.ascii_letters
                                    + string.digits) for n in range(16)])

    begin = st.button("Start")
    if begin:
        st.session_state.start = 1
        st.session_state.startZeit = time.time()

        groupSelect = open(
            r"C:\Users\jan-niklas\OneDrive - Universität Duisburg-Essen\Bachelorarbeit\Streamlit" + "/" + "Gruppe.txt",
            "r+")
        # st.write("Group: ", groupSelect.read(1))
        number = int(groupSelect.read(1))
        groupSelect.close()

        groupSelect = open(
            r"C:\Users\jan-niklas\OneDrive - Universität Duisburg-Essen\Bachelorarbeit\Streamlit" + "/" + "Gruppe.txt",
            "w")
        if number % 2 == 0:
            st.session_state.group = "G2"
        else:
            st.session_state.group = "G1"
        groupSelect.write(str(number + 1))
        groupSelect.close()

        openFile(st.session_state.random, "Essay: " + str(st.session_state.currentFile + 1))

        groupSelect = open(
            r"C:\Users\jan-niklas\OneDrive - Universität Duisburg-Essen\Bachelorarbeit\Streamlit" + "/" +
            st.session_state.group + "/" + "Varianten.txt")
        # st.write("Group: ", groupSelect.read(1))
        variante = groupSelect.readline()
        st.write(groupSelect.readline())
        st.write("varianten: ", variante)
        groupSelect.close()
        st.session_state.essay = variante[0]
        variante = variante[1:len(variante)]

        groupSelect = open(
            r"C:\Users\jan-niklas\OneDrive - Universität Duisburg-Essen\Bachelorarbeit\Streamlit" + "/" +
            st.session_state.group + "/" + "Varianten.txt", "w")
        groupSelect.write(variante)
        groupSelect.close()

        st.experimental_rerun()
