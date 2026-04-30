# https://pyswip.org/
#  pip install pyswip

from pyswip import Prolog

prolog = Prolog()
prolog.consult("animal.pl")

print(list(prolog.query("eats(wolf,X)")))



