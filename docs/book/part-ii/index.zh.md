# 第二部分：安全边界

如果说第一部分是在搭建基础架构图景，那么这一部分开始进入整套系统里最紧张的一层：安全。

这一部分的意义，是避免你产生一个危险错觉，好像 agent 的安全可以“以后再补”。现实正好相反：

- 如果 trust boundaries 没有提前定义好，agent 很快就会把多余上下文一起拖进来；
- 如果 tools 没有隔离，一个糟糕的调用就会变成真实 incident；
- 如果 policy、approval 和 audit 没有嵌进 runtime，团队会在最不合适的时候失去控制。

## 这一部分你会得到什么

- agent systems 关键威胁的地图；
- 一套实用的 security perimeter 模型；
- 一组控制点：ingress、prompt assembly、model gateway、retrieval、tools、egress；
- policy-as-code 和 gated execution 示例；
- 一个能和 security 团队认真讨论的基础，而不是只停留在抽象口号上。

## 导航

- [第 3 章：安全边界与信任边界](chapter-3.zh.md)
- [第 4 章：Tool Gateway、Approval 与 Audit Trail](chapter-4.zh.md)
- [第一部分：基础](../part-i/index.zh.md)
- [参考资料](../../appendix/sources.zh.md)
