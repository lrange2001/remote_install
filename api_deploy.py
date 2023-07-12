from flask import Flask, request
import json
import os
import subprocess
app = Flask(__name__)

#定义预上传文件以及对应的脚本
install_list = {'unicorn_admin-1.0.jar':'start.sh','dist.zip':'deploy.sh'}


#定义接口响应类
class ApiReturn:
    def __init__(self):
        self.success = None
        self.error = None
        self.code = None
        self.msg = [None]
        self.dict1 = {"code":"status_code","msg":"message"}

    @staticmethod
    def delNone(dellist: list):
        '''删除初始化时的空值'''
        dellist.remove(None)

    def SendSuccess(self):
        '''更改初始化的空值 并返回json响应'''
        self.msg.append("SUCCESS")
        self.code = 200
        self.delNone(self.msg)
        for key, value in [('code', self.code), ('msg', self.msg[0])]:
            self.dict1[key] = value
        return json.dumps(self.dict1)

    # def SendError(self):
    #     '''更改初始化的空值 并返回json响应'''
    #     self.msg.append('ERROR')
    #     self.code = 502
    #     self.delNone(self.msg)
    #     for key, value in [('code', self.code), ('msg', self.msg[0])]:
    #         self.dict1[key] = value
    #     return json.dumps(self.dict1)

    @staticmethod
    def SendHandle(code,msg):
        '''自定义返回json响应'''
        result_dict1 = {"code":code,"msg":str(msg).replace('\n\r','')}
        return json.dumps(result_dict1)


'''upload接口 要求POST请求'''
@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        return_result = ApiReturn()
        '''获取文件对象s'''
        file = request.files['file']
        if file:
            '''保存文件'''
            file.save(os.path.join('C:',file.filename))
            # status = 0 if 'dist' in file.filename else 1
            # install_sh = install_list[status]
            '''判断文件名称是否存符合上传要求 install_list字典当中'''
            if install_list.get(str(file.filename)):
                '''符合要求时 执行install_list字典当中对应的脚本文件'''
                command_result = subprocess.run(['sh',os.path.join('/','%s'%install_list.get(str(file.filename)))],capture_output=True, text=True)
                '''脚本运行正常时 返回结果，不正常时返回报错'''
                return return_result.SendSuccess() if command_result.stdout else return_result.SendHandle(code=502,msg=str(command_result.stderr))
            
            else:
                '''文件不符合要求返回'''
                list1 = [key for key,value in install_list.items()]
                return ApiReturn.SendHandle(code=502,msg="请按照格式上传文件%s"%list1)
    except Exception as messageError:
        '''程序异常时 通过接口响应'''
        return_result = ApiReturn()
        return ApiReturn.SendHandle(code=502,msg=str(messageError))


if __name__ == '__main__':
    app.run(debug=True,port=3444)
