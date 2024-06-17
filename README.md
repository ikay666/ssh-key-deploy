# ssh-key-deploy

## 简介

使用Python编写的一个在Windows上创建ssh密钥并且自动部署到Linux服务器上的小工具。

## 功能特点

- 创建具有自定义名称和可选密码的SSH密钥。
- 列出本地存储的所有SSH密钥。
- 将SSH密钥安全地上传到远程服务器。
- 使用直观的命令行界面进行操作，支持菜单导航。
- 友好地处理Ctrl+C中断操作，确保操作流畅。

## 使用方法

1. 克隆本仓库到本地计算机。
2. 运行 `python ssh_manager.py` 开始使用工具。
3. 根据屏幕提示进行操作，创建新密钥或上传现有密钥到远程服务器。

## 环境要求

- Python 3.x
- paramiko库（用于SSH操作）

## 安装步骤

1. 克隆本仓库到本地：

   ```bash
   git clone https://github.com/your-username/ssh-key-manager.git
   cd ssh-key-manager

## 详细使用教程

[我的博客：https://www.cnblogs.com/ikay/p/18253224](https://www.cnblogs.com/ikay/p/18253224)