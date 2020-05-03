function [m1 m2 l1 I1 I2 l2 kt1 kt2 g lin ctrl]=inputs(hObject, eventdata, handles)

m1 = str2double(get(handles.m1_inp, 'string')); 
m2 = str2double(get(handles.m1_inp, 'string')); %mass of links
l1 = str2double(get(handles.l1_inp, 'string')); 
l2 = str2double(get(handles.l2_inp, 'string')); %length of links
I1 = (m1*l1*l1)/3; I2 = (m2*l2*l2)/3; %Inertia of links
kt1 = str2double(get(handles.kt1_inp, 'string')); 
kt2 = str2double(get(handles.kt2_inp, 'string')); %Torsional spring constant
g = 9.81; %acceleration due to gravity
lin = get(handles.checkbox1,'value'); %linearize the EoM
          %1=Yes,0=No
ctrl=0; %control type
        %0=free, 1=forces

