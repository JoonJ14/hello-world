clear all;

%% 2D problem
R=rot2(56,'deg')

V1=[ -1 1 1 -1;-1 -1 1 1]

VR = homtrans(R, V1)
figure (1)
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

figure(2)
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


figure(4);
for p = 1:12
plot3([v_C(1,edges(1,p)) v_C(1,edges(2,p))],[v_C(2,edges(1,p)) v_C(2,edges(2,p))], [v_C(3,edges(1,p)) v_C(3,edges(2,p))])
hold on
end



