function dY = odefunc(T,Y)
%Input data
[M G R]=inputs();

%State equations
r=Y(1); dr=Y(2); th=Y(3); dth=Y(4);
dY = zeros(4,1);
dY(1)=Y(2);
dY(2)=-G*M/(r^2)+r*(dth^2);
dY(3)=Y(4);
dY(4)=-2*dr*dth/r;
%dY
