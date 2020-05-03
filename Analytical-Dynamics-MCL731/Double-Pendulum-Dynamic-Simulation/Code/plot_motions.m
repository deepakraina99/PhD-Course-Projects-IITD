function[]=plot_motions()
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
subplot(1,2,1)
plot(T,Y(:,1),T,Y(:,3));
set (gca,'fontsize',12,'fontweight','n','fontname','times new romans','linewidth',0.5,'Box', 'off','TickDir','out' );
l1=legend('\theta_1','\theta_2');
set(l1,'Orientation','h','Location','northoutside','Color', 'none','Box', 'off','FontAngle','italic','fontsize',14,'fontweight','normal','fontname','times new romans','linewidth',0.5)
xlabel('time(s)','FontSize',12);
ylabel('Joint angle (rad)','FontSize',12);
subplot(1,2,2)
plot(T,Y(:,2),T,Y(:,4))
set (gca,'fontsize',12,'fontweight','n','fontname','times new romans','linewidth',0.5,'Box', 'off','TickDir','out');
l1=legend('$\dot{\theta_1}$','$\dot{\theta_2}$');
set(l1,'interpreter','latex','Orientation','h','Location','northoutside','Color', 'none','Box', 'off','FontAngle','italic','fontsize',14,'fontweight','normal','fontname','times new romans','linewidth',0.5)
xlabel('time(s)','FontSize',12);
ylabel('Rates of joint angle (rad/s)','FontSize',12);

set(0,'DefaultLineLineWidth',1.5)
fh2=figure('Name','Phase plots','NumberTitle','off');
set(fh2, 'color', 'white'); % sets the color to white 
subplot(1,2,1)
plot(Y(:,1),Y(:,2));
set (gca,'fontsize',12,'fontweight','n','fontname','times new romans','linewidth',0.5,'Box', 'off','TickDir','out' );
l1=legend('Joint 1');
set(l1,'interpreter','latex','Orientation','h','Location','northoutside','Color', 'none','Box', 'off','FontAngle','italic','fontsize',12,'fontweight','normal','fontname','times new romans','linewidth',0.5)
xlabel('$\theta_1$','Interpreter','latex','FontSize',16);
ylabel('$\dot{\theta_1}$','Interpreter','latex','FontSize',16);
subplot(1,2,2)
plot(Y(:,3),Y(:,4))
set (gca,'fontsize',12,'fontweight','n','fontname','times new romans','linewidth',0.5,'Box', 'off','TickDir','out');
l1=legend('Joint 2');
set(l1,'interpreter','latex','Orientation','h','Location','northoutside','Color', 'none','Box', 'off','FontAngle','italic','fontsize',12,'fontweight','normal','fontname','times new romans','linewidth',0.5)
xlabel('$\theta_2$','Interpreter','latex','FontSize',16);
ylabel('$\dot{\theta_2}$','Interpreter','latex','FontSize',16);
