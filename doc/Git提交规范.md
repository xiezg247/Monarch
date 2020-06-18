## Git Commit提交规范

### 包含部分
每次提交，commit message包含三个部分：Header， Body，Footer。Header为必需，Body可简略说明一下或者省略，footer如无必要，可以不写。

### 遵循标准
- 所有注释尽量使用英文
- 注释要清晰，尽量包括who how do what
- 每次提交都是解决一类问题，做好问题归类，尽量减少一个问题多个commit的情况(可暂不提交到远程仓库，先在本地的git库中)

### 格式讲解

```
<type>(<scope>): <subject>
<BLANK LINE>
<body>
<BLANK LINE>
<footer>
```
- Header必填, 描述主要修改类型和内容
- Body选填，描述为什么修改, 做了什么样的修改, 以及开发的思路
- Footer可不填，描述Breaking Changes 或 Closed Issues
#### Header

##### type

- feat: 新特性

- enhance: 优化

- fix: 修改问题

- refactor: 代码重构

- docs: 文档修改

- style: 代码格式修改, 注意不是 css 修改

- test: 测试用例修改

- chore: 其他修改, 比如构建流程, 依赖管理.

##### scope

commit 影响的范围 

- 前端: route, component, utils, build…
- 后端: model，view，controller, service, task...

可使用×来描述不太合适的scope
##### subject

commit 的概述, 建议符合 50/72 formatting

- 使用第一人称现在时
- 第一个字母小写
- 结尾不加句号

##### body

commdit 具体修改内容, 可以分为多行, 建议符合 50/72 formatting
- 使用第一人称现在时
- 包括变动的原因和与之前的对比

##### footer

一些备注, 通常是 BREAKING CHANGE 或修复的 bug 的链接.

- 不兼容改动
所有不兼容变更需要放在 footer 上，并且以 BREAKING CHANGE开始，后面是对变更的描述以及理由和迁移方法。

- 关联issues
关闭 issues 必须在 footer 区域的分开的一行，以“Closes”关键词开头：
```
Close #234
```

当然也可以关闭多个：
```
Close #123, #245, #992
```

### 例子
- [angular](https://github.com/angular/angular)

### 参考
- [AngularJS Git Message Conventions](https://docs.google.com/document/d/1QrDFcIiPjSLDn3EL15IJygNPiHORgU1_OOAqWjiDU5Y/edit#heading=h.uyo6cb12dt6w)
