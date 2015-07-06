app-turbo Tutorial
=================

app-turbo 应用的主要结构分为

- [models](model)
- [helpers](helper)
- [app-server](app-server)
- [db](db)


models 包含每个 db 实例对应的 collection，models 由一个到多个model 组成，每个model 对应一个db。

app-server 是独立的应用 server，非 package，根据需要可以有一个到多个 app-server。

helpers 由一个到多个 helper 组成，helper 是对 db 业务的实现，helper 中继承和实例化 model 层，执行对每个 collection 的具体操作，供 app-server 使用。

db 是 mongodb 的连接配置
