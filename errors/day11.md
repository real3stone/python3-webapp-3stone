### MVVC

如果页面大量使用javascript代码，那么模板方式仍会导致javascript和后端代码绑定非常密切，导致难以维护

根本原因在与负责显示的HTML DOM模型与负责数据和交互的javascript代码没有分隔清楚


后端模式的MVC已经无法满足复杂页面的逻辑需求了，新的MVVC模式（Model View ViewModel）应运而生


**MVVC：** 借鉴了桌面应用程序的MVC思想，在前端页面中，把Model用纯javascript对象表示

Model： 负责数据

View： 负责显示

ViewModel： 负责把两者关联起来 （用javascript编写一个通用的ViewModel，这样就可以复用整个MVVC模型了）



