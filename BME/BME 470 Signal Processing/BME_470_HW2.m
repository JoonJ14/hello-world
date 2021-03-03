f=100;
n=10000;
fs=n/2
A=1;
t=linspace(-1,1,n);
y=A*sin(2*pi*f*t);
figure(1);
plot(t,y)

fs1=200;
fs2=150;
fs3=80;

tx=linspace(-1,1,2*n);
yx=A*sin(2*pi*f*tx);

y1=zeros(1,n);
z=1;
ti1=fs/fs1;
for i=1:fs1
    y1(z)=yx(z);
    z=z+ti1;
end
figure(2);
plot(t,y1)


y2=zeros(1,n);
z=1;
ti2=round(fs/fs2);
for i=1:fs2
    y2(z)=yx(z);
    z=z+ti2;
end
figure(3);
plot(t,y2)


y3=zeros(1,n);
z=1;
ti3=round(fs/fs3);
for i=1:fs3
    y3(z)=yx(z);
    z=z+ti3;
end
figure(4);
plot(t,y3)
