# https://github.com/jruizgit/rules

from durable.lang import *

# -------------------------
# WORKING MEMORY HELPERS
# -------------------------
derived = set()


def add_derived(s, p, o):
    fact = (s, p, o)
    if fact not in derived:
        derived.add(fact)
        print("DERIVED:", fact)


# -------------------------
# RULESET
# -------------------------
with ruleset('knowledge'):

    # -------------------------
    # RULE 3:
    # A eats Meat → A is Predator
    # -------------------------
    @when_all((m.predicate == 'eats') & (m.object == 'Meat'))
    def predator(c):
        add_derived(c.m.subject, 'is', 'Predator')


    # -------------------------
    # RULE 4:
    # A eats Plant → A is Herbivore
    # -------------------------
    @when_all((m.predicate == 'eats') & (m.object == 'Plant'))
    def herbivore(c):
        add_derived(c.m.subject, 'is', 'Herbivore')


    # -------------------------
    # RULE 1:
    # A is Meat AND B eats Meat → B eats A
    # -------------------------
    @when_all(
        c.meat << (m.predicate == 'is') & (m.object == 'Meat'),
        c.eats << (m.predicate == 'eats') & (m.object == 'Meat')
    )
    def meat_chain(c):
        a = c.meat.subject
        b = c.eats.subject
        add_derived(b, 'eats', a)


    # -------------------------
    # RULE 2:
    # A is Plant AND B eats Plant → B eats A
    # -------------------------
    @when_all(
        c.plant << (m.predicate == 'is') & (m.object == 'Plant'),
        c.eats << (m.predicate == 'eats') & (m.object == 'Plant')
    )
    def plant_chain(c):
        a = c.plant.subject
        b = c.eats.subject
        add_derived(b, 'eats', a)


# -------------------------
# INITIAL FACTS
# -------------------------
def assert_fact(s, p, o):
    post('knowledge', {
        'subject': s,
        'predicate': p,
        'object': o
    })


# Факти з задачі
assert_fact('Wolf', 'eats', 'Meat')
assert_fact('Hare', 'eats', 'Plant')
assert_fact('Hare', 'is', 'Meat')
assert_fact('Grass', 'is', 'Plant')