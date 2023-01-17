%% Joon Jung BME 575 Final Project
clc
clear all
data=load('project_data_2020_fall-2.dat');
timepoints=data(1,1);
height=data(1,2);
diameter=data(1,3);
% mm to m conversion
height=height*10^(-3);
diameter=diameter*10^(-3);

t0=451;
v0=(0.05*height)/t0;
area=(pi*(diameter^2))/4;
 

for i=1:timepoints
    time(i)=data(i+1,1);
    Load(i)=data(i+1,3);
end

% Kg to Pa conversion (Pa = (Kg*9.8)N/m^2)
Load=(Load*9.8)/area;

%% Ha calculation
Load_avg=0;

for i=(timepoints-10):timepoints
    Load_avg=Load_avg+(Load(i)/10);
end
stress_equil=Load_avg;
strain=0.05;
Ha=stress_equil/strain;

x0(1)=log(10^-15);
%x0(2)=10^5;

%% Curve fitting
cfit=lsqcurvefit(@stressfunction,x0,time,Load);
curvefit=stressfunction(cfit,time);

figure(1);
plot(time,Load,'b')
hold on
plot(time,curvefit,'r')
title('conv function')
legend({'original','filtered'})

%% stress function
function curvefit=stressfunction(x0,time)

data=load('project_data_2020_fall-2.dat');
timepoints=data(1,1);
height=data(1,2);
diameter=data(1,3);
% mm to m conversion
height=height*10^(-3);
diameter=diameter*10^(-3);
t0=451;
v0=(0.05*height)/t0;
area=(pi*(diameter^2))/4;

for i=1:timepoints
    time(i)=data(i+1,1);
    Load(i)=data(i+1,3);
end
% Kg to Pa conversion (Pa = (Kg*9.8)N/m^2)
Load=(Load*9.8)/area;
% Ha calculation
Load_avg=0;

for i=(timepoints-10):timepoints
    Load_avg=Load_avg+(Load(i)/10);
end

stress_equil=Load_avg;
strain=0.05;
Ha=stress_equil/strain;

k=10^-15

for i=1:timepoints
    
    
    syms n 
    sums=symsum(-((Ha*v0*t)/height)-(((2*v0*height)/(k*pi^2))*((1/n^2)*(1-exp(((-n^2)*(pi^2)*Ha*k*t)/height^2)))),1,20  )
    -((Ha*v0*t)/height)-(((2*v0*height)/(k*pi^2))*(sums)
    syms n 
    symsum(-((Ha*v0*t0)/height)-(((2*v0*height)/(k*pi^2))*((1/n^2)*(1-exp(((-n^2)*(pi^2)*Ha*k*(t-t0)/height^2)))),1,20  )
    
    if t<t0
        syms n 
        sums=symsum(((1/n^2)*(1-exp(((-n^2)*(pi^2)*Ha*k*t)/height^2))),1,inf)
        curvefit(i)=-((Ha*v0*t)/height)-(((2*v0*height)/(k*pi^2))*(sums)
    end
    
    if t>=t0
        syms n 
        sums=symsum(((1/n^2)*(1-exp(((-n^2)*(pi^2)*Ha*k*(t-t0))/height^2))*(1-exp((-n^2*pi^2*Ha*k*t0)/height^2))),1,inf)
        curvefit(i)=-((Ha*v0*(t-t0))/height)-(((2*v0*height)/(k*pi^2))*(sums)
        
    end
    curvefit=-curvefit;
end