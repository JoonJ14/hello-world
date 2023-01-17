% Final Project ­ Photogrammetry 
clear all
% 8 Calibration Points 
% x: left to right 
% y: bottom to top 
% z: height 
x = [5.09; 10.09; 6.08; 11.0; 5.7; 11.25; 7.52; 10.18]; 
y = [2.12; 2.1; 3.52; 3.98; 5.28; 7.61; 8.58; 9.76]; 
z = [1.03; 1.42; 1.56; 2.43; 2.91; 1.05; 1.57; 2.36]; 
calib = [x y z]; 
 
% i. Determine camera parameters for different angles (at least 2 angles) based on local coordinates (x,y) and actual 3D coordinates of calibration markers (at least 6 markers) 
% ii. Calculate the 3­D coordinates of calibration markers using the theoretical method based on camera parameters and determine errors in 3 coordinate 
% >> axes: error (%) = [(calculated 3­D coordinate - actual 3­D coordinate)/ actual 3­D coordinate] *100 ; 
%iii. Determine 3­D coordinates of grid intersection points on the surface of femoral condyles (at least 180 points) using camera parameters. 
 
% Left 
Left = xlsread('Left3');
Leftcalib = xlsread('Left3calibpoints');
 
% Right 
Right = xlsread('Right3');
Rightcalib = xlsread('Right3calibpoints');
 
% Equations from lecture on Photogrammetry 
cmatrix1 = zeros(16,11); 
cmatrix2 = zeros(16,11); 
bvector1 = zeros(16,1); 
bvector2 = zeros(16,1); 
 
for i=1:8
 
   bvector1((2*i-1),1) = Leftcalib(i,6); 
   bvector1((2*i),1) = Leftcalib(i,7); 
   bvector2((2*i-1),1) = Rightcalib(i,6);    
   bvector2((2*i),1) = Rightcalib(i,7); 
   
end 
 
% Left 
for i=1:8
 
   cmatrix1((2*i-1),1)= x(i); 
   cmatrix1((2*i-1),2)= y(i); 
   cmatrix1((2*i-1),3)= z(i); 
   cmatrix1((2*i-1),4)= 1; 
   cmatrix1((2*i-1),9)= ((-1)*Leftcalib(i,6)*x(i)); 
   cmatrix1((2*i-1),10)= ((-1)*Leftcalib(i,6)*y(i)); 
   cmatrix1((2*i-1),11)= ((-1)*Leftcalib(i,6)*z(i)); 
   cmatrix1((2*i),5)= x(i); 
   cmatrix1((2*i),6)= y(i); 
   cmatrix1((2*i),7)= z(i); 
   cmatrix1((2*i),8)= 1; 
   cmatrix1((2*i),9)= ((-1)*Leftcalib(i,7)*x(i)); 
   cmatrix1((2*i),10)= ((-1)*Leftcalib(i,7)*y(i)); 
   cmatrix1((2*i),11)= ((-1)*Leftcalib(i,7)*z(i));  
   
end 
   
   
% Right 
for i=1:8 
 
    cmatrix2((2*i-1),1)= x(i); 
    cmatrix2((2*i-1),2)= y(i); 
    cmatrix2((2*i-1),3)= z(i); 
    cmatrix2((2*i-1),4)= 1; 
    cmatrix2((2*i-1),9)= ((-1)*Rightcalib(i,6)*x(i)); 
    cmatrix2((2*i-1),10)= ((-1)*Rightcalib(i,6)*y(i)); 
    cmatrix2((2*i-1),11)= ((-1)*Rightcalib(i,6)*z(i)); 
    cmatrix2((2*i),5)= x(i); 
    cmatrix2((2*i),6)= y(i); 
    cmatrix2((2*i),7)= z(i); 
    cmatrix2((2*i),8)= 1; 
    cmatrix2((2*i),9)= ((-1)*Rightcalib(i,7)*x(i)); 
    cmatrix2((2*i),10)= ((-1)*Rightcalib(i,7)*y(i));     
    cmatrix2((2*i),11)= ((-1)*Rightcalib(i,7)*z(i)); 
    
end 
 
% Left 
A1 = cmatrix1'*cmatrix1; 
B1 = cmatrix1'*bvector1; 
a1 = inv(A1)*B1;
 
% Right 
A2 = cmatrix2'*cmatrix2; 
B2 = cmatrix2'*bvector2; 
a2 = inv(A2)*B2;
 
b_marker = zeros(4,3); 
d_marker = zeros(4,1); 
xyz_marker = zeros(8,3); 
 
for i=1:8 
 
    d_marker(1,1) = Rightcalib(i,6)-a2(4); 
    d_marker(2,1) = Rightcalib(i,7)-a2(8); 
    d_marker(3,1) = Leftcalib(i,6)-a1(4); 
    d_marker(4,1) = Leftcalib(i,7)-a1(8); 
    
    b_marker(1,1) = a2(1)-a2(9)*Rightcalib(i,6); 
    b_marker(1,2) = a2(2)-a2(10)*Rightcalib(i,6); 
    b_marker(1,3) = a2(3)-a2(11)*Rightcalib(i,6);     
    b_marker(2,1) = a2(5)-a2(9)*Rightcalib(i,7); 
    b_marker(2,2) = a2(6)-a2(10)*Rightcalib(i,7); 
    b_marker(2,3) = a2(7)-a2(11)*Rightcalib(i,7);
    
    b_marker(3,1) = a1(1)-a1(9)*Leftcalib(i,6); 
    b_marker(3,2) = a1(2)-a1(10)*Leftcalib(i,6); 
    b_marker(3,3) = a1(3)-a1(11)*Leftcalib(i,6);     
    b_marker(4,1) = a1(5)-a1(9)*Leftcalib(i,7); 
    b_marker(4,2) = a1(6)-a1(10)*Leftcalib(i,7); 
    b_marker(4,3) = a1(7)-a1(11)*Leftcalib(i,7); 
    
    xyz = (b_marker'*b_marker)^(-1)*(b_marker'*d_marker); 
    xyz_marker(i,1)=xyz(1); 
    xyz_marker(i,2)=xyz(2);    
    xyz_marker(i,3)=xyz(3); 
    
end 
 
% (x,y,z) 3D coordinates for all points 
xyzBone = zeros(length(Left(:,1)),3); 
B_bone = zeros(4,3); 
d_bone = zeros(4,1); 
 
for i=1:length(Left(:,1)) 
 
    d_marker(1,1) = Right(i,6)-a2(4); 
    d_marker(2,1) = Right(i,7)-a2(8); 
    d_marker(3,1) = Left(i,6)-a1(4); 
    d_marker(4,1) = Left(i,7)-a1(8); 
    
    b_marker(1,1) = a2(1)-a2(9)*Right(i,6); 
    b_marker(1,2) = a2(2)-a2(10)*Right(i,6); 
    b_marker(1,3) = a2(3)-a2(11)*Right(i,6);     
    b_marker(2,1) = a2(5)-a2(9)*Right(i,7); 
    b_marker(2,2) = a2(6)-a2(10)*Right(i,7); 
    b_marker(2,3) = a2(7)-a2(11)*Right(i,7); 
    
    b_marker(3,1) = a1(1)-a1(9)*Left(i,6); 
    b_marker(3,2) = a1(2)-a1(10)*Left(i,6); 
    b_marker(3,3) = a1(3)-a1(11)*Left(i,6);     
    b_marker(4,1) = a1(5)-a1(9)*Left(i,7); 
    b_marker(4,2) = a1(6)-a1(10)*Left(i,7); 
    b_marker(4,3) = a1(7)-a1(11)*Left(i,7); 
    
    xyz = (b_marker'*b_marker)^(-1)*(b_marker'*d_marker); 
    xyzBone(i,1)=xyz(1);
    xyzBone(i,2)=xyz(2);    
    xyzBone(i,3)=xyz(3); 
    
end 
 
% Display 3D coordinates xyzBone 
 
% Error calculations 
error = ((xyz_marker-calib)./calib)*100;
xerror = 0; 
yerror = 0; 
zerror = 0; 
 
for i=1:8 
 
    xerror = xerror + abs(error(i,1)); 
    yerror = yerror + abs(error(i,2));     
    zerror = zerror + abs(error(i,3)); 
    
end 


% Plot 
numpts=size(xyzBone);
numpts=numpts(1);
x = xyzBone(1:numpts,1); 
y = xyzBone(1:numpts,2); 
z = xyzBone(1:numpts,3); 
tri = delaunay(x,y); 
trisurf(tri,x,y,z); 
hold on;
plot3(x,y,z,'o');
title('Left3 Right3')
error
xerror
yerror
zerror
