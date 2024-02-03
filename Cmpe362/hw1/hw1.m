% Let's create intro of fur elise,
% Intro of fur elise is comprised of these notes: E – D# – E – D# – E – B –
% D – C – A
% Frequencies of notes:
% E = 329.63
% D# = 311.13
% B = 246.94
% D = 293.66
% C = 261.63
% A = 220.00

% assume each of the notes will be played for 0.2 seconds
% there are 9 notes in total, which means in total, our wave will be 1.8
% seconds
srate = 44000;
srate2 = 88000;
note_sample = 0:1/srate:0.2;
note_sample2 = 0:1/srate2:0.4;

e_freq = rand(1, 1, 'double')*200+300;
d_freq = rand(1, 1, 'double')*200+300;
d_sharp_freq = rand(1, 1, 'double')*200+300;
b_freq = rand(1, 1, 'double')*200+300;
c_freq = rand(1, 1, 'double')*200+300;
a_freq = rand(1, 1, 'double')*200+300;

amplitude = 0.25;
e_note = amplitude*sin(note_sample * 2 * pi * e_freq);
dsharp_note =  amplitude*sin(note_sample * 2 * pi * d_sharp_freq);

long_e_note = amplitude*sin(note_sample2 * 2 * pi * e_freq);
b_note = amplitude*sin(note_sample2 * 2 * pi * b_freq);
d_note = amplitude*sin(note_sample2 * 2 * pi * d_freq);
c_note = amplitude*sin(note_sample2 * 2 * pi * c_freq);
a_note = amplitude*sin(note_sample2 * 2 * pi * a_freq);

% this is just concatenation
melody = [e_note dsharp_note e_note dsharp_note long_e_note b_note d_note c_note a_note];

plot(melody);

sound(melody, srate)

audiowrite("2020400147.wav", melody, srate);