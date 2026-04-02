# app.py
from flask import Flask, render_template, request
from src import fullflush_wait

# Flaskアプリケーションのインスタンスを作成
# __name__は現在のモジュール名が入る特別な変数
app = Flask(__name__)

# ルートURL("/")にアクセスが来たときに呼ばれる関数を定義
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chin_machi", methods=["GET", "POST"])
def chin_machi():
    if request.method == "POST":
        # フォームから送信された値を取得
        haishi = request.form.get("haishi")

        # ここで簡易なチェック(本格的なバリデーションは後述)
        if not haishi:
            error = "牌姿は必須です。"
            # エラー時は同じテンプレートにエラーメッセージを渡して再表示
            return render_template("chin_machi.html", error=error, haishi=haishi)

        # 待ち判定ロジックのpythonファイルを実行
        # 入力牌姿のエラーチェック
        result_err_chk = fullflush_wait.check_tehai(haishi)
        
        if result_err_chk[0]:
            error = result_err_chk[1]
            # エラー時は同じテンプレートにエラーメッセージを渡して再表示
            return render_template("chin_machi.html", error=error, haishi=haishi)
        
        # 清一色待ち判定
        agari_str = fullflush_wait.agari_check(haishi)
        return render_template("chin_machi.html", agari_str=agari_str, haishi=haishi)

    # GETメソッド時はフォームを表示
    return render_template("chin_machi.html")

# Pythonスクリプトとして直接実行されたときだけ起動する
if __name__ == "__main__":
    # debug=True でデバッグモードを有効化
    app.run(debug=True, port=5000)