# LG-FrontierAI homepage

统一维护 LG-FrontierAI 各项目的主页源码与网页资源。

项目入口：<https://lg-frontierai.github.io/homepage/>

| 项目目录 | 独立项目页面 | 原官网 |
| --- | --- | --- |
| [oridynamic](oridynamic/) | [OriDynamic](https://lg-frontierai.github.io/homepage/oridynamic/) | [oridynamics.github.io](https://oridynamics.github.io/) |

各项目使用独立子目录。OriDynamic 的研究代码由组织内的 `OriDynamic` 仓库维护。

## 自动发布

GitHub Pages 使用本仓库的 GitHub Actions 工作流 `.github/workflows/pages.yml`。

更新 `main` 分支上的 OriDynamic 文件、入口页面或部署脚本后，工作流会自动构建和校验资源，将 `_site/` 部署到组织网址。也可以在 Actions 中手动运行 **Deploy project homepages**。

原官网仍由 `oridynamics/oridynamics.github.io` 仓库独立发布；本工作流只更新组织网址。

首次导入对应原官网提交 `5e98e84a3dfa700671224eb8268491d68e2f8dd5`，目前已适配组织网站的子目录地址。

## 本地构建与预览

需要 Python 3.10 或更高版本，仅使用标准库。

```sh
python3 build_pages.py
python3 oridynamic/preview_server.py --directory _site --port 4188
```

打开 <http://localhost:4188/oridynamic/>。生成的 `_site/` 仅用于部署，不需要提交。

单独预览 OriDynamic：

```sh
python3 oridynamic/build.py
python3 oridynamic/preview_server.py --port 4187
```

维护说明见 [oridynamic/README.md](oridynamic/README.md)。

## 增加项目

新项目使用独立目录，在 `build_pages.py` 的 `PROJECTS` 中登记，并添加入口页面链接及工作流路径触发条件。每个项目的 `build.py` 应读取 `SITE_URL` 并生成 `dist/`。

## 第三方资源

图标来源及许可证见 `oridynamic/icons/`。主视频中的音乐署名与许可链接见 `oridynamic/video-music-credits.txt`；这些署名也保留在网页中。
