Intro
=====

I has downloaded a movie, which is divdied into 2 parts (CD1 and CD2). This movie has no subtitile, so I downloaded one, but this time it is a file in whole.

I need to divide this whole subtitle into 2 parts. The CD1 part is easy, I only need to keep the subtitle sections until the end of the CD1 movie. I move the other sections into another file(following named as *CD2.srt*).

This *CD2.srt*'s every subtitle section need to be modified, including the `index` part (should start from 1) and the `time` part (should subtract the end point of CD1 movie).

So I write this script to do me this favor...

Depednecy
========

* Python3
* chardet
