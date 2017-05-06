lazydots
========
A library and utility to generate vocalized Hebrew from ascii. It's sort
of just a fun demo of what is possible with the ``deromanize`` library
with minimal effort.

This software tries to be smarty-pants, which really means it is
error-prone, so please report bugs!

You can test out a web implementation here_.

.. _here: https://ninjaaron.github.io/lazydots/

.. contents::

replacement table
-----------------

=====  ======  =====  ======  =====  ======
ascii  hebrew  ascii  hebrew  ascii  hebrew
=====  ======  =====  ======  =====  ======
'        א     H        ח     \`       ע
b        ב     ch       ח     p        פ
v        ב     T        ט     f        פ
g        ג     y        י     q        ק
gh       ג     k        כ     r        ר
d        ד     kh       כ     ts       צ
dh       ד     l        ל     S        שׂ
h        ה     m        מ     sh       שׁ
w        ו     n        נ     t        ת
z        ז     s        ס     th       ת
=====  ======  =====  ======  =====  ======

The consonants are pretty straight-forward. As far as BeGaD KeFaT
letters, the program should actually do the right thing most of the time
with dagesh, but if it's giving you a dagesh some place where you don't
want it, you can use an "explicitly aspirated" form. *v* and *f* in the
case of ב and פ respectively, and by adding an *h* to the end of *g*,
*d*, *k* and *t*. The main time you should need this if you need an
aspirated vowel at the beginning of a word, like, if it were following a
conjunctive accent or whatevs.

If you want these two characters separately, you can always separate
them with a single quote, i.e. *t'h* = תְה This goes for other digraphs as
well, like sh and ts.

Inversely, if you're not getting a dagesh where you want it, you can
mark it explicitly with a period. You should never really need to do
this. Geminated consonants and BeGaD KeFaT letters at the beginnings of
will automatically get their dagesh when it is appropriate. Still, if
something goes wonky, you can get what you need (and you will probably
need to tell it about mappiq).

Please report bugs!

vowels

=====  ======  =====  ======
ascii  hebrew  ascii  hebrew
=====  ======  =====  ======
:         ְ     a         ַ
i         ִ     A         ָ
I         ִי    o:        ֳ
i.        ִי    o         ָ
e:        ֱ     O         ֹ
e         ֶ     o.       וֹ
E         ֵ     u         ֻ
e.        ֵי    U        וּ
a:        ֲ     u.       וּ
=====  ======  =====  ======

Other marks

=====  ======
.         ּ
<         ֫
^         ֑
=====  ======

The general idea is that lower-case represents a short vowel, upper case
represents an unmarked long vowel, and a vowel plus a period represents
a marked long vowel. Of course, in the case of /i/ class and /u/ class,
there is no unmarked long form, so the marking can be inferred from the
length (though the form with the period is also valid). Qamats-he,
segol-he, holem-he and anything else indicated with a he' is followed
by an "h"

You should normally only use the ":" to mark vocal schwa. Silent schwa
will automatically be supplied. You don't always have to mark the vocal
schwa either, but you do need it for BeGaD KeFaT letters and other
circumstances where open or closed sylables can affect vocalizations.

The software should automatically add meteg to disambiguate between
qamats qatan and qamats gadol when necessary. The Oleh accent is
available for regularly accented words, and the atnachta for pausal
forms. I may eventually create a mechanism to add the rest of the
cantillation.

Note that the algorithm tries to be tolerant and will attempt to "fix
your mistakes" and may occasionally give you a long when you specified a
short or marked when you specified unmarked based on phonetic
circumstances; i.e., at the end of words where short vowels are
phonetically impossible. This may cause issues if you're trying to
reproduce rare forms that end with qibbuts or hiriq. If this happens,
just stick an extra consonant on the end and delete it once you get the
Hebrew :D

Some special notes about holems and consonantal vavs:

 Whenever the sofware sees *Ow* it will generate the special unicode
 character "holem haser with vav," which should cause holem to float
 above the vav as it does in a properly pointed text. However, not all
 fonts implement this this, and sometimes a holem-vav looks better.
 If you want it to generate the regular holem-vav in this situation use
 *ow* (with lowercase *o*).

 This means it is impossible to write qamats
 qatan in front a consonantal vav, but I don't think such a thing exists
 in the Hebrew language. The only theoretical exception I can come up
 with would be a wayyiqtol form of קוה. (of course, if such a thing does
 exist, I would be very excited to learn of it!). In any case, one
 should be able to make due by writing *wayyA<qAw* and just not telling
 anyone that it's actually a qamats gadol. If you were in a case with a
 qamats qatan preceeding a consonantal vav in a closed sylables that
 wasn't at the end of the word, you might get a meteg... I guess just
 delete it.

Please report bugs!

CLI utility
-----------
``lazydots`` comes with a CLI utility called ``lzd``. You can give
it strings you want to convert as args. If you don't do that, it will
read from stdin. Output is sent to stdout.

.. code:: sh

  $ lzd "lAmAh attAh hitnAhAghtA kmo. nudnIq"
  לָמָה אַתָּה הִתְנָהָגְתָּ כְּמוֹ נֻדְנִיק

Very fancy. I use this in a little script that I bind to a key so I can
select text and have it replaced with Hebrew when I hit the binding:

.. code:: sh

  #!/bin/sh
  sleep .1
  xdotool key --clearmodifiers ctrl+c
  xclip -o -selection clipboard | lzd | xclip -selection clipboard
  xdotool key --clearmodifiers ctrl+v

This works on linux with X11. Details may vary on other systems.

The ``lzd`` command also has one flag: ``-n``/``--normalize``. This will
output the canonical normalized form. At the moment, by default, it
outputs the form that looks the best with my fonts.

Please report bugs!

Library Usage
-------------
You can also use ``lazydots`` as a library for your stupid website or
where ever you want it. I may eventually try to build an IBUS engine
with it (don't hold your breath).

basically, you do this:

.. code:: python

  >>> import lazydots
  >>> lazydots.make_pointy_text("e.zeh TippEsh attAh")
  "אֵיזֶה טִפֵּשׁ אַתָּה"

You can also do ``make_pointy_line`` if you want to go line by line or
``make_pointy`` if you want to go word by word. You can always used
``make_pointy_text``, but it might be ever so slightly more efficient to
use the other functions in certain cases.

Please report bugs!
