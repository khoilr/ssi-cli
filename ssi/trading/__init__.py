import random
import uuid

from ssi_fctrading import FCTradingClient
from ssi_fctrading.models import fcmodel_requests

from ssi import config


def fc_der_new_order(
    client,
    instrumentID: str,
    market: str,
    buySell: str,
    orderType: str,
    price: float,
    quantity: int,
    account: str,
    stopOrder: bool = False,
    stopPrice: float = 0,
    stopType: str = "",
    stopStep: float = 0,
    lossStep: float = 0,
    profitStep: float = 0,
    deviceId: str = uuid.UUID(int=uuid.getnode()),
    userAgent: str = FCTradingClient.get_user_agent(),
):
    fc_req = fcmodel_requests.NewOrder(
        str(account).upper(),
        str(random.randint(0, 99999999)),
        str(instrumentID).upper(),
        str(market).upper(),
        str(buySell).upper(),
        str(orderType).upper(),
        float(price),
        int(quantity),
        bool(stopOrder),
        float(stopPrice),
        str(stopType),
        float(stopStep),
        float(lossStep),
        float(profitStep),
        deviceId=str(deviceId),
        userAgent=str(userAgent),
    )
    res = client.der_new_order(fc_req)
    return res


def fc_get_otp(client):
    """Get OPT if you use SMS OTP or Email OTP

    Returns:
            string: response json string
    """
    fc_req = fcmodel_requests.GetOTP(config.consumer_id, config.consumer_secret)
    return client.get_otp(fc_req)


def fc_verity_code(client, code: str):
    """Verify OTP or PIN (with TwoFAType in your config), if you use SMS OTP or Email OTP please get call getOtp to receive OTP before verify.
     This function auto save OTP and access token for New/Modify/Cancel order

    Returns:
            string: response json string
    """
    return client.verifyCode(code)
