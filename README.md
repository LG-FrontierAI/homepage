# LG-FrontierAI homepage

统一维护组织各项目的公开主页。当前项目为 **OriDynamics**。

- 项目主页：https://lg-frontierai.github.io/homepage/oridynamics/
- 项目入口：https://lg-frontierai.github.io/homepage/
- 研究代码：https://github.com/LG-FrontierAI/oridynamics

## 目录

```text
homepage/
├── oridynamics/                 # OriDynamics 文案、构建代码、样式及媒体
├── index.html                   # 组织项目入口
├── build_pages.py               # 构建并检查全部网页资源
└── .github/workflows/pages.yml  # main 推送后自动发布 GitHub Pages
```

2026-11-08 根据最新本地版本重建：OriDynamics 品牌、新摘要、新主视频与封面；Applications 依次为 BbFpn、BsPPase、FAK。旧 `oridynamic/` 项目内容已移除，历史提交可供回退；旧网站地址自动跳转至 `oridynamics/`。

## 构建和发布

仅需 Python 3.10+ 标准库，无需原始 PDF 或视频编辑软件。

```sh
python3 build_pages.py
python3 oridynamics/preview_server.py --directory _site --port 4188
```

预览：http://localhost:4188/oridynamics/ 。`_site/` 为忽略的生成目录，不提交。

更新 `oridynamics/` 后提交并推送 `main`，GitHub Actions 自动构建、校验资源并发布。也可手动执行 **Deploy project homepages** 工作流。网页公开访问无需 GitHub 登录。

维护细节见 [oridynamics/README.md](oridynamics/README.md)。原 https://oridynamics.github.io/ 使用另一个仓库独立发布，本仓库不会自动更新该网址。

## 新增项目

将新项目放入独立子目录，在 `build_pages.py` 的 `PROJECTS` 中登记，并更新入口链接及工作流路径。项目的 `build.py` 应读取 `SITE_URL` 并生成 `dist/`。

## 资源许可

保留页面配乐署名及 `oridynamics/video-music-credits.txt`。图标来源和许可证位于 `oridynamics/icons/`；本次重建未为项目内容新增许可证。
