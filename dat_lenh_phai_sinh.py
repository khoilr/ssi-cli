import gevent.monkey

gevent.monkey.patch_all()

from ssi_fctrading import FCTradingClient

from ssi.trading import fc_der_new_order, fc_get_otp, fc_verity_code
from ssi import config

if __name__ == "__main__":
    # ======== THÔNG TIN LỆNH ======== #
    instrumentID = "VN30F2104"  # Mã chứng khoán
    market = "VNFE"  # Thị trường ('VN' hoặc 'VNFE')
    buySell = "B"  # Vị thế (B: mua, S: bán)
    orderType = "MTL"  # Loại lệnh (LO, ATO, ATC, MTL, MOK, MAK)
    price = 0  # Giá. Với lệnh LO, giá phải lớn hơn 0; với các lệnh khác price = 0
    quantity = 1  # Khối lượng
    account = "0000000000"  # Tài khoản
    stopOrder = False  # Chỉ áp dụng cho thị trường VNFE. True nếu là lệnh điều kiện, False nếu là lệnh thường
    stopPrice = 0  # Nếu stopOrder là True, thì stopPrice phải lớn hơn 0
    stopType = ""  # Nu stopOrder là True, thì stopType phải là mot trong (D: Down, U: Up, V: Trailing Up, E: Trailing Down, O: OCO)
    stopStep = 0  # Nếu stopOrder là True, thì stopStep phải lớn hơn 0
    lossStep = 0  # Nếu stopOrder là True và stopType là B, thì lossStep phải lớn hơn 0
    profitStep = 0  # Nếu stopOrder là True và stopType là B, thì profitStep phải lớn hơn 0
    # ================================ #

    client = FCTradingClient(
        config.url_trading,
        config.consumer_id,
        config.consumer_secret,
        config.private_key,
        config.two_fa_type,
    )

    # Xác thực hai yếu tố
    fc_get_otp(client)
    print("Mã OTP đã được gửi đến số điện thoại hoặc email của bạn.")
    otp = input("Nhập mã OTP: ")
    fc_verity_code(client, otp)

    res = fc_der_new_order(
        client=client,
        instrumentID=instrumentID,
        market=market,
        buySell=buySell,
        orderType=orderType,
        price=price,
        quantity=quantity,
        account=account,
        stopOrder=stopOrder,
        stopPrice=stopPrice,
        stopType=stopType,
        stopStep=stopStep,
        lossStep=lossStep,
        profitStep=profitStep,
    )
    if res.status == 200:
        print("Đặt lệnh thành công")
        print(res.message)
    else:
        print("Đặt lệnh thất bại")
        print(res.message)
