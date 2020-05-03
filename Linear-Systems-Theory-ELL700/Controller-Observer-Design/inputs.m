%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% INPUT FILE
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function [mthd,des_p,P]=inputs()
%% SPECIFY METHOD FOR STATE FEEDBACK GAIN (F)
% mthd=1; %for using user-defined desired closed-loop pole locations
mthd=2; %for using LQR method

%% DESIRED CLOSED LOOP POLES (ONLY if mthd=1)
%Note: the vector des_p must have as many entries as rows in A.
des_p = [0.1+0.0i 0.2+0.0i 0.3+0.0i 0.4+0.0i 0.5+0.0i];

%% LQR PARAMETERS (P,Q)
% The controller can be tuned by changing the
% nonzero elements in the Q matrix to achieve a desirable response.
P = 1; %constant value for all non zero elements of Q
%P = []; %vector for all diff. non zero elements of Q
%vector dim. must much as per parameter Q = P*C'*C;
end