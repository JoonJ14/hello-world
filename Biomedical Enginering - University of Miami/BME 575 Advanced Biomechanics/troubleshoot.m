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

curvefit=zeros(timepoints,1);
for i=1:timepoints
    t=time(i)
    sums=0;
    if t<t0
        for n=1:20
        sums=sums+((1/(n^2))*(1-exp(((-n^2)*(pi^2)*Ha*k*t)/height^2)));
        end
        curvefit(i)=-((Ha*v0*t)/height)-(((2*v0*height)/(k*pi^2))*(sums));
    end
    
    if t>=t0
        for n=1:20
        sums=sums+((1/n^2)*(1-exp(((-n^2)*(pi^2)*Ha*k*(t-t0))/height^2))*(1-exp((-n^2*pi^2*Ha*k*t0)/height^2)));
        end
        curvefit(i)=-((Ha*v0*(t-t0))/height)-(((2*v0*height)/(k*pi^2))*(sums));
    end
    curvefit=-curvefit;
end