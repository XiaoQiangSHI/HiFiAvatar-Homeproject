# Git Workflow

这个仓库已经完成了最基础的 Git 建立工作：

- 已存在 Git 仓库（`.git`）
- 已连接远端仓库 `origin`
- 当前线上主分支为 `master`

为了便于后续论文项目页持续迭代，建议使用下面这套轻量流程。

## 分支约定

- `master`：发布分支，保持可直接用于 GitHub Pages/对外展示
- `dev`：开发集成分支，日常内容修改先合到这里
- `feature/*`：新功能或页面模块开发
- `fix/*`：紧急修复
- `docs/*`：文档更新
- `chore/*`：仓库维护、初始化、清理类工作

## 推荐工作流

1. 从 `dev` 拉出新分支
2. 在功能分支上完成单一任务
3. 自测后合并回 `dev`
4. 页面内容确认无误后，再从 `dev` 合并到 `master`

## 常用命令

```bash
# 同步远端
git checkout master
git pull origin master

# 同步开发分支
git checkout dev
git merge master

# 新建功能分支
git checkout dev
git checkout -b feature/update-project-content

# 完成功能后合并回 dev
git checkout dev
git merge feature/update-project-content

# 准备发布时合并到 master
git checkout master
git merge dev
```

## 当前初始化建议

- 把 `master` 当作最终展示版本
- 把 `dev` 当作论文项目页的日常编辑入口
- 后续每次大改都从 `dev` 新开分支，不要直接在 `master` 上改

## 说明

- `figures_method/` 目前存在未跟踪文件，请按需决定是否纳入版本控制
- 如果后续增加构建工具（如 Vite、npm、Python 脚本），当前 `.gitignore` 已预留常见忽略项
