# init wx 数据结构


整体是一个 dict，包含 14 个 key 值:

- Count int
- SystemTime int
- GrayScale int
- MPSubscribeMsgCount int
- InviteStartCount int
- ClickReportInterval int
- ClientVersion int
- SKey unicode
- BaseResponse dict
- ChatSet unicode
- SyncKey dict
- User dict
- MPSubscribeMsgList list
- ContactList list

其中 3 个需要保存:

- SKey unicode
- SyncKey dict
- User

ContactList 此处不完整，保存意义不大。

Skey 和 SyncKey 后续与 Server 通信需要.

## User 结构

- UserName: @5e44df76c4d3ccd266666666666666 (unicode)
- RemarkPYQuanPin:  (unicode)
- SnsFlag: 17 (int)
- HeadImgUrl: /cgi-bin/mmwebwx-bin/webwxgeticon?seq=6618xxxxxxxxxxx (unicode)
- RemarkName:  (unicode)
- PYInitial:  (unicode)
- WebWxPluginSwitch: 0 (int)
- PYQuanPin:  (unicode)
- Uin: 666666666 (int)
- StarFriend: 0 (int)
- Signature: http://jackon.me (unicode)
- RemarkPYInitial:  (unicode)
- ContactFlag: 0 (int)
- HeadImgFlag: 1 (int)
- Sex: 1 (int)
- NickName: Jackon (unicode)
- HideInputBarFlag: 0 (int)
- AppAccountFlag: 0 (int)
- VerifyFlag: 0 (int)
