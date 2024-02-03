% Define the filter parameters
fs = 48000;          % Sampling frequency
fc = 500;            % Cutoff frequency
fhc= 4000;
fpass = [500 4000];  % Passband frequencies
order = 4;           % Filter order

% To load the sound file
filename = 'audio.wav';
[x, fs_orig] = audioread(filename);

% Calculate the time axis
t = linspace(0, length(x)/fs_orig, length(x));

% Plot the waveform
plot(t, x);
xlabel('Time (s)');
ylabel('Amplitude');

% LOWPASS
% Compute the filter coefficients. butter(n,Wn) returns the transfer function 
% coefficients of an nth-order lowpass digital Butterworth filter with normalized 
% cutoff frequency Wn.
[b, a] = butter(order, fc/(fs/2), 'low');

% Compute the frequency response of the filter. freqz(b,a,n) returns the n-point 
% frequency response vector h and the corresponding angular frequency vector w for 
% the digital filter with transfer function coefficients stored in b and a.
[h, w] = freqz(b, a);

% Plot the magnitude of the frequency response
figure;
plot(w*fs/(2*pi), abs(h));
xlabel('Frequency (Hz)');
ylabel('Magnitude');

% Apply the filter. filter(b,a,x) filters the input data x using a rational transfer 
% function defined by the numerator and denominator coefficients b and a.
y1 = filter(b, a, x);
y2 = filter(b, a, y1);

% Save the filtered sound to a new file
filename_filtered = 'kick.wav';
audiowrite(filename_filtered, y2, fs);



% BANDPASS
% Compute the filter coefficients
[bb, ab] = butter(order, fpass/(fs/2), 'bandpass');

% Compute the frequency response of the filter
[hb, wb] = freqz(bb, ab);

% Plot the magnitude of the frequency response
figure;
plot(wb*fs/(2*pi), abs(hb));
xlabel('Frequency (Hz)');
ylabel('Magnitude');

% Apply the filter
yb1 = filter(bb, ab, x);
yb2 = filter(bb, ab, yb1);

% Save the filtered sound to a new file
filename_filtered = 'piano.wav';
audiowrite(filename_filtered, yb2, fs);



% HIGHPASS
% Compute the filter coefficients
[bh, ah] = butter(order, fhc/(fs/2), 'high');

% Compute the frequency response of the filter
[hh, wh] = freqz(bh, ah);

% Plot the magnitude of the frequency response
figure;
plot(wh*fs/(2*pi), abs(hh));
xlabel('Frequency (Hz)');
ylabel('Magnitude');

% Apply the filter
yh1 = filter(bh, ah, x);
yh2 = filter(bh, ah, yh1);

% Save the filtered sound to a new file
filename_filtered = 'cymbal.wav';
audiowrite(filename_filtered, yh2, fs);
