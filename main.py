import streamlit as st
import plotly.graph_objects as go
import time
import random
import string
import os
from xml.etree import ElementTree as ET



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


#Hier den richtigen Pfad einfügen
pfad = r"C:\Users\jan-niklas\OneDrive - Universität Duisburg-Essen\Bachelorarbeit\Streamlit"

promtAD = "**Do you agree or disagree with the following statement?**\n\n**Television advertising directed toward young " \
          "children (aged two to five) should not be allowed.**\n\n**Use specific reasons and examples to support your answer.**"

promtTE ="**Do you agree or disagree with the following statement?**\n\n**A teacher’s ability to relate well with students is " \
         "more important than excellent knowledge of the subject being taught.**\n\n**Use specific reasons and examples to " \
         "support your answer.**"

theme = open(pfad+"/"+".streamlit"+"/"+"config.toml", "w")
theme.write('[theme]\n'+
            'base="light"')
theme.close()

def openFile(fileName, inhalt):
    infos = open(pfad+"/"+st.session_state.group+"/"+fileName+".txt", "a")
    infos.write(inhalt+"\n")
    infos.close()

#Liste mit allen Essays der richtigen Gruppe
def anzahlEssays():
    if st.session_state.essay == "a":
        list = os.listdir(pfad+"/"+"Testgruppe1")
    elif st.session_state.essay == "b":
        list = os.listdir(pfad+"/"+"Testgruppe2")
    elif st.session_state.essay == "c":
        list = os.listdir(pfad+"/"+"Testgruppe3")
    elif st.session_state.essay == "d":
        list = os.listdir(pfad+"/"+"Testgruppe4")
    elif st.session_state.essay == "e":
        list = os.listdir(pfad+"/"+"Testgruppe5")
    return list

    # Klauseln zur Einlesung des richtigen Essaysets
def einlesen(files):
    if st.session_state.essay == "a":
        f = open(pfad+"/"+"Testgruppe1"+"/"+files[st.session_state.currentFile])
    elif st.session_state.essay == "b":
        f = open(pfad+"/"+"Testgruppe2"+"/"+files[st.session_state.currentFile])
    elif st.session_state.essay == "c":
        f = open(pfad+"/"+"Testgruppe3"+"/"+files[st.session_state.currentFile])
    elif st.session_state.essay == "d":
        f = open(pfad+"/"+"Testgruppe4"+"/"+files[st.session_state.currentFile])
    elif st.session_state.essay == "e":
        f = open(pfad+"/"+"Testgruppe5"+"/"+files[st.session_state.currentFile])
    return f


if st.session_state.start == 1:
    #st.header("Test für push")
    # TODO: hier noch anpasen wegen Anzahl der Dateien!
    numberOfFiles = len(anzahlEssays())
    #st.write(file)
    if st.session_state.group == "G1":
        if numberOfFiles > st.session_state.currentFile:
            st.title("Essay " + str(st.session_state.currentFile + 1))
            st.caption("Bitte lesen Sie sich das Essay durch und bewerten Sie es, wie Sie es gewohnt sind. Danach tragen Sie eine Bewertung hinsichtlich der Kompetenz für den Text und  für den Wortschatz ein (Sehr hohe - stark ungenügende Kompetenz). Wenn Sie fertig sind, drücken Sie auf den Button 'Weiter'. Nutzen Sie alle zur Verfügung gestellten Features nach eigenem Belieben.")
            files = anzahlEssays()
            #st.write(files[st.session_state.currentFile])
            file = einlesen(files)
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
                    if x[0].upper() not in finalArray and "KEIN LEVEL" not in finalArray:
                        if x[0].upper() == "NO":
                            finalArray.append("KEIN LEVEL")
                        else:
                            finalArray.append(x[0].upper())
                    elif x[0].upper() not in finalArray and "KEIN LEVEL" in finalArray:
                        if x[0].upper() != "NO":
                            finalArray.append(x[0].upper())
                finalArray.remove(finalArray[0])
                return finalArray

            # Anzahl jedes Types bestimmen
            # TODO Methode draus machen DONE
            def counting(seen, array):
                countArray = []
                for i in range(len(seen)):
                    count = 0
                    for x in range(len(array)):
                        if array[x][0].upper() in seen[i]:
                            count += 1
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
                    if str(finalLevel[i][0]) == "No":
                        wordIndexListLevel.append(["KEIN LEVEL", str(finalXmiListRep[actualIndexLevel][0])])
                        actualIndexLevel += 1
                        i += 1
                    else:
                        indexNow = str(finalXmiListRep[actualIndexLevel][0])
                        wordIndexListLevel.append([str(finalLevel[i][0]), indexNow])
                        actualIndexLevel += 1
                        i += 1
                else:
                    if int(finalLevel[i][1]) > int(finalXmiListRep[actualIndexLevel][1]):

                        actualIndexLevel += 1
                    elif int(finalLevel[i][1]) < int(finalXmiListRep[actualIndexLevel][1]):
                        i += 1
                    else:
                        wordIndexListLevel.append(["KEIN LEVEL", str(finalXmiListRep[actualIndexLevel][0])])
            #st.write("LevelWort: ", wordIndexListLevel)

            alreadySeenLevel = noRep(level)
            if "KEIN LEVEL" not in alreadySeenLevel:
                alreadySeenLevel.append("KEIN LEVEL")
            #st.write("AlreadySeenLevel: ", alreadySeenLevel)
            alreadySeen = noRep(typeArray)
            #st.write("AlreadySeen: ", alreadySeen)

            counter = counting(alreadySeen, finalTypeArray)
            #st.write("Counter: ", counter)
            counterLevel = counting(alreadySeenLevel, wordIndexListLevel)
            #st.write("Final level-counter: ", counterLevel)

            col1, col2 = st.columns([1,1.3])
            availableColors = ["coral", "chartreuse", "orchid", "gold", "cornflowerblue", "lightseagreen",
                               "mediumpurple"]

            allLevels = ["A1", "A2", "B1", "B2", "C1", "C2", "KEIN LEVEL"]
            colorAndLevel = []
            i = 0
            for element in availableColors:
                colorAndLevel.append([allLevels[i], element])
                i += 1

            pieColors = []
            for element in alreadySeenLevel:
                for x in colorAndLevel:
                    if x[0] == element:
                        pieColors.append(x[1])
            fig = go.Figure(
                go.Pie(
                    labels=alreadySeenLevel,
                    values=counterLevel,
                    hoverinfo="label+percent",
                    textinfo="value+label",
                ))
            fig.update_traces(marker=dict(colors=pieColors))
            st.subheader("Anzahl der Verwendeten Wörter nach ihrem Sprachniveau")
            st.plotly_chart(fig)

            color = st.radio("Sprachlevel farbig markiert sehen?", ('Ja', 'Nein'), index=1)

            st.subheader("Essay Prompt:")
            if "AD" in files[st.session_state.currentFile]:
                st.write(promtAD)
            if "TE" in files[st.session_state.currentFile]:
                st.write(promtTE)

            if color == 'Nein':
                st.write(sofaString)

            else:
                chosenTypes = []
                for element in alreadySeenLevel:
                    for x in colorAndLevel:
                        if x[0] == element:
                            element = "<span style=\"background-color: " + x[1] + "\">" + element + "</span>"
                    st.write(element, unsafe_allow_html=True)

                # stringwithcolors ist der finale string zum anzeigen
                stringWithColors = ""
                finalText = ""
                for wordTypePair in wordIndexListLevel:
                    if wordTypePair[0].upper() in alreadySeenLevel:
                        typePosition = alreadySeenLevel.index(str(wordTypePair[0].upper()))
                        #st.write(typePosition)
                        wordTypePair[1] = "<span style=\"background-color: " + pieColors[typePosition] + "\">" + wordTypePair[1] + "</span>"
                        #st.write(wordTypePair)

                    stringWithColors = stringWithColors + " " + wordTypePair[1]

                # und hier die wichtigste Zeile
                st.write(stringWithColors, unsafe_allow_html=True)

            grade = st.selectbox("Kompetenzen beim Schreiben:", ("Sehr Hohe", "Hohe", "Mittlere", "Genügende",
                                                                 "Ungenügende", "Stark Ungenügende"))
            if grade:
                openFile(st.session_state.random, "Grade: " + grade)

            score = st.selectbox("Kompetenzen im Wortschatz:", ("Sehr Hohe", "Hohe", "Mittlere", "Genügende",
                                                                 "Ungenügende", "Stark Ungenügende"))
            if score:
                openFile(st.session_state.random, "Score: " + score)
            #openFile(st.session_state.random, str(score))

            next = st.button("Weiter")
            if next:
                st.session_state.currentFile += 1
                st.session_state.endZeit = time.time()
                zeit = st.session_state.endZeit - st.session_state.startZeit
                openFile(st.session_state.random, "Zeit: " + str(zeit))
                st.session_state.startZeit = time.time()
                openFile(st.session_state.random, "Essay: " + str(st.session_state.currentFile + 1))
                # st.write(zeit)
                st.experimental_rerun()
                # st.write("weiter")
                # st.write(st.session_state.currentFile)

        else:
            st.header("Danke fürs Mitmachen.\n"+"\n"+"Falls Sie noch Anmerkungen haben, nutzen Sie bitte das Textfeld unten.\n"+"\n"+"Ansonsten können Sie die Seite jetzt schließen.")
            text = st.text_area("Anmerkungen")
            st.error("Zum Speichern der Anmerkungen drücken Sie bitte nach der Eingabe 'STRG + ENTER'.")
            openFile(st.session_state.random, text)

    else:
        if numberOfFiles > st.session_state.currentFile:
            st.title("Essay " + str(st.session_state.currentFile + 1))
            st.caption("Bitte lesen Sie sich das Essay durch und bewerten Sie es, wie Sie es gewohnt sind. Danach tragen Sie eine Bewertung hinsichtlich der Kompetenz für den Text und  für den Wortschatz ein (Sehr hohe - stark ungenügende Kompetenz). Wenn Sie fertig sind, drücken Sie auf den Button 'Weiter'. Nutzen Sie alle zur Verfügung gestellten Features nach eigenem Belieben.")
            files = anzahlEssays()
            file = einlesen(files)
            myf = ET.parse(file)
            root = myf.getroot()
            name = file.name
            #type = file.type

            st.subheader("Essay Prompt:")
            if "AD" in files[st.session_state.currentFile]:
                st.markdown(promtAD)
            if "TE" in files[st.session_state.currentFile]:
                st.markdown(promtTE)

            for child in root:
                if child.attrib.get('sofaString') is not None:
                    sofaString = child.attrib.get('sofaString')
            st.write(sofaString)

            grade2 = st.selectbox("Kompetenzen beim Schreiben:", ("Sehr Hohe", "Hohe", "Mittlere", "Genügende",
                                                                 "Ungenügende", "Stark Ungenügende"))
            if grade2:
                openFile(st.session_state.random, "Grade: " + grade2)

            score2 = st.selectbox("Kompetenzen im Wortschatz:", ("Sehr Hohe", "Hohe", "Mittlere", "Genügende",
                                                                "Ungenügende", "Stark Ungenügende"))
            if score2:
                openFile(st.session_state.random, "Score: " + score2)

            next = st.button("Weiter")
            if next:
                st.session_state.currentFile += 1
                st.session_state.endZeit = time.time()
                zeit = st.session_state.endZeit - st.session_state.startZeit
                openFile(st.session_state.random, "Zeit: " + str(zeit))
                st.session_state.startZeit = time.time()
                openFile(st.session_state.random, "Essay: " + str(st.session_state.currentFile + 1))
                # st.write(zeit)
                st.experimental_rerun()
                # st.write("weiter")
                # st.write(st.session_state.currentFile)
        else:
            st.header("Danke fürs Mitmachen.\n"+"\n"+"Falls Sie noch Anmerkungen haben, nutzen Sie bitte das Textfeld unten.\n"+"\n"+"Ansonsten können Sie die Seite jetzt schließen.")
            text = st.text_area("Anmerkungen")
            st.error("Zum Speichern der Anmerkungen drücken Sie bitte nach der Eingabe 'STRG + ENTER'.")
            openFile(st.session_state.random, text)

else:
    st.write("Sehr geehrte Proband*innen,\n"+"\n"+"im Folgenden sehen Sie 8 Essays auf Englisch. Diese unterscheiden sich sowohl in ihrem Sprachniveau, als auch in ihrer Thematik. Die Essays wurden von Schülerinnen und Schülern der Oberstufe verfasst.\n"+"\n"+
             "Zudem besteht die Möglichkeit, dass Sie Zusatzinformationen über den Wortschatz des jeweiligen Essays erhalten. Diese können in Form von Diagrammen und farblichen Markierungen gegeben sein. Ob und wie Sie diese Informationen nutzen, ist Ihnen überlassen.\n"+"\n"+
             "Bitte bewerten Sie alle Essays, so wie Sie es gewohnt sind und geben Sie am Ende eine Gesamtnote ab. Für diese Bewertung benutzen Sie bitte die am Ende der Webseite gekennzeichnete Skala von 'Sehr hohe Kompetenzen' bis 'Stark ungenügende Kompetenzen'. Anschließend finden Sie noch eine weitere Skala zur spezifischen Bewertung des Wortschatzes.\n"+"\n"+
             "Wenn Sie die Bewertung für das erste Essay abgeschlossen haben, drücken Sie auf den Button „Weiter“, welcher unten auf der Webseite zu finden ist, um zum nächsten Essay zu gelangen und dieses auf die gleiche Weise zu bearbeiten. Bitte beachte Sie, dass es keine Möglichkeit gibt, zu einem vorherigen Essay zurückzukehren. Schließen Sie daher die Bewertung erst vollständig ab, bevor Sie den Button drücken.\n"+"\n"+
             "Nach Beendigung des letzten Essays haben Sie noch die Möglichkeit Anmerkungen zu hinterlassen. Falls Sie solche haben, können Sie diese eintragen, ich freue mich auf Ihr Feedback.\n"+"\n"+
             "Um mit der Bewertung zu beginnen, geben Sie bitte Ihr Alter und Ihr Geschlecht ein und drücken Sie danach auf den Button 'Start'.\n"+"\n"+
             "Bitte sehen Sie davon ab, die Webseite zu aktualisieren, da dadurch Ihre Daten nur unvollständig gespeichert werden und Sie wieder von vorne anfangen müssten.\n"+"\n"+
             "Ich danke Ihnen für Ihre Teilnahme und wünsche Ihnen viel Spaß.\n"+"\n"+
             "Kontakt: Jan-Niklas Zutt (jan-niklas.zutt@stud.uni-due.de)"
            )
    st.session_state.random = ''.join([random.choice(string.ascii_letters
                                    + string.digits) for n in range(16)])

    alter = st.text_input("Alter")
    geschlecht = st.selectbox("Geschlecht", ('Männlich', 'Weiblich', 'Divers', 'Keine Angabe'))


    begin = st.button("Start")
    if begin:
        st.session_state.start = 1
        st.session_state.startZeit = time.time()

        groupSelect = open(pfad+"/"+"Gruppe.txt", "r")
        # st.write("Group: ", groupSelect.read(1))
        number = int(groupSelect.readline())
        groupSelect.close()

        groupSelect = open(pfad+"/"+"Gruppe.txt", "w")
        if number % 2 == 0:
            st.session_state.group = "G2"
        else:
            st.session_state.group = "G1"
        groupSelect.write(str(number + 1))
        groupSelect.close()

        groupSelect = open(pfad+"/"+st.session_state.group+"/"+"Varianten.txt")
        # st.write("Group: ", groupSelect.read(1))
        variante = groupSelect.read()
        #st.write(groupSelect.readline())
        #st.write("varianten: ", variante)
        groupSelect.close()
        st.session_state.essay = variante[0]
        variante = variante[1:len(variante)]

        groupSelect = open(pfad+"/"+st.session_state.group+"/"+"Varianten.txt", "w")
        groupSelect.write(variante)
        groupSelect.close()

        openFile(st.session_state.random, "Set: " + st.session_state.essay)
        openFile(st.session_state.random, "Gruppe: " + st.session_state.group)
        openFile(st.session_state.random, "Alter: " + alter)
        openFile(st.session_state.random, "Geschlecht: " + geschlecht)
        openFile(st.session_state.random, "Essay: " + str(st.session_state.currentFile + 1))
        st.experimental_rerun()
