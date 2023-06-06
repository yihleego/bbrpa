# RPA

## 技术选型

- Selenium
- DrissionPage

## 调度设计

## 角色

### Server

集群多实例，无状态，可以滚动发布，提供 TCP 或 WebSocket Endpoint。

- Websocket：可以通过 Nginx 反代和负载均衡，可以通过域名连接，有现成框架
- TCP：报文小性能好，但是需要处理消息流，有开发工作量

为什么使用长连接而不是 HTTP 接口：

1. 请求频繁，减少握手次数
2. 服务端可以感知客户端是否存活
3. 服务端可以主动向客户端推送消息，如：更新了任务流程脚本，调整客户端浏览器数量等

### Client

每个机器仅一个 Client 实例，一个实例维护多个浏览器，多个机器组合成集群，通过 TCP 或 WebSocket 与 Server 保持连接。
与服务器断连后会自动尝试重连，直到连接成功。

### Browser

每个机器多个 Headless 浏览器进程，生命周期由 Client 维护，如果浏览器崩溃，Client 守护进程会重启到指定数量个。

## 流程

简单地说，客户端维护了本地所有浏览器以及登录状态，然后将本地信息上报到服务端，并轮询向服务端请求任务。
如何用户在缓存中状态是已登录，但是超过指定时间没有更新，则标记为不健康，可能是浏览器崩溃或服务端崩溃；
如果客户端崩溃，长连接断开，将该客户端下的所有用户标记为不健康，加入告警系统？

建议 Websocket，这一块性能不是瓶颈

```json
{
  "browserNumber": 100,
  "browsers": [
    {
      "browserId": "123",
      "userInfo": {
        "username": "123"
      },
      "status": 1
    }
  ]
}
```

任务处理完成后一系列ACK为了保证任务完成无误

## 浏览器请求和响应

如何获取浏览器的响应结果

- Http 请求结果
- 页面结果，通过 DOM 获取

## 问题

### 任务脚本

如何将脚本下发到各个客户端，免重启，实现解释器

### 客户端重启

Client 重启是将所有浏览器视为未登录，还是将登录信息保存到Cookie，重启后自动获取一次？
