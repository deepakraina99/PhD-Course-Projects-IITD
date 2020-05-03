% ReDySim trajectory module. The desired indpendent joint trejectories are 
% enterd here
% Contibutors: Dr. Suril Shah and Prof S. K. Saha @IIT Delhi

function [th_d dth_d ddth_d]=trajectory(t, tf)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 1: Joint level trejectory: Cycloidal motion
[y0]=initials();
thin=[deg2rad(y0(1)); deg2rad(y0(3))];
thf=[deg2rad(-90); deg2rad(-90)];
Tp=tf;
for i=1:2
    thi(i,1)=thin(i)+((thf(i)-thin(i))/Tp)*(t-(Tp/(2*pi))*sin((2*pi/Tp)*t));
    dthi(i,1)=((thf(i)-thin(i))/Tp)*(1-cos((2*pi/Tp)*t));
    ddthi(i,1)=(2*pi*(thf(i)-thin(i))/(Tp*Tp))*sin((2*pi/Tp)*t);
    
%     thi(i,1)=thin(i)+((thf(i)-thin(i))/Tp);
%     dthi(i,1)=((thf(i)-thin(i))/Tp);
%     ddthi(i,1)=(2*pi*(thf(i)-thin(i))/(Tp*Tp));
    
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

th_d=thi;
dth_d=dthi;
ddth_d=ddthi;