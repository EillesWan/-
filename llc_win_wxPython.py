

import wx

__ver__ = '0.0.1'
__author__ = '金羿Eilles'




class MainWindow(wx.Frame):
    """We simply derive a new class of Frame."""
    def __init__(self, *args, **kargs):
        super(MainWindow, self).__init__(*args, **kargs)
        

        #创建位于窗口的底部的状态栏
        self.CreateStatusBar()

        # 设置菜单
        filemenu = wx.Menu()

        #wx.ID_ABOUT和wx.ID_EXIT是wxWidgets提供的标准ID
        filemenu.Append(wx.ID_ABOUT, _(u"关于"), _(u"h关于"))
        filemenu.AppendSeparator()
        filemenu.Append(wx.ID_EXIT, item=_(u"退出"), helpString=_(r'h退出') )

        # 创建菜单栏
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, u"文件")
        self.SetMenuBar(menuBar)
        
        # 创建图标
        icon = wx.Icon(name="./resources/msctIcon.png")
        self.SetIcon(icon)

        self.Show(True)

    def initArgs(
        self,
        debug: bool = False,
        menuWidget: dict = {},
        wordView: str = '音·创 Musicreater',
        buttons: list = [],
        settingBox: list = [],
        notemap: list = [],
        infobar: str = '就绪',
    ) -> None:
        '''使用参数初始化一些基本的音·创窗口组件
        :param debug 是否将日志输出到控制台
        wordview: str #言论部分显示的字样
        button: list = [ # 操作按钮部分
            dict = {
                按钮名称 : tuple(按钮图标,执行函数)
            },
        ],
        settingbox: list = [ # 设置部分显示的字样及其对应的设置函数
            (
                设置名称:str,
                值类型:tuple,
                显示内容:str,
                设置操作函数:<function>,
            )
        ],
        map: list = [ # 一首曲目的音符数据
            音符数据
        ]
        :param infobar str 显示信息用
        '''

        if debug:
            log('载入参数')

        # 载入参量 注意！图标将不被载入参数



        self.menuWidgets = menuWidget
        '''菜单设定项'''

        self.wordView = wordView
        '''言·论 所显示的文字'''

        self.buttons = buttons
        '''快捷功能按钮'''

        self.settingBox = settingBox
        '''设置框'''

        self.notemap = notemap
        '''音符列表'''

        self.infoBar = infobar
        '''信息显示版所显示的文字'''

        self.debug = debug
        '''是否打开调试模式'''
    

    def setMenu(self) -> None:
        '''设置根菜单'''
        if not self.menuWidgets:
            # 如果传入空参数则返回当前菜单
            try:
                return self._RootMenu
            except Exception as E:
                if self.debug:
                    raise E
                log('无法读取菜单信息', 'ERROR')
        # 如果不是空参数则新建菜单
        log('新建一个菜单')

        self._RootMenu = {}
        self._mainMenuBar = wx.MenuBar()
        
        # 取得一个菜单名和一堆菜单函数及其显示名称
        for menuName, menuCmd in self.menuWidgets.items():

            # 新建一个菜单
            menu = wx.Menu()

            # 循环得到菜单下的项目，并载入其中
            for cmdName, cmdFunc in menuCmd.items():
                if cmdName:
                    menu.add_command(label=cmdName, command=cmdFunc)
                    log('菜单项 -- ' + cmdName)
                else:
                    menu.add_separator()
                    log('分隔符 -- 分隔符')
            self._mainMenuBar.add_cascade(label=menuName, menu=menu)
            self._RootMenu[menuName] = menu
            log('计入一个菜单 -- ' + menuName)
        self.__root.config(menu=self._mainMenuBar)
        log('菜单设置完毕')



def __main__():
    app = wx.App(False) 
    frame = MainWindow(None, id=wx.ID_ANY, title=f"{_('F音创')} {__ver__}", size=(1600, 900))

    app.MainLoop()
        


if __name__ == '__main__':
    __main__()
