# exergame_fact_generator.py

import itertools
import pyreason as pr

# =========================
# 1. ONTOLOGY DEFINITIONS
# =========================

G = ["balance", "strength", "cardio", "coordination", "flexibility", "rehabilitation"]

P = ["standing", "oneleg", "plank", "sitting", "kneeling", "supine", "prone", "side"]

A = ["core", "lower", "upper", "fullbody", "ankle", "knee", "hip", "spine", "shoulder"]

M = ["static", "tilt", "rotation", "shift", "step", "jump", "ballistic", "strength"]

B = ["rocker", "wobble", "sphere", "pivot", "roller", "sensor"]

Q = ["none", "ball", "band", "dumbbell"]


# =========================
# 2. GAME MECHANICS MAP
# =========================

def infer_mechanics(g, p, m, q):
    mechanics = set()

    if g == "balance" and m in ["tilt", "shift"]:
        mechanics.update(["Move", "Avoid"])

    if p == "oneleg":
        mechanics.add("Random")

    if p == "plank":
        mechanics.add("Match")

    if g == "coordination" and q == "ball":
        mechanics.update(["Select", "Shoot"])

    if g == "strength":
        mechanics.add("Manage")

    return list(mechanics)


# =========================
# 3. TEMPLATE INFERENCE
# =========================

def infer_template(mechanics):
    if "Move" in mechanics and "Avoid" in mechanics:
        return "EndlessRunner"

    if "Match" in mechanics and "Select" in mechanics:
        return "PuzzleGame"

    if "Manage" in mechanics:
        return "FitnessManager"

    return "GenericGame"


# =========================
# 4. DYNAMIC ADAPTATION LOGIC
# =========================

def infer_dynamics(success_rate, fatigue_level):
    dyn = {}

    if success_rate < 0.6:
        dyn["speed"] = "decrease"

    if success_rate > 0.85:
        dyn["speed"] = "increase"
        dyn["size"] = "decrease"

    if fatigue_level == "high":
        dyn["frequency"] = "decrease"
        dyn["size"] = "increase"

    return dyn


# =========================
# 5. PYREASON FACT GENERATOR
# =========================

def add_fact(ex_id, attr, value):
    pr.add_fact(pr.Fact(
        name=f"{attr}_{ex_id}",
        component=ex_id,
        attribute=value,
        bound=[1, 1],
        start_time=0,
        end_time=100
    ))


def generate_pyreason_facts(ex_id, g, p, a, m, b, q):
    add_fact(ex_id, "goal", g)
    add_fact(ex_id, "posture", p)
    add_fact(ex_id, "anatomy", a)
    add_fact(ex_id, "movement", m)
    add_fact(ex_id, "board", b)
    add_fact(ex_id, "equipment", q)


# =========================
# 6. FULL PIPELINE (MAIN ENTRY)
# =========================

def process_exercise(ex_id, g, p, a, m, b, q,
                     success_rate=0.7,
                     fatigue_level="low"):

    # Step 1: generate base facts
    generate_pyreason_facts(ex_id, g, p, a, m, b, q)

    # Step 2: derive mechanics
    mechanics = infer_mechanics(g, p, m, q)

    # Step 3: derive template
    template = infer_template(mechanics)

    # Step 4: derive dynamics
    dynamics = infer_dynamics(success_rate, fatigue_level)

    # Step 5: add derived facts to PyReason
    for mech in mechanics:
        add_fact(ex_id, "mechanic", mech)

    add_fact(ex_id, "template", template)

    for k, v in dynamics.items():
        add_fact(ex_id, k, v)

    return {
        "exercise": ex_id,
        "goal": g,
        "posture": p,
        "movement": m,
        "board": b,
        "equipment": q,
        "mechanics": mechanics,
        "template": template,
        "dynamics": dynamics
    }


# =========================
# 7. BATCH GENERATION (optional)
# =========================

def generate_all_exercises(limit=100):
    results = []

    for i, (g, p, a, m, b, q) in enumerate(
        itertools.product(G, P, A, M, B, Q)
    ):
        if i >= limit:
            break

        ex_id = f"ex_{i}"

        res = process_exercise(
            ex_id, g, p, a, m, b, q,
            success_rate=0.7,
            fatigue_level="low"
        )

        results.append(res)

    return results
    
    