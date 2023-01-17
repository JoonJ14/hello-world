% Brianne Yaryan Stress Function 2
function signal = stressfunc2(x0,time)

data = load('project_data_2020_fall.dat');

points = data(1,1);
time = data(2:end,1);
diameter = data(1,3)*1e-3;
radius = diameter/2;
area = pi*(radius)^2;
height = data(1,2)*1e-3;

t0 = 451;
V0 = (0.05*height)/t0;
Ha_cf = exp(x0(1));
k2 = exp(x0(2));

f = 0;
f1 = 0;
signal = zeros(points,1);
 
for i = 1:points
    if time(i) <= t0
        for n = 1:20
            f = f + (1/(n^2))*(1-exp((-1)*(n^2)*(pi^2)*(Ha_cf)*(k2)*time(i)/(height^2)));
        end
        f1 = f * (-2 * V0* height)/((k2)*(pi^2));
        signal(i) = -(((Ha_cf) * V0 * time(i))/height) + f1;
        f = 0;
    else
        for n = 1:20
            f = f + (1/(n^2))*exp((-1)*((n^2)*(pi^2)*(Ha_cf)*(k2)*(time(i)-t0))/(height^2))*(1-exp(((-1)*(n^2)*(pi^2)*(Ha_cf)*(k2)*time(i)/(height^2))));
        end
        f1 = f * (-2 * V0 * height)/((k2)*(pi^2));
        signal(i) = -(((Ha_cf) * V0 * t0)/height)+f1;
        f = 0;
    end
end

signal = -signal;