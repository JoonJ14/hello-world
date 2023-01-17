f=100;
n=10000;
fs=n/2;
A=1;
samples=(-5000:5000);
t=samples/5000;
y=A*sin(2*pi*f*t);
figure(1);
plot(t,y)

fs1=200;
samples1=(-fs1:fs1);
t1=linspace(-1,1,200)
ps1=1/(4*fs1)
y1=A*sin(2*pi*f*((t1)-(ps)));
figure(2);
stem(t1,y1)