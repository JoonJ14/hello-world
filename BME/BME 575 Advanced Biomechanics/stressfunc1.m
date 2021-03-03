% Brianne Yaryan Stress Function 1
function signal = stressfunc1(x0,time)

data = load('project_data_2020_fall.dat');

points = data(1,1);
time = data(2:end,1);
diameter = data(1,3)*1e-3;
radius = diameter/2;
area = pi*(radius)^2;
height = data(1,2)*1e-3;

t0 = 451;
V0 = (0.05*height)/t0;
k1 = exp(x0(1));

L_eq = 0;
L_resp = data(2:end,3).*(9.81)/area;

f = 0;
f1 = 0;
signal = zeros(points,1);

for i = points-10:points
    L_eq = L_resp(i) + L_eq;
end

Ha_eq = (L_eq/10)/0.05;

for i = 1:points
    if time(i) <= t0
        for n = 1:20
            f = f + (1/(n^2))*(1-exp((-1)*(n^2)*(pi^2)*(Ha_eq)*(k1)*time(i)/(height^2)));
        end
        f1 = f*(-2 * V0 * height)/((k1)*(pi^2));
        signal(i) = -(((Ha_eq) * V0 * time(i))/height) + f1;
        f = 0;
    else 
        for n = 1:20
            f = f+ (1/(n^2))*exp((-1)*((n^2)*(pi^2)*(Ha_eq)*(k1)*(time(i)-t0))/(height^2))*(1-exp(((-1)*(n^2)*(pi^2)*(Ha_eq)*(k1)*time(i)/(height^2))));
        end
        f1 = f*(-2 * V0 * height)/((k1)*(pi^2));
        signal(i) = -(((Ha_eq) * V0 * t0)/height) + f1;
        f = 0;
    end
end

signal = -signal;