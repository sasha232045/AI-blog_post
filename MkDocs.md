# MkDocs自動リンクシステム 技術ドキュメント

## システム概要

このドキュメントは、MkDocsベースの自動リンク生成システムの技術仕様とカスタマイズ方法を記載しています。

## 実装完了機能

### 1. 自動リンク機能
- **技術**: カスタムPythonスクリプト (`prebuild_linker.py`)
- **対応用語**: 19種類以上の専門用語
- **動作**: 記事内の専門用語を自動的に関連記事へのリンクに変換
- **例**: `機械学習` → `<a href="../01_AI基礎/02_機械学習.md">機械学習</a>`

### 2. ポップアップ機能
- **技術**: Material for MkDocsの組み込み`abbr`機能
- **動作**: マウスオーバーで用語の説明をポップアップ表示
- **実装**: 各記事末尾の `*[用語]: 説明` 記法

### 3. 統合ビルドシステム
- **メインスクリプト**: `auto_build.py`
- **機能**: 
  - 自動バックアップ作成
  - リンク生成実行
  - MkDocsビルド
  - 元ファイル復元
  - 開発サーバー起動オプション

## 技術的実装詳細

### リンク生成アルゴリズム
```python
# TERM_MAPPINGSによる用語マッピング
TERM_MAPPINGS = {
    "機械学習": "01_AI基礎/02_機械学習.md",
    "ニューラルネットワーク": "04_用語解説/01_ニューラルネットワーク.md",
    # ...19種類以上の用語
}

# 相対パス計算による正確なリンク生成
def calculate_relative_path(current_file, target_file):
    # ディレクトリ階層を考慮した相対パス計算
    return relative_path
```

### 処理フロー
1. **バックアップ作成**: `docs` → `docs_backup`
2. **リンク生成**: 各`.md`ファイルの専門用語を検出・変換
3. **MkDocsビルド**: 変換されたファイルでサイト生成
4. **復元**: `docs_backup` → `docs` (元ファイル保持)

### 文字コード対応
Windows環境での日本語処理問題を`python -X utf8`オプションで解決:
```bash
python -X utf8 auto_build.py
python -X utf8 -m mkdocs serve
python -X utf8 -m mkdocs gh-deploy
```

## カスタマイズ方法

### 新しい用語の追加
`prebuild_linker.py`内の`TERM_MAPPINGS`辞書に追加:
```python
TERM_MAPPINGS = {
    # 既存の用語...
    "新しい用語": "カテゴリ/XX_新しい用語.md",
}
```

### ポップアップ定義の追加
記事末尾に追加:
```markdown
*[新しい用語]: 新しい用語の説明文
```
        │   └── 01_歴史概要.md
        └── index.md
    ```

2.  **Markdownから呼び出す**: 記事のMarkdownファイル内で、通常のMarkdown画像構文を使って画像への相対パスを記述します。

    ```markdown
    ## ニューラルネットワークの概要

    以下は、ニューラルネットワークの基本的な構造を示す図です。

    ![ニューラルネットワークの概要図](../assets/images/neural_network_overview.png)
    ```
    *   **ポイント**: `01_歴史概要.md`から見て、画像は一つ上の階層(`../`)の`assets/images/`フォルダにあるため、このようなパスになります。

---

### 2. ナビゲーションの改善 (パンくずリストと前後セクション)

これらはMaterial for MkDocsテーマの非常に強力な標準機能です。`mkdocs.yml`の`theme:`セクションに`features:`を追加することで有効化できます。

```yaml
# my-ai-blog/mkdocs.yml

theme:
  name: material
  language: ja
  # 以下のfeaturesセクションを追加または編集
  features:
    # --- ここからがナビゲーション改善のための設定 ---

    # ページ上部にパンくずリストを表示
    - navigation.breadcrumbs

    # ページ上部のタブにトップレベルのセクションを表示
    - navigation.tabs

    # ページ最下部に「前へ」「次へ」のナビゲーションを表示
    - navigation.footer

    # --- ここまで ---
```

**解説:**

*   **`navigation.breadcrumbs`**: これを追加するだけで、ページ上部にパンくずリスト（例: `ホーム > 用語解説 > ニューラルネットワークとは`）が自動で表示されます。
*   **`navigation.tabs`**: スマホではあまり見えませんが、PCで見たときに最上部に「AIの歴史」「用語解説」といったトップレベルのカテゴリがタブとして表示され、アクセスしやすくなります。
*   **`navigation.footer`**: あなたが「[前のセクション][次のセクション]」と呼んでいる機能です。これを有効にすると、各ページの最下部に、`mkdocs.yml`の`nav:`で定義した順序に基づいた前後のページへのリンクが自動で生成されます。

**これら3つを設定するだけで、あなたのサイトのナビゲーションは劇的に改善されます。**

---

### 3. サイトの色の調整

サイトの印象を決定づける色の変更も、`mkdocs.yml`で非常に簡単に行えます。

**基本的な方法（プリセットから選ぶ）:**

`theme:`セクションに`palette:`を追加し、`primary`（メインカラー）と`accent`（アクセントカラー）を指定します。色は英語名で指定します。

```yaml
# my-ai-blog/mkdocs.yml

theme:
  name: material
  language: ja
  features:
    # ... (前述のナビゲーション設定) ...
  
  # 以下のpaletteセクションを追加
  palette:
    # メインカラーをインディゴに、アクセントカラーをブルーに設定
    primary: indigo
    accent: blue
```

*   **色の選択肢**: `red`, `pink`, `purple`, `indigo`, `blue`, `teal`, `green`, `orange`など、多数の色が用意されています。利用可能な色の一覧は、[Material for MkDocsの公式ドキュメント](https://squidfunk.github.io/mkdocs-material/setup/changing-the-colors/#color-palette)で確認できます。

**上級者向けの方法（完全に独自の色を設定）:**

1.  `docs/assets/`内に`stylesheets/extra.css`というファイルを作成します。
2.  `extra.css`に、CSSの変数を上書きするコードを記述します。
    ```css
    /* docs/assets/stylesheets/extra.css */
    :root {
      --md-primary-fg-color: #3f51b5; /* インディゴの色コード */
      --md-accent-fg-color: #2196f3;  /* ブルーの色コード */
    }
    ```
3.  `mkdocs.yml`に、このCSSファイルを読み込むように指示します。
    ```yaml
    # my-ai-blog/mkdocs.yml
    
    # extra_cssをトップレベルに追加
    extra_css:
      - assets/stylesheets/extra.css
    
    theme:
      # ... (以下略) ...
    ```

---

### 4. Wikiのような自動単語リンクの実現

これは静的サイトジェネレータの真骨頂とも言える機能で、**`mkdocs-glossary`**というプラグインを使えば実現できます。

**設定手順:**

1.  **プラグインのインストール**: ターミナルで以下のコマンドを実行します。
    ```bash
    pip install mkdocs-glossary
    ```

2.  **プラグインの有効化**: `mkdocs.yml`に`plugins:`セクションを追加し、`glossary`を記述します。
    ```yaml
    # my-ai-blog/mkdocs.yml

    # pluginsセクションをトップレベルに追加
    plugins:
      - glossary
    
    theme:
      # ... (以下略) ...
    ```

3.  **用語集ファイルの作成**: `docs/`内に、用語を集めたMarkdownファイルを作成します。例えば`glossary.md`という名前にします。

4.  **用語集のフォーマット**: `glossary.md`内に、**レベル2見出し(`##`)**で用語を定義します。この見出しがリンクのアンカーになります。
    ```markdown
    # 用語集
    
    ## ニューラルネットワーク
    
    人間の脳の神経細胞（ニューロン）のネットワーク構造を模した数理モデルです。
    
    ## ディープラーニング
    
    ニューラルネットワークを多層（ディープ）に重ねることで、より複雑なパターンを学習できるようにした機械学習の一分野です。
    ```

5.  **`mkdocs.yml`のナビゲーションに追加**: 他のページと同様に、`glossary.md`もナビゲーションに追加しておくと親切です。
    ```yaml
    # my-ai-blog/mkdocs.yml
    nav:
      - ホーム: index.md
      - 用語集: glossary.md # <- 追加
      - AIの歴史:
        # ...
    ```

これで準備は完了です。`mkdocs serve`や`mkdocs build`を実行すると、**プラグインが自動で全てのMarkdownファイルをスキャンし、`glossary.md`に存在する見出し（例：「ニューラルネットワーク」）と同じ単語を見つけると、自動的にその用語へのリンク（例: `https://.../glossary/#_1`）を生成してくれます。**

これにより、あなたのサイトは非常にインタラクティブで、学習効率の高いWikiのようなナビゲーションを持つことができます。