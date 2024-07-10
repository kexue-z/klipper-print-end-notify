# klipper-print-end-notify

## TD;TL

推送打印完成的信息到 [PushOver](https://pushover.net/) 服务中
适用于 Klipper

## 准备

[PushOver](https://pushover.net/) 中注册并获取下面的内容

- `User key` 注册的时候就有了 
- `API key` 自行创建一个 `Applications`

## 安装

1. 下载 [print_end_notify.py](klippy/extars/print_end_notify.py) 源码
2. 放到 `<klipper目录>/klippy/extras` 文件夹中。例如 `~/klipper/klippy/extars/`
3. 添加配置文件到 `printer.cfg` 中
    ```
    [printendnotify]
    api_key: <API key>
    user_key: <User key>
    ```

    可选项:
    ```
    timeout: 10
    ```

## 使用

在你的 **切片软件** 或者 **打印结束** `PRINT_END` 中添加一行

```
PRINT_END_NOTIFY
```

即可

> 注意: 由于此操作为同步网络请求，如在打印过程中（后续有打印头移动、挤出等操作）请求，可能会由于等待时间过长导致 klipper 报错。因此需要确保后续无操作，或手动添加等待时间。



## 可选项
```
PRINT_END_NOTIFY [DEVICE=<设备ID>] [SOUND=<声效>]
```
- `DEVICE` PushOver 中的 `Your Devices` 名称
- `SOUND` PushOver 中的 `Your Custom Sounds` 名称
