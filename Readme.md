# Sina Weibo Spider

![](https://img.shields.io/badge/License-GPL-brightgreen) ![](https://img.shields.io/badge/Scrapy-v2.4-blue) ![](https://img.shields.io/badge/Python-v3.8-orange) ![](https://img.shields.io/badge/Spider-Weibo-yellow)

## Preface

这个微博爬虫的实现近乎贯穿了我本科学习大半的时间。前前后后经过了大约有3次颠覆级别的重构之后，现在看起来也算是稍微有了那么一点点看得过去的样子。经过小半个月的摸鱼划水，我也完成了对这个微博爬虫从架构的重构到具体实现的优化，以及设计提供自动化部署脚本等工作，使得这个爬虫比较与v1.0版本简直是高到不知道哪里去了。（膜法警告:warning:）其中，v1.0版本的代码可以在仓库分支v1.0中查看，确实是一段不堪回首的往事呀。

总而言之，在不断对地对代码进行重构和优化的过程中，我也在不断地学习。前路漫长，要学的东西还有很多，如果可能的话我会长期对这个项目进行维护（前提是有空摸鱼），也会提供尽可能详细的说明文档，欢迎各位大手子提PR或者Issue，同时也求一个小小的star🌟，也算是我为诸位还在为如何从微博采集数据烦恼的研究者们做出的一点微小的贡献吧。

## 为什么选择M站采集数据？

首先要说明最重要的一点是，本项目是基于开源爬虫框架[**Scrapy**](https://scrapy.org)，针对新浪微博的**移动站点**，即[**M站**](https://m.weibo.cn)，实现的一个**单机**、**高并发**且**高性能**的轻量微博爬虫。

解释一下什么是新浪微博的M站。随着一堆乱七八糟的技术的迅速发展（别问，问我我也不懂是啥），越来越多的国产手机APP（此处特指安卓下）都倾向于在APP中内置一个游览器内核（一般来说都是chromium，不过可能伴随一些魔改），然后通过前端开发实现APP的快速迭代。M站简单明了的说，就是用于为手机客户端的微博APP提供数据来源。（这一段中包含了我许许多多的胡说八道，如果有各种离谱的错误请尽管喷我）

通常，在实现爬虫之前，开发者都需要对目标站点的反爬措施进行充分的调研，然后才下手开干。对于微博来说，现目前已知有三个不同的域名都能够使用其提供的服务。其分别是[**PC站**](https://weibo.com)、[**M站**](https://m.weibo.cn)和一个我不知道该怎么称呼并且[**十分简陋的站**](https://weibo.cn)。所谓PC站就是使用PC端游览器访问新浪微博所看到的网站，M站即前文所述，十分简陋站我现在也不知道是干嘛的，就很尴尬。

这三个站在反爬措施的严格程度上差异较大，其中PC站的反爬措施是最严格的，而M站和十分简陋站的反爬措施设置较为宽松。这之中的缘由也简单易懂，PC站一般而言作为诸多爬虫爱好者的首选目标，自然是承受了非常多的爬虫流量，新浪微博当然也会部署最为严格的反爬措施保证他不会被乱七八糟的爬虫搞崩掉。据我不那么完全的观察，github上现存有数个在3-4年前就已经停止维护的针对PC站的微博爬虫。

由于PC站的反爬虫措施十分的严格，开发者需要耗费大量的经历来绕过反爬机制。这些反爬机制（某些机制不一定仅限于PC站，其它站点同样也适用）主要包含有，如：

1. 对异常IP流量的检测。（说人话就是单个IP的HTTP请求太多了会被封掉）
2. 对用户数据的保护。（不登陆账号就不给你看完整的用户数据）
3. 账户登陆IP的异常检测。（同一个账号使用者的IP不能够上一秒还在美国，下一秒就到了澳大利亚）
4. 以及形形色色、乱七八糟的验证码等等。

同时，本文也大概地总结一下许许多多的前辈他们为了绕过PC的反爬措施需要做的工作：

1. 首先是购买一批专门用来爬数据的小号，构建一个账户池。
2. 然后仔细分析研究新浪微博的认证机制， 实现自动化的模拟登录，期间可能还会遇到验证码识别等困难，可能需要接入打码平台或者人工识别。（通过深度学习的方法自动化识别验证码又是另一个问题了）
3. 通过伪造正常用户的登录过程，模拟登录构建，获取Cookie构建Cookie池，用这些cookie进行下一步的爬取。
4. 购买一定数量的代理IP，为每个cookie（实际上是账户）绑定代理IP。
5. 经过冲冲磨难最终才绕过了反爬，在爬取的过程中还要注意各cookie-IP的负载均衡，在cookie失效之后需要即使的清理。
6. 综上所述，针对PC站爬取数据属实头铁，就算拿到数据之后还需要复杂的数据清洗，才能够得到最终的用户数据，并且采集效率极低，出错率高，很难保证在大规模的数据采集中，能够拿到完整的用户数据。

与之相反的是，微博的M站和十分简陋站的反爬措施就宽松很多。针对十分简陋站，有大佬已经开发了十分完整且可用性极强的爬虫，此处放上传送门[nghuyong:WeiboSpider](https://github.com/nghuyong/WeiboSpider )，能够获取千万级别甚至更高数量级的数据，可以采集到较为完整的微博用户数据。但这个爬虫有一个问题在于，即使十分简陋站的反爬较为宽松，但**仍然需要购买小号建立cookie池**之后才可以进行数据采集。当然，为了提高数据采集的速率，代理IP也是需要的。

综上所述，偷鸡的我选择了微博的**M站**开发爬虫，**无需买小号构建cookie池**，甚至也不需要代理IP（当然对采集速度有很大的限制），就实现了一个轻量高效地微博爬虫。

## 设计原理

简单阐述一下M站微博爬虫的设计原理。打开Firefox游览器（Chrome，Safari啥的都行），输入任意一个微博用户主页的M站网址，这里随便拿一个公众明星[鞠婧祎](https://m.weibo.cn/u/3669102477 )的账户举例通过F12开发者工具，观察微博M站数据加载的过程，结果如下图所示。重点观察红框内的两个请求，事实上微博的M站通过**AJAX**来异步加载用户数据，红框内对应的两个链接，实际为鞠婧祎这个用户的账户信息获取接口，将这个URL提取出来即为：

`https://m.weibo.cn/api/container/getIndex?type=uid&value=3669102477&containerid=1005053669102477`

显然，`3669102477`是鞠婧祎这个账户的**UID**，而`containerid`的构造方法为`100505+uid`，由此分析得出了M站中用户账户资料的数据获取接口。

<img src="img\1.png" style="zoom:50%;" />

打开刚刚分析得到的数据接口，获取到JSON格式的用户数据，如下图所示，可以直接存储到MongoDB等非关系型数据库中。

<img src="img\2.png" style="zoom:50%;" />

同理可推，只要针对微博M站进行仔细的人工分析，就可以提取出微博用户数据请求的构造方法。并且，通过这样的数据接口获取数据不需要进行**用户认证**，也能够获取到**较为完整**的用户数据，意味着即使没有用户cookie，也能够对新浪微博进行大规模的数据采集。

本项目正是根据新浪微博M站这样的特点来构造微博爬虫。

## 为什么使用针对M站的微博爬虫？

咳咳，虽然不免有王婆卖瓜的嫌疑，但也要对本项目的核心亮点进行一下简要的阐述。

1. 轻量：本项目的核心代码大概在500行左右，由于选择了最轻松的道路，所以实现的过程十分愉快，也尽可能的保证了项目的可扩展性和易用性，加之提供了自动化部署脚本，保证在使用上能够做到轻松愉悦。
2. 易用：本项目不需要构建额外的用户池，最多只需要使用额外的代理IP来提高采集速度，就可以实现百万级别的用户数据采集，易用性非常高。
3. 迅速：由于爬取到的数据本身即为JSON格式，所以基本无需进行数据清洗，也大大提高了爬虫的采集速率。同时，通过M站的数据接口获取的JSON数据信息丰度极高，通过一个请求就能够获取到10条左右的博文数据。

## To Start

### 运行环境

- 操作系统：常见的Linux发行版目测都是可行的（本机开发测试环境为Ubuntu 20.04）

- Python >= 3.6.0，本机开发Python版本为3.8.10
- MongoDB >= 4.2
- Docker，开发环境的Docker版本为20.10.7，保持Docker版本最新即可

### 初始化

首先执行下列代码，将爬虫Clone到本地之后，安装相关环境依赖。

```shell
git clone git@github.com:CharesFang/WeiboSpider.git
cd WeiboSpider
pip install -r requirements.txt
```

然后为初始化脚本`./init/init.sh`赋予权限后执行，创建用于存储数据的MongoDB Docker Container.

```shell
sudo chmod 755 ./init/init.sh
./init/init.sh
```

`Init.sh`脚本会为创建MongoDB Container运行必要的配置文件，映射目录等。MongoDB Container数据存储在宿主机的目录为`"$HOME/mongo"`.

然后，根据`init.sh`脚本的提示，执行下列命令，调用MongoDB数据库初始化脚本`db_init.js`，分别创建`admin`管理员用户和一般数据库使用者`weibo`，以及用于存储微博数据的数据库`weibo`和`tweet, user`等集合，请妥善保存这两个用户的密码。

```shell
sudo docker exec -it weibo mongo 127.0.0.1:27017 /etc/resource/db_init.js
```

最后，重写`./WeiboSpider/database/DBconnector.py`文件中的`__init__`方法，将自己的密码写入`__init__`方法中，用于爬虫连接MongoDB数据库。

```python
def __init__(self):
  self.mongo_uri = "127.0.0.1" # 一般不会改写这个参数，因为连接的是本地Docker.
  self.mongo_database = "weibo" # init.sh中创建的`weibo`数据库.
  self.mongo_user_name = "weibo" # init.sh中创建的`weibo`数据库用户`weibo`.
  self.mongo_pass_wd = "Your password."
```

至此，完成爬虫的初始化设置。

### 启动爬虫

微博爬虫的调用方式同其他Scrapy爬虫一样，可以通过命令行或者Python脚本两种方法调用。

#### 命令行调用

本项目目前实现了三个爬虫，它们的具体功能和命令行调用方法如下表所示。

|    Spider Name     |                      CMD                       |                           Function                           |
| :----------------: | :--------------------------------------------: | :----------------------------------------------------------: |
|   `weibo_spider`   |  scrapy crawl weibo_spider -a uid=xxx&verbar;xxx   | 对目标微博用户的账户资料和所有博文进行采集，其中必须传入的参数"-a uid=xxx&verbar;xxx"为目标采集用户的`uid`，多个`uid`间以 &verbar; 分割。 |
| `user_info_spider` | scrapy crawl user_info_spdier -a uid=xxx&verbar;xxx | 对目标微博用户的账户资料进行采集，参数传递同`weibo_spider`.  |
|   `tweet_spider`   |   scrapy crwal tweet_spider -a uid=xxx&verbar;xxx   | 对目标微博用户的所有博文进行采集，参数传递同`weibo_spider`.  |

Markdown对于某些特殊字符的渲染不是特别到位，导致先前上述表格的显示不完整，现已经修复。

#### Python脚本调用

Python脚本调用实质上也是通过CMD调用爬虫，可以方便爬虫的调试。调用脚本示例如下。

```python
from scrapy.cmdline import execute


if __name__ == '__main__':
    spider_cmd = "scrapy crawl weibo_spider -a uid=user0|user2"
    execute(spider_cmd.split())
```

## Docs

To be contiuned...暂时先挖一个坑...

### Init

### WeiboSpider

#### Base

#### Conofig

#### Spiders

#### Items

#### Pipelines

#### Middlewares

### Database

### Extension

#### 我需要做什么？

#### 定义你自己的爬虫

###更新 

2022/5/20
1. 主要 url里page替换成了since_id
2. 不登录，最多2000千条记录
3. LongText 那个URL经常不稳定，可能和反爬有关

2022/5/21
1. Mainly modify the last_page as the controller of the craw cycles.


