function[]=plot_lyponov()
disp('--------------------------------------------');
disp('Double link pendulum simulation');
disp('--------------------------------------------');

% clf;

load statevar1.dat; load statevar2.dat;
load timevar1.dat; load timevar2.dat;
Y1=statevar1;T1=timevar1;
Y2=statevar2;T2=timevar2;
clear statevar1; clear statevar1;
clear timevar1; clear timevar2;

[m1 m2 l1 I1 I2 l2 kt1 kt2 g lin ctrl]=inputs();

th1=[Y1(:,1),Y2(:,1)];
th2=[Y1(:,3),Y2(:,3)];
dth1=[Y1(:,2),Y2(:,2)]; dth2=[Y1(:,4),Y2(:,4)];

lam_th1=0; lam_th2=0; lam_dth1=0; lam_dth2=0;

for i=2:length(T1)
    t=T1(i);
    lam_th1 = lam_th1 + log(abs(th1(i,1)-th1(i,2)));
    lam_th2 = lam_th2 + log(abs(th2(i,1)-th2(i,2)));
    lam_dth1 = lam_dth1 + log(abs(dth1(i,1)-dth1(i,2)));
    lam_dth2 = lam_dth2 + log(abs((dth2(i,1))-dth2(i,2)));
end
N=i-2;
lam_th1=lam_th1/N
lam_th2=lam_th2/N
lam_dth1=lam_dth1/N
lam_dth2=lam_dth2/N