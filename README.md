# Backend

## git 現有的項目到 github 當中

先進行初始化本機端
```
git init
```
遠端(remote)建立一個連線，連線至 https://github.com/e-Toilet/Backend.git 並命名為 origin
```
git remote add origin https://github.com/e-Toilet/Backend.git
```

不確定是否必要，把本機端的 branch master rename 成 main
```
git branch -m master main
```

從 origin 端拉下名為 main 的 branch，且與本機端的 main 合併。
```
git pull origin main:main
git pull (遠端) (遠端分支):(本機分支)
```

![圖片](https://user-images.githubusercontent.com/95761806/145253882-8dfc2306-d1f3-4499-8c3c-33b16a69c1e9.png)

把目前所有的檔案加入到索引， . = all
```
git add .
```

目前加入的檔案 commit 到本機端，取一個註解名
```
git commit -m '<name>'
```

把本機的main push 到遠端的 main  (btw如果本機分支與遠端分支同名，可以省略:)
```
git push -u origin main:main

git push (遠端) (本機分支):(遠端分支)
```

完成 push !
  
[參考](https://blog.csdn.net/kuangdacaikuang/article/details/84632883)
[push -u的意義](https://blog.csdn.net/Lakers2015/article/details/111318801)
