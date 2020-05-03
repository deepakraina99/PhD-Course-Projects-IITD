function [y0, t_initial, t_final, H, incr, rtol, atol]=initials(hObject, eventdata, handles)

%Simulation time
t_initial=0;
t_final=str2double(get(handles.time_span, 'string'));;

[M G R]=inputs(hObject, eventdata, handles);

H = str2double(get(handles.H_inp, 'string'));% Height of canon

%Particle motion [r, dr, th, dth]
r0=str2double(get(handles.x_initial, 'string'))+H;
dr0=str2double(get(handles.dx_initial, 'string')); % position and vel in x-dxn
th0=str2double(get(handles.y_initial, 'string')); 
dth0=str2double(get(handles.dy_initial, 'string'));

%Vecotor of all the initial State Variable
y0=[r0 dr0 th0 dth0];

%ITERATION TOLERANCES
incr=0.1;
rtol=1e-5;         %relative tolerance in integration 
atol=1e-7;         %absolute tolerances in integration 