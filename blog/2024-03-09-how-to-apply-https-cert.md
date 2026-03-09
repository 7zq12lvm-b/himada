---
title: 使用 acme.sh 自动申请 HTTPS 证书（腾讯云 DNS 方案）
authors: [mingqiang]
tags: [HTTPS, SSL, acme.sh, 腾讯云, 运维]
---

本文介绍如何使用 `acme.sh` 客户端，通过腾讯云 DNS 验证方式自动申请并续期 SSL 证书。

<!--truncate-->

## 1. 什么是 acme.sh？

[acme.sh](https://github.com/acmesh-official/acme.sh) 是一个支持 ACME 协议的流行客户端，它可以实现 SSL 证书的自动申请、安装以及到期后的自动续期。

## 2. 安装 acme.sh

### 全新安装
运行以下命令安装：

```bash
curl https://get.acme.sh | sh -s email=my@3455432.xyz
```

### 升级现有版本
如果你已经安装过，可以运行以下命令升级：

```bash
acme.sh --upgrade
```

## 3. 获取腾讯云 API 密钥

为了让 `acme.sh` 能够自动添加 DNS 解析记录以通过验证，你需要准备腾讯云的 API 密钥。

1.  登录 [腾讯云访问管理控制台](https://console.cloud.tencent.com/cam/capi)。
2.  新建或获取现有的 `SecretId` 和 `SecretKey`。
    *   *建议：为了安全，可以创建一个仅具有 DNS 修改权限的子账号（CAM 策略建议包含 `dnspod:DescribeRecordList`, `dnspod:CreateRecord`, `dnspod:DeleteRecord` 等权限）。*

## 4. 申请证书

官方教程: https://docs.dnspod.cn/dns/acme-sh/

### 设置环境变量
将获取到的密钥导入环境变量（仅需执行一次，acme.sh 会自动记录到配置文件中）：

```bash
export Tencent_SecretId="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
export Tencent_SecretKey="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

或者编辑 cat ~/.acme.sh/account.conf
```bash
SAVED_Tencent_SecretId='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
SAVED_Tencent_SecretKey='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
```
### 执行申请命令

```bash
acme.sh --issue --dns dns_tencent -d "*.3455432.xyz" -d "3455432.xyz"
```

执行成功后，证书文件将保存在 `~/.acme.sh/3455432.xyz/` 目录下。

## 5. 安装证书到 Web 服务器

`acme.sh` 建议通过 `--install-cert` 命令将证书安装到指定位置，而不是直接引用其内部目录。

### Nginx 示例

```bash
acme.sh --install-cert -d 3455432.xyz \
--key-file       /etc/nginx/ssl/3455432.xyz.key \
--fullchain-file /etc/nginx/ssl/fullchain.cer \
--reloadcmd     "service nginx force-reload"
```

### Nginx 配置参考

在你的 Nginx 配置文件中，引用刚才安装的路径：

```nginx
server {
    listen 443 ssl http2;
    server_name 3455432.xyz;

    ssl_certificate /etc/nginx/ssl/fullchain.cer;
    ssl_certificate_key /etc/nginx/ssl/3455432.xyz.key;

    ssl_protocols TLSv1.2 TLSv1.3;
    # ... 其他安全配置
}
```

## 6. 自动续期
`acme.sh` 安装时会自动创建 crontab 定时任务，每 60 天会自动尝试续期证书，无需人工干预。
