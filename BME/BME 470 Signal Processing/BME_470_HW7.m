clear all
%Problem 1
load('MATLAB_EX7_GrazDataset.mat')
Signal=data{1,4}.X;
fs=data{1,1}.fs;
time=10;
fullsig=Signal(:,1)';
y=fullsig(1:fs*time);
N=length(y);
t=(0:N-1)/fs;
a=[1];
b=(1/4)*ones(1,4);

filt1=conv(y,b,'same');

filt2=filtfilt(b,a,y);
figure(1)
subplot(2,1,1)
plot(t,y,'b')
hold on
plot(t,filt1,'r')
title('conv function')
legend({'original','filtered'})
subplot(2,1,2);
plot(t,y,'b')
hold on;
plot(t,filt2,'r')
title('filtfilt function')
legend({'original','filtered'})

%Problem 2 
fs=1000;
n=4;

fc=200;
Wn=fc/(fs/2);%low ('low') and high ('high')
[b,a]=butter(n,Wn,'high');%low ('low') and high ('high')
[h,w]=freqz(b,a);
mag=20*log10(abs(h));
phase=rad2deg(angle(h));
f=(w/(2*pi))*fs;
figure(2)
subplot(2,1,1)
plot(f,mag)
title('High Pass filter at 200Hz IIR magnitude response')
subplot(2,1,2)
plot(f,phase)
title('High Pass filter at 200Hz IIR phase response')

fc=45;
Wn=fc/(fs/2);%low ('low') and high ('high')
[b,a]=butter(n,Wn,'low');%low ('low') and high ('high')
[h,w]=freqz(b,a);
mag=20*log10(abs(h));
phase=rad2deg(angle(h));
f=(w/(2*pi))*fs;
figure(3)
subplot(2,1,1)
plot(f,mag)
title('Low Pass filter at 45Hz IIR magnitude response')
subplot(2,1,2)
plot(f,phase)
title('Low Pass filter at 45Hz IIR phase response')

f1=50;
f2=110;
Wn=[f1/(fs/2) f2/(fs/2)];%bandpass ('bandpass') and bandstop ('stop')
[b,a]=butter(n/2,Wn,'bandpass');%bandpass ('bandpass') and bandstop ('stop')
[h,w]=freqz(b,a);
mag=20*log10(abs(h));
phase=rad2deg(angle(h));
f=(w/(2*pi))*fs;
figure(4)
subplot(2,1,1)
plot(f,mag)
title('Band Pass filter at 50-110Hz IIR magnitude response')
subplot(2,1,2)
plot(f,phase)
title('Band Pass filter at 50-110Hz IIR phase response')


f1=60;
f2=90;
Wn=[f1/(fs/2) f2/(fs/2)];%bandpass ('bandpass') and bandstop ('stop')
[b,a]=butter(n/2,Wn,'stop');%bandpass ('bandpass') and bandstop ('stop')
[h,w]=freqz(b,a);
mag=20*log10(abs(h));
phase=rad2deg(angle(h));
f=(w/(2*pi))*fs;
figure(5)
subplot(2,1,1)
plot(f,mag)
title('Band Stop filter at 60-90Hz IIR magnitude response')
subplot(2,1,2)
plot(f,phase)
title('Band Stop filter at 60-90Hz IIR phase response')


%Problem 3 
fs=1000;
n=100;

fc=150;
Wn=fc/(fs/2);%low ('low') and high ('high')
[b,a]=fir1(n,Wn,'high');%low ('low') and high ('high')
[h,w]=freqz(b,a);
mag=20*log10(abs(h));
phase=rad2deg(angle(h));
f=(w/(2*pi))*fs;
figure(6)
subplot(2,1,1)
plot(f,mag)
title('High Pass filter at 150Hz FIR magnitude response')
subplot(2,1,2)
plot(f,phase)
title('High Pass filter at 150Hz FIR phase response')

fc=80;
Wn=fc/(fs/2);%low ('low') and high ('high')
[b,a]=fir1(n,Wn,'low');%low ('low') and high ('high')
[h,w]=freqz(b,a);
mag=20*log10(abs(h));
phase=rad2deg(angle(h));
f=(w/(2*pi))*fs;
figure(7)
subplot(2,1,1)
plot(f,mag)
title('Low Pass filter at 80Hz FIR magnitude response')
subplot(2,1,2)
plot(f,phase)
title('Low Pass filter at 80Hz FIR phase response')


f1=100;
f2=120;
Wn=[f1/(fs/2) f2/(fs/2)];%bandpass ('bandpass') and bandstop ('stop')
[b,a]=fir1(n/2,Wn,'bandpass');%bandpass ('bandpass') and bandstop ('stop')
[h,w]=freqz(b,a);
mag=20*log10(abs(h));
phase=rad2deg(angle(h));
f=(w/(2*pi))*fs;
figure(8)
subplot(2,1,1)
plot(f,mag)
title('Band Pass filter at 100-120Hz FIR magnitude response')
subplot(2,1,2)
plot(f,phase)
title('Band Pass filter at 100-120Hz FIR phase response')


f1=60;
f2=90;
Wn=[f1/(fs/2) f2/(fs/2)];%bandpass ('bandpass') and bandstop ('stop')
[b,a]=fir1(n/2,Wn,'stop');%bandpass ('bandpass') and bandstop ('stop')
[h,w]=freqz(b,a);
mag=20*log10(abs(h));
phase=rad2deg(angle(h));
f=(w/(2*pi))*fs;
figure(9)
subplot(2,1,1)
plot(f,mag)
title('Band Stop filter at 60-90Hz FIR magnitude response')
subplot(2,1,2)
plot(f,phase)
title('Band Stop filter at 60-90Hz FIR phase response')


