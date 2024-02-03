im1 = imread("otter.png", "png");

im1 = rgb2gray(im1);

height = size(im1, 1);
width = size(im1, 2);

% Downsample the image to half of its size
new_im = im1(1:2:height,1:2:width);

% Create a version of the image with 4 copies
new_im = [new_im new_im ; new_im new_im];

n = 2;

most_sig = bitsrl(new_im, 8-n); % 8 - n = 6

transmitted_img = bitor(bitand(im1, 256 - power(2,n)), most_sig); % im1 stores 4+1 images

% Student number : 2020400147

corrupted_img = transmitted_img;

rng(1);

for i = 1:30
    corrupted_img(147 + randi(512-147, 1, 1), :) = randi(256 ,1, 512);
end

% imwrite(corrupted_img, "corrupted_img_otter"+n+".png");

least_sig = bitand(corrupted_img, power(2,n)-1);
temp_img = bitsll(least_sig, 8-n);

recovered_img = zeros(width, height, "uint8");
recovered_img(1:2:height, 1:2:width) = temp_img(1:256, 1:256);
recovered_img(2:2:height, 2:2:width) = temp_img(1:256, 1:256);
recovered_img(1:2:height, 2:2:width) = temp_img(1:256, 1:256);
recovered_img(2:2:height, 1:2:width) = temp_img(1:256, 1:256);


imshow(recovered_img);


% First rmse value
E1    = im1-transmitted_img;
SQE1  = E1.^2;
MSE1  = mean(SQE1(:));
RMSE1 = sqrt(MSE1);

% Second rmse value
E2    = im1-corrupted_img;
SQE2  = E2.^2;
MSE2  = mean(SQE2(:));
RMSE2 = sqrt(MSE2);

% Third rmse value
E3    = im1-recovered_img;
SQE3  = E3.^2;
MSE3  = mean(SQE3(:));
RMSE3 = sqrt(MSE3);

% imwrite(recovered_img, "recovered_otter"+n+".png");

r1 = [0.7195 1.4727 2.9430 5.5190];
r2 = [2.7877 3.0513 3.9252 5.9847];
r3 = [14.9443 12.8917 9.3601 6.0983];
x = [2 3 4 5];
plot(x,r1) 
hold on 
plot(x,r2)
hold on 
plot(x,r3) 
hold off
