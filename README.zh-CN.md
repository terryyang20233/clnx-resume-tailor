# CLNx Resume Tailor

[English](README.md) | **中文**

Chrome 扩展 + 本地 Python 服务：把多伦多大学 [CLNx](https://clnx.utoronto.ca) work-study 岗位说明做成一页 PDF 简历。

这是**非官方的个人工具**，与多伦多大学或 CLNx 无隶属、背书或支持关系。

```
CLNx 岗位页  →  Chrome 扩展  →  127.0.0.1:18765  →  applications/<id>-<slug>/
                                                              job.json  job.md
                                                              resume.tex  resume.pdf
                                                              selection.json
```

选择器按关键词重合度，从本地条目库（`resume_data.py`）打分；再用 `pdflatex` 编译，并贪心丢掉最不相关的块，直到 PDF 只有一页。

仓库里的 `resume_data.py` 是**虚构示例**（Alex Rivera / example.com）。请换成你自己的联系方式和条目。如果仓库是公开的，不要提交真实投递记录、成绩单或完整个人简历数据。

## 环境

- Python 3.10+
- [MacTeX](https://www.tug.org/mactex/) 或带 `pdflatex` 的 [TeX Live](https://tug.org/texlive/)（可选 `pdfinfo`）
- Chrome（加载未打包扩展）
- CLNx 登录（扩展只在 `https://clnx.utoronto.ca/*` 上运行）

## 安装

1. 克隆本仓库。
2. 把 `resume_data.py` 里的示例人物换成你的页眉、教育、经历、项目和技能。字符串里可以使用 LaTeX。
3. 启动本地服务（只绑定回环地址）：

   ```bash
   python3 server.py
   ```

4. 打开 Chrome：`chrome://extensions` → 开发者模式 → 加载已解压的扩展程序 → 选择 `extension/` 文件夹。
5. 打开一个 CLNx work-study 岗位详情页（`#postingDiv`），点击 **Create 1-page resume**。

在岗位列表页（`#postingsTable`）上，侧栏只帮你打开详情。生成简历需要完整描述页。

## 命令行（不用扩展）

```bash
python3 tailor.py examples/sample-job.json
```

`examples/sample-job.json` 是虚构岗位，不是真实的 CLNx 招聘。

## 会写出什么

每次运行会创建 `applications/<岗位编号>-<标题 slug>/`：

| 文件 | 用途 |
|------|------|
| `job.json` | 从岗位页抓到的原始字段 |
| `job.md` | 同一岗位的 Markdown |
| `resume.tex` / `resume.pdf` | 裁切后的一页简历 |
| `selection.json` | 保留了哪些条目以及原因 |

`applications/` 已被 gitignore（`.gitkeep` 除外）。生成的 PDF 只会留在本机，除非你自己加进仓库。

## 隐私

- HTTP 服务只监听 `127.0.0.1`。岗位正文不会发到任何远程 API。
- CORS 仅允许 `https://clnx.utoronto.ca`（以及 Chrome 扩展来源）。其他网页无法在浏览器里调用本地服务。
- 若 `applications/` 或填好的 `resume_data.py` 含个人数据，不要推到公开远程仓库。

## 许可

MIT。`preamble.tex` 中的 LaTeX 章节宏来自 [Jake Gutierrez / sb2nov resume](https://github.com/sb2nov/resume)（MIT）。
