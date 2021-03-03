fs=200;
T=5;
N=fs*T;
t=(0:N)/fs;
f1=10;
f2=40;
x1=10*sin(2*pi*f1*t);
x2=5*sin(2*pi*f2*t);
x=x1+x2;
figure(1);
plot(t,x)

y=fft(x);
fx=((0:(N/2))/N)*fs;
amps=2*abs(y(1:(N/2)+1))/N;
figure(2);
plot(fx,amps)

fs2=500;
T2=2;
N2=fs2*T2;
t=(0:N2)/fs2;
f3=round(rand*250);
f4=round(rand*250);
x3=10*sin(2*pi*f3*t);
x4=5*sin(2*pi*f4*t);
x5=x3+x4;
figure(3);
plot(t,x5)

y2=fft(x5);
fx2=((0:(N2/2))/N2)*fs2;
amps2=2*abs(y2(1:(N2/2)+1))/N2;
figure(4);
plot(fx2,amps2)

Y=2*abs(y2(1:(N2/2)+1));
pows=(Y.*conj(Y))/N2;
figure(5);
plot(fx2,pows)

pows2=pwelch(x5);
figure(6);
pwelch(x5)

figure(7);
[pxx,f]=pwelch(x5,[],[],[],fs2);
plot(f,pxx)
