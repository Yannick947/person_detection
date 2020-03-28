function norm_pred_list = norm_score(pred_list)

norm_pred_list = pred_list;
max_score = realmin('single');
min_score = realmax('single');

parfor j = 1:size(pred_list,1)
    if(isempty(pred_list{j}))
        continue;
    end
    score_list = pred_list{j}(:,5);
    max_score = max(max_score,max(score_list));
    min_score = min(min_score,min(score_list));
end

fprintf('Norm prediction\n');
parfor j = 1:size(pred_list,1)
    if(isempty(pred_list{j}))
        continue;
    end
    score_list = pred_list{j}(:,5);
    norm_score_list = (score_list - min_score)/(max_score - min_score);
    norm_pred_list{j}(:,5) = norm_score_list;
end