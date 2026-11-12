# Cornix 原生 ZMK / Kanata 键位

迁移基准：2026-11-12 本机活动 `kanata.kbd`（文件标注 Kanata 1.12.0）。
所有新增键位行为使用上游 ZMK；没有 Kanata 运行时、第三方 HRM 模块或 C 补丁。
原有 RGB、DYA Studio 等硬件依赖继续保留。
蓝牙选择、固定切层入口与独立数字小键盘层沿用原配置；空占位层与旧文本宏未恢复。

## 键位与层入口

默认层为 Mac 配置，主字母区仍为 QWERTY。

| 物理键 | 轻按 | 按住 |
| --- | --- | --- |
| 原 Caps 位置（A 左侧，位置 12） | Escape | Navigation |
| 左手左侧拇指（41） | Left Shift | Left Shift |
| 左手中间拇指（42） | Escape | Symbols（数字＋符号） |
| 左手右侧拇指（43） | 按下进入 Navigation | 松开退出 |
| 右手左侧拇指（44） | Return | 重复 Return |
| 右手中间拇指（45） | Space | 重复 Space |
| 右手右侧拇指（46） | Right Shift | Right Shift |
| P 右侧（11） | Backspace | 重复删除 |
| 分号右侧（23，原 Enter 位置） | F13 | F13 |

单键 HRM：`A=Alt`、`S=Ctrl`、`D=Shift`、`F=Cmd`；
`J=右 Cmd`、`K=右 Shift`、`L=右 Ctrl`、`;=右 Alt`。
左右实体 Shift 保留，适合连续打字中快速输入大写。

左编码器旋转调音量、按下静音；右编码器旋转滚动、按下播放/暂停。
额外底部键保留 Ctrl、原 `td_num` 数字层入口（39）和方向键，蓝牙层入口仍为位置 40。
左中拇指长按进入数字＋符号层，松开回到原层；右中 Space 不再承担切层。

| 层 | 内容 |
| --- | --- |
| Symbols | Q–P 对应 `! @ # $ % ^ & * ( )`；A–; 对应 `1…0`；Z/X/C/V/B 为 `_ - + = "`；N/M 为左右方向 |
| Navigation | H/J/K/L 为方向；W/A/S/D 移动鼠标；Space 左键、I 右键；Q/E 向下/上滚动，U/O 向左/右滚动 |
| Function | 因 Cornix 无独立数字行，把最上排 12 键映射为 F1–F12；中排 HRM 保留 |
| Number | 恢复原独立数字小键盘层，由蓝牙层 J 进入；拇指按上述新配置，Caps 仍为 Esc／Navigation |
| Bluetooth | 位置 38/24/12 选择蓝牙 0/1/2；H→Base、J→Number、M→Windows、逗号→Symbols、句号→Function，与原入口一致 |

Windows 模式交换 S/F 与 J/L 的 Ctrl/GUI，双键长按随之调整。
Symbols 下右手左侧拇指 Return（44）单击为 Enter，180 ms 内双击启用 Caps Word，空闲 2 秒退出。
单击 Enter 会等待 tap-dance 判定；普通层 Enter 不受此等待影响。

## Combos 与防误触

| 组合 | Base/Windows 轻按 | Base 长按 | Symbols |
| --- | --- | --- | --- |
| W+E | `\` | 重复 `\` | `\|` |
| U+I | `[` | 重复 `[` | `{` |
| I+O | `]` | 重复 `]` | `}` |
| S+D | `_` | Ctrl+Shift | `=` |
| J+K | `'` | Cmd+Shift | `+` |
| K+L | `"` | Shift+Ctrl | `-` |

配置集中在 `config/includes/kanata-timing.h`：

- `HM_TERM=280`：独立长按判定时间。
- `HM_QUICK=175`：快速再次按下同一 HRM 时保留字母重复。
- `HM_IDLE=150`：连续文字输入时优先输出字母，避免误触修饰键。
- `COMBO_TERM=18`：两个键的按下间隔必须在 18 ms 内。
- `COMBO_IDLE=150`：普通输入之后暂时禁止基础层 combo。

HRM 使用 `balanced` 和按释放位置判定的左右手规则。异手/拇指按下再
释放可以提前确定修饰键；同手的快速嵌套输入倾向输出字母。超过 280 ms
仍可主动使用同手快捷键。普通 HRM 和组合 HRM 分开定义，组合通过空闲
保护后不再重复应用该保护。

组合长按使用显式复合修饰键，例如 `LC(LSHFT)`，而不是异步宏。
组合中任一键释放，就释放整个组合的修饰键。此时剩下的单键不会重新
变成独立 HRM；这是避免残留修饰键的明确选择。需要独立释放两个修饰键时，
让两键按下间隔超过 18 ms，或使用实体修饰键。

`J+L` 不定义 combo，保留原生 HRM 与字母按压顺序，避免人为引入 Kanata
v1 chord 分组的回退逻辑。共享 K 的 J+K 与 K+L 应完整释放后再输入下一组；
三键同时按下没有额外定义第三种语义。

**连续符号：**检查的上游 `combo.c` 会忽略 combo 本身产生的按键对空闲计时
的影响，组合内 hold-tap 又沿用最初按下的时间戳，因此设计上允许连续符号
combo，同时阻止普通连打误触。云端有专门测试锁定这一行为。
这比 Kanata 的三个符号专用历史豁免更宽：普通括号等 combo 也不计入普通连打。
普通 HRM 仍保留自己的空闲保护；刚输入符号后立刻使用单键 HRM，不保证与
Kanata 的全部历史条件完全一致。

Symbols 内没有空闲保护：进入此层已经表示主动输入符号/数字。
所以 18 ms 内重叠按下 `2+3` 会得到 `=`；连续输入数字时请顺序释放，或放慢
两次按下间隔。独立 Number、FN、Navigation、鼠标速度层及 Bluetooth 均禁用 combo。

## 鼠标

默认垂直 800、水平 1200 HID 单位/秒，恒速无加速坡道；滚轮约 33 单位/秒。
Navigation 下按住分号减速、按住原单引号位置（23）加速两倍。
两者同时按住时减速优先，松开减速键即恢复加速。
减速后两轴约 200 单位/秒，近似 Kanata 20% 缩放后每 10 ms 四舍五入为 2
像素的效果。ZMK 与 Kanata 的发包频率及操作系统加速不同，不承诺像素轨迹一致。
速度层会在速度键释放时退出，即使先松开 Navigation 入口也不会永久遗留。

## 在新 GitHub 仓库编译

1. 将本仓库完整推送到新仓库，包括 `.github`、`boards`、`zephyr`、`config`、
   `tests`、`scripts` 与 `build.yaml`。无需改成上游仓库名，也无需个人访问令牌。
2. 在仓库 Actions 中允许工作流运行，选择 **Build ZMK firmware** → **Run workflow**。
3. `keymap-tests` 先检查 50 键位置和层绑定，再运行原生 ZMK 事件测试。
   通过后 `build` 调用官方固件构建流程。以后修改子目录中的 `.dtsi`/`.h`
   也会自动触发构建。
4. 在该次运行中下载 `firmware` artifact。默认仍是左右分体方案：
   `cornix_left_default_nosd.uf2` 给左半，`cornix_right_nosd.uf2` 给右半。
   `cornix_reset` 是专用重置固件，不是日常键位固件；改键位通常不需清蓝牙配对。
5. 若失败，下载 `keymap-test-logs` 或提供失败任务日志；不要把“编译通过”
   当作实机手感已验证。首次运行需要获取 Zephyr 与模块，耗时会较长。

没有改板型、闪存分区、settings 后端或 dongle 目标；保留合格板名与现有
no-SoftDevice 布局。不要在本次迁移时混刷其他角色的固件。

如果此前通过 Studio 保存过动态键位，新固件可能继续加载旧的持久化映射。
刷写后若看到旧层名/旧键位，应先在 Studio 中恢复固件默认键位并保存，
而不是直接清除所有蓝牙设置。旧 `config/cornix.json`/`cornix42.json` 是历史
编辑器数据，未同步为本次布局；以 `config/cornix.keymap` 为准，不要用旧 JSON
反向覆盖生成它。42 键备用配置保持原状。

## 验证与调参

`python3 scripts/check-keymap.py` 可在无 SDK 环境检查布局。
`python3 tests/kanata/generate.py` 生成事件测试；在与固件相同 manifest 的 ZMK
环境中运行 `west test /absolute/path/to/tests/kanata/generated`。
测试直接包含生产 keymap，只移除蓝牙操作和编码器的硬件绑定，保留实际切层入口。
预期输出是手工指定的，测试失败不会自动接受结果。

本次编辑环境已验证 9 层各 50 个绑定、位置编号、工作流 YAML，以及使用
上游头文件预处理后的生产键位/测试夹具的 Zephyr 设备树解析、引用和参数数量。
尚未执行固件编译或 native_sim 事件测试；这两项由新仓库首次 Actions 运行确认。

回归用例覆盖：双键正/反序、普通打字保护、同手嵌套、JL/LJ 顺序、异手提前
hold、双修饰键及追加 Alt、连续符号、数字层 combo、Space 滚动输入、
导航与 Function 层的 combo 隔离，以及六个拇指键和 Caps 的新入口；共 22 个用例。

实机仍须检查：

- 快速输入含 `sd`、`jk`、`kl` 的文字，确认无意外符号/修饰键。
- 空闲后分别轻按和长按三个 homerow combo，并与异手字母组合。
- 任意先后松开组合键，再输入普通字母，确认没有残留修饰键。
- 连续输入 `_ ' "`；测试双击字母后按住是否正常重复。
- 左中拇指+数字、左手右侧拇指/Caps+方向、鼠标双速度键不同按压/释放顺序。

若文字误触 combo，先把 `COMBO_TERM` 从 18 降到 15，或把 `COMBO_IDLE`
从 150 提到 175；前者会让主动 combo 更难按准，后者会让打字后需要更久停顿。
若 combo 漏触，先实测 22–25 ms，但会增加滚动输入误判风险。
不要同时修改所有参数。使用这套固件时应让 Kanata 排除 Cornix，避免二次映射。

参考：[Hold-tap](https://zmk.dev/docs/keymaps/behaviors/hold-tap)、
[Combos](https://zmk.dev/docs/keymaps/combos)、
[输入处理器](https://zmk.dev/docs/keymaps/input-processors/usage)、
[urob 配置](https://github.com/urob/zmk-config)。
