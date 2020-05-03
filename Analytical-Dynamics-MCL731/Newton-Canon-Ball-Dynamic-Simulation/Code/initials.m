function [y0, t_initial, t_final, H, incr, rtol, atol]=initials(hObject, eventdata, handles)

%Simulation time
t_initial=0;
t_final=str2double(get(handles.time_span, 'string'));

[M G R]=inputs(hObject, eventdata, handles);

H = str2double(get(handles.H_inp, 'string'));% Height of canon

%Particle motion [x,dx,y,dy]
x0=str2double(get(handles.x_initial, 'string'));
dx0=str2double(get(handles.dx_initial, 'string')); % position and vel in x-dxn
y0=str2double(get(handles.y_initial, 'string'))+H; 
dy0=str2double(get(handles.dy_initial, 'string')); % position and vel in y-dxn

%Vecotor of all the initial State Variable
y0=[x0 dx0 y0 dy0];

%ITERATION TOLERANCES
incr=0.1;
rtol=1e-5;         %relative tolerance in integration 
atol=1e-7;         %absolute tolerances in integration 