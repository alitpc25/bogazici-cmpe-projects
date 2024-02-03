A = imread('dog.jpg');
B = rgb2gray(A);

%% PART1 - Image Compressing Using FFT
set(gcf, 'Position', [1500 100 size(A,2) size(A,1)])

Bt=fft2(B); % B is grayscale image from above
Blog = log(abs(fftshift(Bt))+1); % put FFT on log-scale
imwrite(mat2gray(Blog), 'log_scale.jpg');
set (gcf, 'Position', [1500 100 size(A,2) size(A,1)])

% FFT
% Zero out all small coefficients and inverse transform 
Btsort = sort(abs(Bt(:))); % Sort by magnitude
counter=1;
for keep= [.99 .10 .05 .002]
    subplot(2,2,counter)
    thresh = Btsort(floor((1-keep)*length(Btsort)));
    ind = abs(Bt)>thresh; % Find small indices
    Atlow = Bt.*ind; % Threshold small indices
    Alow = uint8(ifft2(Atlow)); % Compressed image
    imwrite(Alow, sprintf('compressed_image_fft_%d.jpg', counter)); % Save the compressed image
    title(['', num2str(keep*100), '%'], 'Fontsize', 36)
    counter = counter+1;
end
set(gcf,'Position', [1750 100 1750 2000])


%% PART2 - Image Compressing Using Wavelet

% Wavelet compression
[C,S] = wavedec2(B,4,'db1');
Csort = sort(abs(C(:))); % Sort by magnitude

counter = 1;
for keep = [.99 .10 .05 .002]
    subplot(2, 2, counter)
    thresh = Csort(floor((1-keep)*length(Csort)));
    ind = abs(C)>thresh;
    Cfilt = C.*ind; % Threshold small indices

    % Plot Reconstruction
    Arecon=uint8(waverec2(Cfilt,S,'db1'));
    imwrite(Arecon, sprintf('compressed_image_wavelet_%d.jpg', counter));
    imshow(256-int8(Arecon))
    title(['', num2str(keep*100), '%'], 'Fontsize', 36)
    counter = counter+1;
end
set(gcf,'Position', [1750 100 1750 2000])
