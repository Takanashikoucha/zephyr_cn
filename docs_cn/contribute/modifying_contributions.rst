.. _modifying_contributions:

修改其他开发者做出的贡献
************************************************

场景
#########

鼓励 Zephyr 贡献者和协作者作为 pull request 中的审查者提供帮助，
以便补丁可以被批准并合并到 Zephyr 的主分支，
作为原始 pull request 的一部分。
Pull request 的作者负责在审查过程后修改他们的原始 commit。

然而，有时贡献者可能需要修改包含在其他 Zephyr 贡献者提交的
pull request 中的补丁。例如，在以下情况下就是这种情况：

* 开发者将其他贡献者提交的 commit cherry-pick 到他们自己的
  pull request 中，以便：

  * 整合有用内容，该内容是过时 pull request 的一部分，或
  * 将内容作为更大补丁的一部分合并到项目的主分支

* 开发者向另一个贡献者打开的分支或 pull request 推送，以便：

  * 协助更新 pull request，以便将补丁合并到项目的主分支
  * 推动过时的 pull request 完成，以便它们可以被合并


被接受的策略
#################

意图 cherry-pick 并可能修改由另一位贡献者发送的补丁的
开发者应该：

* 在他们的 pull request 中说明 cherry-pick 这些补丁的原因，
  而不是协助在原始 pull request 中合并这些补丁，并且
* 邀请补丁的原始作者加入他们的 pull request 审查。

意图向另一位 Zephyr 贡献者的分支或 pull request 强制推送的
开发者应该在 pull request 中说明推送和修改现有补丁的原因
（例如说明这样做是为了推动 pull request 审查完成，
当 pull request 作者无法这样做时）。

.. note::
   开发者应该尝试将上述做法限制在被识别为*过时*的 pull request 中。
   阅读 :ref:`开发流程和工具 <dev-environment-and-tools>`
   了解如何将 pull request 识别为过时。

如果原始补丁被大幅修改，开发者可以：

* （首选）联系原始作者并请求他们确认修改后的补丁可以在保留
  原始 sign-off 行和作者身份的情况下被合并，或
* 将修改后的补丁作为他们*自己*的工作提交（即带有他们*自己*的
  sign-off 行和作者身份）。在这种情况下，开发者应该在 commit 消息中
  说明提交的工作基于的原始来源（例如提及原始 PR 编号）。

.. note::
   贡献者应该取消勾选*"允许维护者编辑"*复选框，
   以表示他们不希望他们的补丁被其他 Zephyr 开发者
   在他们的原始分支或 pull request 中修改。
