# LG-FrontierAI homepage

统一维护 LG-FrontierAI 各项目的主页源码与网页资源。

| 项目目录 | 当前官网 | 发布仓库 |
| --- | --- | --- |
| [oridynamic](oridynamic/) | [oridynamics.github.io](https://oridynamics.github.io/) | [oridynamics/oridynamics.github.io](https://github.com/oridynamics/oridynamics.github.io) |

各项目使用独立子目录。OriDynamic 的研究代码由组织内的 `OriDynamic` 仓库维护。

## 当前状态

首次导入的是 2026-11-06 的当前主页版本，网页输出与官网发布提交 `5e98e84a3dfa700671224eb8268491d68e2f8dd5` 一致。

本仓库存放可构建源码、当前网页及其图片/视频资源。当前官网仍由原发布仓库提供；跨仓库自动部署尚未配置。提交到本仓库不会自动更新官网。

## 本地构建与预览

需要 Python 3.10 或更高版本，仅使用标准库。

```sh
python3 oridynamic/build.py
python3 oridynamic/preview_server.py --port 4187
```

打开 <http://localhost:4187/>。维护说明见 [oridynamic/README.md](oridynamic/README.md)。

## 第三方资源

图标来源及许可证见 `oridynamic/icons/`。主视频中的音乐署名与许可链接见 `oridynamic/video-music-credits.txt`；这些署名也保留在网页中。
