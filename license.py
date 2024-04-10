import os
import sys
import time
import shutil
import logging
import requests
from enum import Enum
from functools import wraps
from zipfile import ZipFile

logging.basicConfig(
    level=logging.INFO,
    filename='../license.log',
    filemode='a+',
    datefmt='%Y-%m-%d %H:%M:%S',
    format='%(asctime)s [line:%(lineno)d] %(levelname)s %(message)s'
)


def log(func):
    @wraps(func)
    def inner(*args, **kwargs):
        param = args[1:] if isinstance(args[0], object) else args
        try:
            res = func(*args, **kwargs)
            logging.info(f"{func.__name__}调用参数：{param}  {kwargs}->{str(res)}")
            return res
        except Exception as e:
            logging.error(f'{func.__name__}调用异常:{e},参数：{param}  {kwargs}')
            print("\033[1;31m", f'{func.__name__}调用异常:{e},参数：{param}  {kwargs}')
            sys.exit(0)

    return inner


class License:
    _session = requests.Session()

    class Product(Enum):
        ONE = '1'
        SERVER = '2'

    class Deploy(Enum):
        POC = '1'
        CLUSTER = '2'

    def __init__(self):
        self.apply_host = 'http://10.241.110.1:6088'
        self.active_host = 'http://120.133.67.133:20007'
        self.token = 'eyJhbGciOiJIUzI1NiJ9'
        self.username = "admin"
        self.password = "Vayt32IzfiAG/16UBOpEMaV9O6RxlZSZwxQuzRaj4q4="
        self._login()

    """
    登录激活套餐平台，获取激活码步骤需携带cookie所用
    """

    @log
    def _login(self):
        data = {
            "accountName": self.username,
            "password": self.password,
            "captcha": "bonree"
        }
        return self._session.post(f'{self.active_host}/rest/login', json=data).text

    """
    申请license
    """

    @log
    def apply_license(self, license_data):
        push_response = self._session.post(f'{self.apply_host}/api/pushReeJoinLicenseOrder', json=license_data).text
        data = {"orderNo": license_data["orderNo"], "token": self.token, "productTypes": "one"}
        generate_response = self._session.post(f"{self.apply_host}/api/generateReeJoinLicense", json=data).text
        return push_response, generate_response

    """
    根据申请单号下载并解压提取license
    """

    @log
    def download_license(self, order_no, save_path=''):

        order_no = str(order_no)
        suffix = '.zip'
        if save_path == '':
            current_path = os.path.dirname(os.path.realpath(__file__))
            file_path = os.path.join(current_path, '../license', order_no)
            file_name = os.path.join(save_path, order_no + suffix)
        else:
            file_path = os.path.join(save_path, '../license', order_no)
            if not os.path.exists(file_path):
                os.makedirs(save_path)
            file_name = os.path.join(file_path, order_no + suffix)

        license_content = self._session.get(f"{self.active_host}/rest/mgmt/download/{order_no}").content

        with open(file_name, "wb") as code:
            code.write(license_content)

        try:
            with ZipFile(file_name, "r") as f:
                f.extractall(file_path)
        except Exception as e:
            raise Exception("download_license异常:" + license_content.decode())
        finally:
            os.remove(file_name)

        return {
            "order_no": order_no,
            "file_path": os.path.join(file_path, 'Bonree.lic'),
            "file_dir": file_path
        }

    """
    获取license套餐激活码
    """

    @log
    def get_active_code(self, license_file, virtual_id):
        with open(license_file, "r", encoding="utf-8") as f:
            content = f.read().replace("=============================== BRLICENSE ==================================",
                                       "")
            data = {"content": content, "virtualId": virtual_id}
            response = self._session.post(self.active_host + '/rest/generateCode', json=data).json()
            return response['data']

    """
    one产品license参数模板
    """

    @staticmethod
    def one_license_template():
        return {
            "envType": "1",
            "name": "one",
            "buyType": "1",
            "deployType": "1",
            "buyMode2": 92,
            "buyModeName2": "APM监控数据",
            "type": 9,
            "itemId2": "maxOnlineAgent",
            "itemType2": 2,
            "itemName2": "最大APM探针在线数",
            "limitedNum2": 9999,
            "buyMode1": 91,
            "buyModeName1": "DEM监控数据",
            "itemId1": "dau",
            "itemType1": 1,
            "itemName1": "日活",
            "limitedNum1": 9999999999999999,
            "buyMode3": 93,
            "buyModeName3": "基础设施",
            "itemId3": "maxOnlineNode",
            "itemType3": 2,
            "itemName3": "最大节点在线数",
            "limitedNum3": 9999
        }

    """
    server产品license参数模板
    """

    @staticmethod
    def server_license_template():
        return {}

    """
    license申请基础表单
    """

    @staticmethod
    def common_template(order_no):
        _template = {
            "orderNo": order_no,
            "contractNo": "Bonree-202209-2219-S&M-GZ0036",
            "contractValidTime": "2022.09.01 00:00:00--2029.09.30 00:00:00",
            "preSaleName": "华北售前--杨雪松",
            "applicantName": "pqg",
            "applicantEmail": "panqigui@bonree.com",
            "customerName": "pqg",
            "token": "eyJhbGciOiJIUzI1NiJ9",
            "productInfo": [

            ],
            "contractValue": "1000000",
            "saleInfo": "华北--宋戈",
            "applyTime": f"{int(time.time() * 1000)}",
            "projectName": "pqg"
        }
        return _template

    """
    申请license表单
    """

    @staticmethod
    def get_license_template(product_type: Product, deploy_type: Deploy, **kwargs):

        if product_type.value not in [product.value for product in License.Product]:
            raise Exception("传入正确产品类型枚举")

        if deploy_type.value not in [deploy.value for deploy in License.Deploy]:
            raise Exception("传入正确部署方式枚举")

        order_no = str(round(time.time() * 1000))
        license_content = License.common_template(order_no)

        product_info = None

        if product_type.value == License.Product.ONE.value:
            product_info = License.one_license_template()

        product_info["deployType"] = str(deploy_type.value)
        license_content["productInfo"].append(product_info)

        for k, v in kwargs.items():
            if k in license_content.keys():
                license_content[k] = v
        return order_no, license_content


class IAM:
    """
    :param host：项目地址
    :param password：用户密码密文
    """

    def __init__(self, host):
        self.session = requests.Session()
        self.host = host

    """
    登录获取cookie
    """

    @log
    def login(self, username, password, parent=None):
        data = {"username": username, "password": password, "captcha": "bonree"}
        if parent is not None:
            data['parentName'] = parent
        login_response = self.session.post(self.host + "/rest/login", json=data).json()
        if login_response['msg'] != 'success':
            raise Exception("登录异常：" + str(login_response))
        return login_response

    @log
    def is_login(self):
        return self.session.post(self.host + "/rest/isLogin", json={}).json()

    """
    获取环境虚拟id
    """

    @log
    def get_virtual_id(self):
        return self.session.post(f'{self.host}/rest/iam/license/virtualId').json()['data']

    """
    激活license
    """

    @log
    def active_license(self, license_file, active_code):
        files = [
            ('file', ('Bonree.lic', open(license_file, 'rb'), 'application/octet-stream'))
        ]

        license_id = self.session.post(self.host + '/rest/iam/license/upload', files=files).json()
        if license_id['data'] is None:
            raise Exception("导入license异常,检查iam服务器环境密钥：" + str(license_id))
        else:
            data = {"licenseId": license_id['data'], "code": active_code}
            response = self.session.post(self.host + '/rest/iam/license/active', json=data).json()
            return response

    """
    创建主账号，需要初始化IAM时输入admin账号密码
    """

    @log
    def create_parent_user(self, username):
        data = {
            "username": str(username),
            "onePwd": "34IxnVeXrFvkJZHWMu76vGZycdvKLndTxBnqdAm79dk=",  # 密码是前端加密生成的，不知生成规则，所以默认写死bonree123密文
            "validityTime": None,
            "receiverFlag": True,
            "contactName": "",
            "mobilePhone": "",
            "email": "panqigui@bonree.com",
            "orgName": ""
        }
        return self.session.post(self.host + '/rest/iam/account/add', json=data).json()

    @log
    def create_child_user(self, username):
        data = {
            "username": str(username),
            "onePwd": "34IxnVeXrFvkJZHWMu76vGZycdvKLndTxBnqdAm79dk=",
            "receiverFlag": True,
            "contactName": "",
            "orgName": "",
            "email": "panqigui@bonree.com",
            "mobilePhone": ""
        }
        return self.session.post(self.host + '/rest/iam/access/user/add', json=data).json()


class Tools:
    """
    更换one环境iam的环境密钥
    """

    @staticmethod
    def change_iam_pem(hostname, username, password, port=2226):
        import paramiko
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=hostname, port=port, username=username, password=password)

        pem = ""
        pem_file = '/data/br/conf/one_api/static/one-iam/rsa_public_key.pem'
        ssh_client.exec_command(f"mv {pem_file} {pem_file}.backup")
        ssh_client.exec_command(f"echo {pem} > {pem_file}")


if __name__ == '__main__':
    """
    :param product_type 部署产品：one:License.Product.ONE
    :param deploy_type  部署方式: 集群：License.Deploy.CLUSTER，poc:License.Deploy.POC
    :param apply_mail   接收license邮箱
    :param host         one平台地址，用于获取环境虚拟id、导入激活
    :param username     申请license的one平台账号
    :param password     one平台密码（密文）
    """


    def apply_license(product_type: License.Product, deploy_type: License.Deploy, apply_mail, host, username, password):
        iam = IAM(host)
        iam.login(username, password)
        virtual_id = iam.get_virtual_id()

        bonree_license = License()
        other_apply_content = {
            "applicantEmail": apply_mail
        }
        order_no, one_license = bonree_license.get_license_template(product_type, deploy_type, **other_apply_content)
        bonree_license.apply_license(one_license)
        license_file = bonree_license.download_license(order_no)

        active_code = bonree_license.get_active_code(license_file['file_path'], virtual_id)

        iam.active_license(license_file['file_path'], active_code)
        # 激活成功后删除license解压目录
        shutil.rmtree(license_file['file_dir'])


    password_dict = {
        "bonree123": "34IxnVeXrFvkJZHWMu76vGZycdvKLndTxBnqdAm79dk=",
        "bonree1234": "JrDCq22W01n7N9UBJTr8/Wwfg6TwQLVD9rp1EyfLclw=",
        "brxm@123": "7mFpTXo33fr+KyF+8/+uuwm3idTFH7x/WDJuplOb+9A="
    }

    host = "http://10.241.131.14:38090/cas/login?"
    username = "admin"
    password = password_dict["bonree123"]

    iam = IAM(host)
    # iam.login(username, password)
    parent_user_name = 'admin'
    # iam.create_parent_user(parent_user_name)
    apply_email = "yuanchongxiang@bonree.com"
    apply_license(License.Product.ONE, License.Deploy.CLUSTER, apply_email, host, parent_user_name, password)
