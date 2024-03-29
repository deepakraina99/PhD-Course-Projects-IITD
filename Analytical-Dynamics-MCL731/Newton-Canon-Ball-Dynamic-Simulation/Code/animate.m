% Animate module. This module animates the system under study
% Contibutors: Deepak Raina @IIT Delhi
function [] = animate(hObject, eventdata, handles)
load timevar.dat;
load statevar.dat;
T=timevar;
Y=statevar;
%figure('Name','Animation Window','NumberTitle','off');


[y0, t_initial, t_final, H, incr, rtol, atol]=initials(hObject, eventdata, handles);
[M G R]=inputs(hObject, eventdata, handles);

%Plot earth
th=0:0.01:2*pi;
%R = 6.37 * 10^6;
earth_x = R*cos(th);
earth_y = R*sin(th);

%xy limits
h = H;
f = 3.5;
xmin=-R-(f*h); xmax=R+(f*h); ymin=-R-(f*h); ymax=R+(f*h);
for i=1:length(T)
    t=T(i);
    t=num2str(t);
    %plot earth
    plot(earth_x,earth_y,'LineWidth',2);
    hold on;
    %plot tower
    plot([0,0],[R,R+h],'k','LineWidth',2)
    hold on;
    %plot particle
    plot(Y(1:i,1),Y(1:i,3),'r','LineWidth',2);
    hold on;
    plot(Y(i,1),Y(i,3),'o',...
        'LineWidth',1,...
        'MarkerEdgeColor','k',...
        'MarkerFaceColor','r',...
        'MarkerSize',8);
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

