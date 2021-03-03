clear all;

%% 2D problem
R=rot2(56,'deg')

V1=[ -1 1 1 -1;-1 -1 1 1]

VR = homtrans(R, V1)
figure (1)
axis([-2 3 -2 3])
axis square
hold on
x1=[-1 1];
y1=[-1 -1];

plot(x1,y1,'r')
x2=[1 1];
y2=[-1 1];
plot(x2,y2,'r')
x3=[1 -1];
y3=[1 1];
plot(x3,y3,'r')
x4=[-1 -1];
y4=[1 -1];
plot(x4,y4,'r')

v1=[x1;y1];
r1=v1*R;
rx1=[r1(1),r1(3)];
ry1=[r1(2),r1(4)];
plot(rx1,ry1,'b')
v2=[x2;y2];
r2=v2*R;
rx2=[r2(1),r2(3)];
ry2=[r2(2),r2(4)];
plot(rx2,ry2,'b')
v3=[x3;y3];
r3=v3*R;
rx3=[r3(1),r3(3)];
ry3=[r3(2),r3(4)];
plot(rx3,ry3,'b')
v4=[x4;y4];
r4=v4*R;
rx4=[r4(1),r4(3)];
ry4=[r4(2),r4(4)];
plot(rx4,ry4,'b')

figure(2)
axis([-2 3 -2 3])
axis square
hold on
plot(V1(1,1:2),V1(2,1:2),'b',V1(1,2:3),V1(2,2:3),'b',V1(1,3:4),V1(2,3:4),'b',V1(1,[1,4]),V1(2,[1,4]),'b')
plot(VR(1,1:2),VR(2,1:2),'r',VR(1,2:3),VR(2,2:3),'r',VR(1,3:4),VR(2,3:4),'r',VR(1,[1,4]),VR(2,[1,4]),'r')


%% 3D Problem

V2= [
    -1 1 1 -1 -1 1 1 -1 
    -1 -1 1 1 -1 -1 1 1 
    -1 -1 -1 -1 1 1 1 1 ];
edges = [
    1 2 3 4 5 6 7 8 1 2 3 4 
    2 3 4 1 6 7 8 5 5 6 7 8];

P= [5, 6, 4];
C= transl(P) * oa2tr([0 1 0], -P);

V_r = homtrans(C, V2)

X=V_r(1,:);
Y=V_r(2,:);
Z=V_r(3,:);

figure(3)
hold on
plot3(X([1,2]),Y([1,2]),Z([1,2]),'b')
plot3(X([2,3]),Y([2,3]),Z([2,3]),'b')
plot3(X([3,4]),Y([3,4]),Z([3,4]),'b')
plot3(X([4,1]),Y([4,1]),Z([4,1]),'b')
plot3(X([5,6]),Y([5,6]),Z([5,6]),'b')
plot3(X([6,7]),Y([6,7]),Z([6,7]),'b')
plot3(X([7,8]),Y([7,8]),Z([7,8]),'b')
plot3(X([8,5]),Y([8,5]),Z([8,5]),'b')
plot3(X([1,5]),Y([1,5]),Z([1,5]),'b')
plot3(X([2,6]),Y([2,6]),Z([2,6]),'b')
plot3(X([3,7]),Y([3,7]),Z([3,7]),'b')
plot3(X([4,8]),Y([4,8]),Z([4,8]),'b')

figure(4)
for i = 1:12
plot3([V_r(1,edges(1,i)) V_r(1,edges(2,i))],[V_r(2,edges(1,i)) V_r(2,edges(2,i))], [V_r(3,edges(1,i)) V_r(3,edges(2,i))])
hold on
end





