"""
Exergame PyReason System
- Fact generation from E = G×P×A×M×B×Q
- Rule-based inference (Rule 1–11)
- Game mechanics + template + adaptation layer
"""

import itertools
import pyreason as pr


# =========================================================
# 1. ONTOLOGY (YOUR MODEL E = G×P×A×M×B×Q)
# =========================================================

G = ["balance", "strength", "cardio", "coordination", "flexibility", "rehabilitation"]

P = ["standing", "oneleg", "plank", "sitting", "kneeling", "supine", "prone", "side"]

A = ["core", "lower", "upper", "fullbody", "ankle", "knee", "hip", "spine", "shoulder"]

M = ["static", "tilt", "rotation", "shift", "step", "jump", "ballistic", "strength"]

B = ["rocker", "wobble", "sphere", "pivot", "roller", "sensor"]

Q = ["none", "ball", "band", "dumbbell"]


# =========================================================
# 2. FACT GENERATOR
# =========================================================

def add_fact(ex_id, attr, value):
    pr.add_fact(pr.Fact(
        name=f"{attr}_{ex_id}",
        component=ex_id,
        attribute=value,
        bound=[1, 1],
        start_time=0,
        end_time=100
    ))


def generate_facts(ex_id, g, p, a, m, b, q):
    add_fact(ex_id, "goal", g)
    add_fact(ex_id, "posture", p)
    add_fact(ex_id, "anatomy", a)
    add_fact(ex_id, "movement", m)
    add_fact(ex_id, "board", b)
    add_fact(ex_id, "equipment", q)


# =========================================================
# 3. DERIVED CLASSIFICATION FACTS
# =========================================================

def add_derived_facts(ex_id, success_rate, fatigue):

    if success_rate < 0.6:
        add_fact(ex_id, "success", "low_success")

    if success_rate > 0.85:
        add_fact(ex_id, "success", "high_success")

    if fatigue == "high":
        add_fact(ex_id, "fatigue", "high_fatigue")


# =========================================================
# 4. RULES MODULE (Rule 1–11)
# =========================================================

def load_rules():

    # -------------------------
    # EXERCISE → MECHANICS
    # -------------------------

    pr.add_rule(pr.Rule(
        'Move(x) <- goal_balance(x), posture_standing(x), movement_tilt(x)',
        'r1_move'
    ))

    pr.add_rule(pr.Rule(
        'Avoid(x) <- goal_balance(x), posture_standing(x), movement_tilt(x)',
        'r1_avoid'
    ))

    pr.add_rule(pr.Rule(
        'Random(x) <- posture_oneleg(x)',
        'r2_random'
    ))

    pr.add_rule(pr.Rule(
        'Match(x) <- posture_plank(x), anatomy_core(x)',
        'r3_match'
    ))

    pr.add_rule(pr.Rule(
        'Select(x) <- goal_coordination(x), equipment_ball(x)',
        'r4_select'
    ))

    pr.add_rule(pr.Rule(
        'Shoot(x) <- goal_coordination(x), equipment_ball(x)',
        'r4_shoot'
    ))

    # -------------------------
    # TEMPLATE SELECTION
    # -------------------------

    pr.add_rule(pr.Rule(
        'EndlessRunner(x) <- Move(x), Avoid(x)',
        'r8_runner'
    ))

    pr.add_rule(pr.Rule(
        'PuzzleGame(x) <- Match(x), Select(x)',
        'r9_puzzle'
    ))

    pr.add_rule(pr.Rule(
        'FitnessManager(x) <- strength(x)',
        'r10_fitness'
    ))

    # -------------------------
    # ADAPTATION LAYER
    # -------------------------

    pr.add_rule(pr.Rule(
        'decrease_speed(x) <- low_success(x)',
        'r5_speed_down'
    ))

    pr.add_rule(pr.Rule(
        'increase_speed(x) <- high_success(x)',
        'r6_speed_up'
    ))

    pr.add_rule(pr.Rule(
        'decrease_size(x) <- high_success(x)',
        'r6_size_down'
    ))

    pr.add_rule(pr.Rule(
        'decrease_frequency(x) <- high_fatigue(x)',
        'r7_freq_down'
    ))

    pr.add_rule(pr.Rule(
        'increase_size(x) <- high_fatigue(x)',
        'r7_size_up'
    ))


# =========================================================
# 5. SINGLE EXERCISE PIPELINE
# =========================================================

def process_exercise(ex_id, g, p, a, m, b, q,
                     success_rate=0.7,
                     fatigue="low"):

    # 1. Base facts
    generate_facts(ex_id, g, p, a, m, b, q)

    # 2. Derived facts (performance layer)
    add_derived_facts(ex_id, success_rate, fatigue)

    # 3. Run inference
    pr.run()

    return ex_id


# =========================================================
# 6. EXAMPLE RUN
# =========================================================

if __name__ == "__main__":

    # Load rules once
    load_rules()

    # Example exercise
    ex = process_exercise(
        ex_id="ex_001",
        g="balance",
        p="standing",
        a="core",
        m="tilt",
        b="wobble",
        q="none",
        success_rate=0.55,
        fatigue="low"
    )

    print("Processed:", ex)