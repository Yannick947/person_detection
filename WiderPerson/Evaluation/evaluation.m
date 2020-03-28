function eval_results = evaluation(pred_list,file_list,gt_list,setting_name)
img_num = length(file_list);
IoU_thresh = 0.5;
thresh_num = 1000;
org_roc_cruve = zeros(thresh_num,2);
count_ped = 0;

img_roc_info_list = cell(img_num,1);
for i = 1:length(file_list)
    fprintf('%s: current image %d/%d\n',setting_name, i, img_num);
    file_name = file_list{i};
    gt_file = sprintf('../Annotations/%s.jpg.txt',file_name);
    msg = importdata(gt_file);
    gt_num = msg(1,1);
    gt_bbx_tmp = msg(2:end, 1);
    gt_bbx_tmp = reshape(gt_bbx_tmp, [5, gt_num])';
    gt_bbx = gt_bbx_tmp(:,2:end);
    
    pred_info = pred_list{i};
    keep_index = gt_list{i};
    count_ped = count_ped + length(keep_index);
    
    if isempty(gt_bbx) || isempty(pred_info)
        continue;
    end
    ignore = zeros(size(gt_bbx,1),1);
    if ~isempty(keep_index)
        ignore(keep_index) = 1;
    end
    
    [pred_recall, proposal_list] = image_evaluation(pred_info, gt_bbx, ignore, IoU_thresh);
    
    img_roc_info = image_roc_info(thresh_num, pred_info, proposal_list, pred_recall);
    img_roc_info_list{i} = img_roc_info;
end
for i = 1:length(file_list)
    img_roc_info = img_roc_info_list{i};
    if ~isempty(img_roc_info)
        org_roc_cruve(:,1) = org_roc_cruve(:,1) + img_roc_info(:,1);
        org_roc_cruve(:,2) = org_roc_cruve(:,2) + img_roc_info(:,2);
    end
end

pr_cruve = dataset_pr_info(thresh_num, org_roc_cruve, count_ped);
roc_cruve = dataset_roc_info(thresh_num, org_roc_cruve, count_ped, img_num);

%Recall
recall = max(pr_cruve(:,2));

%Average Precision (AP)
%xs=tp/np; ys=tp./(fp+tp); xs1=[xs; inf]; ys1=[ys; 0];
%for i=1:m, j=find(xs1>=ref(i)); ref(i)=ys1(j(1)); end
prec = pr_cruve(:,1);
rec = pr_cruve(:,2);
ap = VOCap(rec,prec);

%Miss Rate (MR)
samples = 10.^(-2:.25:0); % samples for computing area under the curve
m = length(samples);
xs = roc_cruve(:,2);
ys = roc_cruve(:,1);
xs1=[-inf; xs];
ys1=[0; ys];
for i=1:m, j=find(xs1<=samples(i)); samples(i)=ys1(j(end)); end
score = 1 - samples;
mr=exp(mean(log(score)));

eval_results = [recall ap mr];

end

function [pred_recall,proposal_list] = image_evaluation(pred_info, gt_bbx, ignore, IoU_thresh)
pred_recall = zeros(size(pred_info,1),1);
recall_list = zeros(size(gt_bbx,1),1);
proposal_list = zeros(size(pred_info,1),1);
proposal_list = proposal_list + 1;
for h = 1:size(pred_info,1)
    overlap_list = boxoverlap(gt_bbx, pred_info(h,1:4));
    [max_overlap, idx] = max(overlap_list);
    if max_overlap >= IoU_thresh
        if (ignore(idx) == 0)
            recall_list(idx) = -1;
            proposal_list(h) = -1;
        elseif (recall_list(idx)==0)
            recall_list(idx) = 1;
        end
    end
    r_keep_index = find(recall_list == 1);
    pred_recall(h) = length(r_keep_index);
end
end

function img_roc_info = image_roc_info(thresh_num, pred_info, proposal_list, pred_recall)
img_roc_info = zeros(thresh_num,2);
for t = 1:thresh_num
    thresh = 1-t/thresh_num;
    r_index = find(pred_info(:,5)>=thresh,1,'last');
    if (isempty(r_index))
        img_roc_info(t,2) = 0;
        img_roc_info(t,1) = 0;
    else
        p_index = find(proposal_list(1:r_index) == 1);
        img_roc_info(t,1) = length(p_index);
        img_roc_info(t,2) = pred_recall(r_index);
    end
end
end

function pr_cruve = dataset_pr_info(thresh_num, org_roc_cruve, count_ped)
pr_cruve = zeros(thresh_num,2);
for i = 1:thresh_num
    pr_cruve(i,1) = org_roc_cruve(i,2)/org_roc_cruve(i,1);
    pr_cruve(i,2) = org_roc_cruve(i,2)/count_ped;
end
end

function roc_cruve = dataset_roc_info(thresh_num, org_roc_cruve, count_ped, img_num)
roc_cruve = zeros(thresh_num,2);
for i = 1:thresh_num
    roc_cruve(i,1) = org_roc_cruve(i,2)/count_ped;
    roc_cruve(i,2) = (org_roc_cruve(i,1)-org_roc_cruve(i,2))/img_num;
end
end

function ap = VOCap(rec,prec)
mrec=[0 ; rec ; 1];
mpre=[0 ; prec ; 0];
for i=numel(mpre)-1:-1:1
    mpre(i)=max(mpre(i),mpre(i+1));
end
i=find(mrec(2:end)~=mrec(1:end-1))+1;
ap=sum((mrec(i)-mrec(i-1)).*mpre(i));
end
