# import torch
import torch.multiprocessing as mp
from torch.utils.data.distributed import DistributedSampler
from torch.utils.data import DataLoader
import os

from main import deal
from mulu import redeal

world_size = 2
# dir_path = r"E:\pythonProject\工大目录抽取数据集"
# output_path = r"E:\pythonProject\pdf_txt"
# fail_path = r"E:\pythonProject\failed_file.txt"
dir_path = r"E:\pythonProject\工大目录抽取数据集"
txt_path = r"E:\pythonProject\CED_txt\pdf_txt_old"
output_path = r"E:\pythonProject\CED_txt\pdf_txt_new"
fail_path = r"E:\pythonProject\failed_file.txt"

def find_all_pdfs(root_dir):
    pdf_paths = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith(".pdf"):
                pdf_paths.append(file)
    return pdf_paths

class Dataset():
    def __init__(self, dir_path):
        self.files = find_all_pdfs(dir_path)
    
    def __len__(self):
        return len(self.files)
    
    def __getitem__(self, index):
        return self.files[index]

def deal_fn(rank, world_size):
    dataset = Dataset(dir_path)
    sampler = DistributedSampler(dataset, num_replicas=world_size, rank=rank)
    dataloader = DataLoader(dataset, batch_size=1, sampler=sampler)
    # for file in dataloader:
    #     out_path = os.path.join(output_path, file[0][:-3] + "txt")
    #     pdf_path = os.path.join(dir_path, file[0])
    #     if not os.path.exists(out_path):
    #         try:
    #             deal(pdf_path, out_path)
    #         except:
    #             with open(fail_path, "a", encoding="utf-8") as f:
    #                 f.write(f"{pdf_path}\n")
    for file in dataloader:
        old_path = os.path.join(txt_path, file[0][:-3] + "txt")
        new_path = os.path.join(output_path, file[0][:-3] + "txt")
        pdf_path = os.path.join(dir_path, file[0])
        if not os.path.exists(new_path):
            try:
                redeal(pdf_path, old_path, new_path)
            except:
                with open(fail_path, "a", encoding="utf-8") as f:
                    f.write(f"{pdf_path}\n")


if __name__ == '__main__':
    os.makedirs(output_path, exist_ok=True)
    # os.makedirs(fail_path, exist_ok=True)
    mp.spawn(deal_fn,
                args=(world_size,),
                nprocs=world_size,
                join=True)