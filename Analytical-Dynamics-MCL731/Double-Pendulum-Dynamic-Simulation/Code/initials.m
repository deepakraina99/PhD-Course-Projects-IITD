function [y0, t_initial, t_final, incr, rtol, atol]=initials(hObject, eventdata, handles)

%Simulation time
t_initial=0;
t_final=str2double(get(handles.time_span, 'string'));

[m1 m2 l1 I1 I2 l2 kt1 kt2 g lin]=inputs(hObject, eventdata, handles);

%Double link pendulum
th1=deg2rad(str2double(get(handles.th1_initial, 'string'))); 
th2=deg2rad(str2double(get(handles.th2_initial, 'string')));
dth1=str2double(get(handles.dth1_initial, 'string'));
dth2=str2double(get(handles.dth2_initial, 'string'));

%Vecotor of all the initial State Variable
y0=[th1 dth1 th2 dth2];

%ITERATION TOLERANCES
incr=0.1;
rtol=1e-5;         %relative tolerance in integration 
atol=1e-7;         %absolute tolerances in integration 