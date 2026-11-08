# 第3回 解答

## 演習

- 第1回（素のLLM）とエージェントの回答の違い：エージェントの回答はより詳しく、具体的な内容になっていた。また、用語集を検索して情報を取得するため、回答の根拠となる引用元も表示されていた。
- `--trace` で見えたツール呼び出し（ツール名と引数）：search_glossary が2回呼び出された。
- 1つの質問での LLM 呼び出し回数（`requests`）：2回
- 追加したツールと、docstring に書いた説明：
　def make_quiz(lecture: int) -> str:
    """
    指定した回の用語から1つを選び、
    確認問題と答えを返す。

    第2回の確認問題を出して、のように
    復習用の問題を求められたときに使う。
    """
    # 1. 用語集を読み込む
    glossary = load_glossary()

    # 2. 指定された講義回の用語を集める
    terms = [
        item for item in glossary
        if item["lecture"] == lecture
    ]

    # 3. 該当する用語がなければエラーを返す
    if not terms:
        return json.dumps({
            "error": f"{lecture}回目の用語が見つかりません。"
        }, ensure_ascii=False)

    # 4. 用語をランダムに1つ選ぶ
    selected = random.choice(terms)

    # 5. 問題と答えを返す
    return json.dumps({
        "question": f"「{selected['term']}」の意味は？",
        "answer": selected["definition"]
    }, ensure_ascii=False)

## 宿題

- 取り組んだレベル：基礎
- やったこと：`INSTRUCTIONS` から「必ず search_glossary で用語集を確認する」の行を消すと、検索せずに答えるようになるか
- 結果：どちらも変わらず、用語集を確認し、回答している。
- 気づき・疑問：このレベルの修正だと変化はないのかもしれない。
