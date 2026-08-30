import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
from torch.utils.data import DataLoader, random_split
import matplotlib.pyplot as plt
import numpy as np
import os

# 设置随机种子，保证结果可复现
torch.manual_seed(42)
np.random.seed(42)

# 检查设备
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

#1. 数据预处理
# 训练集数据增强：随机水平翻转、随机裁剪（填充后裁剪回32x32）、转为Tensor、归一化
transform_train = transforms.Compose([
    transforms.RandomHorizontalFlip(),          # 随机水平翻转，增加数据多样性
    transforms.RandomCrop(32, padding=4),       # 随机裁剪：先填充4像素再随机裁剪32x32
    transforms.ToTensor(),
    transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010))
])

# 验证集和测试集仅进行归一化，不进行数据增强
transform_test = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010))
])

# 本地数据集路径（包含 cifar-10-batches-py 的根目录）
data_root = r'D:\DDesktop\cifar-10-python'

# 检查路径是否存在
if not os.path.exists(data_root):
    raise FileNotFoundError(f"数据集路径不存在: {data_root}")

# 加载原始训练集和测试集（训练集使用增强，测试集使用普通变换）
full_trainset = torchvision.datasets.CIFAR10(root=data_root, train=True, download=False, transform=transform_train)
testset = torchvision.datasets.CIFAR10(root=data_root, train=False, download=False, transform=transform_test)

# 划分训练集和验证集：从 50000 张训练图片中随机选 10% 作为验证集
val_ratio = 0.1
val_size = int(len(full_trainset) * val_ratio)
train_size = len(full_trainset) - val_size
train_subset, val_subset = random_split(full_trainset, [train_size, val_size])

print(f"训练集大小: {train_size}, 验证集大小: {val_size}, 测试集大小: {len(testset)}")

# 创建数据加载器
batch_size = 64
trainloader = DataLoader(train_subset, batch_size=batch_size, shuffle=True, num_workers=0)
valloader = DataLoader(val_subset, batch_size=batch_size, shuffle=False, num_workers=0)
testloader = DataLoader(testset, batch_size=batch_size, shuffle=False, num_workers=0)

# 类别名称
classes = ('plane', 'car', 'bird', 'cat', 'deer',
           'dog', 'frog', 'horse', 'ship', 'truck')

# -------------------- 2. 搭建改进版CNN模型 --------------------
class ImprovedCNN(nn.Module):
    """
    卷积神经网络结构：
    包含三个卷积块，每个块 = Conv2d + BatchNorm2d + ReLU + MaxPool2d
    之后展平，接两个全连接层（带Dropout）
    """
    def __init__(self, num_classes=10):
        super(ImprovedCNN, self).__init__()
        # 第一个卷积块：输入3通道，输出32通道
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(32)           # 批归一化，加速收敛，提高稳定性
        self.pool = nn.MaxPool2d(2, 2)          # 2x2最大池化，尺寸减半

        # 第二个卷积块：输入32通道，输出64通道
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(64)

        # 第三个卷积块：输入64通道，输出128通道
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.bn3 = nn.BatchNorm2d(128)

        # 全连接层：经过三次池化后特征图尺寸为 4x4（32->16->8->4），通道数128
        self.fc1 = nn.Linear(128 * 4 * 4, 256)
        self.fc2 = nn.Linear(256, num_classes)
        self.dropout = nn.Dropout(0.5)          # Dropout正则化
        self.relu = nn.ReLU()

    def forward(self, x):
        # 卷积块1
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.pool(x)        # 输出: (batch, 32, 16, 16)

        # 卷积块2
        x = self.conv2(x)
        x = self.bn2(x)
        x = self.relu(x)
        x = self.pool(x)        # 输出: (batch, 64, 8, 8)

        # 卷积块3
        x = self.conv3(x)
        x = self.bn3(x)
        x = self.relu(x)
        x = self.pool(x)        # 输出: (batch, 128, 4, 4)

        # 展平
        x = x.view(-1, 128 * 4 * 4)

        # 全连接层
        x = self.dropout(self.relu(self.fc1(x)))
        x = self.fc2(x)
        return x

# 实例化模型并移至设备
model = ImprovedCNN(num_classes=10).to(device)
print(model)

#3.损失函数与优化器
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)   # Adam优化器，初始学习率0.001
# 学习率调度器：每10个epoch学习率乘以0.5（这里总epoch=15，可调整）
scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.5)

#4.模型训练
num_epochs = 50                                 # 增加训练轮数
train_loss_history = []
train_acc_history = []
val_acc_history = []
test_acc_history = []

global_step = 0
print_every = 200

for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0
    correct_train = 0
    total_train = 0

    for i, (inputs, labels) in enumerate(trainloader):
        inputs, labels = inputs.to(device), labels.to(device)

        # 前向传播
        outputs = model(inputs)
        loss = criterion(outputs, labels)

        # 反向传播与优化
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # 统计
        running_loss += loss.item()
        _, predicted = torch.max(outputs, 1)
        total_train += labels.size(0)
        correct_train += (predicted == labels).sum().item()

        # 每200个batch打印损失
        global_step += 1
        if global_step % print_every == 0:
            print(f"Step {global_step}, Current Batch Loss: {loss.item():.4f}")

    epoch_loss = running_loss / len(trainloader)
    epoch_train_acc = 100 * correct_train / total_train
    train_loss_history.append(epoch_loss)
    train_acc_history.append(epoch_train_acc)

    # 验证集评估
    model.eval()
    correct_val = 0
    total_val = 0
    with torch.no_grad():
        for inputs, labels in valloader:
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            _, predicted = torch.max(outputs, 1)
            total_val += labels.size(0)
            correct_val += (predicted == labels).sum().item()
    epoch_val_acc = 100 * correct_val / total_val
    val_acc_history.append(epoch_val_acc)

    # 测试集评估
    correct_test = 0
    total_test = 0
    with torch.no_grad():
        for inputs, labels in testloader:
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            _, predicted = torch.max(outputs, 1)
            total_test += labels.size(0)
            correct_test += (predicted == labels).sum().item()
    epoch_test_acc = 100 * correct_test / total_test
    test_acc_history.append(epoch_test_acc)

    # 更新学习率
    scheduler.step()

    print(f"Epoch [{epoch+1}/{num_epochs}] "
          f"Train Loss: {epoch_loss:.4f} | "
          f"Train Acc: {epoch_train_acc:.2f}% | "
          f"Val Acc: {epoch_val_acc:.2f}% | "
          f"Test Acc: {epoch_test_acc:.2f}% | "
          f"LR: {scheduler.get_last_lr()[0]:.6f}")

print("训练完成！")

# -------------------- 5. 结果可视化 --------------------
# 5.1 绘制损失曲线和准确率曲线
plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.plot(range(1, num_epochs+1), train_loss_history, marker='o', label='Train Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Training Loss Curve')
plt.legend()
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(range(1, num_epochs+1), train_acc_history, marker='o', label='Train Accuracy')
plt.plot(range(1, num_epochs+1), val_acc_history, marker='^', label='Validation Accuracy')
plt.plot(range(1, num_epochs+1), test_acc_history, marker='s', label='Test Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy (%)')
plt.title('Accuracy Curves')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig('training_curves_improved.png')
plt.show()

# 5.2 可视化部分测试样本的预测结果
def imshow(img):
    img = img / 2 + 0.5     # 反归一化
    npimg = img.numpy()
    plt.imshow(np.transpose(npimg, (1, 2, 0)))
    plt.axis('off')

dataiter = iter(testloader)
images, labels = next(dataiter)

model.eval()
with torch.no_grad():
    images_device = images.to(device)
    outputs = model(images_device)
    _, predicted = torch.max(outputs, 1)
    predicted = predicted.cpu()

fig = plt.figure(figsize=(12, 8))
for idx in range(8):
    ax = fig.add_subplot(2, 4, idx+1, xticks=[], yticks=[])
    imshow(images[idx])
    title_color = 'green' if predicted[idx] == labels[idx] else 'red'
    ax.set_title(f"True: {classes[labels[idx]]}\nPred: {classes[predicted[idx]]}",
                 color=title_color)
plt.tight_layout()
plt.savefig('predictions_improved.png')
plt.show()