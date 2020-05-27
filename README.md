# Paradigma
Paradigma für das FoPra

---------------------Stimuli-------------------------------

- 440 Day1 (je nach Subject Number die eine oder andere Hälfte als Targets)
- 4 Distractors Day1 (Tests am Ende der Blocks)
- 1 Distractor Day2 (Die müssen natürlich noch aufgefüllt werden, hatte aber keine weiteren Bilder)

-------------------Ablauf------------------

Probanden sehen eine Abfolge von Bildern, die sie sich einprägen sollen. Nach jedem Block müssen sie für ein in diesem Block gesehendes und ein neues Bild entscheiden, ob das Bild neu ist oder aus dem gerade betrachteten Block stammt. Einen Tag später wird eine Hälfte dieser Bilder erneut gezeigt, mit ebenso vielen Fillern. Hier muss entschieden werden, ob ein Bild alt oder neu ist und ein Remember-/Know-Judgement abgegeben werden. Danach soll per Selection Rectangle markiert werden, welcher Bildbereich zur Erinnerung geführt hat (Wenn das Bild für ein bereits gesehendes gehalten wird). Dann gibt es Feedback über die alt-/neu-Entscheidung.

- Day1: Enkodierung. Ausbalanciert, welche Hälfte der Bilder Targets ist nach Subject Number. Außderdem ausbalacniert nach high/low memo. Bilder, die für den Test am Ende jedes Blocks genutzt wurden, werden im Output entsprechend markiert.

- Day2: Abfrage new/old, Abfrage remember/know, selection rectangle

-----------------Was muss eingestellt werden?---------------------------------

Alle Variablen befinden sich unter den import statements der Dateien "Day1.py" und Day2.py"

#Day 1:
- image_test (Liste mit ZIffern der Durchgänge, bei denen ein Block beginnt)
- block_size (Wie viele Bilder befinden sich in einem Block)
- col_tested (In welcher Spaltennummer befindet sich im Output die Info, ob ein Bild am Ende eines Blocks getestet ´´d wurde (Muss angepasst werden, sollte die Struktur des Outputfiles verändert werden)
- fixation_time (Dauer des Fixationskreuzes)
- presentation_time (Dauer der Bildpräsentation)

#Day 2:
- fixation_time (Dauer des Fixationskreuzes)
- presentation_time (Dauer der Bildpräsentation)
- rounds (Anzahl Durchläufe, also Bildpräsentationen)
