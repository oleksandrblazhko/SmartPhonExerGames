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

% 1. GAME MECHANICS (Mc)
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

% template, uses

template(soccer_heading,t101).
uses(t101,match).
uses(t101,avoid).

template(ski_slalom,t102).
uses(t102,move).
uses(t102,avoid).

template(fruit_slicer,t201).
uses(t201,destroy).
uses(t201,avoid).

template(crazy_snowboard,t301).
uses(t301,move).
uses(t301,manage).
uses(t301,create).



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

