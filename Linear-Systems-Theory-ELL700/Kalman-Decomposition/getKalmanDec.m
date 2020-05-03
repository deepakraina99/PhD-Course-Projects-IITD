%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% A MATLAB code which would accept a triplet (A,B,C)
% and perform the Kalman Decomposition of the system.
% The output is the similarity transformation matrix T and
% the system matrices of the transformed system.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Contributor: Deepak Raina (2019MEZ8497) PhD@IITD
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function [Abar,Bbar,Cbar,T]=getKalmanDec(A,B,C)
    disp('---------------------------------------------------')
    disp('Kalman decomposition of LTI System');
    disp('Contributor: Deepak Raina (2019MEZ8497) PhD@IITD')
    disp('---------------------------------------------------')
    
    %Checking the state of LTI System
    CM = ctrb(A,B); % calculate controllability matrix
    OM = obsv(A,C) ; % calculate observability matrix
    rc=rank(CM); % calculate rank of controllability matrix
    ro=rank(OM) ;% calculate rank of observability matrix
    n=size(A,1);

    if (rc==n && ro==n)
        disp('---------------------------------------------------')
        disp('The given system is controllable and observable.');
        disp('No decomposition required.')
        disp('---------------------------------------------------')
        T = eye(n);
        
    elseif (rc<n && ro==n)
        disp('---------------------------------------------------')
        disp('The system is observable but uncontrollable.')
        disp('Obtaining controllability decomposition')
        disp('---------------------------------------------------')
        [Q,~]=qr(CM);
        T=Q;
        
    elseif (rc==n && ro<n)
        disp('---------------------------------------------------')
        disp('The system is controllable but unobservable')
        disp('Obtaining observability decomposition')
        disp('---------------------------------------------------')
        [Q,~]=qr(OM');
        T=Q;
        
    elseif (rc<n && ro<n)
        disp('---------------------------------------------------')
        disp('The system is both uncontrollable and unobservable')
        disp('Obtaining Kalman decomposition')
        disp('---------------------------------------------------')
        %find the Subspaces
        %controllable (S_C) and uncontrollable (S_UC) subspace
        [Q,~]=qr(CM);
        S_C = Q(:,1:rc);
        S_UC = Q(:,rc+1:n);
        %observable (S_O) and unobservable (S_UO) subspace
        [Q,~]=qr(OM');
        S_O = Q(:,1:ro);
        S_UO = Q(:,ro+1:n);
        
        %Transformation matrix
        %for contr. and unobsv. subspace
        [T_C_UO,n1] = getIntersect(S_C,S_UO);
        %for contr. and obsv. subspace
        [T_C_O,n2] = getIntersect(S_C,S_O);
        %for uncontr. and obsv. subspace
        [T_UC_UO,n3] = getIntersect(S_UC,S_UO);
        %for uncontr. and obsv. subspace
        [T_UC_O,n4] = getIntersect(S_UC,S_O);
        
        T = [T_C_UO T_C_O T_UC_UO T_UC_O];
        
    end
    %Transformed tuple
    Abar = inv(T)*A*T;
    Bbar = inv(T)*B;
    Cbar = C*T;
    disp('---------------------------------------------------')
end
