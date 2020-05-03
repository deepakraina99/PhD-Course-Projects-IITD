% Animate module. This module animates the system under study
% Contibutors: Deepak Raina @IIT Delhi
function [] = animate()
load timevar.dat;
load statevar.dat;
T=timevar;
Y=statevar;
figure('Name','Animation Window','NumberTitle','off');

[m1 m2 l1 I1 I2 l2 kt1 kt2 g lin ctrl]=inputs();

%xy limits
limit=l1+l2+1;
xmin=-limit; xmax=limit; ymin=-limit; ymax=limit;
th1=Y(:,1); th2=Y(:,3);
for i=1:length(T)
    t=T(i);
    t=num2str(t);
    %Link Centres
    O0x=0; O0y=0;
    O1x=l1*sin(th1(i)); O1y=l1*cos(th1(i));
    O2x=l2*sin(th1(i)+th2(i)); O2y=l2*cos(th1(i)+th2(i));
    XX=[O0x O0x+O1x O0x+O1x+O2x];
    YY=[O0y O0y+O1y O0y+O1y+O2y];
    path1(i,:)=[O0x+O1x O0y+O1y];
    path2(i,:)=[O0x+O1x+O2x O0y+O1y+O2y];
    plot(XX,YY,'linewidth',1.5);
    hold on;
    plot(path1(1:i,1),path1(1:i,2));
    hold on;
    plot(path2(1:i,1),path2(1:i,2),'m');
    hold on
    plot(XX(2),YY(2),'o',...
        'LineWidth',1,...
        'MarkerEdgeColor','k',...
        'MarkerFaceColor','r',...
        'MarkerSize',8);
    hold on;
    plot(XX(3),YY(3),'o',...
        'LineWidth',1,...
        'MarkerEdgeColor','k',...
        'MarkerFaceColor','r',...
        'MarkerSize',8);
    hold on;
    hold on;
    axis([xmin xmax ymin ymax]);
    set (gca,'fontsize',10,'fontweight','normal','fontname','times new romans','linewidth',0.5,'Box', 'off','TickDir','out' );
    xlabel('X (m)','fontweight','n','fontsize',10);
    ylabel('Y (m)','fontweight','n','fontsize',10);
    title(['Current time t=',t],'fontweight','normal','fontsize',10);
    grid on;
    hold off;
    pause(0.01)
end

