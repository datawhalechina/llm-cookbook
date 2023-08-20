import os, sys
import random
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from tqdm.auto import tqdm
from matplotlib.animation import FuncAnimation, PillowWriter
from PIL import Image
from torch.utils.data import DataLoader, Dataset
from torchvision.utils import make_grid, save_image

#定义模型的运算方式
def get_device():
    "Pick GPU if cuda is available, mps if Mac, else CPU"
    if torch.cuda.is_available():
        return torch.device("cuda")
    elif sys.platform == "darwin" and torch.backends.mps.is_available():
        return torch.device("mps")
    else:
        return torch.device("cpu")

def _fig_bounds(x):
    r = x//32
    return min(5, max(1,r))
#展示图片的方法
def show_image(im, ax=None, figsize=None, title=None, **kwargs):
    "Show a PIL or PyTorch image on `ax`."
    cmap=None
    # Handle pytorch axis order
    if isinstance(im, torch.Tensor):
        im = im.data.cpu()
        if im.shape[0]<5: im=im.permute(1,2,0)
    elif not isinstance(im, np.ndarray): 
        im=np.array(im)
    # Handle 1-channel images
    if im.shape[-1]==1: 
        cmap = "gray"
        im=im[...,0]
    
    if figsize is None: 
        figsize = (_fig_bounds(im.shape[0]), _fig_bounds(im.shape[1]))
    if ax is None: 
        _,ax = plt.subplots(figsize=figsize)
    ax.imshow(im, cmap=cmap, **kwargs)
    if title is not None: 
        ax.set_title(title)
    ax.axis('off')
    return ax

class ContextUnet(nn.Module):
    def __init__(self, in_channels, n_feat=256, n_cfeat=10, height=28):  # cfeat - 上下文特征
        super(ContextUnet, self).__init__()

        # 输入通道数、中间特征图数和类数
        self.in_channels = in_channels
        self.n_feat = n_feat
        self.n_cfeat = n_cfeat
        self.h = height  #假设 h == w。 必须能被 4 整除，所以 28,24,20,16...

        # 初始化初始卷积层
        self.init_conv = ResidualConvBlock(in_channels, n_feat, is_res=True)

        # 用两个级别初始化U-Net的下采样路径
        self.down1 = UnetDown(n_feat, n_feat)        # 第一个下采样层#[10, 256, 8, 8]
        self.down2 = UnetDown(n_feat, 2 * n_feat)    # 第一个下采样层 #[10, 256, 4,  4]
        
         # original: self.to_vec = nn.Sequential(nn.AvgPool2d(7), nn.GELU())
        self.to_vec = nn.Sequential(nn.AvgPool2d((4)), nn.GELU())

        # 使用一层全连接神经网络嵌入时间步长和上下文标签
        self.timeembed1 = EmbedFC(1, 2*n_feat)
        self.timeembed2 = EmbedFC(1, 1*n_feat)
        self.contextembed1 = EmbedFC(n_cfeat, 2*n_feat)
        self.contextembed2 = EmbedFC(n_cfeat, 1*n_feat)

        # 初始化U-Net的三层上采样路径
        self.up0 = nn.Sequential(
            nn.ConvTranspose2d(2 * n_feat, 2 * n_feat, self.h//4, self.h//4), # 上采样
            nn.GroupNorm(8, 2 * n_feat), # 归一化                      
            nn.ReLU(),
        )
        self.up1 = UnetUp(4 * n_feat, n_feat)
        self.up2 = UnetUp(2 * n_feat, n_feat)

        # 初始化最终的卷积层以映射到与输入图像相同数量的通道
        self.out = nn.Sequential(
            nn.Conv2d(2 * n_feat, n_feat, 3, 1, 1), # 减少特征图数量#in_channels、out_channels、kernel_size、stride=1、padding=0
            nn.GroupNorm(8, n_feat), # 归一化
            nn.ReLU(),
            nn.Conv2d(n_feat, self.in_channels, 3, 1, 1), # 映射到与输入相同数量的通道
        )

    def forward(self, x, t, c=None):
        """
        x : (batch, n_feat, h, w) : input image
        t : (batch, n_cfeat)      : time step
        c : (batch, n_classes)    : context label
        """
        # x 是输入图像，c 是上下文标签，t 是时间步长，context_mask 表示要阻止上下文的样本

        # 将输入图像传递给初始卷积层
        x = self.init_conv(x)
        # 将结果通过下采样路径传递
        down1 = self.down1(x)       #[10, 256, 8, 8]
        down2 = self.down2(down1)   #[10, 256, 4, 4]
        
        # 将特征图转换为向量并应用激活
        hiddenvec = self.to_vec(down2)
        
        # 如果 context_mask == 1，则屏蔽上下文
        if c is None:
            c = torch.zeros(x.shape[0], self.n_cfeat).to(x)
            
        # 嵌入上下文和时间步长
        cemb1 = self.contextembed1(c).view(-1, self.n_feat * 2, 1, 1)     # (batch, 2*n_feat, 1,1)
        temb1 = self.timeembed1(t).view(-1, self.n_feat * 2, 1, 1)
        cemb2 = self.contextembed2(c).view(-1, self.n_feat, 1, 1)
        temb2 = self.timeembed2(t).view(-1, self.n_feat, 1, 1)
        #print(f"uunet forward: cemb1 {cemb1.shape}. temb1 {temb1.shape}, cemb2 {cemb2.shape}. temb2 {temb2.shape}")


        up1 = self.up0(hiddenvec)
        up2 = self.up1(cemb1*up1 + temb1, down2)  # 加法和乘法嵌入
        up3 = self.up2(cemb2*up2 + temb2, down1)
        out = self.out(torch.cat((up3, x), 1))
        return out

class ResidualConvBlock(nn.Module):
    def __init__(
        self, in_channels: int, out_channels: int, is_res: bool = False
    ) -> None:
        super().__init__()

        # 检查剩余连接的输入和输出通道是否相同
        self.same_channels = in_channels == out_channels

        # 是否使用剩余连接的标志
        self.is_res = is_res

        # 第一个卷积层
        self.conv1 = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, 3, 1, 1),   # 3x3 内核，步幅为 1，填充为 1
            nn.BatchNorm2d(out_channels),   # 批量归一化
            nn.GELU(),   # GELU激活函数
        )

        # 第二个卷积层
        self.conv2 = nn.Sequential(
            nn.Conv2d(out_channels, out_channels, 3, 1, 1),   # 3x3 内核，步幅为 1，填充为 1
            nn.BatchNorm2d(out_channels),   # 批量归一化
            nn.GELU(),   # GELU激活函数
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:

        # 如果使用剩余连接
        if self.is_res:
            # 应用第一个卷积层
            x1 = self.conv1(x)

            # 应用第二个卷积层
            x2 = self.conv2(x1)

            # 如果输入输出通道相同，则直接添加残差连接
            if self.same_channels:
                out = x + x2
            else:
                # 如果没有，则在添加残差连接之前应用 1x1 卷积层来匹配维度
                shortcut = nn.Conv2d(x.shape[1], x2.shape[1], kernel_size=1, stride=1, padding=0).to(x.device)
                out = shortcut(x) + x2
            #print(f"resconv forward: x {x.shape}, x1 {x1.shape}, x2 {x2.shape}, out {out.shape}")

            # 标准化输出张量
            return out / 1.414

        # 如果不使用残差连接，则返回第二个卷积层的输出
        else:
            x1 = self.conv1(x)
            x2 = self.conv2(x1)
            return x2

    # 获取该块的输出通道数的方法
    def get_out_channels(self):
        return self.conv2[0].out_channels

    # 设置该块的输出通道数的方法
    def set_out_channels(self, out_channels):
        self.conv1[0].out_channels = out_channels
        self.conv2[0].in_channels = out_channels
        self.conv2[0].out_channels = out_channels

        

class UnetUp(nn.Module):
    def __init__(self, in_channels, out_channels):
        super(UnetUp, self).__init__()
        
        # 为上采样块创建层列表
        # 该块包含一个用于上采样的 ConvTranspose2d 层，后面是两个 ResidualConvBlock 层
        layers = [
            nn.ConvTranspose2d(in_channels, out_channels, 2, 2),
            ResidualConvBlock(out_channels, out_channels),
            ResidualConvBlock(out_channels, out_channels),
        ]
        
        # 使用图层创建顺序模型
        self.model = nn.Sequential(*layers)

    def forward(self, x, skip):
        # 将输入张量 x 与沿通道维度的跳跃连接张量连接起来
        x = torch.cat((x, skip), 1)
        
        # 将连接的张量传递给顺序模型并返回输出
        x = self.model(x)
        return x

    
class UnetDown(nn.Module):
    def __init__(self, in_channels, out_channels):
        super(UnetDown, self).__init__()
        
        # 为下采样块创建层列表
        # 每个块由两个 ResidualConvBlock 层组成，后面是一个用于下采样的 MaxPool2d 层
        layers = [ResidualConvBlock(in_channels, out_channels), ResidualConvBlock(out_channels, out_channels), nn.MaxPool2d(2)]
        
        # 使用图层创建顺序模型
        self.model = nn.Sequential(*layers)

    def forward(self, x):
        # 将输入传递给顺序模型并返回输出
        return self.model(x)

class EmbedFC(nn.Module):
    def __init__(self, input_dim, emb_dim):
        super(EmbedFC, self).__init__()
        '''
        这个类定义了一个通用的单层前馈神经网络，用于嵌入输入数据
         维度 input_dim 到维度 emb_dim 的嵌入空间。
        '''
        self.input_dim = input_dim
        
        # 定义网络层
        layers = [
            nn.Linear(input_dim, emb_dim),
            nn.GELU(),
            nn.Linear(emb_dim, emb_dim),
        ]
        
        # 创建由定义的层组成的 PyTorch 顺序模型
        self.model = nn.Sequential(*layers)

    def forward(self, x):
        # 展平输入张量
        x = x.view(-1, self.input_dim)
        # 将模型层应用于展平张量
        return self.model(x)
    
def unorm(x):
    # 统一规范。 结果范围为 [0,1]
    # 设定 x (h,w,3)
    xmax = x.max((0,1))
    xmin = x.min((0,1))
    return(x - xmin)/(xmax - xmin)

def norm_all(store, n_t, n_s):
    # 对所有样本的所有时间步运行统一范数
    nstore = np.zeros_like(store)
    for t in range(n_t):
        for s in range(n_s):
            nstore[t,s] = unorm(store[t,s])
    return nstore

def norm_torch(x_all):
    # 对所有样本的所有时间步运行统一范数
    # 输入是 (n_samples, 3,h,w)，torch图像格式
    x = x_all.cpu().numpy()
    xmax = x.max((2,3))
    xmin = x.min((2,3))
    xmax = np.expand_dims(xmax,(2,3)) 
    xmin = np.expand_dims(xmin,(2,3))
    nstore = (x - xmin)/(xmax - xmin)
    return torch.from_numpy(nstore)

def gen_tst_context(n_cfeat):
    """
    生成测试上下文向量
    """
    vec = torch.tensor([
    [1,0,0,0,0], [0,1,0,0,0], [0,0,1,0,0], [0,0,0,1,0], [0,0,0,0,1],  [0,0,0,0,0],      # human, non-human, food, spell, side-facing
    [1,0,0,0,0], [0,1,0,0,0], [0,0,1,0,0], [0,0,0,1,0], [0,0,0,0,1],  [0,0,0,0,0],      # human, non-human, food, spell, side-facing
    [1,0,0,0,0], [0,1,0,0,0], [0,0,1,0,0], [0,0,0,1,0], [0,0,0,0,1],  [0,0,0,0,0],      # human, non-human, food, spell, side-facing
    [1,0,0,0,0], [0,1,0,0,0], [0,0,1,0,0], [0,0,0,1,0], [0,0,0,0,1],  [0,0,0,0,0],      # human, non-human, food, spell, side-facing
    [1,0,0,0,0], [0,1,0,0,0], [0,0,1,0,0], [0,0,0,1,0], [0,0,0,0,1],  [0,0,0,0,0],      # human, non-human, food, spell, side-facing
    [1,0,0,0,0], [0,1,0,0,0], [0,0,1,0,0], [0,0,0,1,0], [0,0,0,0,1],  [0,0,0,0,0]]      # human, non-human, food, spell, side-facing
    )
    return len(vec), vec

def plot_grid(x,n_sample,n_rows,save_dir,w):
    # x:(n_sample, 3, h, w)
    ncols = n_sample//n_rows
    grid = make_grid(norm_torch(x), nrow=ncols)  # n_rows是列数..或行中的项目数。
    save_image(grid, save_dir + f"run_image_w{w}.png")
    print('saved image at ' + save_dir + f"run_image_w{w}.png")
    return grid

def plot_sample(x_gen_store,n_sample,nrows,save_dir, fn,  w, save=False):
    ncols = n_sample//nrows
    sx_gen_store = np.moveaxis(x_gen_store,2,4)                               # 更改为 Numpy 图像格式 (h,w,channels) 与 (channels,h,w)
    nsx_gen_store = norm_all(sx_gen_store, sx_gen_store.shape[0], n_sample)   # np.imshow 的统一范数置于 [0,1] 范围内
    
    # 基于 x_gen_store 创建随时间演变的 gif 图像
    fig, axs = plt.subplots(nrows=nrows, ncols=ncols, sharex=True, sharey=True,figsize=(ncols,nrows))
    def animate_diff(i, store):
        print(f'gif animating frame {i} of {store.shape[0]}', end='\r')
        plots = []
        for row in range(nrows):
            for col in range(ncols):
                axs[row, col].clear()
                axs[row, col].set_xticks([])
                axs[row, col].set_yticks([])
                plots.append(axs[row, col].imshow(store[i,(row*ncols)+col]))
        return plots
    ani = FuncAnimation(fig, animate_diff, fargs=[nsx_gen_store],  interval=200, blit=False, repeat=True, frames=nsx_gen_store.shape[0]) 
    plt.close()
    if save:
        ani.save(save_dir + f"{fn}_w{w}.gif", dpi=100, writer=PillowWriter(fps=5))
        print('saved gif at ' + save_dir + f"{fn}_w{w}.gif")
    return ani


default_tfms = transforms.Compose([
    transforms.ToTensor(),                # 从 [0,255] 到范围 [0.0,1.0]
    transforms.RandomHorizontalFlip(),    # 随机翻转和旋转
    transforms.Normalize((0.5,), (0.5,))  # 范围 [-1,1]
])

class CustomDataset(Dataset):
    def __init__(self, sprites, slabels, transform=default_tfms, null_context=False, argmax=False):
        self.sprites = sprites
        if argmax:
            self.slabels = np.argmax(slabels, axis=1)
        else:
            self.slabels = slabels
        self.transform = transform
        self.null_context = null_context

    @classmethod
    def from_np(cls, 
                path, 
                sfilename="sprites_1788_16x16.npy", lfilename="sprite_labels_nc_1788_16x16.npy", transform=default_tfms, null_context=False, argmax=False):
        sprites = np.load(Path(path)/sfilename)
        slabels = np.load(Path(path)/lfilename)
        return cls(sprites, slabels, transform, null_context, argmax)

    # 返回数据集中的图像数量
    def __len__(self):
        return len(self.sprites)
    
    # 获取给定索引处的图像和标签
    def __getitem__(self, idx):
        # 以元组形式返回图像和标签
        if self.transform:
            image = self.transform(self.sprites[idx])
            if self.null_context:
                label = torch.tensor(0).to(torch.int64)
            else:
                label = torch.tensor(self.slabels[idx]).to(torch.int64)
        return (image, label)
    

    def subset(self, slice_size=1000):
        # 返回数据集的子集
        indices = random.sample(range(len(self)), slice_size)
        return CustomDataset(self.sprites[indices], self.slabels[indices], self.transform, self.null_context)

    def split(self, pct=0.2):
        "split dataset into train and test"
        train_size = int((1-pct)*len(self))
        test_size = len(self) - train_size
        train_dataset, test_dataset = torch.utils.data.random_split(self, [train_size, test_size])
        return train_dataset, test_dataset

def get_dataloaders(data_dir, batch_size, slice_size=None, valid_pct=0.2):
    "Get train/val dataloaders for classification on sprites dataset"
    dataset = CustomDataset.from_np(Path(data_dir), argmax=True)
    if slice_size:
        dataset = dataset.subset(slice_size)

    train_ds, valid_ds = dataset.split(valid_pct)

    train_dl = DataLoader(train_ds, batch_size=batch_size, shuffle=True, num_workers=1)    
    valid_dl = DataLoader(valid_ds, batch_size=batch_size, shuffle=False, num_workers=1)

    return train_dl, valid_dl


## 扩散函数

def setup_ddpm(beta1, beta2, timesteps, device):
    # 构建 DDPM 噪声表和采样函数
    b_t = (beta2 - beta1) * torch.linspace(0, 1, timesteps + 1, device=device) + beta1
    a_t = 1 - b_t
    ab_t = torch.cumsum(a_t.log(), dim=0).exp()    
    ab_t[0] = 1

    # 辅助函数：将图像扰乱到指定的噪声水平
    def perturb_input(x, t, noise):
        return ab_t.sqrt()[t, None, None, None] * x + (1 - ab_t[t, None, None, None]) * noise

    # 辅助功能； 消除预测的噪声（但添加一些噪声以避免崩溃）
    def _denoise_add_noise(x, t, pred_noise, z=None):
        if z is None:
            z = torch.randn_like(x)
        noise = b_t.sqrt()[t] * z
        mean = (x - pred_noise * ((1 - a_t[t]) / (1 - ab_t[t]).sqrt())) / a_t[t].sqrt()
        return mean + noise

    # 使用标准算法的上下文样本
    # 我们对原始算法进行了更改，以明确地考虑上下文（噪音）
    @torch.no_grad()
    def sample_ddpm_context(nn_model, noises, context, save_rate=20):
        # 数组来跟踪生成的绘图步骤
        intermediate = [] 
        pbar = tqdm(range(timesteps, 0, -1), leave=False)
        for i in pbar:
            pbar.set_description(f'sampling timestep {i:3d}')

            # 重塑时间张量
            t = torch.tensor([i / timesteps])[:, None, None, None].to(noises.device)

            # 采样一些随机噪声以注入回。对于 i = 1，不要添加回噪声
            z = torch.randn_like(noises) if i > 1 else 0

            eps = nn_model(noises, t, c=context)    # 预测噪声 e_(x_t,t, ctx)
            noises = _denoise_add_noise(noises, i, eps, z)
            if i % save_rate==0 or i==timesteps or i<8:
                intermediate.append(noises.detach().cpu().numpy())

        intermediate = np.stack(intermediate)
        return noises.clip(-1, 1), intermediate
    
    return perturb_input, sample_ddpm_context


def setup_ddim(beta1, beta2, timesteps, device):
    # 为 DDIM 定义采样函数 
    b_t = (beta2 - beta1) * torch.linspace(0, 1, timesteps + 1, device=device) + beta1
    a_t = 1 - b_t
    ab_t = torch.cumsum(a_t.log(), dim=0).exp()    
    ab_t[0] = 1
    # 使用 ddim 消除噪声
    def denoise_ddim(x, t, t_prev, pred_noise):
        ab = ab_t[t]
        ab_prev = ab_t[t_prev]
        
        x0_pred = ab_prev.sqrt() / ab.sqrt() * (x - (1 - ab).sqrt() * pred_noise)
        dir_xt = (1 - ab_prev).sqrt() * pred_noise

        return x0_pred + dir_xt
    
    # 带上下文的快速采样算法
    @torch.no_grad()
    def sample_ddim_context(nn_model, noises, context, n=25): 
        # 数组来跟踪生成的绘图步骤
        intermediate = [] 
        step_size = timesteps // n
        pbar=tqdm(range(timesteps, 0, -step_size), leave=False)
        for i in pbar:
            pbar.set_description(f'sampling timestep {i:3d}')

            # 重塑时间张量
            t = torch.tensor([i / timesteps])[:, None, None, None].to(device)

            eps = nn_model(noises, t, c=context)    # 预测噪声 e_(x_t,t)
            noises = denoise_ddim(noises, i, i - step_size, eps)
            intermediate.append(noises.detach().cpu().numpy())

        intermediate = np.stack(intermediate)
        return noises.clip(-1, 1), intermediate
    
    return sample_ddim_context

def to_classes(ctx_vector):
    classes = "hero,non-hero,food,spell,side-facing".split(",")
    return [classes[i] for i in ctx_vector.argmax(dim=1)]