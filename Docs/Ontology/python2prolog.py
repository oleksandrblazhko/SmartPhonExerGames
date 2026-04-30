# https://pyswip.org/
#  pip install pyswip

from pyswip import Prolog

prolog = Prolog()
prolog.consult("animal.pl")

result = list(prolog.query("eats(wolf,hare)"))

print(result)

