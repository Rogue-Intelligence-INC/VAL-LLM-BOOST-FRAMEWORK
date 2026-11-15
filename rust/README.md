# Rust 移植件（2026-11-14 从 Valhalla-main hub-f64 移植，2026-11-15 同步至现行引擎状态）

这些代码已在 Valhalla-main 落地并部署验证；本目录是移植到本框架
的副本与集成说明。原版设计规范见 `docs/ORIGINAL_FATE_DESIGN.md`。

## 内容

- `fate_qa.rs` — Fate 抓取读数模块：`FateGrasp { selected_fragments,
  fragment_scores, candidate_scores, grasped_idx }` + diff/margin
  读数与离线单测向量。本期只暴露读数，不改任何行为。
- `engine/` — 引擎侧改动文件的当前快照（对照用）：
  - `native_qa.rs`：`NativeQaBatchItem.fate_grasp` 出口，按题组装
    激活区块、候选分数序列（top-5 matches 的 score）、抓取行；
  - `valhalla_base.rs`：`ValhallaBaseRow.fate_grasp` 透传到 HTTP row；
  - `open_qa_interface.rs`：默认构造补 `fate_grasp: None`；
  - `lib.rs`：注册 `pub mod fate_qa`；
  - `fate_orchestrator.rs`：两处关键修复——
    1. segmenter 编号按会话已有 fragments 播种（区块 ID 跨 append 唯一）；
    2. 动态卸载修复：`export_fragment` 只带本片 tick 窗口内收口的
       tiles（空窗回退全量），`merge_fragments` 按 tile id 去重。
       效果：长对话会话线 46MB→1.49MB（见分析文档 §4）。

## 构建与部署（本机已验证流程）

```powershell
# CUDA 12.8 必须在 PATH 首位（cudarc 不认 13.4）
$env:CUDA_PATH = "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.8"
$env:PATH = "$env:CUDA_PATH\bin;$env:PATH"
cargo build -p hub-f64 --release --bin valhalla_base   # 工作区 C:\Ai\Valhalla-main\manifestsys
```

网关部署：删 `valhalla-server\runtime\valhalla_base.exe.enc` 后重启
网关强制重封（runtime 已修为源更新自动重封）。验证：任意 open 题
row 应带 `fate_grasp.candidate_scores`（5 元降序）。

## 回滚锚点

`valhalla-server\archive\20261114-fate-p1-backup.zip`（含旧引擎 exe、
改动源、基线 FOG 表、五步回滚流程）。基线：基线表逐题 fog 不许
翻转到错误侧；长对话核心不低于 23/24、编造恒 0。

## 待续（P1b 以后，顺序按实测发现定）

1. ~~`fate_grasp` 补 `candidate_indices`（候选分对应行号）~~ ✅；
2. ~~首段收口成区块（line 0–1 当前无块可归）~~ ✅ `prelearn_head`；
3. ~~区块内候选序列离线复验相对 margin，可分才换门~~ ✅ 门已落地
   （`true_block_reading`，只换 margin 型弃权）；阈值已经业主裁定
   改归 Fate：`bundle_fits` + 会话活方程自己的 threshold，闸门内
   无标定常数。实测：20 题仅 absent_ent 一题因出生阈值翻转（归因
   见分析文档 §7）、长对话与标定版逐项一致、核心 24/24、编造 0；
4. premise/swap 类移出口层处理（引原文纪律），不进门； ⬅ 下一步
5. 实体-属性绑定（para 类改述针、distractor 沉默的根），属场读数。
