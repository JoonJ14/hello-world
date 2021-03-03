% stress function
function curvefit=stressfunction(x0,time)

x0(1)=10^-15;
x0(2)=10^5;
height=0.0011;
v0=1.2239*10^-7;

for i=1:656
    t=time(i);
    x1=-((Ha*v0*t)/height);
    x2=-((Ha*v0*t0)/h);
    y=((2*v0*height)/(k*pi^2));
    z1=0;
    z2=0;
    for n=1:20
        z1=z1+(1/n^2)*(1-exp((-n^2*pi^2*Ha*k*t)/h^2));
        z2=z2+(1/n^2)*(exp((-n^2*pi^2*Ha*k*(t-t0))/h^2))*(1-exp((-n^2*pi^2*Ha*k*t)/h^2));
    end
    
    if t<t0
        curvefit(i)=x1-y*z1;
    end
    
    if t>=t0
        curvefit(i)=x2-y*z2
    end
    curvefit=-curvefit;
end
end

