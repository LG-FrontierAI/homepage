# OriDynamics 主页

**Towards a World Model for Biomolecular Dynamics**

公开访问：https://lg-frontierai.github.io/homepage/oridynamics/

研究代码：https://github.com/LG-FrontierAI/oridynamics

## 维护文件

- `content.json`：标题、摘要、作者、机构与 Highlights。
- `application-cases.json`：BbFpn → BsPPase → FAK 三案例及媒体配置。
- `case-explanations.json`、`case-structure-map.json`：机制说明和结构参考文献。
- `video-manifest.json`、`video-music-credits.txt`：主视频参数、SHA-256 与配乐署名。
- `figure-manifest.json`：当前 Overview、Performance 等配图配置。
- `build.py`：从配置生成页面、robots.txt 和 sitemap.xml。
- `dist/site.css`、`dist/site.js`：直接维护的样式与交互源码。
- `dist/assets/`：当前页面使用的图片和四段视频。
- `icons/`：内联图标及许可。
- `preview_server.py`：支持 HTTP Range 和视频拖动的本地服务器。

## 编辑与预览

仓库根目录运行：

```sh
python3 build_pages.py
python3 oridynamics/preview_server.py --directory _site --port 4188
```

打开 http://localhost:4188/oridynamics/ 。也可在本目录执行 `python3 build.py` 与 `python3 preview_server.py --port 4188` 单独预览。

文案源文件修改后须重新构建。图片和视频已经包含，不依赖本地绝对路径或未发布论文。替换媒体时同步更新相应清单中的尺寸、时长和 SHA-256；构建时资源 URL 使用内容哈希避免旧缓存。

`SITE_URL` 默认指向组织项目网址，GitHub Actions 通过 `build_pages.py` 自动传入实际部署地址。页面资源使用相对路径，支持子目录部署。构建产物和文案源码一并提交。

推送 main 后由 `.github/workflows/pages.yml` 自动部署。首次重建以 2026-11-08 确认的本地版本为准，包括新主视频、新摘要和统一的 OriDynamics 名称。
