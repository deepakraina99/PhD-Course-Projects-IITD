%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Function for finding intersaction of two subspaces V and W
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Contributor: Deepak Raina (2019MEZ8497) PhD@IITD
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function [inters,dim] = getIntersect(V,W)
dim_v = min(size(V)); % compute dimension of contr. subspace
dim_w = min(size(W)); % compute dimension of unobs. subspace
inters = V*[eye(dim_v) zeros(dim_v,dim_w)]*null([V W]);
dim= size(inters,2);
end
