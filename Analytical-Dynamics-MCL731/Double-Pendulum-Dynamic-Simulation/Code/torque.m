% ReDySim torque module. The control algorithm is entered here
% Contibutors: Dr. Suril Shah and Prof S. K. Saha @IIT Delhi

function [tu_th] = torque(t, tf, th, dth)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
[m1 m2 l1 I1 I2 l2 kt1 kt2 g lin]=inputs();

%Desired Joint trejectory
[th_d dth_d ddth_d]=trajectory(t, tf);

% 1: Joint level PD control
% kp=49; kd=14;
kp=200; kd=140;
tu_th=kp*(th_d(1:2)-th(1:2))+kd*(dth_d(1:2)-dth(1:2));
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
