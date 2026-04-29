/* Для формалізації бази даних фактів продукційної моделі знань, 
які стосуються фізичних вправ, 
введено множини допустимих значень атрибутів: 
G - множина терапевтичних цілей, 
P - множина положень тіла, 
A - множина анатомічних зон, 
M - множина типів рухів, 
B - множина типів балансуючих дошок, 
Q - множина додаткового обладнання.
*/

% GOALS (G)
goal(balance).
goal(strength).
goal(cardio).
goal(coordination).
goal(flexibility).
goal(proprioception).
goal(rehabilitation).

% BODY POSITIONS (P)
position(standing).
position(oneleg).
position(plank).
position(sitting).
position(kneeling).
position(supine).
position(prone).
position(side).

% ANATOMICAL AREAS (A)
area(core).
area(lower).
area(upper).
area(fullbody).
area(ankle).
area(knee).
area(hip).
area(spine).
area(shoulder).

% MOVEMENT TYPES (M)
movement(static).
movement(tilt).
movement(rotation).
movement(shift).
movement(step).
movement(jump).
movement(ballistic).
movement(strength).

% BOARD TYPES (B)
board(rocker).
board(wobble).
board(sphere).
board(pivot).
board(roller).
board(sensor).

% EQUIPMENT (Q)
equipment(none).
equipment(ball).
equipment(band).
equipment(dumbbell).

% exercise(G, P, A, M, B, Q)
exercise(coordination, standing, fullbody, tilt, sensor, none).        % Soccer Heading
exercise(balance, standing, lower, tilt, sensor, none).                % Ski Slalom
exercise(proprioception, standing, core, tilt, sensor, none).          % Table Tilt
exercise(balance, standing, lower, strength, sensor, none).            % Ski Jump
exercise(coordination, standing, lower, step, sensor, none).           % Tightrope Walk
exercise(proprioception, standing, core, tilt, sensor, none).          % Balance Bubble
exercise(coordination, standing, core, shift, sensor, none).           % Penguin Slide
exercise(balance, standing, lower, tilt, sensor, none).                % Snowboard Slalom
exercise(balance, sitting, core, static, sensor, none).                % Lotus Focus
exercise(coordination, standing, core, tilt, sensor, none).            % Perfect 10
exercise(coordination, standing, fullbody, step, sensor, none).        % Rhythm Kung Fu
exercise(coordination, standing, fullbody, move, sensor, none).        % Bulls-Eye
exercise(coordination, standing, fullbody, shoot, sensor, none).       % Snowball Fight
exercise(cardio, standing, fullbody, step, sensor, none).              % Obstacle Course
exercise(balance, standing, core, tilt, sensor, none).                 % Tilt City
exercise(strength, standing, lower, strength, sensor, none).           % Trampoline Target
exercise(strength, sitting, core, static, sensor, none).               % Core Luge
exercise(coordination, standing, fullbody, shoot, sensor, gamepad).    % Hosedown
exercise(balance, standing, lower, manage, sensor, gamepad).           % Dessert Course
exercise(balance, standing, fullbody, create, sensor, none).           % Skateboard Arena
exercise(strength, plank, core, tilt, rocker, none).                   % Fruit Slicer
exercise(strength, plank, core, move, rocker, none).                   % Hopper
exercise(strength, plank, core, move, rocker, none).                   % Stix & Stones
exercise(strength, plank, core, shoot, rocker, none).                 % Meteor Madness
exercise(strength, plank, core, manage, rocker, none).                % Candy Monster
exercise(strength, plank, core, shoot, rocker, none).                 % Duck Shoot
exercise(strength, plank, core, move, rocker, none).                  % Snow Cruisin
exercise(strength, plank, core, match, rocker, none).                 % Pong Goal
exercise(strength, plank, core, move, rocker, none).                  % Wave Rider
exercise(strength, plank, core, match, rocker, none).                 % Gift Rush
exercise(balance, standing, core, move, wobble, none).               % Crazy Snowboard
exercise(balance, standing, core, move, wobble, none).               % Color Tunnel
exercise(proprioception, standing, core, move, wobble, none).        % Space Ball
exercise(balance, standing, lower, manage, wobble, none).            % Car
exercise(proprioception, standing, core, move, wobble, none).        % Mini Golf
exercise(proprioception, standing, core, move, wobble, none).        % Maze
exercise(balance, standing, lower, move, wobble, none).              % Fall Down
exercise(balance, standing, lower, manage, wobble, none).            % Candy Rex
exercise(balance, standing, lower, destroy, wobble, none).           % Ice Adventure
exercise(balance, standing, lower, manage, wobble, none).            % Submarine
exercise(balance, standing, lower, manage, wobble, none).            % Harvest Rush
exercise(coordination, standing, lower, avoid, wobble, none).       % Tetromino

/* Для формалізації бази даних фактів продукційної моделі знань, 
які стосуються комп’ютерних ігор, 
введено множини допустимих значень атрибутів: 
- Tm – шаблон механіки гри в моделі GamePlay-Bricks, я
як комбінація типів механік { Create, Destroy, Avoid, Match, Move, Select, Write, Random, Shoot, Manage }
- D – множина динамічних властивостей гри.
*/


/* =========================================
   GAME MECHANIC TYPES (Mc)
========================================= */

mechanic(create).
mechanic(destroy).
mechanic(avoid).
mechanic(match).
mechanic(move).
mechanic(select).
mechanic(write).
mechanic(random).
mechanic(shoot).
mechanic(manage).


/* =========================================
   GAME MECHANIC TEMPLATES
   template(TemplateName, MechanicSet)
========================================= */

% T1: Arcade navigation template
template(t1_move_avoid,
         [move, avoid]).

% T2: Balance / puzzle coordination template
template(t2_move_match,
         [move, match]).

% T3: Cognitive template
template(t3_match_select,
         [match, select]).

% T4: Reactive shooter template
template(t4_shoot_avoid_move,
         [shoot, avoid, move]).

% T5: Control-management template
template(t5_manage_move,
         [manage, move]).

% T6: Destruction-reactive template
template(t6_destroy_shoot_avoid,
         [destroy, shoot, avoid]).

% T7: Pure navigation template
template(t7_move,
         [move]).

% T8: Locomotion template
template(t8_move_step,
         [move, step]).

% T9: Static balance template
template(t9_static_match,
         [match]).

% T10: Complex coordination template
template(t10_move_step_match_select,
         [move, step, match, select]).

% T11: Plank-strength exergame template
template(t11_plank_strength,
         [move, destroy, shoot, match]).

% T12: Hybrid arcade template
template(t12_move_avoid_manage_match,
         [move, avoid, manage, match]).


% USERS
user(user1).
user(user2).
user(user3).

% SUCCESS RATE
rate(low).
rate(avg).
rate(high).

% SPEED DOMAIN
speed(1).
speed(2).
speed(3).
speed(4).
speed(5).

% SIZE DOMAIN
size(1_20).
size(1_15).
size(1_10).
size(1_5).

% Множина динаміки гри
dynamics(Template, Speed, Size).

% Результат гравця
player(User, Template, Rate).

