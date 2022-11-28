//发送验证码
function bindCaptchaClick() {
  $("#captcha-btn").on("click", function () {
    let $this = $(this);
    let email = $("input[name='email']").val();
    if (!email) {
      alert("请输入邮箱！");
    } else {
      // 通过js发送网络请求：ajax
      //alert("start ajax")
      $.ajax({
        url: "/user/captcha",
        method: "POST",
        data: {
          email: email,
          operation: "Registration",
        },
        success: function (res) {
          //res是视图函数返回的东西
          let code = res["code"];
          if (code === 200) {
            alert("Captcha sent successfully!");
            $this.off("click");
            $this.attr("disabled",true);
            let countDown = 60;
            let timer = setInterval(function () {
              countDown--;
              if (countDown > 0) {
                $this.text("Resent in "+countDown + "s");
                //完成之后可以重新点击
              } else {
                //clearInterval(timer);
                $this.text("Get captcha");
                $this.attr("disabled",false);
                bindCaptchaClick();
                clearInterval(timer); //  清除计时器
              }
            }, 1000);
          } else {
            alert(res["message"]);
          }
        },
      });
    }
  });
}

// 等网页加载完成后再执行
$(function () {
  bindCaptchaClick();
});
