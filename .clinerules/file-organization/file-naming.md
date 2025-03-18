# ファイル命名規則

## 結果ファイル

- パターン: `p{persona}_{model}_n{trial}_temp{temp}_t{text}.txt`

### コンポーネント

- persona: p1-p4
  - p1: 大学１年生
  - p2: 文学研究者
  - p3: 感情豊かな詩人
  - p4: 無感情なロボット

- model: モデル識別子
  - gemini15f
  - gemini20pe
  - claude30h
  - claude37s
  など

- trial: 試行番号
  - n01, n02, n03...

- temp: 温度値
  - temp50 (0.5)
  - temp75 (0.75)
  など

- text: テキスト識別子
  - t1: 懐中時計
  - t2: お金とピストル
  - t3: ぼろぼろな駝鳥

## 例

```
p1_gemini15f_n01_temp50_t1.txt
p2_claude37s_n02_temp75_t3.txt
```

## ディレクトリ構造

結果ファイルは以下のように配置：

```
results/
├── gemini/
│   ├── p1_gemini15f_n01_temp50_t1.txt
│   └── ...
└── claude/
    ├── p2_claude37s_n02_temp75_t3.txt
    └── ...
