import os
import panel as pn
from dotenv import load_dotenv


# 确保加载面板扩展以实现基于 Web 的可视化。
pn.extension()


class Utils:
    """
    实用工具类，用于从环境变量中获取配置信息。
    """
    def __init__(self):
        # 实例创建时只加载一次环境变量。
        load_dotenv()

    def get_dlai_api_key(self):
        """
        从环境变量中检索 DLAI API 密钥。

        返回值：
            str: DLAI API 密钥（如果已设置）；否则为 None。
        """
        return os.getenv("DLAI_API_KEY")

    def get_dlai_url(self):
        """
        从环境变量中获取 DLAI API URL。

        返回值：
            str: DLAI API URL（如果已设置）；否则为 None。
        """
        print(os.getenv("DLAI_API_URL"))

        return os.getenv("DLAI_API_URL")


class UploadFile:
    """
    通过面板小部件处理文件上传，仅允许特定文件类型。
    """
    def __init__(self):
        self.widget_file_upload = pn.widgets.FileInput(accept='.pdf,.ppt,.png,.html', multiple=False)
        # 注意 "文件名" 的变化，以触发 save_filename 方法。
        self.widget_file_upload.param.watch(self.save_filename, 'filename')

    def save_filename(self, event):
        """
        如果上传文件的大小在限制范围内（2 MB），则保存该文件。

        参数：
            event: 包含文件输入小部件中更改的详细信息。不直接用于此功能，但回调签名需要它。

        如果文件大小超过 2 MB 限制，则打印信息，否则保存文件。
        """
        # 将文件大小限制为 2 MB。
        max_file_size = 2 * 1024 * 1024

        if len(self.widget_file_upload.value) > max_file_size:
            print("文件过大。2 MB 限制！")
        else:
            # 确保目录存在。
            output_dir = './example_files'
            os.makedirs(output_dir, exist_ok=True)

            # 将文件保存到指定目录。
            with open(os.path.join(output_dir, self.widget_file_upload.filename), 'wb') as f:
                f.write(self.widget_file_upload.value)
