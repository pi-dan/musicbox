musicbox
=================
Thanks vellow

感谢原作者vellow，原作者地址：https://github.com/darknessomi/musicbox

本musicbox是由原作者vellow的musicbox修改而来

高品质网易云音乐命令行版本，简洁优雅，丝般顺滑，基于Python编写。

![NetEase-MusicBox](http://a.picphotos.baidu.com/album/s%3D1100%3Bq%3D90/sign=8db895d723a446237acaa163a812497f/a686c9177f3e670929a7aa5238c79f3df9dc55fc.jpg)

### 功能特性

1. 320kps的高品质音乐
2. 歌曲，艺术家，专辑检索
3. 网易热门歌曲排行榜
4. 网易新碟推荐
5. 网易精选歌单
6. 网易DJ节目
7. 私人歌单
8. 随心打碟
9. 本地收藏（不提供下载）
10. Vimer式快捷键让操作丝般顺滑
11. 可使用数字快捷键

### 增加或修改功能：
1. 轻微调整了显示界面
2. 歌曲列表只显示歌名与作者，去掉了专辑名
3. 增加了上下左右方向键支持（与k j h l 键功能相同）
4. 歌曲列表更随当前播放歌曲
5. 自动回到播放歌曲突出显示项，默认时间30s （在歌曲列表内）
6. 增加了进度条
7. 增加了歌曲播放通知
8. mpg123播放器替换成mplayer
### 键盘快捷键

<table>
	<tr> <td>J</td> <td>Down</td> <td>下移</td> </tr>
	<tr> <td>K</td> <td>Up</td> <td>上移</td> </tr>
	<tr> <td>H</td> <td>Back</td> <td>后退</td> </tr>
	<tr> <td>L</td> <td>Forword</td> <td>前进</td> </tr>
	<tr> <td>U</td> <td>Prev page</td> <td>上一页</td> </tr>
	<tr> <td>D</td> <td>Next page</td> <td>下一页</td> </tr>
	<tr> <td>F</td> <td>Search</td> <td>快速搜索</td> </tr>
	<tr> <td>[</td> <td>Prev song</td> <td>上一曲</td> </tr>
	<tr> <td>]</td> <td>Next song</td> <td>下一曲</td> </tr>
	<tr> <td>Space</td> <td>Play/Pause</td> <td>播放/暂停</td> </tr>
	<tr> <td>M</td> <td>Menu</td> <td>主菜单</td> </tr>
	<tr> <td>P</td> <td>Present</td> <td>当前播放列表</td> </tr>
	<tr> <td>A</td> <td>Add</td> <td>添加曲目到打碟</td> </tr>
	<tr> <td>Z</td> <td>DJ list</td> <td>打碟列表</td> </tr>
	<tr> <td>S</td> <td>Star</td> <td>添加到收藏</td> </tr>
	<tr> <td>C</td> <td>Collection</td> <td>收藏列表</td> </tr>
	<tr> <td>R</td> <td>Remove</td> <td>删除当前条目</td> </tr>
	<tr> <td>Q</td> <td>Quit</td> <td>退出</td> </tr>
</table>

################################
 需要安装mplayer
 例如：
 sudo apt-get install mpg123
 其他linux版本类似 
################################	


#### 错误处理

1. pkg_resources.DistributionNotFound: requests
	
	$ sudo pip install requests

    如果是运行 $ musicbox 出错

	$ sudo pip install --upgrade setuptools

2. pip: Command not found

	$ sudo apt-get install python-pip

3. ImportError: No module named setuptools
    
    $ sudo easy_install pip
    
    $ sudo apt-get install python-setuptools
	
### 使用

	$ musicbox


Enjoy it !

