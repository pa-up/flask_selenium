// フォームの少々お待ちくださいボタン
function OnButtonClick() {
    target = document.getElementById("js_wait_btn_output");
    target.innerHTML = "<br><h3>実行中〜少々お待ちください</h3>";
}


function copyToClipboard() {
    const textToCopy = document.querySelector('.display-text');
    const tempInput = document.createElement('textarea');
    tempInput.value = textToCopy.innerText;
    document.body.appendChild(tempInput);
    tempInput.select();
    document.execCommand('copy');
    document.body.removeChild(tempInput);

    target = document.getElementById("copyMessage");
    target.innerText = "Copied!";
    }