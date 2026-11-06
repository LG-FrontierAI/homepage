# OriDynamic 主页

当前标题：**Toward a World Model for Biomolecular Dynamics through Latent Ensemble Decomposition with OriDynamic**

组织网站：<https://lg-frontierai.github.io/homepage/oridynamic/>

原官网：<https://oridynamics.github.io/>

## 文件分工

- `content.json`：标题、摘要、作者、机构与页面文字。
- `application-cases.json`：五个案例的标题、视频、封面、时长和配图配置。
- `case-explanations.json`、`case-structure-map.json`：案例说明、结构来源及参考文献。
- `video-manifest.json`、`video-music-credits.txt`：主视频配置和音乐署名。
- `figure-manifest.json`：当前配图尺寸和文件校验值。
- `build.py`：生成 HTML、性能图 SVG、robots.txt 与 sitemap.xml。
- `dist/site.css`、`dist/site.js`：页面样式及交互的源文件，直接在这里修改。
- `dist/assets/`：当前使用的图片与六段 MP4，以及构建性能图所需的原始 PNG。
- `icons/`：构建时内联的图标及其许可证。
- `preview_server.py`：支持 HTTP Range 的本地预览服务，可拖动视频进度。
- `snapshot.json`：首次导入时的线上版本和网页资源校验清单。

## 编辑、构建与预览

在仓库根目录执行：

```sh
python3 oridynamic/build.py
python3 oridynamic/preview_server.py --port 4187
```

打开 <http://localhost:4187/>。端口已被其他预览使用时，可指定 `--port 4188`。

修改文字、作者或案例说明后执行构建。CSS/JS 直接维护在 `dist/` 中；生成的 `dist/index.html` 应通过 `build.py` 更新。提交时一并提交修改后的源码和构建输出。

现有 SVG 科学配图、视频和封面已包含，无需原始 PDF 或原制作机器即可重建网页。替换视频时同步更新配置中的时长、尺寸与 SHA-256；`application-cases.json` 的哈希用于视频链接缓存刷新。

## 发布

将主页修改推送到本仓库 `main` 后，GitHub Actions 自动构建并发布到 <https://lg-frontierai.github.io/homepage/oridynamic/>。

`build.py` 默认使用组织项目网址；可通过 `SITE_URL` 设置另一个发布地址。图片、视频、样式和交互脚本使用相对路径，支持子目录部署。`build_pages.py` 只将网页引用的资源复制到 `_site/oridynamic/`，并检查引用文件是否齐全。

原官网 <https://oridynamics.github.io/> 仍由其独立仓库发布，本工作流不会同步更新该地址。

首次导入与原官网提交 `5e98e84a3dfa700671224eb8268491d68e2f8dd5` 一致，历史校验清单保存在 `snapshot.json`。

## 署名与资源许可

保留网页中的音乐署名以及 `video-music-credits.txt`。图标许可见 `icons/LICENSE.txt` 和 `icons/SOURCES.txt`。本仓库未为项目内容新增开源许可；第三方资源遵循各自的许可。
