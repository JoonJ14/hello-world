zero=11
value=1
impulse=zeros(1,21);
impulse(zero)=value
step=zeros(1,21);
step(zero:21)=value
x=(-10:10)

y=impulse
n=1
y(zero)=0
y(zero+n)=3*value
figure(1)
stem(x,y)

y=impulse
n=3
y(zero)=0
y(zero+n)=-3*value
figure(2)
stem(x,y)

y=impulse
n=-4
y(zero)=0
y(zero+n)=1*value
n=1
y(zero)=0
y(zero+n)=-3*value
n=3
y(zero)=0
y(zero+n)=1*value
figure(3)
stem(x,y)

y=step
n=-1
for i=1-n:21
    y(i+n)=y(i)
    i=i+1
end
figure(4)
stem(x,y)

y=step
n=3
for i=1:21-n
    y(i)=-3*(y(i+n))
    i=i+1
end
figure(5)
stem(x,y)




y1=step
y2=step
y3=step

n=-5
for i=1-n:21
    y1(i+n)=-2*y1(i)
    i=i+1
end

n=-1
for i=1-n:21
    y2(i+n)=y2(i)
    i=i+1
end

n=3
for i=1:21-n
    y3(i)=y3(i+n)
    i=i+1
end

figure(6)
stem(x,y1+y2+y3)

