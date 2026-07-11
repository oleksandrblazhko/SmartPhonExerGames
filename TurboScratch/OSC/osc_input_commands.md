На сьогодні офіційна документація не містить опису кожної окремої команди /input/.... Вона лише вказує, що:

/input/<input_name> — Simulate game inputs like jump, move, etc.

Але ми можемо достовірно встановити призначення багатьох команд, зіставивши їх з офіційною документацією керування клавіатурою та контролерами:
https://docs.chilloutvr.net/chilloutvr/controls/mouse-and-keyboard

Команди, призначення яких підтверджено
OSC команда	Призначення	Підтвердження
/input/Jump	Стрибок	Space = Jump
/input/Run	Біг (утримання)	Left Shift = Run
/input/Crouch	Присідання	C = Crouch
/input/Prone	Лежачи	X = Prone
/input/Voice	Push-to-Talk / Voice Toggle	V = Voice
/input/ToggleFlightMode	Перемикання режиму польоту	Num5 = Flight Mode
/input/Respawn	Респавн	Назва однозначна, використовується механіка Respawn у грі
/input/QuitGame	Вихід із гри	Назва однозначна
/input/ToggleHUD	Показати/сховати HUD	Назва однозначна
/input/ToggleCamera	Перемикання внутрішньої камери	Назва однозначна
/input/ToggleSeated	Перемикання режиму сидячи	Назва однозначна


Команди, призначення яких дуже ймовірне, але документація не описує їх окремо.
Є припущення - https://docs.chilloutvr.net/cck/avatar/animator-core-parameters

Команда	Найімовірніше значення
/input/MoveForward	Рух вперед
/input/MoveBackward	Рух назад
/input/MoveLeft	Рух ліворуч
/input/MoveRight	Рух праворуч
/input/LookLeft	Поворот погляду ліворуч
/input/LookRight	Поворот погляду праворуч
/input/Horizontal	Горизонтальна вісь руху
/input/Vertical	Вертикальна вісь руху
/input/LookHorizontal	Горизонтальна вісь огляду
/input/LookVertical	Вертикальна вісь огляду
/input/GripLeftValue	Аналогове значення стискання лівого контролера
/input/GripRightValue	Аналогове значення стискання правого контролера
/input/GrabLeft	Захопити предмет лівою рукою
/input/GrabRight	Захопити предмет правою рукою
/input/DropLeft	Відпустити предмет лівою рукою
/input/DropRight	Відпустити предмет правою рукою
/input/UseLeft	Використати предмет лівою рукою
/input/UseRight	Використати предмет правою рукою
/input/GestureLeft	Жест лівої руки
/input/GestureRight	Жест правої руки
/input/Emote	Відтворити емоцію
/input/Toggle	Перемикання одного з avatar toggle

Ці назви добре узгоджуються з офіційними параметрами аніматора (GestureLeft, GestureRight, MovementX, MovementY, Toggle, Emote), але документація не стверджує, що OSC-команди працюють саме так.

Але щодо питання "що робить кожна команда" — поки що OSCQuery відповів лише на частину:

назву;
тип (T, f, i);
поточне значення;
доступ (ACCESS=2, що відповідає запису / write-only за специфікацією OSCQuery).

Описів (DESCRIPTION) для окремих команд сервер не надає.

Що ми можемо встановити достовірно
Типи даних

З отриманих даних видно:

T — булевий вхід (натиснути / відпустити).
f — число з плаваючою комою (аналогова вісь).
i — ціле число (індекс або номер).

Це вже дозволяє зробити кілька надійних висновків.

Наприклад:

Команда	Тип	Достовірний висновок
Horizontal	float	аналогова вісь
Vertical	float	аналогова вісь
LookHorizontal	float	аналогова вісь
LookVertical	float	аналогова вісь
GripLeftValue	float	аналогове значення
GripRightValue	float	аналогове значення
GestureLeft	float	аналогове значення
GestureRight	float	аналогове значення
Emote	int	вибір номера емоції
Toggle	int	вибір номера toggle

Це випливає безпосередньо з типів, а не з припущень.

1. Horizontal ↔ MovementX

OSC:

/input/Horizontal

Тип:

float [-1..1]

У документації CCK існує параметр

MovementX

з описом

Horizontal movement input value.

Отже можна практично впевнено стверджувати

OSC	Animator
Horizontal	MovementX
2. Vertical ↔ MovementY

OSC

/input/Vertical

CCK

MovementY

Опис:

Vertical movement input value.

3. LookHorizontal

CCK має

Input Look X

з діапазоном

[-1..1]

і описом

Horizontal look input.

Практично напевно

/input/LookHorizontal

є OSC-аналогом цього входу.

4. LookVertical

Аналогічно

Input Look Y

5. GripLeftValue

У CCK існує

Grip Left Value

діапазон

0..1

6. GripRightValue

Повністю збігається

Grip Right Value

7. Jump

Є

Input Jump

Тип

Bool

Опис

Jump input.

8. GestureLeft

У Core Parameters

GestureLeft

діапазон

-1 … 6

опис

Current gesture state of the left hand.

9. GestureRight

Повністю аналогічно.

10. Emote

Core Parameters

Emote

опис

Target emote to play.

11. Toggle

Core Parameters

Toggle

опис

Currently selected toggle state.
