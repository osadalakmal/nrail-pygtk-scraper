nrail-pygtk-scraper
===================

Python GTK application that scrapes the national rail website 

This was written mostly because I was unsatisfied with the user interface that national rail site provided.
For my uses it was too simplistic. I for example wanted to specifically buy tickets that went from *A->B* and *B->C*
and not just using via. Also if it was possible I wanted to compare *A->D->C* journey to above as well. But also be
aware that this was mostly written as an excercise in using python and should be treated as such. The code is 
amteuarish to say the least.

It uses the httpparser module from python libraries for parsing the web page. The UI is written using [PyGTK] (http://en.wikipedia.org/wiki/PyGTK). 
I considered several options for writing the GUI and settled on PyGTK. Funnily enough it was mostly because it was
already installed and required no downloads. But more seriously it seems comparable to the more flashy 
[PyQT] (http://en.wikipedia.org/wiki/PyQt) and [PySide] (http://en.wikipedia.org/wiki/PySide) (the offshoot from 
Nokia's QT team) in terms of the features. But seemed much simpler. Also I have had some run ins with the 
Gnome library and was somewhat comfortable with it. (The last time I tried porting Qt however was a completely 
different story)

The usage is pretty simple for now. Same controls present in the web page is there. You select the From, To, 
the date and the time of departure of arrival and it will list all options and highlight the best possible price.

TODO
----

 * Imeplement the *A->B->C* station feature
 * Add a way to compare across days
 * Add graphing to show the way prices vary on time and across days