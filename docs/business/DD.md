# Due Diligence Pack — VAL-LLM

Rogue Intelligence INC · 2026-11-14 · 本地版（未入库）
用途：供投资人/客户技术尽调按图索骥。所有声明可复现。

## 1. 声明-证据索引（核心声明 → 工件）

| 声明 | 工件 | 位置 |
|---|---|---|
| 1495 万 token 三档 17/21、编造 0 | enhancement_ceiling_lines{30006,100006,1000006}.json | val-llm-fusion-framework/tests/results_extreme |
| 极端 806/3006/10006 hybrid 12/12 | extreme_targeted_lines*.json、extreme_rerun2.log | 同上 |
| 注入免疫（修复前后对照） | 报告 §11.7 + hybrid.py 隔离规则 | docs/MISTRAL24_VS_VALHALLA_UNIQUE_POINTS_20261113.md |
| 多模 9/9、特征抓取 | multimodal_fixed.json、mm_fixed5.log、probe_grasp_cos.py | tests/ |
| BOOST 17→20/21、三版对照 | boost_adapt_lines100006.json、boost_adapt{,2,3,4}.log | tests/results_extreme |
| Fate 裁决代数理由在线 | probe_fate_gateway.py 输出、fate_telemetry 字段 | valhalla_server/app.py |
| 烘焙 Δw≈0.604、40 层、fate_converged | data/decode_heads.json（mistral24-auto-v1） | val-llm-fusion-framework/data |
| multihop_fate/v2 切片 15/25（内部先例） | multihop_rag_hybrid_test.json | valhalla-unified-core/reports |

复现环境：Windows 11、i9-14900KF、RTX 4090、Mistral-24B
Q4_K_M（llama.cpp, 16K ctx）、valhalla_base v1.1.0。

## 2. 架构速览
语料→定向选行→ValhallaBase 会话（Fate 裁决 emit/abstain，
代数 margin）→证据卫生（会话内取证、注入隔离、集束）→
Mistral-24B 解码头 verbalize；多模经共摄入+网关特征抓取；
BOOST 算子（扩散/聚合/意图门）在证据层，已验待集成 resolve。

## 3. 已知局限（如实清单，尽调重点核对区）
1. LoCoMo-15：Valhalla 0/15 vs RAG 9/15、Mem0 5/15——不赢，
   不对外宣称长对话记忆领先；
2. 多跳：BOOST 后 1/2，残留 hop_employer（桥接人名同名 ~90 行
   的实体消歧问题），失败模式为弃权而非乱答；
3. 矛盾事实：静默选后写值（HAL-2），冲突上报在 Q1 路线图；
4. proactive 主动发声：本机协议复核未实现（只弃权半边成立），
   不营销；
5. 特征抓取：同文件再识别已测，跨实例（重录/重拍）未测；
6. 编码器为产品层适配（本地 CLIP ViT-H/时段 mel，384 契约），
   非引擎原生对齐空间；
7. 全部测试为单机、合成语料为主 + 官方套件子集；客户真实
   语料泛化待试点验证；
8. 运行时 Fate 权重固定（fate_weight_mode:"fixed"），在线学习
   未实现，离线适应在路线图 Q3。

## 4. IP 与开源边界
- 已公开：Rogue-Intelligence-INC/val-llm-fusion-framework、
  VAL-LLM-BOOST-FRAMEWORK（分析与已测代码）；
- 引擎 valhalla_base 为组织自研 Rust 运行时（协议
  valhalla-base-v1 v1.1.0）；解码头为 Mistral-24B 权重
  （遵循其上游许可）+ 本组织烘焙 patch；
- 商业许可与开源边界划分：【TBD 法务定版——尽调时以书面为准】。

## 5. 常见尽调问答
Q：与 GraphRAG 差别？A：图只是我们五件套之一；独有的是
Fate 接地裁决（弃权带代数理由）、权重烘焙沉淀、特征抓取。
Q：换基座模型还成立？A：Fusion 与头正交（内部 MCQ 阶梯
0.5B→3B 已证缩放）；第二头适配在 Q3 里程碑，未测前不承诺数字。
Q：为什么 LoCoMo 输还敢卖记忆？A：我们卖的是"不敢答时
不乱答+答了能举证"，长对话召回是另一赛道，不冒领。
Q：零编造的边界？A：指"答案断言的代号/数字在语料有出处"
（脚本审计口径），信源本身被投毒属另一类风险，已有证据
卫生防线，语料真实性不在系统保证内。

## 6. 待补材料（定版前）
团队履历、财务预测、融资条款、客户试点名单、法务意见。
——以上均未预填，尽调时以创始团队正式版为准。
