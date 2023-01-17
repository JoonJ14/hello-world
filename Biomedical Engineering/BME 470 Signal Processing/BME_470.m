f=4;
A=1;
N=500;
fs=500;
x=(0:N-1)/fs;
y=A*sin(2*pi*f*x);
y1=rms(y);
y2=std(y);
y3=var(y);
figure(1);
plot(x,y)
xlabel('time')
ylabel('amplitude')
hold on
plot(x,y1*ones(1,N),'r')
plot(x,y2*ones(1,N),'b')
plot(x,y3*ones(1,N),'g')
hold off

data=left(1,:);
Y1=rms(data);
Y2=std(data);
Y3=var(data);
fs2=2048;
N2=length(data);
x2=(0:N2-1)/fs2;
figure(2)
plot(x2,data);
xlabel('time')
ylabel('amplitude')
hold on;
plot(x2,Y1*ones(1,N2),'r')
plot(x2,Y2*ones(1,N2),'b')
plot(x2,Y3*ones(1,N2),'g')
hold off;


RMS=1:19;
for i=1:19
    RMS(i)=rms(left(i,:))
end

STD=1:19;
for i=1:19
    STD(i)=std(left(i,:))
end

figure(3)
bar(RMS) 
xlabel('channel')
ylabel('RMS value')
hold on
plot(STD)
hold off 



