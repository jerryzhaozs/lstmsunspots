import jieba
from tqdm import tqdm
import multiprocessing

tmp_catalog = 'C:/Users/Administrator/Desktop/dogcat/cnews/'
# file_list = [tmp_catalog+'cnews.train.txt', tmp_catalog+'cnews.test.txt', tmp_catalog+'cnews.val.txt']
# write_list = [tmp_catalog+'train_token.txt', tmp_catalog+'test_token.txt', tmp_catalog+'val_token.txt']
file_list = [tmp_catalog+'cnews.train.txt']
write_list = [tmp_catalog+'train_token.txt']

def tokenFile(file_path, write_path):
    with open(write_path, 'w', encoding='utf-8') as w:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in tqdm(f.readlines(), desc=f"Processing {file_path}", ncols=80):
                line = line.strip()
                label, text = line.split('\t')
                seg_list = jieba.cut(text)
                seg_text = ' '.join(seg_list)
                w.write(label + '\t' + seg_text + '\n') 
    print(file_path + ' has been token and token_file_name is ' + write_path)

if __name__ == '__main__':
    pool = multiprocessing.Pool(processes=3)  # 创建进程池
    for file_path, write_path in zip(file_list, write_list):
        pool.apply_async(tokenFile, (file_path, write_path))  # 异步执行任务
    pool.close()  # 关闭进程池
    pool.join()  # 等待所有进程执行完毕
    print("All files have been tokenized.")
