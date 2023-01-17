clear all
a=[1 -0.75];
b=[1 0.5];
figure(1)
zplane(b,a)
title('y[n]-0.75[n-1]=x[n]+0.5x[n-1]')

fs=400;
td=2;
N=td*fs;
t=(0:N)/fs;
x=2*sin(40*pi*t);
filt=filter(b,a,x);
figure(2);
plot(t,x,'b')
hold on;
plot(t,filt,'r')
title('filter function')
legend({'original','filtered'})


fs1=400;
td1=5;
N1=td1*fs1;
t1=(0:N1)/fs1;
x1=5*sin(50*pi*t1)+2*sin(200*pi*t1);
a=[1];
b=[0.25 0.25 0.25 0.25];
ft1=filter(b,a,x1);
x2=double(x1);
ft2=filtfilt(b,a,x2);
figure(3);
subplot(2,1,1);
plot(t1,x1,'b')
hold on;
plot(t1,ft1,'r')
title('filter function')
legend({'original','filtered'})
subplot(2,1,2)
plot(t1,x1,'b')
hold on;
plot(t1,ft2,'r')
title('filtfilt no phase shift')
legend({'original','filtered'})

load('BME470_Data_Exercise6.mat')
Signal=Signal.';
N=length(Signal);
t=(0:N-1)/(N/5);
a=[1];
b=[0.25 0.25 0.25 0.25];
ft1=filter(b,a,Signal);
Signal2=double(Signal);
ft2=filtfilt(b,a,Signal2);
figure(4);
subplot(2,1,1);
plot(t,Signal,'b')
hold on;
plot(t,ft1,'r')
title('filter function')
legend({'original','filtered'})
subplot(2,1,2);
plot(t,Signal,'b')
hold on;
plot(t,ft2,'r')
title('filtfilt no phase shift')
legend({'original','filtered'})

