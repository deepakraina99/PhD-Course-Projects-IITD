%% Project 2 Double Pendulum %%
% Contributors: Deepak Raina @IIT delhi
%%
function [] = run_me(hObject, eventdata, handles)
%Use this file to run your program
% clear all;
% fclose all;
% clc;
disp('---------------------------------------------')
disp('Dynamic Simulation of 2-link simple pendulum')
disp('---------------------------------------------')
%Input data
[m1 m2 l1 I1 I2 l2 kt1 kt2 g lin ctrl]=inputs(hObject, eventdata, handles);

%Initial data
[y0, t_initial, t_final, incr, rtol, atol]=initials(hObject, eventdata, handles);

%ODE Solver
opts = odeset('RelTol',rtol,'AbsTol',atol);
[T,Y] = ode45(@(T,Y) odefunc(T,Y,hObject, eventdata, handles),t_initial:incr:t_final,y0,opts);

%Exporting data to .dat
%OPENING DATA FILE
fomode='w';
fip1=fopen('timevar.dat',fomode);%time
fip2=fopen('statevar.dat',fomode);%all state variables

%FOR LOOP FOR READING & WRITING SOLUTIONS FOR EACH INSTANT
for j=1:length(T)
    tsim=T(j);
    %WRITING SOLUTION FOR EACH INSTANT IN FILES
    fprintf(fip1,'%e\n',tsim);
    fprintf(fip2,'%e ',Y(j,:));
    fprintf(fip2,'\n');
end

%Plot all
plot_all(hObject, eventdata, handles);

% %Animation
% animate;
% 
% %Plot motion
%plot_motions;
% 
% %Plot motion
% plot_tor;
