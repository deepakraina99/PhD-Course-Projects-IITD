%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% A MATLAB code which would accept a triplet (A,B,C)
% and design a state-feedback controller and
% an linear functional observer for the system
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Author: Deepak Raina (2019MEZ8497) PhD@IITD
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% HOW TO RUN THE CODE:
% Specify (A,B,C) as input in this file or LTI_SYS.m file
% Run getCtrlObsDesign.m file

%%
clc; clear all;
%LTI SYSTEM
%EITHER USE LTI_SYS(1-15) OR SPECIFY A,B,C here
%A=[];B[];C=[]
[A,B,C]=LTI_SYS(14)
[mthd,des_p,P]=inputs();
CtrlObsDesign(A,B,C,mthd,des_p,P)

function []=CtrlObsDesign(A,B,C,mthd,des_p,P)
%%
disp('---------------------------------------------------')
disp('Controller-Observer design of LTI system');
disp('Author: Deepak Raina (2019MEZ8497) PhD@IITD')
disp('---------------------------------------------------')

% Error Check
if any([size(A,1)~=size(A,2) size(A,2)~=size(B,1) size(A,1)~=size(C,2)])
    error('Matrix Dimensions Incompatible');
end

%Checking the state of LTI System
CM = ctrb(A,B);  %calculate controllability matrix
OM = obsv(A,C) ; %calculate observability matrix
rc=rank(CM); %calculate rank of controllability matrix
ro=rank(OM); %calculate rank of observability matrix
n=size(A,1);

if (rc==n && ro==n)
    disp('---------------------------------------------------')
    disp('The given system is controllable and observable');
    disp('---------------------------------------------------')
    disp('Designing a Full State Feedback (SFB) Controller')
    disp('---------------------------------------------------')
    %Gain Matrix K
    disp('SFB Gain Matrix')
    F = getFeedbackGain(A,B,C,mthd,des_p,P)
    %eig(A-B*K)
    %Check if SFB is observale
    SFBObservable = checkSFBObservable(F,A,C);
    if SFBObservable == false
        disp('---------------------------------------------------')
        disp('The SFB gain is not observable.')
        disp('Functional observer can not be designed')
        disp('---------------------------------------------------')
    elseif SFBObservable == true
        disp('---------------------------------------------------')
        disp('The SFB gain is observable.')
        disp('---------------------------------------------------')
        disp('Designing a Linear Functional Observer')
        disp('---------------------------------------------------')
        disp('Observer design parameters (N,D,J,H,K)')
        [N,D,J,K,H]=funcObsDesign(A,B,C,F)
    end
    
elseif (rc<n && ro==n)
    disp('---------------------------------------------------')
    disp('The system is uncontrollable but observable')
    disp('---------------------------------------------------')
    Stablizable = checkStabilizable(A,B);
    
    if Stablizable==false
        disp('---------------------------------------------------')
        disp('The given LTI system is not stablizable.')
        disp('SFB Controller and functional observer can not be designed')
        disp('---------------------------------------------------')
    elseif Stablizable==true
        disp('---------------------------------------------------')
        disp('The given LTI system is stablizable')
        disp('Designing a Full State Feedback (SFB) Controller')
        disp('---------------------------------------------------')
        %controllable and uncontrollable decomposition
        [Q,~]=qr(CM);
        T=Q;
        Abar=inv(T)*A*T; Bbar=inv(T)*B; Cbar=C*T;
        A_c=Abar(1:rc,1:rc); B_c=Bbar(1:rc,:); C_c=Cbar(:,1:rc);
        %Gain Matrix K
        disp('SFB Gain Matrix')
        F = getFeedbackGain(A_c,B_c,C_c,mthd,des_p(1:rc),P);
        F = [F zeros(1,n-rc)]*(inv(T))
        %eig(A-B*F)
        %Check if SFB is observale
        SFBObservable = checkSFBObservable(F,A,C);
        if SFBObservable == false
            disp('---------------------------------------------------')
            disp('The SFB gain is not observable.')
            disp('Functional observer can not be designed')
            disp('---------------------------------------------------')
        elseif SFBObservable == true
            disp('---------------------------------------------------')
            disp('The SFB gain is observable.')
            disp('---------------------------------------------------')
            disp('Designing a Linear Functional Observer')
            disp('---------------------------------------------------')
            disp('Controller-Observer design parameters (N,D,J,K,H)')
            [N,D,J,K,H]=funcObsDesign(A,B,C,F)
        end
    end
    
elseif (ro<n && rc==n)
    disp('---------------------------------------------------')
    disp('The system is unobservable but controllable')
    disp('---------------------------------------------------')
    disp('Designing a Full State Feedback (SFB) Controller')
    disp('---------------------------------------------------')
    %Gain Matrix K
    disp('SFB Gain Matrix')
    F = getFeedbackGain(A,B,C,mthd,des_p,P)
    %eig(A-B*F)
    
    % Checking if system is detectable
    Detectable = checkDetectable(A,C);
    
    if Detectable==false
        disp('---------------------------------------------------')
        disp('The given LTI system is not detectable.')
        disp('Observer can not be designed')
        disp('---------------------------------------------------')
    elseif Detectable==true
        disp('The given LTI system is detectable.')
        disp('---------------------------------------------------')
        %Check if SFB is observale
        SFBObservable = checkSFBObservable(F,A,C);
        if SFBObservable == false
            disp('---------------------------------------------------')
            disp('The SFB gain is not observable.')
            disp('Functional observer can not be designed')
            disp('---------------------------------------------------')
        elseif SFBObservable == true
            disp('---------------------------------------------------')
            disp('The SFB gain is observable.')
            disp('---------------------------------------------------')
            disp('Designing a Linear Functional Observer')
            disp('---------------------------------------------------')
            disp('Observer design parameters (N,D,J,K,H)')
            [N,D,J,K,H]=funcObsDesign(A,B,C,F)
        end
    end
    
elseif (ro<n && rc<n)
    disp('---------------------------------------------------')
    disp('The system is both uncontrollable and unobservable')
    disp('---------------------------------------------------')
    %checking stabilizability
    Stablizable = checkStabilizable(A,B);
    % Checking if system is detectable
    Detectable = checkDetectable(A,C);
    
    if Stablizable==false
        disp('The given LTI system is not stabilizable.')
        disp('SFB Controller and functional observer can not be designed')
        disp('--------------------------------------------------')
    elseif Stablizable==true
        disp('The given LTI system is stabilizable')
        disp('---------------------------------------------------')
        disp('Designing a Full State Feedback (SFB) Controller')
        disp('---------------------------------------------------')
        %controllable and uncontrollable decomposition
        [Q,~]=qr(CM);
        Tc=Q;
        Abar=inv(Tc)*A*Tc;
        Bbar=inv(Tc)*B;
        Cbar=C*Tc;
        A_c=Abar(1:rc,1:rc); B_c=Bbar(1:rc,:); C_c=Cbar(:,1:rc);
        %Gain Matrix F
        disp('SFB Gain Matrix')
        F = getFeedbackGain(A_c,B_c,C_c,mthd,des_p(1:rc),P);
        F = [F zeros(1,n-rc)]*(inv(Tc))
        %eig(A-B*F)
        
        if Detectable==false
            disp('---------------------------------------------------')
            disp('The given LTI system is not detectable.')
            disp('Observer can not be designed')
            disp('---------------------------------------------------')
        elseif Detectable==true
            disp('---------------------------------------------------')
            disp('The given LTI system is detectable')
            disp('---------------------------------------------------')
            %Check if SFB is observale
            SFBObservable = checkSFBObservable(F,A,C);
            if SFBObservable == false
                disp('The SFB gain is not observable.')
                disp('Functional observer can not be designed')
                disp('---------------------------------------------------')
            elseif SFBObservable == true
                disp('The SFB gain is observable.')
                disp('---------------------------------------------------')
                disp('Designing a Linear Functional Observer')
                disp('---------------------------------------------------')
                disp('Controller-Observer design parameters (N,D,J,K,H)')
                [N,D,J,K,H]=funcObsDesign(A,B,C,F)
            end
        end
    end
end

end
%function to get state feedback gain matrix
function K = getFeedbackGain(A,B,C,mthd,des_p,P)
if mthd==1
    K=place(A,B,des_p);
elseif mthd==2
    Q = P*C'*C; R = eye(size(B,2));
    [K,~,~] = lqr(A,B,Q,R);
end
end

%function to get observer gain matrix
function K = getObserverGain(A,B,C)
P = 1; Q = P*B*B'; R = eye(size(C',2));
[K,~,~] = lqr(A',C',Q,R);
end

%function to check if system is stabilizable or not
function Stablizable = checkStabilizable(A,B)
Stablizable = true;
n=size(A,1);
eval=eig(A);
pos_eval=eval(real(eval)>=0);
for i=1:size(pos_eval)
    pbh_rank = rank([pos_eval(i)*eye(n)-A B]);
    if pbh_rank<n
        Stablizable = false;
        break;
    end
end
end

%function to check if SFB is observable
function SFBObservable = checkSFBObservable(F,A,C)
OM = obsv(A,C);
rc=rank(OM);
rfc=rank([F;OM]);
if rfc==rc
    SFBObservable=true;
else
    SFBObservable=false;
end
end

%function to check if system is detectable
function Detectable = checkDetectable(A,C)
Detectable = true;
n=size(A,1);
eval=eig(A);
pos_eval=eval(real(eval)>=0);
for i=1:size(pos_eval)
    pbh_rank = rank([pos_eval(i)*eye(n)-A' C']);
    if pbh_rank<n
        Detectable = false;
        break;
    end
end
end
