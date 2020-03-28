function pred_list = read_pred(file_dir, file_list)

img_num = length(file_list);
pred_list = cell(img_num,1);
for j = 1:img_num
    if ~exist(sprintf('%s/%s.txt',file_dir,file_list{j}),'file')
        fprintf('Can not find the prediction file %s \n',file_list{j});
        continue;
    end
    
    fid = fopen(sprintf('%s/%s.txt',file_dir,file_list{j}),'r');
    tmp = textscan(fid,'%s','Delimiter','\n');
    tmp = tmp{1};
    fclose(fid);
    try
        bbx_num = tmp{1,1};
        bbx_num = str2num(bbx_num);
        bbx = zeros(bbx_num,5);
        if bbx_num ==0
            continue;
        end
        for k = 1:bbx_num
            raw_info = str2num(tmp{k+1,1});
            bbx(k,1) = raw_info(1);
            bbx(k,2) = raw_info(2);
            bbx(k,3) = raw_info(3);
            bbx(k,4) = raw_info(4);
            bbx(k,5) = raw_info(5);
        end
        [~, s_index] = sort(bbx(:,5),'descend');
        pred_list{j} = bbx(s_index,:);
    catch
        fprintf('Invalid format %s\n',file_list{j});
    end
end
