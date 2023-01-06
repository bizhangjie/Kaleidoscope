import torch # 如果pytorch安装成功即可导入
print(torch.__version__) # 打印pytorch版本号
print(torch.cuda.is_available()) # 查看CUDA是否可用
print(torch.cuda.device_count()) # 查看可用的CUDA数量
print(torch.version.cuda) # 查看CUDA的版本号
print(torch.cuda.get_device_name(0)) # 查看第0块GPU的名称
print(torch.cuda.current_device()) # 查看当前使用的GPU编号
print(torch.cuda.memory_allocated()) # 查看当前GPU的显存占用
print(torch.cuda.memory_cached()) # 查看当前GPU的显存缓存


# https://zhuanlan.zhihu.com/p/586937647
# cuda的版本号是指pytorch的cuda版本号。如果你前面那个cuda可用是False，需要重装pytorch，因为你很可能从错误的源安装了pytorch