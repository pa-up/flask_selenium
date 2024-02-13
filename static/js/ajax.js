// 使い方：headタグ内に「<script src="~~~/js/ajax.js') }}"></script>」を記載

function send_to_python_ajax() {
    // 少々お待ちくださいボタン
    target = document.getElementById("js_wait_btn_output");
    target.innerHTML = "<br><h3>実行中〜少々お待ちください</h3>";

    // 非同期フォームの処理
    var send_data = $("#inputbox").val();
    $.ajax("/call_from_ajax", {
        type: "post",
        data: { "data": send_data },              // 連想配列をPOSTする
    }).done(function (received_data) {           // 戻ってきたのはJSON（文字列）
        var dict = JSON.parse(received_data);   // JSONを連想配列にする
        // 以下、Javascriptで料理する
        var answer = dict["answer"];
        $("#ajax_result").html(answer);              // html要素を書き換える

        // 少々お待ちくださいメッセージを消滅
        target.innerHTML = "";

    }).fail(function () {
        console.log("失敗");
    });

};

function reset() {
    //これは普通のJavaScript（jQuery）
    $("#inputbox").val("");
    $("#result").text("");
};
