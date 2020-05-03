function dY = odefunc(T,Y)
%Input data
[M G R]=inputs();

%State equations
x=Y(1); dx=Y(2); y=Y(3); dy=Y(4);
dY = zeros(4,1);
dY(1)=Y(2);
dY(2)=-G*M*x/((x^2 + y^2)^(3/2));
dY(3)=Y(4);
dY(4)=-G*M*y/((x^2 + y^2)^(3/2));
%dY
