function dY = odefunc(t,Y,hObject, eventdata, handles)
%Input data
[m1 m2 l1 I1z I2z l2 kt1 kt2 g lin ctrl]=inputs(hObject, eventdata, handles);
[y0, ti, tf]=initials(hObject, eventdata, handles);
disp(t)
th1=Y(1); th2=Y(3); dth1=Y(2); dth2=Y(4);
%State equations
%Mass Matrix [M]
if lin==0
    m11 = (m1+m2)*l1*l1 + m2*l2*l2 + 2*m2*l1*l2*cos(th2)+ I1z + I2z;
    m12 = m2*l2*l2 + m2*l1*l2*cos(th2) + I2z;
    m21 = m12;
    m22 = m2*l2*l2 + I2z;
    M = [m11 m12
        m21 m22];
    
    %Coupling Vector
    c1=-m2*l1*l2*(dth2^2)*sin(th2) - 2*m2*l1*l2*(dth1*dth2)*sin(th2) ;
    c2=m2*l1*l2*(dth1^2)*sin(th2);
    C = [c1
        c2];
    
    %Gravity Vector [G]
    g1=(m1+m2)*l1*g*sin(th1) + m2*l2*g*sin(th1+th2) + kt1*th1;
    g2=m2*l2*g*sin(th1+th2) + kt2*th2;
    G = [g1
        g2];
else
    m11 = (m1+m2)*l1*l1 + m2*l2*l2 + 2*m2*l1*l2*1 + I1z + I2z;
    m12 = m2*l2*l2 + m2*l1*l2*1 + I2z;
    m21 = m12;
    m22 = m2*l2*l2 + I2z;
    M = [m11 m12
        m21 m22];
    
    %Coupling Vector
%     c1=-m2*l1*l2*(dth2^2)*(th2) - 2*m2*l1*l2*(dth1*dth2)*(th2);
%     c2=m2*l1*l2*(dth1^2)*(th2);
    C = [0
         0];

    %Gravity Vector [G]
    g1=(m1+m2)*l1*g*(th1) + m2*l2*g*(th1+th2) + kt1*th1;
    g2=m2*l2*g*(th1+th2) + kt2*th2;
    G = [g1
        g2];
end
if ctrl==0
    %Force Vector
    F1 = 0;
    F2 = 0;
    F = [F1
        F2];
else
    th=[th1; th2]; dth=[dth1; dth2];
    [tu_th] = torque(t, tf, th, dth);
    F = [tu_th(1)
        tu_th(2)];
end

ddth = inv(M)*(F-C-G);

%New
dY=zeros(4,1);
dY(1)=Y(2);
dY(2)=ddth(1);
dY(3)=Y(4);
dY(4)=ddth(2);
%dY
