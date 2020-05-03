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

function [N,D,J,K,H]=funcObsDesign2(A,B,C,F)

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
A11=Abar(1:p,1:p);
A12=Abar(1:p,p+1:n);
A21=Abar(p+1:n,1:p);
A22=Abar(p+1:n,p+1:n);

mat_omega = zeros((n-p)*m,n*q);
mat_eye = eye(n-p);
for i = 1:m
    for j=1:q
        mat_omega(((i-1)*(n-p))+1:((i)*(n-p)),(j-1)*n+p+1:j*n)=D(i,j)*mat_eye;
    end
end

mat_shi = zeros((n-p)*q,n*q);
for i = 1:size(N,1)
    mat_shi((i-1)*(n-p)+1:(i)*(n-p),(i-1)*n+1:(i)*n)=[A12' A22'-N(i,i)*mat_eye];
end

vec_f = zeros((m)*(n-p),1);
for i = 1:m
    vec_f((i-1)*(n-p)+1:(i)*(n-p))=F(i,p+1:end);
end

RHS = [vec_f;zeros((q)*(n-p),1)];
LHS = [mat_omega; mat_shi];
t = pinv(LHS)*RHS;

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
