# OriDynamic 主页

当前标题：**Toward a World Model for Biomolecular Dynamics through Latent Ensemble Decomposition with OriDynamic**

官网：<https://oridynamics.github.io/>

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

## 发布状态

网页资源已与原官网发布提交 `5e98e84a3dfa700671224eb8268491d68e2f8dd5` 核对一致。当前导入只建立源码仓库，尚未启用从本仓库到原官网的自动同步。

`dist/` 中的网页保持当前正式站点地址。官网发布仓库为 <https://github.com/oridynamics/oridynamics.github.io>。

## 署名与资源许可

保留网页中的音乐署名以及 `video-music-credits.txt`。图标许可见 `icons/LICENSE.txt` 和 `icons/SOURCES.txt`。本仓库未为项目内容新增开源许可；第三方资源遵循各自的许可。
