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
t1=samples1/fs1;
ps1=1/(4*fs1)
y1=A*sin(2*pi*f*((t1)-(ps1)));
figure(2);
stem(t1,y1)

fs2=150;
samples2=(-fs2:fs2);
t2=samples2/fs2;
ps2=1/(4*fs2)
y2=A*sin(2*pi*f*((t2)-(ps2)));
figure(3);
stem(t2,y2)

fs3=80;
samples3=(-fs3:fs3);
t3=samples3/fs3;
ps3=1/(4*fs3)
y3=A*sin(2*pi*f*((t3)));
figure(4);
stem(t3,y3)


fs4=100;
samples4=(-fs4:fs4);
t4=samples4/fs4;
ps4=1/(4*fs4)
y4=A*sin(2*pi*f*((t4)-(ps4)));
figure(5);
stem(t4,y4)


