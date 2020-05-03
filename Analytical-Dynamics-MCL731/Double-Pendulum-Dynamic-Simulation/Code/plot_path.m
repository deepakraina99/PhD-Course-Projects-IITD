% Animate module. This module animates the system under study
% Contibutors: Deepak Raina @IIT Delhi
function [] = plot_path()
load timevar.dat;
load statevar.dat;
T=timevar;
Y=statevar;
figure('Name','Animation Window','NumberTitle','off');

%Plot earth
th=0:0.01:2*pi;
R = 6.37 * 10^6;
earth_x = R*cos(th);
earth_y = R*sin(th);

%xy limits
h = 500000;
f = 1.5;
xmin=-R-(f*h); xmax=R+(f*h); ymin=-R-(f*h); ymax=R+(f*h);
i=length(T);
%plot earth
plot(earth_x,earth_y,'LineWidth',2);
hold on;
%plot tower
plot([0,0],[R,R+h],'k','LineWidth',2)
hold on;
%plot particle
xp=Y(:,1).*cos(Y(:,3));
yp=Y(:,1).*sin(Y(:,3));
% [xp yp];
plot(xp,yp,'r','LineWidth',2);
hold on;
% plot(Y(i,1),Y(i,3),'o',...
%     'LineWidth',1,...
%     'MarkerEdgeColor','k',...
%     'MarkerFaceColor','r',...
%     'MarkerSize',8);
% hold on;
axis([xmin xmax ymin ymax]);
set (gca,'fontsize',10,'fontweight','normal','fontname','times new romans','linewidth',0.5,'Box', 'off','TickDir','out' );
xlabel('X (m)','fontweight','n','fontsize',10);
ylabel('Y (m)','fontweight','n','fontsize',10);
%title(['Current time t=',t],'fontweight','normal','fontsize',10);
grid on;
hold off;


