function[]=plot_motion()
disp('------------------------------------------------------------------');
disp('Generating plots for joint motions');

load statevar.dat;
load timevar.dat;
Y=statevar;T=timevar;
clear statevar;
clear timevar;

set(0,'DefaultLineLineWidth',1.5)
fh1=figure('Name','Joint Motions','NumberTitle','off');
set(fh1, 'color', 'white'); % sets the color to white
for i=1:length(T)
    t=T(i);
    t=num2str(t);
    subplot(1,2,1)
    
    
    plot(T(1:i),Y(1:i,1),T(1:i),Y(1:i,3));
%     set (gca,'fontsize',12,'fontweight','n','fontname','times new romans','linewidth',0.5,'Box', 'off','TickDir','out' );
%     l1=legend('\theta_1','\theta_2');
%     set(l1,'Orientation','h','Location','northoutside','Color', 'none','Box', 'off','FontAngle','italic','fontsize',14,'fontweight','normal','fontname','times new romans','linewidth',0.5)
    xmin=min(T); xmax=max(T); ymin=min(min(Y(:,1)),min(Y(:,3))); ymax=max(max(Y(:,1)),max(Y(:,3)));
    axis([xmin xmax ymin ymax]);
    xlabel('time(s)','FontSize',12);
    ylabel('Joint angle (rad)','FontSize',12);
    subplot(1,2,2)
    
    plot(T(1:i),Y(1:i,2),T(1:i),Y(1:i,4))
%     set (gca,'fontsize',12,'fontweight','n','fontname','times new romans','linewidth',0.5,'Box', 'off','TickDir','out');
%     l1=legend('$\dot{\theta_1}$','$\dot{\theta_2}$');
%     set(l1,'interpreter','latex','Orientation','h','Location','northoutside','Color', 'none','Box', 'off','FontAngle','italic','fontsize',14,'fontweight','normal','fontname','times new romans','linewidth',0.5)
    xmin=min(T); xmax=max(T); ymin=min(min(Y(:,2)),min(Y(:,4))); ymax=max(max(Y(:,2)),max(Y(:,4))); 
    axis([xmin xmax ymin ymax]);
    title(['joint angle 2'],'fontweight','normal','fontsize',10);
    xlabel('time(s)','FontSize',12);
    ylabel('Rates of joint angle (rad/s)','FontSize',12);
    pause(0.01)
end