%% Joon Jung BME 575 Final Project
clc
clear all
data=load('project_data_2020_fall.dat');
timepoints=data(1,1);
height=data(1,2);
diameter=data(1,3);

for i=1:timepoints
    time(i)=data(i+1,1);
    displacement(i)=data(i+1,2);
    Load(i)=data(i+1,3);
end

% mm to m conversion
height=height*10^(-3);
diameter=diameter*10^(-3);
displacement=displacement*10^(-3);

t0=451;
v0=(0.05*height)/t0;
area=(pi*(diameter^2))/4;

% Kg to Pa conversion (Pa = (Kg*9.8)N/m^2)
Load=(Load*9.81)/area;


%% Displacement function


for i = 1:timepoints
    t=time(i);
    if t<=t0
        u_z(i) = -0.05*height*(t/t0);
    else
        u_z(i) = -0.05*height;
    end
    u_z=abs(u_z);
end

figure(1)
plot(time,u_z,'b')
hold on
plot(time,displacement,'r')
xlabel('Time (s)')
ylabel('-u_z')
title('Displacement (m)')
legend({'Applied displacement function','Displacement data'})


%% Ha calculation
Load_eq_avg=0;

for i=(timepoints-10):timepoints
    Load_eq_avg=Load_eq_avg+(Load(i)/10);
end
stress_equil=Load_eq_avg;
strain=0.05;
Ha_eq=stress_equil/strain


%% k Curve fitting
x0(1)=log(10^-15);
cfit=lsqcurvefit(@stressfunction1,x0,time,Load);
curvefit=stressfunction1(cfit,time);
k1=exp(cfit)
Ha1=Ha_eq

figure(2);
plot(time,Load,'b')
hold on
plot(time,curvefit,'r')
xlabel('Time(s)')
ylabel('Force(Kg)')
title('Load response k curve fitting')
legend({'Experiment','Theoretical'})


%% r^2 for k curve fitting
Load_avg=mean(Load);
num1=0;
den1=0;
for i=1:timepoints
    num1=num1+((Load(i)-curvefit(i))^2);
    den1=den1+((Load(i)-Load_avg)^2);
end
rsq1=(1-(num1/den1))

%% Ha and k Curve fitting
x0(1)=log(10^-15);
x0(2)=log(10^5);
cfit2=lsqcurvefit(@stressfunction2,x0,time,Load);
curvefit2=stressfunction2(cfit2,time);
k2=exp(cfit2(1))
Ha2=exp(cfit2(2))

figure(3);
plot(time,Load,'b')
hold on
plot(time,curvefit2,'r')
xlabel('Time(s)')
ylabel('Force(Kg)')
title('Load response Ha and k curve fitting')
legend({'Experiment','Theoretical'})

%% r^2 for Ha and k curve fitting
num2=0;
den2=0;
for i=1:timepoints
    num2=num2+((Load(i)-curvefit2(i))^2);
    den2=den2+((Load(i)-Load_avg)^2);
end
rsq2=(1-(num2/den2))

%% stress function for k 
function curvefit=stressfunction1(x0,time)

data=load('project_data_2020_fall.dat');
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

k=exp(x0);


for i=1:timepoints
    t=time(i);
    sums=0;
    if t<t0
        for n=1:20
        sums=sums+(1/(n^2))*(1-exp((-n^2*pi^2*Ha*k*t)/height^2));
        end
        curvefit(i)=(-(Ha*v0*t)/height)-(((2*v0*height)/(k*pi^2))*(sums));
    end
    
    if t>=t0
        for n=1:20
        sums=sums+(1/n^2)*(exp((-n^2*pi^2*Ha*k*(t-t0))/height^2))*(1-exp((-n^2*pi^2*Ha*k*t0)/height^2));
        end
        curvefit(i)=(-(Ha*v0*t0)/height)-(((2*v0*height)/(k*pi^2))*(sums));
    end
    curvefit=abs(curvefit);
end
end

%% stress function for Ha and k
function curvefit=stressfunction2(x0,time)

data=load('project_data_2020_fall.dat');
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


k=exp(x0(1));
Ha=exp(x0(2));

for i=1:timepoints
    t=time(i);
    sums=0;
    if t<t0
        for n=1:20
        sums=sums+(1/(n^2))*(1-exp((-n^2*pi^2*Ha*k*t)/height^2));
        end
        curvefit(i)=(-(Ha*v0*t)/height)-(((2*v0*height)/(k*pi^2))*(sums));
    end
    
    if t>=t0
        for n=1:20
        sums=sums+(1/n^2)*(exp((-n^2*pi^2*Ha*k*(t-t0))/height^2))*(1-exp((-n^2*pi^2*Ha*k*t0)/height^2));
        end
        curvefit(i)=(-(Ha*v0*t0)/height)-(((2*v0*height)/(k*pi^2))*(sums));
    end
    curvefit=abs(curvefit);
end
end
