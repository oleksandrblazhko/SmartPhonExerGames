% =========================================================
% RULE-BASED INFERENCE: EXERCISE → GAME TEMPLATE
% Each rule includes:
% - explanation (why rule exists)
% - weight (importance in recommendation scoring)
% =========================================================


% ---------------------------------------------------------
% Balance games
% Explanation: Standing posture + core engagement + unstable platform
% leads to balance-oriented gameplay mechanics.
% Weight: 0.95
% ---------------------------------------------------------
exercise_game_temp(E, balance_game) :-
    exercise(E, standing, core, tilt, sensor, _).


% ---------------------------------------------------------
% Racing games
% Explanation: Step-based movement in standing position corresponds
% to locomotion and racing-style dynamics.
% Weight: 0.75
% ---------------------------------------------------------
exercise_game_temp(E, racing_game) :-
    exercise(E, standing, _, step, _, _).


% ---------------------------------------------------------
% Shooter games
% Explanation: Presence of shoot mechanic implies reaction-based
% targeting gameplay.
% Weight: 0.90
% ---------------------------------------------------------
exercise_game_temp(E, shooter_game) :-
    exercise(E, _, _, shoot, _, _).


% ---------------------------------------------------------
% Arcade / Avoidance games
% Explanation: Combination of movement and avoidance implies
% obstacle-navigation gameplay patterns.
% Weight: 0.85
% ---------------------------------------------------------
exercise_game_temp(E, arcade_game) :-
    exercise(E, _, _, move, _, _),
    exercise(E, _, _, avoid, _, _).


% ---------------------------------------------------------
% Puzzle games
% Explanation: Sitting posture combined with matching mechanics
% indicates cognitive/logic-oriented interaction.
% Weight: 0.70
% ---------------------------------------------------------
exercise_game_temp(E, puzzle_game) :-
    exercise(E, sitting, _, match, _, _).


% ---------------------------------------------------------
% Strength training games
% Explanation: Plank position with strength-oriented movement
% defines core stability and force-based training.
% Weight: 0.92
% ---------------------------------------------------------
exercise_game_temp(E, strength_game) :-
    exercise(E, plank, core, strength, _, _).


% ---------------------------------------------------------
% Coordination games
% Explanation: Full-body standing movement with step + move
% reflects coordination-intensive motor control tasks.
% Weight: 0.80
% ---------------------------------------------------------
exercise_game_temp(E, coordination_game) :-
    exercise(E, standing, fullbody, step, _, _),
    exercise(E, _, _, move, _, _).


% ---------------------------------------------------------
% Rehabilitation games
% Explanation: Slow controlled motion with sensor feedback
% supports rehabilitation and controlled recovery training.
% Weight: 0.88
% ---------------------------------------------------------
exercise_game_temp(E, rehab_game) :-
    exercise(E, _, _, slow, sensor, _).


% ---------------------------------------------------------
% Cardio games
% Explanation: Jumping full-body movements correspond to
% cardiovascular load in gamified training.
% Weight: 0.83
% ---------------------------------------------------------
exercise_game_temp(E, cardio_game) :-
    exercise(E, standing, fullbody, jump, _, _).


% ---------------------------------------------------------
% Precision games
% Explanation: Selection-based mechanics correspond to
% accuracy and decision-control gameplay.
% Weight: 0.65
% ---------------------------------------------------------
exercise_game_temp(E, precision_game) :-
    exercise(E, _, _, select, _, _).