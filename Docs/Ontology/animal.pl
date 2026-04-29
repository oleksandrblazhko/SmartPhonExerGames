% SWI Prolog
% 
% =========================
% FACTS
% =========================

eats(wolf, meat).
eats(hare, plant).

meat(hare).
plant(grass).

% =========================
% RULES
% =========================

% Rule 3: meat eater → predator
is(X, predator) :-
    eats(X, meat).


% Rule 4: plant eater → herbivore
is(X, herbivore) :-
    eats(X, plant).


% Rule 1: if A is meat and B eats meat → B eats A
eats(B, A) :-
    meat(A),
    eats(B, meat).


% Rule 2: if A is plant and B eats plant → B eats A
eats(B, A) :-
    plant(A),
    eats(B, plant).