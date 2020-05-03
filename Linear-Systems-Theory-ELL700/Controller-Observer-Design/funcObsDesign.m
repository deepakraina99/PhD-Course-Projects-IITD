%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% A MATLAB function which would accept a triplet (A,B,C) and
% matrix F, and design a linear functional observer for
% the system. Matrix F depends upon the purpose of observer
% In this case, it is choosen to be a SFB gain matrix, thus
% observer provides an estimate of the corresponding control
% signal to be directly fed into the system
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Contributor: Deepak Raina (2019MEZ8497) PhD@IITD
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function [N,D,J,K,H]=funcObsDesign(A,B,C,F)

%Simplification of equations
P = [pinv(C) null(C)];
Abar = inv(P)*A*P; Bbar = inv(P)*B; Cbar = C*P;
F=F*P;

n=size(A,1);
m=size(B,2);
p=size(C,1);
q=round((m*(n-p))/p);
r=size(F,1);

%MATRIX D
D=F(1:r,1:q);

%MATRIX N
Ne(:,1)= eig(A-B*F);
for i= 1:q
    ne(1,i)= min(real(Ne));
end
N = diag(ne);

F1=F(1:r,1:p);
F2=F(1:r,p+1:n);

%MATRIX T
rho = [];
for i=1:r
    for j=1:q
        rho = [rho zeros(n-p,p) D(i,j)*eye(n-p)];
    end
end
rho=rho;
f = F2;

A11=Abar(1:p,1:p);
A12=Abar(1:p,p+1:n);
A21=Abar(p+1:n,1:p);
A22=Abar(p+1:n,p+1:n);

vec={};
if q==1
    psi = [A12' A22'-N(1,1)*eye(n-p)];
else
    for i=1:q
        vec={vec{:},[A12' A22'-N(i,i)*eye(n-p)]};
    end
    psi = blkdiag(vec{:});
end

matAinv = pinv([rho;psi]);
t = matAinv*[f';zeros(size(matAinv,2)-size(f',1),1)];
% t = [rho;psi]\[f';zeros(size(matAinv,2)-size(f',1),1)];
k=1;
for i=1:q
    for j=1:n
        T(i,j)=t(k,1);
        k=k+1;
    end
end
T1=T(:,1:p);
T2=T(:,p+1:n);

%MATRIX K,J,H
K = F1 - D*T1;
J = T1*A11 + T2*A21 - N*T1;
H = T*B;
end
