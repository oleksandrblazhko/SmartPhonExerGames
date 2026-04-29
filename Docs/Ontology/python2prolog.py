# https://pyswip.org/
#  pip install pyswip

from pyswip import Prolog

prolog = Prolog()
prolog.consult("animals.pl")

result = list(prolog.query("is(wolf, predator)"))

print(result)

