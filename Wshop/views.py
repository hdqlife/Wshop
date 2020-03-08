import hashlib
from django.shortcuts import HttpResponseRedirect


def setPassword(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    result = md5.hexdigest()
    return result

def loginValid(fun):
    def inner(request,*args,**kwargs):
        username = request.COOKIES.get("username")
        if username:
            return fun(request,*args,**kwargs)
        else:
            return HttpResponseRedirect("/Store/login/")
    return inner

def loginValid_buyer(fun):
    def inner(request,*args,**kwargs):
        username = request.COOKIES.get("username")
        if username:
            return fun(request,*args,**kwargs)
        else:
            return HttpResponseRedirect("/Buyer/login/")
    return inner

from alipay import AliPay
def pay(order_id,money):
    alipay_public_key_string = '''-----BEGIN PUBLIC KEY-----
        MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAxCKm8OBVH6LI6a6OpzGTpCj8hrgg55Pf9YjSUZifhSrpqbBhRn3In4/oFFTXjYwTvPBGLFmhvWEI17fHBQ9gLZVkvovgBkBitGlgrAGkRSXU9jv9jKNxzSygjFYjDEa/RjH6sj44k0wc71IkeFRWg2l1lk4W4duFGMa0XHlgB9JFIRc0Dxa9kDEDcaEMtZHFxkyJ9pzTZ6oEe1RMKrMymg7q3Tm96Ftz3AsTi8vuONpMg79mw94U4HTnxL+nkbPwsyHOodskRShBILj0r2hD+WGUKejJBu5281mcY6SuMlDJghuoUesCOExV8Nzknj5em3CvkiQWA5UQjRYkxpFV4QIDAQAB
    -----END PUBLIC KEY-----'''

    app_private_key_string = '''-----BEGIN RSA PRIVATE KEY-----
        MIIEowIBAAKCAQEAxCKm8OBVH6LI6a6OpzGTpCj8hrgg55Pf9YjSUZifhSrpqbBhRn3In4/oFFTXjYwTvPBGLFmhvWEI17fHBQ9gLZVkvovgBkBitGlgrAGkRSXU9jv9jKNxzSygjFYjDEa/RjH6sj44k0wc71IkeFRWg2l1lk4W4duFGMa0XHlgB9JFIRc0Dxa9kDEDcaEMtZHFxkyJ9pzTZ6oEe1RMKrMymg7q3Tm96Ftz3AsTi8vuONpMg79mw94U4HTnxL+nkbPwsyHOodskRShBILj0r2hD+WGUKejJBu5281mcY6SuMlDJghuoUesCOExV8Nzknj5em3CvkiQWA5UQjRYkxpFV4QIDAQABAoIBAQC5THOjxo0lYkmmXH/xfWkbAo3xSSvtHUvNUQJCjIrI6Q3wfu6oBlXwSajc7HrpA5nyOp5RcCzaGj6cbsfcA/a9mhKf4s43mcSm5ZerabGkkmVsbKjSoef2C19ytj5ObthunPFYTGhu4M3FXDmQZT2G0a+B3SzJHPfVvITRiOos99YcovMVekfU6r28W4cc7tHJwfOT0yWmVo7dTgTDJLub/uTMhyvnoSWrWfdRBksoWK3KrK2WNx11oCfELNr3iIBFGz5LK3syj8ncCK/3w2A0u+B0ELP2K4Ql6X50GN992GVs4knQrENZSOUEdU+QjYd0VpnJSoMTBKB03Wqj28RxAoGBAPJVsF559nBJ3vDarfd+R8BWhEQLxZHuBSxDEE0wxba/zWjIzzD8DhSRYsgmi3XwSK8M6UDDt4Ms+acSq9eSzjdnk7IW3jCOciW84aKB/7s7Ar1xk9RfkAmyqKP3F7nXnUulyKCLkZCghd1S59x3Ul+APJoEJDG8GG7Gett64GlPAoGBAM8yCRQYr0FrfRQQt7H3YFIKb2wuH/g4SGOj5Q5m5NbccfZ2vOkdItziGi8zlHfkZUQ1WalrnXuJUWvG8krb3vXaRKZZO5tSxe7A06ZB5vzo7HyE5GksJHMZ98D68z8+/+LbLzJdpuCG56vIGrCjkXsnczP4MTmDNW+Kx2nFpyHPAoGAS9BBAB2Z2qFRrPpNCKuqGOM4N+2S3sefOKy2cd+7SyQQSCLipwmEAi1FwSZF5RzKMHGSm59fTxuH8xvlROj5uN2fmEyNMJWv4lyIHoYbEmEwx0G8JOnMrywElF9ePdbVr+/qp0div+NoXchtH0z5KUV+MBTxmdmlrypLD1UO1gMCgYAMfbi8ZGyUZhWJUySv7vj4mTZ0cCdvQH1kvGm/v4ZGSc35DNmAuEf0xxDLDbICtFtCjHDWXO2GmBW3iKvsxWqgqcL/wFtulsPmC+v2lvyE/MndC+n1STr9UXB1SuvFQVgN5ibnQ2wfFyL6YTrysTnBEfTJCkp1bCqZieVRxB+6UwKBgE5cDGLdogaTNaTWdyCgEH+KnDtsEhrsgqZz//IwRA9Wx5vCJZxtyDCinQYzG7a/5OYC7ymDHaNq943W0zgvs15KujFUF/1nX60y51Cu2qLZ2mCEKKKgktJr+oyDFvWUI18wxI8y+P4aiMGxuSHUfzahTZ4x6Eu8K/qgNolDUHLz
    -----END RSA PRIVATE KEY-----'''

    # 如果在Linux下，我们可以采用AliPay方法的app_private_key_path和alipay_public_key_path方法直接读取.emp文件来完成签证
    # 在windows下，默认生成的txt文件，会有两个问题
    # 1、格式不标准
    # 2、编码不正确 windows 默认编码是gbk

    # 实例化应用
    alipay = AliPay(
        appid="2016093000628370",  # 支付宝app的id
        app_notify_url=None,  # 回调视图
        app_private_key_string=app_private_key_string,  # 私钥字符
        alipay_public_key_string=alipay_public_key_string,  # 公钥字符
        sign_type="RSA2",  # 加密方法
    )
    # 发起支付
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=order_id,  # 订单号
        total_amount=str(money),  # 将Decimal类型转换为字符串交给支付宝
        subject="商贸商城",
        return_url=None,
        notify_url=None  # 可选, 不填则使用默认notify url
    )
    # 让用户进行支付的支付宝页面网址
    return "https://openapi.alipaydev.com/gateway.do?" + order_string