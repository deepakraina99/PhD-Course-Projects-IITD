%% Newton Canon Ball Problem %%
% Contributors: Deepak Raina @IIT delhi
% Project 1 - Newton Canon Ball Problem
%%
function [] = run_me(hObject, eventdata, handles)
%Use this file to run your program
% clear all;
% fclose all;
% clc;

%Input data
[M G R]=inputs();

%Initial data
[y0, t_initial, t_final, H, incr, rtol, atol]=initials(hObject, eventdata, handles);

%ODE Solver
opts = odeset('RelTol',rtol,'AbsTol',atol);
[T,Y] = ode45(@odefunc,t_initial:incr:t_final,y0,opts)

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

%Animation
%animate(hObject, eventdata, handles); %slow
animate_fast(hObject, eventdata, handles); %fast

%Plot Path
plot_path(hObject, eventdata, handles);


