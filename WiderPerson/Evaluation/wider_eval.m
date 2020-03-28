%% WiderPerson Evaluation
% Conduct the evaluation on the WiderPerson validation set. 
%
% Shifeng Zhang July 2018

clear;
close all;

load widerperson_val_info.mat

%Please specify your algorithm name.
legend_name = 'vgg16_frcnn';

%Please specify your prediction directory.
pred_dir = './vgg16_frcnn';

%% Preprocessing
pred_list = read_pred(pred_dir, file_list);
norm_pred_list = norm_score(pred_list);

%% evaluate on different settings
setting_name_list = {'easy';'medium';'hard'};
setting_class = 'setting_int';
easy = evaluation(norm_pred_list,file_list,easy_gt_list,setting_name_list{1});
medium = evaluation(norm_pred_list,file_list,medium_gt_list,setting_name_list{2});
hard = evaluation(norm_pred_list,file_list,hard_gt_list,setting_name_list{3});

%% Display results
results = [easy;medium;hard];
results = round(results * 100, 2);
Recall = results(:,1);
AP = results(:,2);
MR = results(:,3);
Subset = {'Easy';'Medium';'Hard'};
T = table(Subset, Recall,AP,MR)
writetable(T, [pred_dir '/' legend_name '_eval_result.txt'], 'Delimiter', ' ');
