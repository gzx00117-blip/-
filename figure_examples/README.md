# Editable training figures

所有数值为合成训练数据，无实验意义。曲线、散点、误差和叠谱用于学习最终尺寸与可编辑输出，不能填进论文Results。3个期刊版本使用同一份训练数据；字体/配色是本库工作选择，不是编辑偏好证明。

安装requirements后运行：

```powershell
python scripts/make_figure_examples.py
python scripts/preflight_figures.py
```

`synthetic_training.csv`保留每个训练重复；分电流由成对的总电流和FE计算。`generated/*.svg`可在Inkscape或Illustrator编辑文字/线条；本地运行也生成PDF、600dpi PNG与灰度图。仓库只同步作者原创SVG、CSV、代码及验证记录，不上传文献图像。

CSV也可导入Origin，按[实操指南](../analysis/软件绘图与期刊风格实操.md)重建；本包不包含原生OPJU。将来使用真实数据时，另存新的数据/脚本/项目，去掉训练字样前必须完成数据、单位与误差来源核验。

TOC SVG为55×50 mm原创假设图。虚线表示待验证路径，不能当作用户材料已经证实的机理。
