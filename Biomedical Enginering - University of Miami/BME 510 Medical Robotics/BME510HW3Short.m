clear all;

%% 2D problem
R=rot2(56,'deg')

V1=[ -1 1 1 -1;-1 -1 1 1]

VR = homtrans(R, V1)

figure(1)
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
for i = 1:12
plot3([V_r(1,edges(1,i)) V_r(1,edges(2,i))],[V_r(2,edges(1,i)) V_r(2,edges(2,i))], [V_r(3,edges(1,i)) V_r(3,edges(2,i))])
hold on
end


