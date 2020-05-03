function[]=plot_all(hObject, eventdata, handles)
disp('--------------------------------------------');
disp('Double link pendulum simulation');
disp('--------------------------------------------');

% clf;
load statevar.dat;
load timevar.dat;
Y=statevar;T=timevar;
clear statevar;
clear timevar;
[m1 m2 l1 I1 I2 l2 kt1 kt2 g lin ctrl]=inputs(hObject, eventdata, handles);
m1s=num2str(m1); m2s=num2str(m2); l1s=num2str(l1); l2s=num2str(l2);
kt1s=num2str(kt1); kt2s=num2str(kt2);
if lin==1
    str = 'Linearized EOM';
else
    str = 'Non-linearized EOM';
end

if ctrl==1
    str1 = 'Forced control';
else
    str1 = 'Free fall under gravity';
end

th1=Y(:,1); th2=Y(:,3);
th1s = num2str(rad2deg(th1(1))); th2s = num2str(rad2deg(th2(1)));

% set(0,'DefaultLineLineWidth',1.5)
% figure('Name','Double Pendulum Simulation','NumberTitle','off','Position', [10 10 1000 1000]);
%set(fh1, 'color', 'white'); % sets the color to white
for i=1:length(T)
    t=T(i);
    t=num2str(t);
    %Animation
    s1 = subplot(2,2,[1,3]);
    s1.Position = [0.05 0.1 0.35 0.6];
    O0x=0; O0y=0;
    O1x=l1*sin(th1(i)); O1y=-l1*cos(th1(i));
    O2x=l2*sin(th1(i)+th2(i)); O2y=-l2*cos(th1(i)+th2(i));
    XX=[O0x O0x+O1x O0x+O1x+O2x];
    YY=[O0y O0y+O1y O0y+O1y+O2y];
    path1(i,:)=[O0x+O1x O0y+O1y];
    path2(i,:)=[O0x+O1x+O2x O0y+O1y+O2y];
    plot(XX,YY,'linewidth',3);
    hold on;
    plot(path1(1:i,1),path1(1:i,2));
    hold on;
    plot(path2(1:i,1),path2(1:i,2),'m');
    hold on
%     plot(XX(2),YY(2),'o',...
%         'LineWidth',1,...
%         'MarkerEdgeColor','k',...
%         'MarkerFaceColor','r',...
%         'MarkerSize',8);
%     hold on;
%     plot(XX(3),YY(3),'o',...
%         'LineWidth',1,...
%         'MarkerEdgeColor','k',...
%         'MarkerFaceColor','r',...
%         'MarkerSize',8);
%     hold on;
    limit=l1+l2+1;
    xmin=-limit; xmax=limit; ymin=-limit; ymax=limit;
    axis([xmin xmax ymin ymax]);
    set(gca,'fontsize',10,'fontweight','normal','fontname','times new romans','linewidth',0.5,'Box', 'off','TickDir','out' );
    xlabel('X (m)','fontweight','n','fontsize',10);
    ylabel('Y (m)','fontweight','n','fontsize',10);
    title({['m_1= ',m1s,', m_2=',m2s,', l_1=',l1s,', l_2=',l2s,', Kt_1= ',kt1s,', Kt_2=',kt2s],['Initial \theta = [',th1s,'\circ,',th2s,'\circ]'],str,str1,'',['Current time t=',t]},'fontweight','normal','fontsize',12);
    grid on;
    %     hold off;
    %Phase Plot mass 1
    if ctrl==0
        s2 = subplot(2,2,2);
        s2.Position = [0.48 0.58 0.25 0.35];
        plot(Y(1:i,1),Y(1:i,2));
        %set(gca,'fontsize',12,'fontweight','n','fontname','times new romans','linewidth',0.5,'Box', 'off','TickDir','out' );
        %l1=legend('\theta_1','\theta_2');
        %set(l1,'Orientation','h','Location','northoutside','Color', 'none','Box', 'off','FontAngle','italic','fontsize',14,'fontweight','normal','fontname','times new romans','linewidth',0.5)
        xmin=min(Y(:,1)); xmax=max(Y(:,1)); ymin=min(Y(:,2)); ymax=max(Y(:,2));
        axis([xmin xmax ymin ymax]);
        title('Phase Plane Plot Mass 1','fontweight','normal','fontsize',10);
        xlabel('$\theta_1$','Interpreter','latex','FontSize',16);
        ylabel('$\dot{\theta_1}$','Interpreter','latex','FontSize',16);
        
        %Phase Plot mass 2
        s4 = subplot(2,2,4);
        s4.Position = [0.48 0.1 0.25 0.35];
        plot(Y(1:i,3),Y(1:i,4));
        %set(gca,'fontsize',12,'fontweight','n','fontname','times new romans','linewidth',0.5,'Box', 'off','TickDir','out');
        %l1=legend('$\dot{\theta_1}$','$\dot{\theta_2}$');
        %set(l1,'interpreter','latex','Orientation','h','Location','northoutside','Color', 'none','Box', 'off','FontAngle','italic','fontsize',14,'fontweight','normal','fontname','times new romans','linewidth',0.5)
        xmin=min(Y(:,3)); xmax=max(Y(:,3)); ymin=min(Y(:,4)); ymax=max(Y(:,4));
        axis([xmin xmax ymin ymax]);
        title('Phase Plane Plot Mass 2','fontweight','normal','fontsize',10);
        xlabel('$\theta_2$','Interpreter','latex','FontSize',16);
        ylabel('$\dot{\theta_2}$','Interpreter','latex','FontSize',16);
    else
        subplot(2,2,2)
        plot(T(1:i),Y(1:i,1),T(1:i),Y(1:i,3));
        xmin=min(T); xmax=max(T); ymin=min(min(Y(:,1)),min(Y(:,3))); ymax=max(max(Y(:,1)),max(Y(:,3)));
        axis([xmin xmax ymin ymax]);
        title('Mass position 1 and 2','fontweight','normal','fontsize',10);
        xlabel('time(s)','FontSize',12);
        ylabel('Joint angle (rad)','FontSize',12);
        subplot(2,2,4)
        plot(T(1:i),Y(1:i,2),T(1:i),Y(1:i,4))
        xmin=min(T); xmax=max(T); ymin=min(min(Y(:,2)),min(Y(:,4))); ymax=max(max(Y(:,2)),max(Y(:,4))); 
        axis([xmin xmax ymin ymax]);
        title('Mass velocity 1 and 2','fontweight','normal','fontsize',10);
        xlabel('time(s)','FontSize',12);
        ylabel('Rates of joint angle (rad/s)','FontSize',12);
    end
        pause(0.01)
    end