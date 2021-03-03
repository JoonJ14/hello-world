clear all;

% 2D rotation -50 degree
R1=rot2(-50,'deg')
% Verify R is orthonormal 
det(R1)
% ans = 1 

% pose operation
T1=transl2(3,4)
T2=transl2(5,6)*trot2(-30,'deg')

% Use trplot2 to plot 2D poses 
axis([-5 10 -5 10])
axis square
hold on
trplot2(R1,'frame','R1','color','r')
trplot2(T1,'frame','T1','color','b')
trplot2(T2,'frame','T2','color','g')


PA_0=[6.5; 4.3]; % point A with respect to {0}
PB_2=[1.2; -2.7]; % point B with respect to {2}

hold on
% plotting the point just to visually verify if transformation is correct
plot_point(PA_0,'+','color','r')
% Transform point from one frame to another
PA_2=inv(T2)*[PA_0;1]
PA_2=PA_2(1:2)

% Transform point from one frame to another
PB_1=inv(T1)*[PB_2;1]
PB_1=PB_1(1:2)

% PA_2 and PB_2 is now both in reference to frame 2
% Use pythagorean theorem ( (x2-x1)^2 + (y2-y1)^2 )^(1/2)

D_AB=(((PA_2(1)-PB_2(1))^2)+((PA_2(2)-PB_2(2))^2))^0.5

