# 创建公开仓库，这里演示名为【box_tvlive】
添加 readme 文件，默认main分支

# 获取token
【右上角头像】-【Settings】-【Developer settings】-【Personal access tokens】-【Tokens】-【Generate new token】-【Generate new token (classic)】  
【Note】可以随便填写名称，这边演示为【actions】  
【Expiration】选择【No expiration】 永不过期  
【Select scopes】勾选下面的【repo】即可，拉到最下面，按绿色的【Generate token】  
会得到【ghp_xxxxxxxxxxxxxxxxxxx】的一串token值，记得保存好，这个只显示一次  

# 添加私密变量
在box_tvlive仓库内，选【Settings】-左侧下面的【Secrets】-【Actions】-页面中间右上角绿色的按钮【New repository secret】  
【Name】填写【TOKEN】  
【Secret】填写上一步获取的token值【ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx】  
【Add secret】  

# 创建分支，这里演示名为【bf】
点击页面中间左上角的【main】分支，搜索框搜索【bf】，点击下方弹出的【Create branch: bf from main'】即可创建分支  

# 修改配置文件
【data.txt】保存的是数据源  
格式为：类型@=链接，需要用 @= 分隔开，一行一条源数据地址  
类型有：【m3u】，【txt】，【keep】  
【m3u】格式为 第一行#EXTINF开头，第二行为链接  
【txt】格式为  第一行【分类名称,#genre#】，下面n行 【节目名，链接】  
【keep】格式为 【节目名，链接】，与【txt】格式类似，但是不能包含分类，例如这个【分类名称,#genre#】，且里面的源不会进行自动检测是否有效，tvbox中会自动归类为【自选频道】  
【name.txt】是在tvbox中，所要保留的 电视台名，会自动归类到【更多频道】  

【settings.txt】是设置 【用户名】，【仓库名】和【分支名】  
格式为：类别=内容，需要用 = 分隔开，一行一条数据
第一行必须是用户名，第二行必须是仓库名，第三行必须是分支名

【log.txt】是存放在【bf】分支的，用作调试输出日志  

【live_lists.txt】是存放在【bf】分支的，用作输出可用的数据源

【all_list.txt】是存放在【bf】分支的，用作输出所有的数据源，包括失效的

【main.py】爬取程序，无需修改  

【box_tvlists.yml】github actions的配置文件，如果默认创建的是【main】分支则无需修改，如果创建的是【master】分支，则需要在第4行的branches: [ main ]改成branches: [ master ]

# 部署 
在【box_tvlive】仓库的【bf】分支 上传【log.txt】和【live_lists.txt】文件

在【box_tvlive】仓库的【main】分支 上传 【main.py】、【data.txt】、【name.txt】、【settings.txt】文件

点击页面中间的【Actions】，在搜索框搜索【python】找到【Publish Python Package】，点击【Configure】
修改一下上面的文件名，这边改成【box_tvlists.yml】，再把下面的内容全部删掉，复制粘贴【box_tvlists.yml】文件里面的内容进去，点右上角绿色按钮的【Start commit】【Commit new file】

再次点点击页面中间的【Actions】即可看到 workflow run 正在运行，点击【Create box_tvlists.yml 】【build-linux】可以看到运行的情况

