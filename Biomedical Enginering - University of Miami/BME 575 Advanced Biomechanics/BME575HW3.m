clear all
n=[2/(sqrt(9));1/(sqrt(9));2/(sqrt(9))]
E=[1,0,0.5;0,0,3;0.5,3,8]
m=[-1/(sqrt(2));0;1/(sqrt(2))]
ue=dot(n,E*m)
deet=det(E)

m=[1/sqrt(5);0;-2/sqrt(5)]
angle=2*dot(m,E*n)
angle2=2*dot(n,E*m)