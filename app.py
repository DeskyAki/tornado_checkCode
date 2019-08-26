
import tornado.ioloop
import tornado.web
import io
import check_code


class CheckCodeHandler(tornado.web.RequestHandler):
    def get(self):
        # 创建一个文件流
        mstream = io.BytesIO()
        # 生成图片对象和对应字符串
        img, code = check_code.create_validate_code()
        # 将图片信息保存到文件流
        img.save(mstream, "GIF")
        # self.session["CheckCode"] = code
        # 嫌麻烦存在了cookie里了
        self.set_cookie('CheckCode', code)
        print(mstream.getvalue())
        self.write(mstream.getvalue())


class MainHandler(tornado.web.RequestHandler):

    # 添加一个处理get请求方式的方法
    def get(self):
        self.render('index.html')

    def post(self, *args, **kwargs):
        username = self.get_argument('user')
        password = self.get_argument('pwd')
        code = self.get_argument('code')
        right_code = self.get_cookie('CheckCode')
        if username == 'admin' and password == '123' and code.upper() == right_code.upper():
            self.write('登录成功')
        else:
            self.write('用户密码错误')
        self.clear_cookie('CheckCode')


settings = {
    'template_path': 'template',
    'static_path': 'static',
    'static_url_prefix': '/static/',
    'cookie_secret': 'aiuasdhflashjdfoiuashdfiuh',
}

application = tornado.web.Application([
    (r"/index", MainHandler),
    (r"/check_code", CheckCodeHandler),
], **settings)


if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
