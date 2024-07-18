# 開發筆記

## 要實現的功能

### Disscussion about the selected idea (點子討論) [Idea Meansure]

Function -> check idea is already implemented

- (Yes) -> find those papers and show them also suggest idea from those paper's future work

- (No) -> suggest papers that are related to the idea

#### 工作流程

### Function -> 論文主題的確定 [Idea Meansure]

1. 根據使用者選擇的點子，進行關鍵字提取。
2. 使用關鍵字進行搜索(Arxiv, Google Scholar)。
3. 搜索結果會是論文的 Abstract， 使用語言模型判斷是否與點子相關以及相似度。
4. 返回相關的論文，並提供多個研究問題、假設和目標。

或許可以考慮 單獨 keyword 與 summary 去產生新的 topic

### Function -> 結構草擬

- 提供工具幫助使用者確定研究問題、假設和目標。
- 根據已有的研究建議和未來的研究方向生成論文提案的草案。

### Function -> 實驗設計

- 根據研究問題和目標，提供實驗設計的建議。