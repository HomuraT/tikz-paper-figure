# tikz-paper-figure

![二次元学术工作台：用 TikZ 与 pgfplots 将想法绘成论文配图，两种风格、63 个范例、可编辑 TeX](docs/images/repository-banner-v0.2.2.png)

用 TikZ 和 pgfplots 绘制论文配图。从卡片示意图、实验数据图到多面板组合图，提供两种风格、63 个已编译范例，以及从数据到渲染图的 agent 工作流。

[版本 0.2.2 · 2026-09-30](CHANGELOG.md#022-2026-09-30)

[English](README.md) · [安装](#安装) · [快速上手](#快速上手) · [完整图库](skills/tikz-paper-figure/references/gallery.md)

## 内容

- 样式包。`cardfig.sty` 提供带深色标题栏、标签条、脚注带和阴影的卡片，以及基准条形面板；`plotfig.sty` 给 pgfplots 一个 `paper` 坐标轴样式，同一套字体与配色，系列名直接标在图上，柱从零起，灰色刻度，数字用正文字体。
- 经典风格 `classicfig.sty`：把 Matplotlib 的默认参数（rcParams）搬进 pgfplots（DejaVu Sans、四边框、tab10 配色、圆角图例框），并为认真的 Matplotlib 用户常加的每一处打磨配一个键或宏：浅色网格、白边标记点、文字白色描边、区间色带、文本框、显著性括号、断轴、整张组合图共用的图例。
- 三个模板（`template.tex`、`template-bars.tex`、`template-plot.tex`）和 63 个带渲染图的范例：统一风格（卡片与数据图共用字体配色的那一套）3 张卡片图、1 张条形面板、28 张数据图、4 张组合图；经典风格 13 张单图和 5 张组合图（拟合加残差、散点加边际分布、局部放大插图、断轴、拼图），附生成数据的 numpy 脚本；另有 9 张本体与 RDF 图：3 张记法示例（W3C RDF、VOWL、TBox/ABox）和 6 张柔和配色关系图，含 26–28 个节点的密集示例；`softontology.sty` 统一节点、白底属性值、连线和分区样式。
- 脚本。`build_figure.py` 编译（默认 pdflatex，文件要求时用 LuaLaTeX）、清理、对照正文宽度检查尺寸并输出 PNG；`bars_from_csv.py`、`flows_from_csv.py`、`treemap_from_csv.py` 从数据生成图；`palette_check.py` 在模拟色觉缺陷下测量配色距离；`compare_sheet.py` 把两版图叠成一张对照；`gallery_sheet.py` 拼出范例总览；`check_env.py` 列出本机装了什么。
- 参考文档。Wilke《Fundamentals of Data Visualization》的要点笔记与选图决策表、卡片元素目录、每种图一份配方、经典风格的工作流与画图技巧（整理自 Rougier《Scientific Visualization: Python + Matplotlib》和 Matplotlib 官方图库）、本体图的记法与布局规则、常见问题与修法。
- `SKILL.md`：agent 从选风格、确定内容到交付渲染图的工作流。

## 安装

**作为 Claude Code skill。** 把 skill 目录复制到个人 skills 目录，或某个论文仓库的 `.claude/skills/`。

```bash
git clone https://github.com/HomuraT/tikz-paper-figure.git
cp -r tikz-paper-figure/skills/tikz-paper-figure ~/.claude/skills/
```

```powershell
git clone https://github.com/HomuraT/tikz-paper-figure.git
Copy-Item -Recurse tikz-paper-figure/skills/tikz-paper-figure "$env:USERPROFILE/.claude/skills/"
```

目录布局也符合 `npx skills add HomuraT/tikz-paper-figure --skill tikz-paper-figure` 的要求，这条路径没有测过。

**只要模板，不用 agent。** 把 `skills/tikz-paper-figure/assets/cardfig.sty`、`plotfig.sty`、`classicfig.sty` 或 `softontology.sty` 复制到图源目录，按下面的快速上手走。`.sty` 进了项目，Overleaf 上也能编译。

## 快速上手

先跑一次 `python skills/tikz-paper-figure/scripts/check_env.py`，它会列出缺哪个 TeX 宏包或工具，以及缺了会坏什么。

1. 把 `plotfig.sty`（数据图）、`cardfig.sty`（卡片、条形面板）、`classicfig.sty`（经典的 Matplotlib 风格）或 `softontology.sty`（柔和配色的本体与映射关系图）复制进论文的 `figures/`。保持论文的字体和视觉约定一致；`softontology.sty` 本身不指定字体。
2. 从 `skills/tikz-paper-figure/assets/examples/` 挑最接近的范例复制为 `figures/name.tex`，换成自己的数据。结果榜单改从 CSV 生成：
   ```bash
   python skills/tikz-paper-figure/scripts/bars_from_csv.py results.csv --ours Ours --cols 2 --out figures/results.tex
   ```
3. 构建，然后看 PNG：
   ```bash
   python skills/tikz-paper-figure/scripts/build_figure.py figures/name.tex --png-dir figures
   ```
   脚本会打印页面尺寸，并按 5.5 英寸正文宽给出是否超宽的判定（别的版式用 `--max-width`）。`ontology/soft-*` 范例宽约 17 cm，按原尺寸重建时使用 `--max-width 500`；新论文按实际版心设置宽度，必要时重新布局。
4. 论文里写 `\graphicspath{{figures/}}` 和不带宽度的 `\includegraphics{name.pdf}`。图按最终尺寸设计，缩放会改变字号。

## 配合 agent 使用

装好 skill 后，这类要求会触发它：

- 「给这篇论文画 Figure 1：三张卡片，例子用 Listing 1。」
- 「把表 2 画成结果图，我们的系统用蓝色。」
- 「5.2 节的消融用什么图？画出来。」
- 「把 `figures/curves.tex` 的图例挪到图上方，别的都不动。」
- 「用经典风格画这组 XRD 数据，把金红石那个小峰放大。」
- 「把这个本体画成柔和配色的关系图，白底属性值也统一黑边和轻阴影。」

skill 按论文定风格，按段落要回答的问题选图，复制最近的范例，编译，读渲染图，汇报跑了哪些检查。经典风格下，它先用 Python 算好所有统计量，再把标签、图例和文本框放进数据留出的空白处。修改已有图时，要求被拆成「改什么」和「保持什么」两张清单（数据、颜色、尺寸、没点名的元素位置），回复里给出 diff 和前后对照图。机器上没有 TeX 时，skill 会说明图没有编译，不会描述一张谁也没见过的渲染图。

## 环境要求

| | |
|---|---|
| TeX | TeX Live 2023 或更新（或 MiKTeX），含 `standalone`、`pgfplots` 1.18+、`tikzmark`、`fontawesome5`、`sourcesanspro`、`inconsolata`；经典风格另需 `dejavu`、`mathastext`、`contour`；柔和配色本体范例使用 `dejavu`；`lualatex` 只有等高线图用到 |
| PDF 工具 | poppler 的 `pdfinfo` 与 `pdftoppm`（Windows 版 TeX Live 自带） |
| Python | 3.9 或更新；Pillow 只有 `gallery_sheet.py` 用到，numpy 只有经典风格范例的数据脚本用到 |

在 Windows 11、TeX Live 2025、Python 3.13 和 Claude Code 上测过。`SKILL.md` 遵循 [Agent Skills](https://agentskills.io/specification) 格式，读这种格式的其他 agent 应该也能加载，只试过 Claude Code。

## 图库

| 统一风格 · 示意与结果 | Classic 风格 · 科学绘图 |
| :---: | :---: |
| <a href="skills/tikz-paper-figure/assets/examples/plots/curves-bands.png"><img src="skills/tikz-paper-figure/assets/examples/plots/curves-bands.png" width="320" alt="统一风格：带置信区间的双面板曲线图"></a> | <a href="skills/tikz-paper-figure/assets/examples/classic/xrd.png"><img src="skills/tikz-paper-figure/assets/examples/classic/xrd.png" width="320" alt="Classic 风格：带局部放大与参考谱线的 XRD 图"></a> |
| 卡片、榜单、曲线与消融分析 | 光谱、分布、拟合与组合图 |

点击预览查看原图。

[浏览全部 63 个范例与源码 →](skills/tikz-paper-figure/references/gallery.md) 每张图都附有适用问题、源码路径和对应配方。

| 风格 | 范例 | 说明 |
| --- | --- | --- |
| 统一风格 | 36 张：卡片、条形面板、数据图与组合图 | [选图与配方](skills/tikz-paper-figure/references/gallery.md) |
| Classic 风格 | 18 张：线与点、分布、类别与场、组合图 | [经典风格指南](skills/tikz-paper-figure/references/classic.md) |
| 本体图 | 9 张：3 张记法示例、6 张柔和配色关系图（含密集版） | [本体图指南](skills/tikz-paper-figure/references/ontology.md) |

**统一风格总览 · 36 张图**

![36 个统一风格范例，按模板分组](skills/tikz-paper-figure/assets/examples/gallery.png)

**Classic 风格总览 · 18 张图**

![18 个经典风格范例，按图型分组](skills/tikz-paper-figure/assets/examples/classic/gallery.png)

**本体与 RDF 图总览 · 9 张图**

![9 个本体与 RDF 图范例：记法示例与柔和配色关系图](skills/tikz-paper-figure/assets/examples/ontology/gallery.png)

新增范例后，用 `gallery_sheet.py` 重新生成总览图。

## 范例与测试

- [`examples/results-from-csv`](examples/results-from-csv)：从 CSV 生成四个基准的结果榜单，其中一项因为越低越好而反向排序，附命令与构建输出。
- [`examples/constrained-revision`](examples/constrained-revision)：给一张已有图加一条参考线，附改动清单、保持清单、diff 和前后对照图。
- [`tests/`](tests)：三条带验收标准的任务（从 CSV 生成结果图、三张风格各异的图统一而不改数据、只挪图例），用于对比有无 skill 的运行结果。目前还没跑过。

## 规则出处

样式、配色和选图背后的道理写在博客文章里：[用 TikZ 统一论文配图：样式规范、模板与构建流程](https://blog.homura.work/posts/tech/latex/tikz-paper-figure/)。数据图的默认值来自 Claus O. Wilke 的《Fundamentals of Data Visualization》，[`references/principles.md`](skills/tikz-paper-figure/references/principles.md) 是转述的要点笔记，每条规则链接到原书章节，并写明本样式有意偏离原书的地方。卡片版式参考了 SWE-bench、Spider 2.0 和 BIRD 的 Figure 1。经典风格的尺寸与颜色取自 Matplotlib 的默认 rcParams，打磨手法来自 Nicolas P. Rougier 的《Scientific Visualization: Python + Matplotlib》（开放获取）、他的《Ten simple rules for better figures》以及 Matplotlib 官方图库的范例；[`references/classic.md`](skills/tikz-paper-figure/references/classic.md) 为每条技巧注明出处和示范它的范例。

## 相关项目

- [OpenTikZ](https://github.com/opentikz/opentikz)：概念示意图的图标库与可编辑模板，带 Claude Code skill。本仓库每个模板里的修订约定来自它的 `edit_contract` 思路。
- [tikz-academic](https://github.com/Noi1r/tikz-academic)：面向学术 TikZ 图的 skill，每种图型一份参考文件。
- [tikz-constraint-harness](https://github.com/zane-gao/tikz-constraint-harness)：面向 Codex 的约束优先 TikZ 生成与修复。本仓库修订流程里的「改什么、保持什么」两张清单沿用了同一思路。
- [tikz-diagrams-skill](https://github.com/Patrick-Healy/tikz-diagrams-skill)：从文字、截图和手绘到 TikZ，带编译、渲染、检查脚本。
- [scientific-plotting-skill](https://github.com/dazhiyang/scientific-plotting-skill)：ggplot2 与 plotnine 的出版规范，只有一个 `SKILL.md`。

## 赞赏

项目免费使用。如果这套模板对你有帮助，欢迎用下面的微信赞赏码请我喝杯咖啡。

<img src="docs/sponsor/wechat-reward.png" width="240" alt="微信赞赏码">

## 许可证

脚本、`SKILL.md` 和参考文档采用 [MIT 许可证](LICENSE)。`docs/sponsor/` 下的赞赏码不在两份许可证的范围内。`skills/tikz-paper-figure/assets/` 下的全部内容（三个样式包、模板、范例源码、数据及其渲染图）以 [CC0 1.0](LICENSE-ASSETS) 放入公有领域，论文仓库复制它们不必附带任何声明。

未打包进仓库的部分：字体（Source Sans Pro、Inconsolata、DejaVu Sans）和 Font Awesome 图标来自 TeX Live 宏包，各有自己的许可证。Wilke 的书是 CC BY-NC-ND 4.0，本仓库只转述其规则并链接到章节，不复制其文字或图片。Rougier 的书与代码（BSD）以及 Matplotlib 官方图库同样只转述并附链接，不复制其文字、代码或图片。
