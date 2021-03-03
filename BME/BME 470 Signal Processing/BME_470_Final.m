clear all
load ('BME_470_Final.mat')
move=BME_Final.Move;
rest=BME_Final.Rest;
fs=BME_Final.fs;

N=length(move);
t=(0:N-1)/fs;

figure(1)
subplot(2,1,1);
plot(t,move,'b');
title('move data');
xlabel('time');
ylabel('move signal amplitude'); 
subplot(2,1,2);
plot(t,rest,'b');
title('rest data');
xlabel('time'); 
ylabel('signal amplitude');

f1=30;
f2=70;
n=8;
Wn=[f1/(fs/2) f2/(fs/2)];%bandpass ('bandpass') and bandstop ('stop')
[b,a]=butter(n/2,Wn,'bandpass');%bandpass ('bandpass') and bandstop ('stop')

figure(2);
zplane(b,a);
title('pole-zero plot Band Pass Filter at 30-70Hz IIR');


[h,w]=freqz(b,a);
mag=20*log10(abs(h));
phase=rad2deg(angle(h));
f=(w/(2*pi))*fs;

figure(3);
subplot(2,1,1);
plot(f,mag);
ylim([-200 50]);
title('Band Pass filter at 30-70Hz IIR magnitude response');
xlabel('frequency Hz'); 
ylabel('dB magnitude');
subplot(2,1,2);
plot(f,phase);
title('Band Pass filter at 30-70Hz IIR phase response');
xlabel('frequency Hz'); 
ylabel('degrees');


ft1=filter(b,a,move);
ft2=filter(b,a,rest);
figure(4);
subplot(2,1,1);
plot(t,move,'b');
hold on;
plot(t,ft1,'r');
title('move data');
legend({'original','filtered'});
xlabel('time');
ylabel('signal amplitude'); 
subplot(2,1,2);
plot(t,rest,'b');
hold on;
plot(t,ft2,'r');
title('rest data');
legend({'original','filtered'});
xlabel('time'); 
ylabel('signal amplitude');


[pxx1,f1]=pwelch(ft1,[],[],[],fs);
[pxx2,f2]=pwelch(ft2,[],[],[],fs);
figure(5);
subplot(2,1,1);
plot(f1,pxx1);
title('Power sprectra of filtered move signal');
xlabel('frequency Hz'); 
ylabel('power spectra');
subplot(2,1,2);
plot(f2,pxx2);
title('Power sprectra of filtered rest signal');
xlabel('frequency Hz'); 
ylabel('power spectra');


f1=59;
f2=61;
n=4;
Wn=[f1/(fs/2) f2/(fs/2)];%bandpass ('bandpass') and bandstop ('stop')
[b,a]=butter(n/2,Wn,'stop');%bandpass ('bandpass') and bandstop ('stop')
[h,w]=freqz(b,a);
mag=20*log10(abs(h));
phase=rad2deg(angle(h));
f=(w/(2*pi))*fs;
figure(6);
subplot(2,1,1);
plot(f,mag);
title('Band Stop filter at 59-61Hz IIR magnitude response');
xlabel('frequency Hz'); 
ylabel('dB magnitude');
subplot(2,1,2);
plot(f,phase);
title('Band Stop filter at 59-61Hz IIR phase response');
xlabel('frequency Hz'); 
ylabel('degrees');

ft3=filter(b,a,ft1);
ft4=filter(b,a,ft2);
[pxx3,f3]=pwelch(ft3,[],[],[],fs);
[pxx4,f4]=pwelch(ft4,[],[],[],fs);

figure(7);
subplot(2,1,1);
plot(f3,pxx1,'b');
hold on;
plot(f3,pxx3,'r');
title('move data');
legend({'original','filtered'});
xlabel('frequency Hz');
ylabel('power spectra'); 
subplot(2,1,2);
plot(f4,pxx2,'b');
hold on;
plot(f4,pxx4,'r');
title('rest data');
legend({'original','filtered'});
xlabel('frequency Hz');
ylabel('power spectra'); 

a=[1];
b=(1/4)*ones(1,4);

pxx5=conv(pxx3,b,'same');
pxx6=conv(pxx4,b,'same');


figure(8);
subplot(2,1,1);
plot(f3,pxx3,'b');
ylim([0 0.2]);
hold on;
plot(f3,pxx5,'r');
ylim([0 0.2]);
title('move-filtered signal-4 point moving average filter');
legend({'original','filtered'});
xlabel('frequency Hz');
ylabel('power spectra'); 

subplot(2,1,2);
plot(f4,pxx4,'b');
ylim([0 0.2]);
hold on;
plot(f4,pxx6,'r');
ylim([0 0.2]);
title('rest-filtered signal-4 point moving average filter');
legend({'original','filtered'});
xlabel('frequency Hz');
ylabel('power spectra'); 


