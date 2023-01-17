clear
figure(1)
subplot(3,1,1)
b=[3 -1];
a=[1 -2];
zplane(b,a)
title('y[n]-2y[n-1]=3x[n]-x[n-1]')

subplot(3,1,2)
b=[0.25 0.25 0.25 0.25];
a=[1];
zplane(b,a)
title('4point moving average filter')

subplot(3,1,3)
b=[0.25 0.65 0.7];
a=[0.3 0.25 0.75];
zplane(b,a)
title('b=[0.25,0.65,0.7], a=[0.3,0.25,0.75]')

figure(2)
subplot(2,1,1)
b=[0 -6283];
a=[1 -0.16];
bode(b,a)

subplot(2,1,2)
b=[0 -6283];
a=[1 -0.16];
zplane(b,a)
